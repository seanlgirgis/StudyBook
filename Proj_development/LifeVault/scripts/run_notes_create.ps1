param(
    [Parameter(Mandatory = $true)][string]$Title,
    [string]$Story = "",
    [string]$Tags = "",
    [string]$Body = "",
    [Parameter(Mandatory = $true)][string]$NotesRoot,
    [string]$Filename
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$srcPath = Join-Path $projectRoot "src"
if ($env:PYTHONPATH) { $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH" } else { $env:PYTHONPATH = $srcPath }

$args = @("-m", "lifevault.notes_cli", "create", "--title", $Title, "--story", $Story, "--tags", $Tags, "--body", $Body, "--notes-root", $NotesRoot)
if ($Filename) { $args += @("--filename", $Filename) }
python @args
exit $LASTEXITCODE
