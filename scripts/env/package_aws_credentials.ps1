param(
    [string]$CredentialsPath = "$env:USERPROFILE\.aws\credentials",
    [string]$ConfigPath = "$env:USERPROFILE\.aws\config",
    [string]$OutputPlainFile = "config/secrets/aws.profiles.secrets.json",
    [string]$OutputEncryptedFile = "config/secrets/aws.profiles.secrets.enc.json",
    [string]$PreferredProfile,
    [switch]$DeletePlaintext,
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

function Get-IniSectionNames {
    param(
        [string]$Content,
        [switch]$TrimProfilePrefix
    )

    $names = New-Object System.Collections.Generic.List[string]
    if ([string]::IsNullOrWhiteSpace($Content)) {
        return @()
    }

    foreach ($rawLine in $Content -split "`r?`n") {
        $line = $rawLine.Trim()
        if ($line -match "^\[(.+)\]$") {
            $name = [string]$Matches[1].Trim()
            if ($TrimProfilePrefix -and $name -match "^profile\s+(.+)$") {
                $name = [string]$Matches[1].Trim()
            }
            if (-not [string]::IsNullOrWhiteSpace($name) -and -not $names.Contains($name)) {
                $names.Add($name)
            }
        }
    }

    return @($names.ToArray())
}

$credentialsPathExpanded = [Environment]::ExpandEnvironmentVariables($CredentialsPath)
$configPathExpanded = [Environment]::ExpandEnvironmentVariables($ConfigPath)
$credentialsPathFull = [System.IO.Path]::GetFullPath($credentialsPathExpanded)
$configPathFull = [System.IO.Path]::GetFullPath($configPathExpanded)

if (-not (Test-Path -LiteralPath $credentialsPathFull)) {
    throw "AWS credentials file not found: $credentialsPathFull"
}

$passphrase = Get-SecretPassphrase -NonInteractive:$NonInteractive -ProjectRoot $projectRoot
if (-not $passphrase) {
    throw "Missing passphrase. Set STUDYBOOK_SECRET_PASSPHRASE or run interactively."
}
$passphraseText = ConvertTo-PlainTextFromSecureString -SecureString $passphrase
if ([string]::IsNullOrWhiteSpace($passphraseText)) {
    throw "Passphrase cannot be empty."
}

$credentialsRaw = Get-Content -LiteralPath $credentialsPathFull -Raw -Encoding UTF8
$configRaw = if (Test-Path -LiteralPath $configPathFull) {
    Get-Content -LiteralPath $configPathFull -Raw -Encoding UTF8
}
else {
    ""
}

$credentialsProfiles = @(Get-IniSectionNames -Content $credentialsRaw)
$configProfiles = @(Get-IniSectionNames -Content $configRaw -TrimProfilePrefix)
$allProfiles = @($credentialsProfiles + $configProfiles | Sort-Object -Unique)
$selectedProfile = if (-not [string]::IsNullOrWhiteSpace($PreferredProfile)) {
    $PreferredProfile.Trim()
}
elseif ($allProfiles.Count -gt 0) {
    [string]$allProfiles[0]
}
else {
    ""
}

$payload = [ordered]@{
    AWS_EXPORT_UTC         = (Get-Date).ToUniversalTime().ToString("o")
    AWS_SOURCE_HOST        = [string]$env:COMPUTERNAME
    AWS_SOURCE_CREDENTIALS = $credentialsPathFull
    AWS_SOURCE_CONFIG      = if (Test-Path -LiteralPath $configPathFull) { $configPathFull } else { "" }
    AWS_AVAILABLE_PROFILES = $allProfiles
    AWS_PREFERRED_PROFILE  = $selectedProfile
    AWS_CREDENTIALS_INI    = $credentialsRaw
    AWS_CONFIG_INI         = $configRaw
}

$plainPath = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $OutputPlainFile
$encryptedPath = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $OutputEncryptedFile

$plainDir = Split-Path -Path $plainPath -Parent
if (-not [string]::IsNullOrWhiteSpace($plainDir)) {
    New-Item -ItemType Directory -Path $plainDir -Force | Out-Null
}

$payloadJson = $payload | ConvertTo-Json -Depth 8
Set-Content -LiteralPath $plainPath -Value $payloadJson -Encoding UTF8

Protect-StudyBookSecretFile -InputJsonPath $plainPath -OutputEncryptedPath $encryptedPath -Passphrase $passphrase
Write-Host "Encrypted AWS profile bundle written to: $encryptedPath" -ForegroundColor Green
Write-Host "Profiles discovered: $($allProfiles -join ', ')" -ForegroundColor Gray

if ($DeletePlaintext) {
    Remove-Item -LiteralPath $plainPath -Force
    Write-Host "Deleted plaintext AWS bundle: $plainPath" -ForegroundColor DarkYellow
}


