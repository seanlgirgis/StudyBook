[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Key,
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

$secrets.Remove($secretId) | Out-Null
Save-VaultSecretsHashtable -Secrets $secrets -Passphrase $passphrase

if (Test-Path -LiteralPath $script:RegistryPath) {
    $content = Get-Content -LiteralPath $script:RegistryPath -Raw -Encoding UTF8
    $pattern = "(?m)^\| $([regex]::Escape($secretId)) \|.*\r?\n?"
    $content = [regex]::Replace($content, $pattern, '')
    Set-Content -LiteralPath $script:RegistryPath -Value $content -Encoding UTF8 -NoNewline
}

Write-Host "Removed text secret: $secretId" -ForegroundColor Green