[CmdletBinding()]
param(
    [string]$RepoRoot = (Join-Path $PSScriptRoot '..'),
    [string]$VaultDrive = 'V:',
    [string]$BackupSubdir = 'StudyBook_ignored_backup'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$hashExtensions = @(
    '.pdf', '.docx', '.xlsx', '.png', '.jpg', '.jpeg', '.zip',
    '.eml', '.msg', '.ics', '.txt', '.md', '.json', '.csv',
    '.wav', '.mp3', '.mp4', '.m4a'
)
$maxHashSizeBytes = 128MB

function Get-CanonicalPath {
    param([string]$Path)
    return [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $Path).Path)
}

function Test-TransientFile {
    param([string]$RelativePath)

    $name = [System.IO.Path]::GetFileName($RelativePath)
    $lower = $name.ToLowerInvariant()

    if ($RelativePath -like '.git\*' -or $RelativePath -eq '.git') { return $true }
    if ($lower -in @('thumbs.db', 'desktop.ini', '.ds_store')) { return $true }
    if ($name.StartsWith('~$')) { return $true }
    if ($lower.EndsWith('.tmp') -or $lower.EndsWith('.temp')) { return $true }

    return $false
}

function Should-UseHash {
    param([System.IO.FileInfo]$File)

    if ($File.Length -le $maxHashSizeBytes) { return $true }
    return $hashExtensions -contains $File.Extension.ToLowerInvariant()
}

function Get-FileSignature {
    param([string]$Path)

    $file = Get-Item -LiteralPath $Path
    if (Should-UseHash -File $file) {
        return @{
            Mode = 'hash'
            Value = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
        }
    }

    return @{
        Mode = 'size_only'
        Value = $file.Length
    }
}

function Get-RepoRelativePath {
    param(
        [string]$FullPath,
        [string]$RootPath
    )

    $fullUri = [Uri]((Get-CanonicalPath -Path $FullPath).TrimEnd('\') + '\')
    $rootUri = [Uri]((Get-CanonicalPath -Path $RootPath).TrimEnd('\') + '\')
    $relative = $rootUri.MakeRelativeUri($fullUri).ToString().TrimEnd('/')
    return [Uri]::UnescapeDataString($relative).Replace('/', '\')
}

$repoRootCanonical = Get-CanonicalPath -Path $RepoRoot
$gitRoot = (& git -C $repoRootCanonical rev-parse --show-toplevel 2>$null).Trim()
if ($LASTEXITCODE -ne 0 -or -not $gitRoot) {
    throw "Could not resolve a Git repository at $RepoRoot."
}
$repoRootCanonical = [System.IO.Path]::GetFullPath($gitRoot)
$vaultDriveRoot = $VaultDrive.TrimEnd('\') + '\'

if (-not (Test-Path -LiteralPath $VaultDrive)) {
    throw "Encrypted backup volume $VaultDrive is not mounted. Mount and unlock the BitLocker-protected VHDX before running verification."
}

$vaultRoot = Join-Path $vaultDriveRoot $BackupSubdir
$currentRoot = Join-Path $vaultRoot 'current'
$logRoot = Join-Path $vaultRoot 'logs'
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$logPath = Join-Path $logRoot ("verify_{0}.log" -f $timestamp)

if (-not (Test-Path -LiteralPath $currentRoot)) {
    throw "Backup current mirror not found at $currentRoot"
}
if (-not (Test-Path -LiteralPath $logRoot)) {
    New-Item -ItemType Directory -Path $logRoot | Out-Null
}

function Write-Log {
    param([string]$Message)

    $line = '{0} {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Add-Content -LiteralPath $logPath -Value $line
    Write-Host $Message
}

Write-Log "Starting Git-ignored backup verification for $repoRootCanonical"

$ignoredOutput = & git -C $repoRootCanonical ls-files --others --ignored --exclude-standard 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Git ignored-file discovery failed in $repoRootCanonical."
}

$ignoredRelativePaths = @(
    $ignoredOutput |
        Where-Object { $_ -and -not (Test-TransientFile -RelativePath $_.Replace('/', '\')) } |
        ForEach-Object { $_.Replace('/', '\') }
)

$ignoredSet = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
foreach ($relativePath in $ignoredRelativePaths) {
    [void]$ignoredSet.Add($relativePath)
}

$verifiedCount = 0
$missingCount = 0
$mismatchCount = 0
$extraCount = 0

foreach ($relativePath in ($ignoredRelativePaths | Sort-Object -Unique)) {
    $sourcePath = Join-Path $repoRootCanonical $relativePath
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        continue
    }

    $backupPath = Join-Path $currentRoot $relativePath
    if (-not (Test-Path -LiteralPath $backupPath -PathType Leaf)) {
        $missingCount++
        Write-Log "Missing backup copy: $relativePath"
        continue
    }

    $sourceItem = Get-Item -LiteralPath $sourcePath
    $backupItem = Get-Item -LiteralPath $backupPath
    if ($sourceItem.Length -ne $backupItem.Length) {
        $mismatchCount++
        Write-Log "Size mismatch: $relativePath"
        continue
    }

    $sourceSignature = Get-FileSignature -Path $sourcePath
    $backupSignature = Get-FileSignature -Path $backupPath
    if ($sourceSignature.Mode -eq 'hash' -and $sourceSignature.Value -ne $backupSignature.Value) {
        $mismatchCount++
        Write-Log "Hash mismatch: $relativePath"
        continue
    }

    $verifiedCount++
}

$currentBackupFiles = Get-ChildItem -LiteralPath $currentRoot -Recurse -File
foreach ($backupFile in $currentBackupFiles) {
    $relativePath = Get-RepoRelativePath -FullPath $backupFile.FullName -RootPath $currentRoot
    if (Test-TransientFile -RelativePath $relativePath) {
        continue
    }

    if (-not $ignoredSet.Contains($relativePath)) {
        $extraCount++
        Write-Log "Extra file in current backup mirror: $relativePath"
    }
}

Write-Log "Verification complete. Verified=$verifiedCount Missing=$missingCount Mismatch=$mismatchCount Extra=$extraCount"
Write-Log "Verification log written to $logPath"

if ($missingCount -gt 0 -or $mismatchCount -gt 0) {
    throw "Git-ignored backup verification failed. See $logPath"
}
