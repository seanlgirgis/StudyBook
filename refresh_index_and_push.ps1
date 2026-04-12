param(
    [switch]$SkipGit
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$RefreshScript = Join-Path $Root "coding_challenges\scripts\refresh_index.py"
if (-not (Test-Path -LiteralPath $RefreshScript)) {
    throw "refresh_index.py not found at $RefreshScript"
}

function Resolve-PythonCmd {
    if (-not [string]::IsNullOrWhiteSpace($env:VIRTUAL_ENV)) {
        $venvPython = Join-Path $env:VIRTUAL_ENV "Scripts\python.exe"
        if (Test-Path -LiteralPath $venvPython) {
            return $venvPython
        }
    }

    $pythonCommands = @(Get-Command python -All -ErrorAction SilentlyContinue)
    foreach ($cmd in $pythonCommands) {
        $candidate = $cmd.Source
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }
        if ($candidate -like "*\WindowsApps\python.exe") { continue }
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher -and (Test-Path -LiteralPath $pyLauncher.Source)) {
        return $pyLauncher.Source
    }

    return $null
}

$PythonCmd = Resolve-PythonCmd
if (-not $PythonCmd) {
    throw "No Python runtime found. Activate a venv or ensure python/py is on PATH."
}

if ($PythonCmd -like "*\py.exe") {
    & $PythonCmd -3 $RefreshScript
}
else {
    & $PythonCmd $RefreshScript
}

if (-not $SkipGit) {
    gitq
}
