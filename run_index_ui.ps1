Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$AppPath = Join-Path $Root "coding_challenges\scripts\index_ui_streamlit.py"
$EnvSetterPath = Join-Path $Root "env_setter.ps1"

if (-not (Test-Path -LiteralPath $AppPath)) {
    throw "Streamlit app not found at $AppPath"
}

if (Test-Path -LiteralPath $EnvSetterPath) {
    # Ensure project-standard Python/venv activation before launching Streamlit.
    . $EnvSetterPath -NonInteractive
}

# Keep Streamlit state local to this repo/session to avoid machine-profile permission issues.
$StreamlitHome = Join-Path $Root ".streamlit_local"
if (-not (Test-Path -LiteralPath $StreamlitHome)) {
    New-Item -ItemType Directory -Path $StreamlitHome | Out-Null
}
$env:HOME = $StreamlitHome
$env:USERPROFILE = $StreamlitHome
$env:STREAMLIT_BROWSER_GATHER_USAGE_STATS = "false"

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
    & $PythonCmd -3 -m streamlit run $AppPath --server.headless true --browser.gatherUsageStats false
}
else {
    & $PythonCmd -m streamlit run $AppPath --server.headless true --browser.gatherUsageStats false
}
