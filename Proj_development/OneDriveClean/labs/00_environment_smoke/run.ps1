$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "..\..\scripts\_lab_common.ps1")
$ctx = Get-LabContext -ScriptDir $scriptDir -LabName "00_environment_smoke"
"PWD: $(Get-Location)" | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "pwd.txt")
"Shell: PowerShell" | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "shell.txt")
python --version | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "python_version.txt")
$markers = @("README.md","config","src","labs") | Where-Object { Test-Path (Join-Path $ctx.RepoRoot $_) }
($markers -join ", ") | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "repo_markers.txt")
Write-Host "Environment smoke complete: $($ctx.RunDir)"
