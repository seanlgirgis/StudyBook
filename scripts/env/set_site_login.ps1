param(
    [Parameter(Mandatory=$true)][string]$SiteKey,
    [Parameter(Mandatory=$true)][string]$Email,
    [Parameter(Mandatory=$true)][string]$Url,
    [string]$Machine,
    [string]$EncryptedFile,
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

if ($NonInteractive) {
    throw "set_site_login.ps1 requires interactive password entry. Remove -NonInteractive."
}

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

$normalizedSite = ($SiteKey.Trim().ToUpperInvariant() -replace "[^A-Z0-9]", "_")
if ([string]::IsNullOrWhiteSpace($normalizedSite)) {
    throw "Invalid SiteKey '$SiteKey'."
}

$userKey = "JOBSITE_${normalizedSite}_USER"
$urlKey = "JOBSITE_${normalizedSite}_URL"
$passKey = "JOBSITE_${normalizedSite}_PASSWORD"

$securePassword = Read-Host -AsSecureString "Enter password for $SiteKey"
$password = ConvertTo-PlainTextFromSecureString -SecureString $securePassword
if ([string]::IsNullOrWhiteSpace($password)) {
    throw "Password cannot be empty."
}

$passphrase = Get-SecretPassphrase -NonInteractive:$NonInteractive -ProjectRoot $projectRoot
if (-not $passphrase) {
    throw "No passphrase source available. Seed or STUDYBOOK_SECRET_PASSPHRASE is required."
}

$secrets = @{}
if (Test-Path -LiteralPath $encryptedPath) {
    $existingJson = Unprotect-StudyBookSecretFile -EncryptedPath $encryptedPath -Passphrase $passphrase
    if (-not [string]::IsNullOrWhiteSpace($existingJson)) {
        $existing = ConvertFrom-JsonToHashtable -Json $existingJson
        foreach ($k in $existing.Keys) {
            $secrets[[string]$k] = [string]$existing[$k]
        }
    }
}

$secrets[$userKey] = $Email
$secrets[$urlKey] = $Url
$secrets[$passKey] = $password

$plainJson = $secrets | ConvertTo-Json -Depth 20
Protect-StudyBookSecretContent -PlainText $plainJson -OutputEncryptedPath $encryptedPath -Passphrase $passphrase

Write-Host "Saved encrypted site login for '$SiteKey'" -ForegroundColor Green
Write-Host "Machine scope: $normalizedMachine" -ForegroundColor Gray
Write-Host "Keys: $userKey, $urlKey, $passKey" -ForegroundColor Cyan
Write-Host "Retrieve password later:" -ForegroundColor Yellow
Write-Host "  .\\scripts\\env\\copy_site_password.ps1 -SiteKey '$SiteKey'" -ForegroundColor Yellow
