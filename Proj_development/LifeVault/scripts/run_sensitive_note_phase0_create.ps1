param(
    [Parameter(Mandatory = $true)][string]$Title,
    [Parameter(Mandatory = $true)][string]$PublicHint,
    [string]$Story = "",
    [string]$Tags = "",
    [Parameter(Mandatory = $true)][string]$DemoProtectedBody,
    [Parameter(Mandatory = $true)][string]$NotesRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$srcPath = Join-Path $projectRoot "src"
if ($env:PYTHONPATH) { $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH" } else { $env:PYTHONPATH = $srcPath }

python -m lifevault.notes_cli create-sensitive-phase0 --title $Title --public-hint $PublicHint --story $Story --tags $Tags --demo-protected-body $DemoProtectedBody --notes-root $NotesRoot
exit $LASTEXITCODE
