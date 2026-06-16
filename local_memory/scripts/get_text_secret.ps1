[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Key,
    [switch]$ShowPlaintext,
    [switch]$SetEnv,
    [switch]$NonInteractive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path -Path $PSScriptRoot -ChildPath '_vault_common.ps1')

$secretId = ConvertTo-SecretId -RawId $Key
$passphrase = Get-VaultPassphrase -NonInteractive:$NonInteractive
$secrets = Get-VaultSecretsHashtable -Passphrase $passphrase

if (-not $secrets.ContainsKey($secretId)) {
    throw "Secret '$secretId' not found in vault."
}

$value = [string]$secrets[$secretId]

if ($SetEnv) {
    Set-Item -Path "Env:$secretId" -Value $value
    Write-Host "Set environment variable: $secretId" -ForegroundColor Green
    return
}

if ($ShowPlaintext) {
    Write-Output $value
    return
}

Write-Host "Secret: $secretId" -ForegroundColor Cyan
Write-Host "Masked: $(Format-SecretMask -Value $value)" -ForegroundColor Gray
Write-Host "Use -ShowPlaintext to print the value, or -SetEnv to load into the current shell." -ForegroundColor Gray