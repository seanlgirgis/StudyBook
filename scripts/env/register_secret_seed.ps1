param(
    [string]$SeedPath = "config/secrets/.local/studybook.secret.seed.dpapi.json",
    [switch]$Force,
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

$seedPathResolved = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $SeedPath

if ((Test-Path -LiteralPath $seedPathResolved) -and -not $Force) {
    if ($NonInteractive) {
        throw "Seed file already exists at $seedPathResolved. Re-run with -Force to overwrite."
    }

    $confirm = Read-Host "Seed file exists at $seedPathResolved. Overwrite? [y/N]"
    if ($confirm.Trim().ToLowerInvariant() -notin @('y','yes')) {
        Write-Host "Seed registration cancelled." -ForegroundColor Yellow
        exit 0
    }
}

$passphraseSecure = $null
if (-not [string]::IsNullOrWhiteSpace($env:STUDYBOOK_SECRET_PASSPHRASE)) {
    $passphraseSecure = ConvertTo-SecureString -String $env:STUDYBOOK_SECRET_PASSPHRASE -AsPlainText -Force
}
elseif ($NonInteractive) {
    throw "Missing passphrase. Set STUDYBOOK_SECRET_PASSPHRASE or run interactively."
}
else {
    $pass1 = Read-Host -AsSecureString "Enter STUDYBOOK secrets passphrase"
    $pass2 = Read-Host -AsSecureString "Confirm STUDYBOOK secrets passphrase"
    $plain1 = ConvertTo-PlainTextFromSecureString -SecureString $pass1
    $plain2 = ConvertTo-PlainTextFromSecureString -SecureString $pass2
    if ($plain1 -ne $plain2) {
        throw "Passphrases did not match."
    }
    $passphraseSecure = $pass1
}

Protect-StudyBookSecretSeed -Passphrase $passphraseSecure -SeedPath $seedPathResolved
Write-Host "Seed file created: $seedPathResolved" -ForegroundColor Green
Write-Host "This file is machine/user-bound via DPAPI and should remain local only." -ForegroundColor Gray
