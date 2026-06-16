[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Key,
    [string]$Purpose,
    [string]$Value,
    [switch]$NonInteractive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path -Path $PSScriptRoot -ChildPath '_vault_common.ps1')

$secretId = ConvertTo-SecretId -RawId $Key
$purposeText = if ([string]::IsNullOrWhiteSpace($Purpose)) { $secretId } else { $Purpose.Trim() }

$plainValue = $Value
if ([string]::IsNullOrWhiteSpace($plainValue)) {
    if ($NonInteractive) {
        throw "Provide -Value or run interactively without -NonInteractive."
    }
    $secureValue = Read-Host -AsSecureString "Enter secret value for $secretId"
    $plainValue = ConvertTo-PlainTextFromSecureString -SecureString $secureValue
}

if ([string]::IsNullOrWhiteSpace($plainValue)) {
    throw "Secret value cannot be empty."
}

$passphrase = Get-VaultPassphrase -NonInteractive:$NonInteractive
$secrets = Get-VaultSecretsHashtable -Passphrase $passphrase
$secrets[$secretId] = [string]$plainValue
Save-VaultSecretsHashtable -Secrets $secrets -Passphrase $passphrase

$storage = 'secrets\vault.secrets.enc.json'
$retrieve = "pwsh -File local_memory\scripts\get_text_secret.ps1 -Key $secretId"
Update-SecretRegistryRow -Id $secretId -Type 'text' -Purpose $purposeText -Storage $storage -Retrieve $retrieve

Write-Host "Stored text secret: $secretId" -ForegroundColor Green
Write-Host "Encrypted file: $script:VaultEncryptedPath" -ForegroundColor Gray
Write-Host "Registry updated: $script:RegistryPath" -ForegroundColor Gray