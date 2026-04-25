param(
    [string]$Machine,
    [switch]$PersistToUserEnv
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function ConvertTo-NormalizedMachineName {
    param([Parameter(Mandatory = $true)][string]$Name)
    $normalized = $Name.Trim().ToLowerInvariant()
    $normalized = $normalized -replace "[^a-z0-9\-_. ]", ""
    $normalized = $normalized -replace "[\s_]+", "-"
    return $normalized
}

function ConvertTo-PlainText {
    param([Parameter(Mandatory = $true)][Security.SecureString]$SecureString)
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$machineName = if ([string]::IsNullOrWhiteSpace($Machine)) { $env:COMPUTERNAME } else { $Machine }
$normalizedMachine = ConvertTo-NormalizedMachineName -Name $machineName

$localConfigPath = Join-Path $projectRoot ("config\machines\{0}.local.psd1" -f $normalizedMachine)
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $localConfigPath) | Out-Null
$fallbackDir = Join-Path $projectRoot "config\secrets\.local"
$fallbackFile = Join-Path $fallbackDir "openai_api_key.txt"

$secureKey = Read-Host -AsSecureString "Enter OPENAI_API_KEY"
$plainKey = ConvertTo-PlainText -SecureString $secureKey

if ([string]::IsNullOrWhiteSpace($plainKey)) {
    throw "OPENAI_API_KEY cannot be empty."
}

$escaped = $plainKey.Replace("'", "''")
$content = @"
@{
    Environment = @{
        OPENAI_API_KEY = '$escaped'
    }
}
"@

Set-Content -LiteralPath $localConfigPath -Value $content -Encoding UTF8
New-Item -ItemType Directory -Force -Path $fallbackDir | Out-Null
Set-Content -LiteralPath $fallbackFile -Value $plainKey -Encoding UTF8

if ($PersistToUserEnv) {
    [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $plainKey, "User")
}

Write-Host "Saved OPENAI_API_KEY to local machine config:" -ForegroundColor Green
Write-Host "  $localConfigPath" -ForegroundColor Gray
Write-Host "Saved OPENAI_API_KEY fallback file:" -ForegroundColor Green
Write-Host "  $fallbackFile" -ForegroundColor Gray
Write-Host "This file is gitignored and will not sync to GitHub." -ForegroundColor DarkGray
if ($PersistToUserEnv) {
    Write-Host "Also persisted OPENAI_API_KEY to User environment variables." -ForegroundColor DarkGray
}
Write-Host ""
Write-Host "Next step: run .\env_setter.ps1" -ForegroundColor Yellow
