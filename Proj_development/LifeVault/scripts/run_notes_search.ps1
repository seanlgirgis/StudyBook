param(
    [Parameter(Mandatory = $true)][string]$Query,
    [Parameter(Mandatory = $true)][string]$NotesRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$srcPath = Join-Path $projectRoot "src"
if ($env:PYTHONPATH) { $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH" } else { $env:PYTHONPATH = $srcPath }

python -m lifevault.notes_cli search --query $Query --notes-root $NotesRoot
exit $LASTEXITCODE
