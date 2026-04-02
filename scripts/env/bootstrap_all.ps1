param(
    [string]$MachineName,
    [switch]$NonInteractive,
    [switch]$DeletePlaintextSecrets,
    [switch]$SkipValidation
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $PSScriptRoot -ChildPath "..\.."))
$coreScript = Join-Path -Path $projectRoot -ChildPath "scripts\env\env_core.ps1"
if (-not (Test-Path -LiteralPath $coreScript)) {
    throw "Missing env core script: $coreScript"
}
. $coreScript

function Get-YesNoAnswer {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Prompt,
        [bool]$DefaultYes = $true
    )

    if ($NonInteractive) {
        return $DefaultYes
    }

    $suffix = if ($DefaultYes) { "[Y/n]" } else { "[y/N]" }
    $response = Read-Host "$Prompt $suffix"
    if ([string]::IsNullOrWhiteSpace($response)) {
        return $DefaultYes
    }

    $normalized = $response.Trim().ToLowerInvariant()
    return $normalized -in @("y", "yes")
}

function Ensure-MachineProfile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$NormalizedMachineName
    )

    $profilePath = Join-Path -Path $projectRoot -ChildPath "config\machines\$NormalizedMachineName.psd1"
    if (Test-Path -LiteralPath $profilePath) {
        Write-Host "Machine profile exists: $profilePath" -ForegroundColor Green
        return $profilePath
    }

    $templatePath = Join-Path -Path $projectRoot -ChildPath "config\machines\_template.psd1"
    if (-not (Test-Path -LiteralPath $templatePath)) {
        throw "Machine template file not found: $templatePath"
    }

    $template = Get-Content -LiteralPath $templatePath -Raw -Encoding UTF8
    $content = $template.Replace("replace-me", $NormalizedMachineName)
    Set-Content -LiteralPath $profilePath -Value $content -Encoding UTF8
    Write-Host "Created machine profile: $profilePath" -ForegroundColor Yellow
    return $profilePath
}

function Ensure-PlaintextSecretFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$TemplatePath
    )

    if (Test-Path -LiteralPath $Path) {
        return $false
    }

    if (-not (Test-Path -LiteralPath $TemplatePath)) {
        throw "Secret template file not found: $TemplatePath"
    }

    Copy-Item -LiteralPath $TemplatePath -Destination $Path -Force
    Write-Host "Created plaintext secrets template: $Path" -ForegroundColor Yellow
    return $true
}

function Test-SecretJsonReady {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return $false
    }

    $json = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($json)) {
        return $false
    }

    $data = $json | ConvertFrom-Json -AsHashtable
    foreach ($key in $data.Keys) {
        $value = [string]$data[$key]
        if ([string]::IsNullOrWhiteSpace($value) -or $value -eq "replace-me") {
            return $false
        }
    }
    return $true
}

function Get-ConfirmedPassphrase {
    if (-not [string]::IsNullOrWhiteSpace($env:STUDYBOOK_SECRET_PASSPHRASE)) {
        return ConvertTo-SecureString -String $env:STUDYBOOK_SECRET_PASSPHRASE -AsPlainText -Force
    }

    if ($NonInteractive) {
        return $null
    }

    $pass1 = Read-Host -AsSecureString "Enter encryption passphrase"
    $pass2 = Read-Host -AsSecureString "Confirm encryption passphrase"
    $plain1 = ConvertTo-PlainTextFromSecureString -SecureString $pass1
    $plain2 = ConvertTo-PlainTextFromSecureString -SecureString $pass2
    if ($plain1 -ne $plain2) {
        throw "Passphrases did not match."
    }
    return $pass1
}

if ([string]::IsNullOrWhiteSpace($MachineName)) {
    $MachineName = $env:COMPUTERNAME
}
$normalizedMachine = ConvertTo-NormalizedMachineName -Name $MachineName

Write-Host "== StudyBook Portable Bootstrap ==" -ForegroundColor Cyan
Write-Host "Project Root: $projectRoot" -ForegroundColor Gray
Write-Host "Machine: $normalizedMachine" -ForegroundColor Gray

