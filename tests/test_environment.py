import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'packages/boss-apply-codex/scripts/doctor.py'
spec = importlib.util.spec_from_file_location('doctor', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class EnvironmentTest(unittest.TestCase):
    def inspect(self, commands=(), **kwargs):
        return m.inspect_environment(lookup=lambda name: '/private-test-location/'+name if name in commands else None, **kwargs)

    def test_os_matrix_preserves_current_session(self):
        for system in ('Windows', 'Darwin', 'Linux'):
            for client in ('codex', 'workbuddy'):
                with self.subTest(system=system, client=client):
                    result = self.inspect(client=client, system=system, commands=['agent-browser'],
                                          exposed_tools=['native'], existing_session='agent-browser')
                    self.assertEqual(result['selected_route'], 'agent-browser')
                    self.assertEqual(result['next_action'], 'CHECK_EXISTING_SESSION')
                    self.assertFalse(result['browser_ready'])
                    self.assertFalse(result['send_authorized'])

    def test_native_tool_not_inferred_from_client_name(self):
        result = self.inspect(client='codex', commands=[])
        self.assertIsNone(result['selected_route'])
        self.assertEqual(result['candidate_providers'], [])

    def test_native_preferred_when_exposed(self):
        result = self.inspect(client='codex', exposed_tools=['native'], commands=['agent-browser', 'ego-browser'])
        self.assertEqual(result['selected_route'], 'native')

    def test_client_exposed_tool_can_work_without_path_cli(self):
        result = self.inspect(client='workbuddy', exposed_tools=['ego'])
        self.assertEqual(result['selected_route'], 'ego')

    def test_unavailable_current_tool_never_silently_switches(self):
        result = self.inspect(client='workbuddy', existing_session='ego', commands=['agent-browser'])
        self.assertEqual(result['next_action'], 'RECONNECT_EXISTING_TOOL')
        self.assertEqual(result['selected_route'], 'ego')

    def test_missing_tool_install_routes(self):
        for client, commands, action in [
            ('workbuddy', [], 'CHECK_SKILLHUB_AGENT_BROWSER'),
            ('codex', ['npm'], 'INSTALL_OPTIONAL_AGENT_BROWSER'),
            ('codex', [], 'CONNECT_CLIENT_BROWSER_OR_SETUP_OPTIONAL_TOOL'),
        ]:
            self.assertEqual(self.inspect(client=client, commands=commands)['next_action'], action)

    def test_no_private_paths_in_report(self):
        result = self.inspect(client='codex', commands=['node', 'npm', 'agent-browser'])
        self.assertNotIn('private-test-location', json.dumps(result))

    def test_invalid_provider_and_unknown_os(self):
        with self.assertRaises(ValueError):
            self.inspect(client='codex', exposed_tools=['made-up-tool'])
        result = self.inspect(client='codex', system='Unknown')
        self.assertFalse(result['supported_os_family'])

    def test_cli_from_unicode_space_directory_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)/'路径 with spaces';work.mkdir()
            result = subprocess.run([sys.executable, str(SCRIPT), '--client', 'workbuddy'],
                                    cwd=work, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'ENVIRONMENT_ONLY')
            self.assertEqual(list(work.iterdir()), [])

    def test_client_copies_identical(self):
        for name in ('scripts/doctor.py', 'references/setup.md'):
            self.assertEqual((ROOT/'packages/boss-apply-codex'/name).read_bytes(),
                             (ROOT/'packages/boss-apply-workbuddy'/name).read_bytes())

if __name__ == '__main__':
    unittest.main()
