#!/usr/bin/env python3
"""Read-only environment routing. Does not start browsers, read profiles or install tools."""
import argparse
import json
import platform
import shutil
import sys

PROVIDERS = ("native", "ego", "agent-browser")
COMMANDS = ("agent-browser", "ego-browser", "node", "npm")

def inspect_environment(client, exposed_tools=(), existing_session=None, system=None, lookup=None):
    if client not in ("codex", "workbuddy"):
        raise ValueError("unsupported client")
    if set(exposed_tools) - set(PROVIDERS) or (existing_session and existing_session not in PROVIDERS):
        raise ValueError("unknown browser provider")
    lookup = lookup or shutil.which
    system = system or platform.system()
    # Presence only. Never execute PATH programs, print machine paths or inspect credentials.
    available = {name: bool(lookup(name)) for name in COMMANDS}
    candidates = [name for name in PROVIDERS if name in exposed_tools or
                  (name != "native" and available[name + "-browser" if name == "ego" else name])]
    if existing_session and existing_session not in candidates:
        route, action = existing_session, "RECONNECT_EXISTING_TOOL"
    elif existing_session:
        route, action = existing_session, "CHECK_EXISTING_SESSION"
    elif candidates:
        route, action = candidates[0], "DISCOVER_EXISTING_SESSIONS"
    elif client == "workbuddy":
        route, action = None, "CHECK_SKILLHUB_AGENT_BROWSER"
    elif available["npm"]:
        route, action = None, "INSTALL_OPTIONAL_AGENT_BROWSER"
    else:
        route, action = None, "CONNECT_CLIENT_BROWSER_OR_SETUP_OPTIONAL_TOOL"
    return {
        "schema_version": 1, "client": client, "os": system,
        "supported_os_family": system in ("Darwin", "Windows", "Linux"),
        "command_presence": available, "client_exposed_tools": sorted(set(exposed_tools)),
        "existing_session_provider": existing_session, "candidate_providers": candidates,
        "selected_route": route, "next_action": action,
        "session_discovery_required": bool(route and not existing_session),
        "status": "ENVIRONMENT_ONLY", "browser_ready": False, "send_authorized": False,
        "instructions": "references/setup.md",
        "limitations": ["PATH presence is not working browser access",
                        "no supplied session does not mean no existing browser; discover before creating",
                        "client tools must be supplied from the actual exposed tool list",
                        "login, permissions and live page checks remain required"],
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", choices=("codex", "workbuddy"), required=True)
    parser.add_argument("--tool", action="append", default=[], choices=PROVIDERS,
                        help="only tools actually exposed by the current client")
    parser.add_argument("--existing-session", choices=PROVIDERS,
                        help="provider of an observed reusable session, including one opened before this task")
    args = parser.parse_args()
    result = inspect_environment(args.client, args.tool, args.existing_session)
    # ASCII JSON remains readable on legacy Windows console encodings.
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
