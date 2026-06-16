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
        Mode = 'size_mtime'
        Value = '{0}:{1}' -f $file.Length, $file.LastWriteTimeUtc.Ticks
    }
}

function Ensure-Directory {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Remove-EmptyDirectoriesUpward {
    param(
        [string]$StartPath,
        [string]$StopPath
    )

    $current = Split-Path -Parent $StartPath
    $stopCanonical = (Get-CanonicalPath -Path $StopPath).TrimEnd('\')

    while ($current -and (Test-Path -LiteralPath $current)) {
        $currentCanonical = (Get-CanonicalPath -Path $current).TrimEnd('\')
        if ($currentCanonical -eq $stopCanonical) {
            break
        }

        if ((Get-ChildItem -LiteralPath $current -Force | Measure-Object).Count -eq 0) {
            Remove-Item -LiteralPath $current -Force
            $current = Split-Path -Parent $current
        } else {
            break
        }
    }
}

$repoRootCanonical = Get-CanonicalPath -Path $RepoRoot
$gitRoot = (& git -C $repoRootCanonical rev-parse --show-toplevel 2>$null).Trim()
if ($LASTEXITCODE -ne 0 -or -not $gitRoot) {
    throw "Could not resolve a Git repository at $RepoRoot."
}
$repoRootCanonical = [System.IO.Path]::GetFullPath($gitRoot)
$vaultDriveRoot = $VaultDrive.TrimEnd('\') + '\'

if (-not (Test-Path -LiteralPath $VaultDrive)) {
    throw "Encrypted backup volume $VaultDrive is not mounted. Mount and unlock the BitLocker-protected VHDX before running this backup."
}

$vaultRoot = Join-Path $vaultDriveRoot $BackupSubdir
$currentRoot = Join-Path $vaultRoot 'current'
$snapshotRoot = Join-Path $vaultRoot 'snapshots'
$logRoot = Join-Path $vaultRoot 'logs'
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$runSnapshotRoot = Join-Path $snapshotRoot $timestamp
$changedSnapshotRoot = Join-Path $runSnapshotRoot 'changed'
$removedSnapshotRoot = Join-Path $runSnapshotRoot 'removed'
$logPath = Join-Path $logRoot ("backup_{0}.log" -f $timestamp)

Ensure-Directory -Path $currentRoot
Ensure-Directory -Path $snapshotRoot
Ensure-Directory -Path $logRoot

function Write-Log {
    param([string]$Message)

    $line = '{0} {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Add-Content -LiteralPath $logPath -Value $line
    Write-Host $Message
}

Write-Log "Starting Git-ignored backup for $repoRootCanonical"
Write-Log "Backup root: $vaultRoot"

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

$copiedCount = 0
$unchangedCount = 0
$changedSnapshotCount = 0
$removedSnapshotCount = 0

foreach ($relativePath in ($ignoredRelativePaths | Sort-Object -Unique)) {
    $sourcePath = Join-Path $repoRootCanonical $relativePath
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        Write-Log "Skipping non-file ignored path: $relativePath"
        continue
    }

    $destinationPath = Join-Path $currentRoot $relativePath
    Ensure-Directory -Path (Split-Path -Parent $destinationPath)

    $needsCopy = $true
    if (Test-Path -LiteralPath $destinationPath -PathType Leaf) {
        $sourceSignature = Get-FileSignature -Path $sourcePath
        $destinationSignature = Get-FileSignature -Path $destinationPath

        if ($sourceSignature.Mode -eq $destinationSignature.Mode -and $sourceSignature.Value -eq $destinationSignature.Value) {
            $needsCopy = $false
            $unchangedCount++
        } else {
            $snapshotPath = Join-Path $changedSnapshotRoot $relativePath
            Ensure-Directory -Path (Split-Path -Parent $snapshotPath)
            Copy-Item -LiteralPath $destinationPath -Destination $snapshotPath -Force
            $changedSnapshotCount++
            Write-Log "Snapshotted changed backup copy: $relativePath"
        }
    }

    if ($needsCopy) {
        Copy-Item -LiteralPath $sourcePath -Destination $destinationPath -Force

        if (-not (Test-Path -LiteralPath $destinationPath -PathType Leaf)) {
            throw "Backup copy missing after copy: $relativePath"
        }

        $sourceItem = Get-Item -LiteralPath $sourcePath
        $destinationItem = Get-Item -LiteralPath $destinationPath
        if ($sourceItem.Length -ne $destinationItem.Length) {
            throw "Backup copy size mismatch for $relativePath"
        }

        $sourceSignature = Get-FileSignature -Path $sourcePath
        $destinationSignature = Get-FileSignature -Path $destinationPath
        if ($sourceSignature.Mode -eq 'hash' -and $sourceSignature.Value -ne $destinationSignature.Value) {
            throw "Backup copy hash mismatch for $relativePath"
        }

        $copiedCount++
        Write-Log "Copied ignored file: $relativePath"
    }
}

if (Test-Path -LiteralPath $currentRoot) {
    $currentBackupFiles = Get-ChildItem -LiteralPath $currentRoot -Recurse -File
    foreach ($backupFile in $currentBackupFiles) {
        $relativePath = Get-RepoRelativePath -FullPath $backupFile.FullName -RootPath $currentRoot
        if ($ignoredSet.Contains($relativePath)) {
            continue
        }

        if (Test-TransientFile -RelativePath $relativePath) {
            continue
        }

        $snapshotPath = Join-Path $removedSnapshotRoot $relativePath
        Ensure-Directory -Path (Split-Path -Parent $snapshotPath)
        Copy-Item -LiteralPath $backupFile.FullName -Destination $snapshotPath -Force
        Remove-Item -LiteralPath $backupFile.FullName -Force
        Remove-EmptyDirectoriesUpward -StartPath $backupFile.FullName -StopPath $currentRoot
        $removedSnapshotCount++
        Write-Log "Snapshotted removed ignored file and removed from current mirror: $relativePath"
    }
}

Write-Log "Backup complete. Copied=$copiedCount Unchanged=$unchangedCount ChangedSnapshots=$changedSnapshotCount RemovedSnapshots=$removedSnapshotCount"
Write-Log "Backup log written to $logPath"
