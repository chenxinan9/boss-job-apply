"""Installer contracts using local fixtures, not desktop/BOSS acceptance."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MAC_HASH = '5d37a1d760c37553dcecb3b505a8c8b36bfc389de4d46498cbcf6e6c88e7eb1a'
WIN_HASH = '0ca3c940dc7d1467b70a0a6f95d04974120b5225d2f8174fdbc8df5099270acb'


class PrepareTest(unittest.TestCase):
    def test_business_flow_identical_and_no_private_defaults(self):
        texts = [(ROOT/'packages'/('boss-apply-workbuddy-'+s)/'SKILL.md').read_text(encoding='utf-8')
                 for s in ('macos', 'windows')]
        self.assertEqual(*(t.split('## 本人资料与授权')[1] for t in texts))
        for t in texts:
            self.assertIn('DESKTOP.md', t)
            for private in ('深圳', 'CMO', '海外营销', '/Users/', 'TaskSpace'):
                self.assertNotIn(private, t)

    @unittest.skipUnless(sys.platform in ('darwin', 'win32'), 'native preparation needs macOS or Windows')
    def test_prepare_and_bad_hash_and_existing_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = (Path(temp)/'测试 with spaces').resolve(); root.mkdir()
            fixture = root/'fixture.zip'
            mac = sys.platform == 'darwin'
            rel = 'Open Computer Use.app/Contents/MacOS/OpenComputerUse' if mac else 'open-computer-use.exe'
            with zipfile.ZipFile(fixture, 'w') as z:
                info = zipfile.ZipInfo(rel); info.create_system = 3; info.external_attr = 0o100755 << 16
                z.writestr(info, '#!/bin/sh\nexit 99\n')  # Must never execute this fixture.
            sha = hashlib.sha256(fixture.read_bytes()).hexdigest()
            folder = ROOT/'packages'/('boss-apply-workbuddy-macos' if mac else 'boss-apply-workbuddy-windows')
            original = (folder/('prepare-desktop.sh' if mac else 'prepare-desktop.ps1')).read_text(encoding='utf-8')
            env = dict(os.environ, FIXTURE=str(fixture))
            # Host environment variables are not a reliable CPU architecture source.
            env.pop('PROCESSOR_ARCHITECTURE', None)
            env.pop('PROCESSOR_ARCHITEW6432', None)
            if mac:
                mocks = root/'bin'; mocks.mkdir()
                # Mock download and signature only; real hash, extraction, JSON and no-overwrite checks.
                for name, body in {
                    'curl': 'while [ "$1" != "-o" ]; do shift; done; cp "$FIXTURE" "$2"',
                    'codesign': 'exit 0',
                }.items():
                    p = mocks/name; p.write_text('#!/bin/sh\n'+body+'\n'); p.chmod(0o755)
                env['PATH'] = str(mocks)+os.pathsep+os.environ['PATH']
                script = root/'prepare.sh'; command = ['bash', str(script), str(root)]
                old_hash = MAC_HASH
                prefix = ''
            else:
                script = root/'prepare.ps1'; command = ['powershell', '-NoProfile', '-File', str(script), '-Workspace', str(root)]
                old_hash = WIN_HASH
                prefix = 'function Invoke-WebRequest { param($UseBasicParsing,$Uri,$OutFile,$TimeoutSec) Copy-Item -LiteralPath $env:FIXTURE -Destination $OutFile }\n'
                # The mock switch must accept -UseBasicParsing like the real cmdlet.
                prefix = prefix.replace('param($UseBasicParsing', 'param([switch]$UseBasicParsing')
            def run(text):
                text = text.replace('# Download only:', prefix+'# Download only:', 1)
                script.write_text(text, encoding='utf-8-sig' if not mac else 'utf-8')
                return subprocess.run(command, env=env, capture_output=True, timeout=30)
            target = root/'.boss-runtime/computer-use/1.1.0'
            bad = run(original)
            self.assertNotEqual(bad.returncode, 0)
            self.assertFalse(target.exists(), bad.stdout)
            # Missing workspace must fail before download and cannot fall back to a global directory.
            missing = subprocess.run(command[:-1]+[str(root/'missing')], env=env, capture_output=True, timeout=30)
            self.assertNotEqual(missing.returncode, 0)
            self.assertFalse((root/'missing').exists())
            good_source = original.replace(old_hash, sha)
            good = run(good_source)
            self.assertEqual(good.returncode, 0, good.stderr)
            cfg = json.loads((target/'connection.json').read_text(encoding='utf-8'))
            self.assertEqual(cfg['mcpServers']['boss-desktop'], {'command': str(target/rel), 'args': ['mcp']})
            self.assertIn(b'PREPARED (not connected, not tested)', good.stdout)
            keep = target/'personal-keep'; keep.write_bytes(b'do not remove')
            repeat = run(good_source)
            self.assertNotEqual(repeat.returncode, 0)
            self.assertEqual(keep.read_bytes(), b'do not remove')
            self.assertFalse(list(target.parent.glob('.prepare*')))


if __name__ == '__main__':
    unittest.main()
