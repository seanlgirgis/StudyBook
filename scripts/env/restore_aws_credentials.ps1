param(
    [string]$InputEncryptedFile = "config/secrets/aws.profiles.secrets.enc.json",
    [string]$DestinationDir = "$env:USERPROFILE\.aws",
    [switch]$BackupExisting,
    [switch]$NonInteractive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $PSScriptRoot -ChildPath "..\.."))
$coreScript = Join-Path -Path $projectRoot -ChildPath "scripts\env\env_core.ps1"
if (-not (Test-Path -LiteralPath $coreScript)) {
    throw "Missing env core script: $coreScript"
}
. $coreScript

$passphrase = Get-SecretPassphrase -NonInteractive:$NonInteractive -ProjectRoot $projectRoot
if (-not $passphrase) {
    throw "Missing passphrase. Set STUDYBOOK_SECRET_PASSPHRASE or run interactively."
}
$passphraseText = ConvertTo-PlainTextFromSecureString -SecureString $passphrase
if ([string]::IsNullOrWhiteSpace($passphraseText)) {
    throw "Passphrase cannot be empty."
}

$encryptedPath = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $InputEncryptedFile
if (-not (Test-Path -LiteralPath $encryptedPath)) {
    throw "Encrypted AWS bundle not found: $encryptedPath"
}

$payloadJson = Unprotect-StudyBookSecretFile -EncryptedPath $encryptedPath -Passphrase $passphrase
$data = $payloadJson | ConvertFrom-Json -AsHashtable

if (-not $data.ContainsKey("AWS_CREDENTIALS_INI")) {
    throw "Encrypted payload does not include AWS_CREDENTIALS_INI."
}

$destinationExpanded = [Environment]::ExpandEnvironmentVariables($DestinationDir)
$destinationFull = [System.IO.Path]::GetFullPath($destinationExpanded)
New-Item -ItemType Directory -Path $destinationFull -Force | Out-Null

$credentialsTarget = Join-Path -Path $destinationFull -ChildPath "credentials"
$configTarget = Join-Path -Path $destinationFull -ChildPath "config"

if ($BackupExisting) {
    $stamp = (Get-Date).ToString("yyyyMMddHHmmss")
    if (Test-Path -LiteralPath $credentialsTarget) {
        Copy-Item -LiteralPath $credentialsTarget -Destination "$credentialsTarget.bak.$stamp" -Force
    }
    if (Test-Path -LiteralPath $configTarget) {
        Copy-Item -LiteralPath $configTarget -Destination "$configTarget.bak.$stamp" -Force
    }
}

Set-Content -LiteralPath $credentialsTarget -Value ([string]$data.AWS_CREDENTIALS_INI) -Encoding UTF8

if ($data.ContainsKey("AWS_CONFIG_INI") -and -not [string]::IsNullOrWhiteSpace([string]$data.AWS_CONFIG_INI)) {
    Set-Content -LiteralPath $configTarget -Value ([string]$data.AWS_CONFIG_INI) -Encoding UTF8
}

$profileHint = ""
if ($data.ContainsKey("AWS_PREFERRED_PROFILE")) {
    $profileHint = [string]$data.AWS_PREFERRED_PROFILE
}

Write-Host "AWS credentials restored to: $destinationFull" -ForegroundColor Green
if (-not [string]::IsNullOrWhiteSpace($profileHint)) {
    Write-Host "Preferred profile in bundle: $profileHint" -ForegroundColor Gray
}


