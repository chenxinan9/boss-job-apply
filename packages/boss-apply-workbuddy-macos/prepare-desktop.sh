#!/bin/bash
# Download only: no MCP registration, permission changes, or desktop actions.
set -euo pipefail
[[ "$(uname -s)" == Darwin ]] || { echo 'This package requires macOS.' >&2; exit 1; }
[[ "$(sw_vers -productVersion | cut -d. -f1)" -ge 14 ]] || { echo 'macOS 14+ required.' >&2; exit 1; }
[[ $# -eq 1 && -d "$1" ]] || { echo 'Pass one existing, authorized persistent workspace directory.' >&2; exit 1; }
workspace=$(cd -- "$1" && pwd -P)
target="$workspace/.boss-runtime/computer-use/1.1.0"
mkdir -p "$(dirname "$target")"
[[ ! -e "$target" && ! -L "$target" ]] || { echo "Already exists; preserve it and inspect: $target" >&2; exit 1; }
stage=$(mktemp -d "$(dirname "$target")/.prepare.XXXXXX")
trap 'rm -rf "$stage"' EXIT
asset='Open-Computer-Use-1.1.0-macOS-universal.app.zip'
expected='5d37a1d760c37553dcecb3b505a8c8b36bfc389de4d46498cbcf6e6c88e7eb1a'
curl --fail --location --proto '=https' --proto-redir '=https' --connect-timeout 20 --max-time 600 \
  "https://github.com/iFurySt/open-codex-computer-use/releases/download/v1.1.0/$asset" -o "$stage/runtime.zip"
actual=$(shasum -a 256 "$stage/runtime.zip" | cut -d' ' -f1)
[[ "$actual" == "$expected" ]] || { echo 'SHA-256 mismatch; nothing installed.' >&2; exit 1; }
mkdir "$stage/payload"
ditto -x -k "$stage/runtime.zip" "$stage/payload"
binary='Open Computer Use.app/Contents/MacOS/OpenComputerUse'
[[ -x "$stage/payload/$binary" ]] || { echo 'Native executable missing.' >&2; exit 1; }
codesign --verify --deep --strict "$stage/payload/Open Computer Use.app"
config="$stage/payload/connection.json"
plutil -create xml1 "$config"
plutil -insert mcpServers -json '{}' "$config"
plutil -insert mcpServers.boss-desktop -json '{}' "$config"
plutil -insert mcpServers.boss-desktop.command -string "$target/$binary" "$config"
plutil -insert mcpServers.boss-desktop.args -json '["mcp"]' "$config"
plutil -convert json "$config"
printf '%s  %s\n' "$expected" "$asset" > "$stage/payload/SOURCE.sha256"
# Reserve the destination; a concurrent install must never be overwritten.
mkdir "$target"
mv "$stage/payload/Open Computer Use.app" "$stage/payload/connection.json" "$stage/payload/SOURCE.sha256" "$target/"
echo "PREPARED (not connected, not tested): $target/connection.json"
