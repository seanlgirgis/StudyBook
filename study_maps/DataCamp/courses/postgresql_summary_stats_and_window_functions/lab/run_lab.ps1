[CmdletBinding()]
param(
    [string]$Database = 'studybook',
    [string]$User = 'postgres',
    [string]$HostName = 'localhost',
    [int]$Port = 5432,
    [switch]$RunSolutions
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$LabRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $LabRoot

function Invoke-PsqlFile {
    param([Parameter(Mandatory)][string]$Path)

    Write-Host "[RUN] $Path" -ForegroundColor Cyan
    & psql `
        -h $HostName `
        -p $Port `
        -U $User `
        -d $Database `
        -v ON_ERROR_STOP=1 `
        -f $Path

    if ($LASTEXITCODE -ne 0) {
        throw "psql failed for: $Path"
    }
}

Invoke-PsqlFile '.\sql\00_create_schema.sql'
Invoke-PsqlFile '.\sql\01_create_table.sql'
Invoke-PsqlFile '.\sql\02_load_data.sql'
Invoke-PsqlFile '.\sql\03_validate_data.sql'

if ($RunSolutions) {
    Get-ChildItem '.\sql\solutions\*.sql' |
        Sort-Object Name |
        ForEach-Object { Invoke-PsqlFile $_.FullName }
}

Write-Host ''
Write-Host '[OK] Lab setup and validation completed.' -ForegroundColor Green

if (-not $RunSolutions) {
    Write-Host 'Next: start with .\sql\exercises\01_window_foundations_exercises.sql'
}
