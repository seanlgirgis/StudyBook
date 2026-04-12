param(
    [Parameter(Mandatory=$true)][string]$SiteKey,
    [string]$Machine,
    [string]$EncryptedFile,
    [switch]$ShowInfo,
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

$machineName = if (-not [string]::IsNullOrWhiteSpace($Machine)) {
    $Machine
}
elseif (-not [string]::IsNullOrWhiteSpace($env:STUDYBOOK_MACHINE)) {
    $env:STUDYBOOK_MACHINE
}
else {
    $env:COMPUTERNAME
}
$normalizedMachine = ConvertTo-NormalizedMachineName -Name $machineName

$encryptedPath = if ([string]::IsNullOrWhiteSpace($EncryptedFile)) {
    Join-Path -Path $projectRoot -ChildPath "config\secrets\$normalizedMachine.secrets.enc.json"
}
else {
    Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $EncryptedFile
}

if (-not (Test-Path -LiteralPath $encryptedPath)) {
    throw "Encrypted secrets file not found: $encryptedPath"
}

$normalizedSite = ($SiteKey.Trim().ToUpperInvariant() -replace "[^A-Z0-9]", "_")
if ([string]::IsNullOrWhiteSpace($normalizedSite)) {
    throw "Invalid SiteKey '$SiteKey'."
}

$userKey = "JOBSITE_${normalizedSite}_USER"
$urlKey = "JOBSITE_${normalizedSite}_URL"
$passKey = "JOBSITE_${normalizedSite}_PASSWORD"

$passphrase = Get-SecretPassphrase -NonInteractive:$NonInteractive -ProjectRoot $projectRoot
if (-not $passphrase) {
    throw "No passphrase source available. Seed or STUDYBOOK_SECRET_PASSPHRASE is required."
}

$plain = Unprotect-StudyBookSecretFile -EncryptedPath $encryptedPath -Passphrase $passphrase
if ([string]::IsNullOrWhiteSpace($plain)) {
    throw "Decrypted secrets content is empty."
}

$secrets = ConvertFrom-JsonToHashtable -Json $plain
if (-not $secrets.ContainsKey($passKey)) {
    throw "No password key found for site '$SiteKey' (expected key: $passKey)."
}

$password = [string]$secrets[$passKey]
if ([string]::IsNullOrWhiteSpace($password)) {
    throw "Password value for '$SiteKey' is empty."
}

Set-Clipboard -Value $password
Write-Host "Password copied to clipboard for '$SiteKey'." -ForegroundColor Green

if ($ShowInfo) {
    if ($secrets.ContainsKey($userKey)) {
        Write-Host "User: $($secrets[$userKey])" -ForegroundColor Gray
    }
    if ($secrets.ContainsKey($urlKey)) {
        Write-Host "URL: $($secrets[$urlKey])" -ForegroundColor Gray
    }
}
