[CmdletBinding()]
param(
    [switch]$NonInteractive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path -Path $PSScriptRoot -ChildPath '_vault_common.ps1')

if (-not (Test-Path -LiteralPath $script:VaultEncryptedPath)) {
    Write-Host "No encrypted vault file yet: $script:VaultEncryptedPath" -ForegroundColor Yellow
    return
}

$passphrase = Get-VaultPassphrase -NonInteractive:$NonInteractive
$secrets = Get-VaultSecretsHashtable -Passphrase $passphrase
$keys = @($secrets.Keys | Sort-Object)

if ($keys.Count -eq 0) {
    Write-Host "Vault exists but contains no text secrets." -ForegroundColor Yellow
    return
}

Write-Host "Text secrets in vault ($($keys.Count)):" -ForegroundColor Cyan
foreach ($key in $keys) {
    Write-Host "  - $key"
}
Write-Host "See runbooks\secret_registry.md for purpose and retrieve commands." -ForegroundColor Gray