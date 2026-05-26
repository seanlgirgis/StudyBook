$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path

Write-Host "Starting LifeVault Streamlit Help Console (read-only) ..."
Set-Location $projectRoot
python -m streamlit run app/streamlit/lifevault_help_console.py
exit $LASTEXITCODE
