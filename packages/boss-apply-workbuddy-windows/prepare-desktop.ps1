param([string]$Workspace)
# Download only: no MCP registration, permission changes, or desktop actions.
$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'This package requires Windows.' }
# Hosts may supply a module search path for a different PowerShell version.
Import-Module (Join-Path $PSHOME 'Modules\Microsoft.PowerShell.Utility')
Import-Module (Join-Path $PSHOME 'Modules\Microsoft.PowerShell.Archive')
$arch = [Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
if ($arch -eq 'X64') { $arch = 'AMD64' }
$hashes = @{
    AMD64 = '0ca3c940dc7d1467b70a0a6f95d04974120b5225d2f8174fdbc8df5099270acb'
    ARM64 = '723f37b8805ba03ab87b5d7305e06998f82a24cf64b44414a7578f9ddab0cea1'
}
if (-not $hashes.ContainsKey($arch)) { throw "Unsupported Windows architecture: $arch" }
if (-not $Workspace -or -not (Test-Path -LiteralPath $Workspace -PathType Container)) {
    throw 'Pass one existing, authorized persistent workspace directory with -Workspace.'
}
$target = Join-Path (Resolve-Path -LiteralPath $Workspace).Path '.boss-runtime\computer-use\1.1.0'
if (Test-Path -LiteralPath $target) { throw "Already exists; preserve it and inspect: $target" }
New-Item -ItemType Directory -Path (Split-Path $target) -Force | Out-Null
$stage = Join-Path (Split-Path $target) ('.prepare-' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $stage | Out-Null
try {
    $asset = 'open-computer-use-cli-1.1.0-windows-' + $arch.ToLowerInvariant() + '.zip'
    $archive = Join-Path $stage 'runtime.zip'
    $url = 'https://github.com/iFurySt/open-codex-computer-use/releases/download/v1.1.0/' + $asset
    Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $archive -TimeoutSec 600
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash -ne $hashes[$arch]) {
        throw 'SHA-256 mismatch; nothing installed.'
    }
    $payload = Join-Path $stage 'payload'
    Expand-Archive -LiteralPath $archive -DestinationPath $payload
    if (-not (Test-Path -LiteralPath (Join-Path $payload 'open-computer-use.exe') -PathType Leaf)) {
        throw 'Native executable missing.'
    }
    $config = @{ mcpServers = @{ 'boss-desktop' = @{
        command = (Join-Path $target 'open-computer-use.exe'); args = @('mcp')
    } } } | ConvertTo-Json -Depth 5
    [IO.File]::WriteAllText((Join-Path $payload 'connection.json'), $config, (New-Object Text.UTF8Encoding($false)))
    [IO.File]::WriteAllText((Join-Path $payload 'SOURCE.sha256'), ($hashes[$arch] + '  ' + $asset))
    # Directory.Move refuses an existing destination, including concurrent installs.
    [IO.Directory]::Move($payload, $target)
    Write-Output "PREPARED (not connected, not tested): $target\connection.json"
} finally {
    Remove-Item -LiteralPath $stage -Recurse -Force
}
