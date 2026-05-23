$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

& ..\..\env_setter.ps1
streamlit run (Join-Path $repoRoot "app\odc_control_center.py")
