param(
    [string]$Machine,
    [string]$EncryptedFile,
    [string[]]$Entry,
    [string]$JsonFile,
    [string[]]$PromptSecretKey,
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

$hasEntry = ($Entry -and $Entry.Count -gt 0)
$hasJson = -not [string]::IsNullOrWhiteSpace($JsonFile)
$hasPromptSecret = ($PromptSecretKey -and $PromptSecretKey.Count -gt 0)
if (-not $hasEntry -and -not $hasJson -and -not $hasPromptSecret) {
    throw "Provide -Entry KEY=VALUE, -JsonFile <path>, or -PromptSecretKey <KEY>."
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

if ([string]::IsNullOrWhiteSpace($EncryptedFile)) {
    $encryptedPath = Join-Path -Path $projectRoot -ChildPath "config\secrets\$normalizedMachine.secrets.enc.json"
}
else {
    $encryptedPath = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $EncryptedFile
}

$updates = @{}

if ($hasJson) {
    $jsonPath = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $JsonFile
    if (-not (Test-Path -LiteralPath $jsonPath)) {
        throw "Json file not found: $jsonPath"
    }

    $jsonRaw = Get-Content -LiteralPath $jsonPath -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($jsonRaw)) {
        throw "Json file is empty: $jsonPath"
    }

    $jsonData = ConvertFrom-JsonToHashtable -Json $jsonRaw
    foreach ($key in $jsonData.Keys) {
        $updates[[string]$key] = [string]$jsonData[$key]
    }
}

if ($hasEntry) {
    foreach ($item in $Entry) {
        if ([string]::IsNullOrWhiteSpace($item)) {
            continue
        }

        $eqIndex = $item.IndexOf("=")
        if ($eqIndex -lt 1) {
            throw "Invalid -Entry '$item'. Expected KEY=VALUE."
        }

        $key = $item.Substring(0, $eqIndex).Trim()
        $value = $item.Substring($eqIndex + 1)
        if ([string]::IsNullOrWhiteSpace($key)) {
            throw "Invalid -Entry '$item'. Key cannot be empty."
        }

        $updates[$key] = [string]$value
    }
}

if ($hasPromptSecret) {
    if ($NonInteractive) {
        throw "-PromptSecretKey requires interactive mode. Remove -NonInteractive."
    }

    foreach ($keyRaw in $PromptSecretKey) {
        $key = [string]$keyRaw
        if ([string]::IsNullOrWhiteSpace($key)) {
            continue
        }

        $trimmedKey = $key.Trim()
        $secureValue = Read-Host -AsSecureString "Enter secret value for $trimmedKey"
        $plainValue = ConvertTo-PlainTextFromSecureString -SecureString $secureValue
        if ([string]::IsNullOrWhiteSpace($plainValue)) {
            throw "Secret value for '$trimmedKey' cannot be empty."
        }

        $updates[$trimmedKey] = $plainValue
    }
}

if ($updates.Count -eq 0) {
    throw "No valid updates were provided."
}

$passphrase = Get-SecretPassphrase -NonInteractive:$NonInteractive -ProjectRoot $projectRoot
if (-not $passphrase) {
    throw "No passphrase source available. Set STUDYBOOK_SECRET_PASSPHRASE, register seed, or run interactively."
}

$secrets = @{}
if (Test-Path -LiteralPath $encryptedPath) {
    $existingJson = Unprotect-StudyBookSecretFile -EncryptedPath $encryptedPath -Passphrase $passphrase
    if (-not [string]::IsNullOrWhiteSpace($existingJson)) {
        $existing = ConvertFrom-JsonToHashtable -Json $existingJson
        foreach ($key in $existing.Keys) {
            $secrets[[string]$key] = [string]$existing[$key]
        }
    }
}

foreach ($key in $updates.Keys) {
    $secrets[$key] = [string]$updates[$key]
}

$plainJson = $secrets | ConvertTo-Json -Depth 20
Protect-StudyBookSecretContent -PlainText $plainJson -OutputEncryptedPath $encryptedPath -Passphrase $passphrase

$updatedKeys = @($updates.Keys | Sort-Object)
Write-Host "Updated encrypted secrets: $encryptedPath" -ForegroundColor Green
Write-Host "Machine scope: $normalizedMachine" -ForegroundColor Gray
Write-Host "Keys updated: $($updatedKeys -join ', ')" -ForegroundColor Cyan
