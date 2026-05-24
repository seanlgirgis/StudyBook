param(
    [Parameter(Mandatory = $true)][string]$Title,
    [string]$Story = "",
    [string]$Tags = "",
    [Parameter(Mandatory = $true)][string]$NotesRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$srcPath = Join-Path $projectRoot "src"
if ($env:PYTHONPATH) { $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH" } else { $env:PYTHONPATH = $srcPath }

python -m lifevault.notes_cli create-folder --title $Title --story $Story --tags $Tags --notes-root $NotesRoot
exit $LASTEXITCODE
