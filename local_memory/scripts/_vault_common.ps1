Set-StrictMode -Version Latest

$script:LocalMemoryRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $PSScriptRoot -ChildPath '..'))
$script:StudyBookRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $script:LocalMemoryRoot -ChildPath '..'))
$script:VaultEncryptedPath = Join-Path -Path $script:LocalMemoryRoot -ChildPath 'secrets\vault.secrets.enc.json'
$script:VaultFilesRoot = Join-Path -Path $script:LocalMemoryRoot -ChildPath 'secrets\files'
$script:RegistryPath = Join-Path -Path $script:LocalMemoryRoot -ChildPath 'runbooks\secret_registry.md'

$coreScript = Join-Path -Path $script:StudyBookRoot -ChildPath 'scripts\env\env_core.ps1'
if (-not (Test-Path -LiteralPath $coreScript)) {
    throw "Missing StudyBook env core script: $coreScript"
}
. $coreScript

function Get-VaultEncryptedRelativePath {
    return 'local_memory\secrets\vault.secrets.enc.json'
}

function Ensure-VaultDirectories {
    $secretsRoot = Join-Path -Path $script:LocalMemoryRoot -ChildPath 'secrets'
    if (-not (Test-Path -LiteralPath $secretsRoot)) {
        New-Item -ItemType Directory -Path $secretsRoot -Force | Out-Null
    }
    if (-not (Test-Path -LiteralPath $script:VaultFilesRoot)) {
        New-Item -ItemType Directory -Path $script:VaultFilesRoot -Force | Out-Null
    }
}

function Get-VaultPassphrase {
    param([switch]$NonInteractive)

    $passphrase = Get-SecretPassphrase -NonInteractive:$NonInteractive -ProjectRoot $script:StudyBookRoot
    if (-not $passphrase) {
        throw "No passphrase available. Register seed: StudyBook\scripts\env\register_secret_seed.ps1 — or set STUDYBOOK_SECRET_PASSPHRASE."
    }
    return $passphrase
}

function Get-VaultSecretsHashtable {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$Passphrase
    )

    if (-not (Test-Path -LiteralPath $script:VaultEncryptedPath)) {
        return @{}
    }

    $json = Unprotect-StudyBookSecretFile -EncryptedPath $script:VaultEncryptedPath -Passphrase $Passphrase
    if ([string]::IsNullOrWhiteSpace($json)) {
        return @{}
    }

    return ConvertFrom-JsonToHashtable -Json $json
}

function Save-VaultSecretsHashtable {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Secrets,
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$Passphrase
    )

    Ensure-VaultDirectories
    $plainJson = $Secrets | ConvertTo-Json -Depth 20
    Protect-StudyBookSecretContent -PlainText $plainJson -OutputEncryptedPath $script:VaultEncryptedPath -Passphrase $Passphrase
}

function ConvertTo-SecretId {
    param([Parameter(Mandatory = $true)][string]$RawId)

    $normalized = $RawId.Trim().ToUpperInvariant() -replace '[^A-Z0-9]+', '_'
    $normalized = $normalized.Trim('_')
    if ([string]::IsNullOrWhiteSpace($normalized)) {
        throw "Secret ID '$RawId' is invalid after normalization."
    }
    return $normalized
}

function Format-SecretMask {
    param([string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return '<empty>'
    }
    if ($Value.Length -le 4) {
        return '****'
    }
    return $Value.Substring(0, 2) + ('*' * [Math]::Min(8, $Value.Length - 2))
}

function Update-SecretRegistryRow {
    param(
        [Parameter(Mandatory = $true)][string]$Id,
        [Parameter(Mandatory = $true)][string]$Type,
        [Parameter(Mandatory = $true)][string]$Purpose,
        [Parameter(Mandatory = $true)][string]$Storage,
        [Parameter(Mandatory = $true)][string]$Retrieve
    )

    $today = Get-Date -Format 'yyyy-MM-dd'
    $row = "| $Id | $Type | $Purpose | $Storage | $Retrieve | $today |"

    if (-not (Test-Path -LiteralPath $script:RegistryPath)) {
        throw "Secret registry not found: $script:RegistryPath"
    }

    $content = Get-Content -LiteralPath $script:RegistryPath -Raw -Encoding UTF8
    $pattern = "(?m)^\| $([regex]::Escape($Id)) \|.*$"
    if ([regex]::IsMatch($content, $pattern)) {
        $content = [regex]::Replace($content, $pattern, $row)
    }
    else {
        $content = $content.TrimEnd() + "`r`n$row`r`n"
    }

    Set-Content -LiteralPath $script:RegistryPath -Value $content -Encoding UTF8 -NoNewline
}