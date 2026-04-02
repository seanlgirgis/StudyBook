param(
    [Parameter(Mandatory = $true)]
    [string]$InputFile,
    [Parameter(Mandatory = $true)]
    [string]$OutputFile,
    [switch]$DeleteInput
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $PSScriptRoot -ChildPath "..\.."))
$coreScript = Join-Path -Path $projectRoot -ChildPath "scripts\env\env_core.ps1"
. $coreScript

$inPath = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $InputFile
$outPath = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $OutputFile

$pass1 = Read-Host -AsSecureString "Enter encryption passphrase"
$pass2 = Read-Host -AsSecureString "Confirm encryption passphrase"

$plain1 = ConvertTo-PlainTextFromSecureString -SecureString $pass1
$plain2 = ConvertTo-PlainTextFromSecureString -SecureString $pass2
if ($plain1 -ne $plain2) {
    throw "Passphrases did not match."
}

Protect-StudyBookSecretFile -InputJsonPath $inPath -OutputEncryptedPath $outPath -Passphrase $pass1
Write-Host "Encrypted secrets written to: $outPath" -ForegroundColor Green

if ($DeleteInput) {
    Remove-Item -LiteralPath $inPath -Force
    Write-Host "Deleted plaintext input file: $inPath" -ForegroundColor Yellow
}