$profilePath = Ensure-MachineProfile -NormalizedMachineName $normalizedMachine

$templateSecretPath = Join-Path -Path $projectRoot -ChildPath "config\secrets\secrets.template.json"
$sharedSecretPlain = Join-Path -Path $projectRoot -ChildPath "config\secrets\shared.secrets.json"
$machineSecretPlain = Join-Path -Path $projectRoot -ChildPath "config\secrets\$normalizedMachine.secrets.json"
$sharedSecretEnc = Join-Path -Path $projectRoot -ChildPath "config\secrets\shared.secrets.enc.json"
$machineSecretEnc = Join-Path -Path $projectRoot -ChildPath "config\secrets\$normalizedMachine.secrets.enc.json"

$createdSharedTemplate = Ensure-PlaintextSecretFile -Path $sharedSecretPlain -TemplatePath $templateSecretPath
$createdMachineTemplate = Ensure-PlaintextSecretFile -Path $machineSecretPlain -TemplatePath $templateSecretPath

if ($createdSharedTemplate -or $createdMachineTemplate) {
    Write-Host "Fill plaintext secret files before encryption:" -ForegroundColor Yellow
    Write-Host "- $sharedSecretPlain" -ForegroundColor Yellow
    Write-Host "- $machineSecretPlain" -ForegroundColor Yellow
}

$wantsEncryption = Get-YesNoAnswer -Prompt "Encrypt ready secret files now?" -DefaultYes $true
if ($wantsEncryption) {
    $readyShared = Test-SecretJsonReady -Path $sharedSecretPlain
    $readyMachine = Test-SecretJsonReady -Path $machineSecretPlain

    if (-not $readyShared -and -not $readyMachine) {
        Write-Warning "No ready plaintext secret files found. Fill values (no 'replace-me') and rerun bootstrap."
    }
    else {
        $passphrase = Get-ConfirmedPassphrase
        if (-not $passphrase) {
            Write-Warning "Passphrase unavailable. Set STUDYBOOK_SECRET_PASSPHRASE or rerun interactively."
        }
        else {
            if ($readyShared) {
                Protect-StudyBookSecretFile -InputJsonPath $sharedSecretPlain -OutputEncryptedPath $sharedSecretEnc -Passphrase $passphrase
                Write-Host "Encrypted: $sharedSecretEnc" -ForegroundColor Green
                if ($DeletePlaintextSecrets) {
                    Remove-Item -LiteralPath $sharedSecretPlain -Force
                    Write-Host "Deleted plaintext: $sharedSecretPlain" -ForegroundColor DarkYellow
                }
            }
            else {
                Write-Host "Skipped shared secrets encryption (file not ready)." -ForegroundColor Yellow
            }

            if ($readyMachine) {
                Protect-StudyBookSecretFile -InputJsonPath $machineSecretPlain -OutputEncryptedPath $machineSecretEnc -Passphrase $passphrase
                Write-Host "Encrypted: $machineSecretEnc" -ForegroundColor Green
                if ($DeletePlaintextSecrets) {
                    Remove-Item -LiteralPath $machineSecretPlain -Force
                    Write-Host "Deleted plaintext: $machineSecretPlain" -ForegroundColor DarkYellow
                }
            }
            else {
                Write-Host "Skipped machine secrets encryption (file not ready)." -ForegroundColor Yellow
            }
        }
    }
}
else {
    Write-Host "Secret encryption skipped by user choice." -ForegroundColor Yellow
}

if (-not $SkipValidation) {
    Write-Host "Running environment validation..." -ForegroundColor Cyan
    $envSetterPath = Join-Path -Path $projectRoot -ChildPath "env_setter.ps1"
    & $envSetterPath -Machine $normalizedMachine -NonInteractive -SkipVenvActivation
}

Write-Host "Bootstrap complete." -ForegroundColor Green
Write-Host "Machine profile: $profilePath" -ForegroundColor Gray
Write-Host "Read docs: docs/PORTABLE_ENV.md" -ForegroundColor Gray
