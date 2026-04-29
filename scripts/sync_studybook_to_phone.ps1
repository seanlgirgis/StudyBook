param(
    [switch]$Force,
    [switch]$DryRun,
    [string[]]$IncludeFiles,
    [string[]]$IncludePlaylists,
    [string]$RegistryPath = "D:\Workarea\StudyBook\config\audio\phone_sync_registry.json",
    [string]$RegistryProfile,
    [switch]$PruneDestination,
    [switch]$SyncPlaylists
)

$Source           = "D:\temp\studybook_audio"
$Destination      = "C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook"
$PlaylistDestRoot = "C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\pl"

function Resolve-Mp3Path {
    param(
        [string]$Root,
        [string]$Entry
    )
    $e = $Entry.Trim()
    if ([string]::IsNullOrWhiteSpace($e)) { return $null }
    if ($e.StartsWith("..\StudyBook\", [System.StringComparison]::OrdinalIgnoreCase)) {
        return (Join-Path $Root ($e.Substring("..\StudyBook\".Length)))
    }
    $direct = Join-Path $Root $e
    if (Test-Path -LiteralPath $direct) {
        return $direct
    }
    $nameOnly = Split-Path -Path $e -Leaf
    $hit = Get-ChildItem -Path $Root -Recurse -Filter $nameOnly -File -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) {
        return $hit.FullName
    }
    return $direct
}

function Get-DisplayNameFromPath {
    param([string]$PathLine)
    $leaf = Split-Path -Path $PathLine -Leaf
    if ([string]::IsNullOrWhiteSpace($leaf)) { return "StudyBook Track" }
    $base = [System.IO.Path]::GetFileNameWithoutExtension($leaf)
    if ($base -like "final_*") {
        $base = $base.Substring(6)
    }
    $pretty = $base -replace "[-_]+", " "
    if ([string]::IsNullOrWhiteSpace($pretty)) { return $leaf }
    $ti = [System.Globalization.CultureInfo]::CurrentCulture.TextInfo
    return $ti.ToTitleCase($pretty.ToLower())
}

function Normalize-M3UContent {
    param([string]$RawText)
    $lines = @($RawText -split "(`r`n|`n|`r)")
    $out = New-Object System.Collections.Generic.List[string]
    $out.Add("#EXTM3U")
    $pendingTitle = $null

    foreach ($line in $lines) {
        $trim = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trim)) { continue }
        if ($trim -eq "#EXTM3U") { continue }
        if ($trim.StartsWith("#EXTINF:", [System.StringComparison]::OrdinalIgnoreCase)) {
            $pendingTitle = $trim
            continue
        }
        if ($trim.StartsWith("#")) { continue }

        if ($pendingTitle) {
            $out.Add($pendingTitle)
        } else {
            $title = Get-DisplayNameFromPath -PathLine $trim
            $out.Add("#EXTINF:-1,$title")
        }
        $out.Add($trim)
        $pendingTitle = $null
    }

    return ($out -join "`r`n") + "`r`n"
}

# Validate source
if (-not (Test-Path -LiteralPath $Source)) {
    Write-Host "ERROR: Source not found: $Source" -ForegroundColor Red
    exit 1
}

# Create destination if missing
if (-not (Test-Path -LiteralPath $Destination)) {
    if ($DryRun) {
        Write-Host "[DRY RUN] Would create: $Destination" -ForegroundColor Yellow
    } else {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        Write-Host "Created: $Destination" -ForegroundColor Green
    }
}

# Load optional registry profile
$registryFiles = @()
$registryPlaylists = @()
if ($RegistryProfile) {
    if (-not (Test-Path -LiteralPath $RegistryPath)) {
        Write-Host "ERROR: Registry file not found: $RegistryPath" -ForegroundColor Red
        exit 1
    }
    try {
        $registry = Get-Content -Raw -LiteralPath $RegistryPath | ConvertFrom-Json -ErrorAction Stop
    } catch {
        Write-Host "ERROR: Failed to parse registry JSON at $RegistryPath" -ForegroundColor Red
        exit 1
    }

    $profile = $registry.profiles.PSObject.Properties[$RegistryProfile].Value
    if (-not $profile) {
        Write-Host "ERROR: Registry profile '$RegistryProfile' not found in $RegistryPath" -ForegroundColor Red
        exit 1
    }
    if ($profile.files) {
        $registryFiles = @($profile.files | ForEach-Object { [string]$_ })
    }
    if ($profile.playlists) {
        $registryPlaylists = @($profile.playlists | ForEach-Object { [string]$_ })
    }
}

$effectiveIncludeFiles = @()
if ($registryFiles.Count -gt 0) {
    $effectiveIncludeFiles += $registryFiles
}
if ($IncludeFiles) {
    $effectiveIncludeFiles += $IncludeFiles
}
$effectiveIncludeFiles = @($effectiveIncludeFiles | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)

$effectiveIncludePlaylists = @()
if ($registryPlaylists.Count -gt 0) {
    $effectiveIncludePlaylists += $registryPlaylists
}
if ($IncludePlaylists) {
    $effectiveIncludePlaylists += $IncludePlaylists
}
$effectiveIncludePlaylists = @($effectiveIncludePlaylists | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)

# Collect final_*.mp3 in either targeted or full mode.
if ($effectiveIncludeFiles.Count -gt 0) {
    $files = @()
    foreach ($entry in $effectiveIncludeFiles) {
        $resolved = Resolve-Mp3Path -Root $Source -Entry $entry
        if (-not $resolved) { continue }
        if (-not (Test-Path -LiteralPath $resolved)) {
            Write-Host "WARN: Requested audio not found, skipping: $entry" -ForegroundColor Yellow
            continue
        }
        $item = Get-Item -LiteralPath $resolved
        if ($item.Name -like "final_*.mp3") {
            $files += $item
        } else {
            Write-Host "WARN: Requested file is not final_*.mp3, skipping: $entry" -ForegroundColor Yellow
        }
    }
    $files = @($files | Sort-Object Name -Unique)
} else {
    $files = Get-ChildItem -Path $Source -Recurse -Filter "final_*.mp3" | Sort-Object Name
}

$copied  = 0
$skipped = 0
$failed  = 0
$totalMB = 0.0

Write-Host ""
Write-Host "StudyBook -> Pixel 8 Pro Sync" -ForegroundColor Cyan
Write-Host "Source : $Source"
Write-Host "Dest   : $Destination"
Write-Host "Files  : $($files.Count) found"
if ($effectiveIncludeFiles.Count -gt 0) {
    Write-Host "Scope  : TARGETED" -ForegroundColor Cyan
} else {
    Write-Host "Scope  : FULL LIBRARY" -ForegroundColor DarkYellow
}
if ($DryRun) {
    Write-Host "Mode   : DRY RUN - no files will be written`n" -ForegroundColor Yellow
} else {
    $modeText = if ($Force) { "FORCE (overwrite all)" } else { "SMART (skip unchanged)" }
    Write-Host "Mode   : $modeText`n"
}

# Copy loop
foreach ($file in $files) {
    $dest = Join-Path $Destination $file.Name
    $sizeMB = [math]::Round($file.Length / 1MB, 1)

    # Skip logic: skip if dest exists, same size, and not -Force
    $needsCopy = $true
    if (-not $Force -and (Test-Path -LiteralPath $dest)) {
        $existing = Get-Item -LiteralPath $dest
        if ($existing.Length -eq $file.Length) {
            $needsCopy = $false
        }
    }

    if ($needsCopy) {
        if ($DryRun) {
            Write-Host "  [COPY]  $($file.Name)  ($sizeMB MB)" -ForegroundColor Yellow
        } else {
            try {
                # On MTP/CrossDevice targets, overwrite can create duplicate-suffixed files.
                # Delete first, then copy to enforce a clean refresh of the same filename.
                if (Test-Path -LiteralPath $dest) {
                    Remove-Item -LiteralPath $dest -Force -ErrorAction Stop
                }
                Copy-Item -LiteralPath $file.FullName -Destination $dest -Force
                Write-Host "  COPIED  $($file.Name)  ($sizeMB MB)" -ForegroundColor Green
                $copied++
                $totalMB += $sizeMB
            } catch {
                Write-Host "  FAILED  $($file.Name) - $($_.Exception.Message)" -ForegroundColor Red
                $failed++
            }
        }
    } else {
        Write-Host "  skip    $($file.Name)" -ForegroundColor DarkGray
        $skipped++
    }
}

# Optional pruning for exact destination set.
if ($PruneDestination -and $effectiveIncludeFiles.Count -gt 0) {
    $selectedNames = @($files | ForEach-Object { $_.Name })
    $destMp3 = @(Get-ChildItem -Path $Destination -Filter "final_*.mp3" -ErrorAction SilentlyContinue)
    foreach ($d in $destMp3) {
        if ($selectedNames -notcontains $d.Name) {
            if ($DryRun) {
                Write-Host "  [DELETE] $($d.Name)" -ForegroundColor Yellow
            } else {
                try {
                    Remove-Item -LiteralPath $d.FullName -Force -ErrorAction Stop
                    Write-Host "  DELETED $($d.Name)" -ForegroundColor Magenta
                } catch {
                    Write-Host "  FAILED DELETE $($d.Name) - $($_.Exception.Message)" -ForegroundColor Red
                    $failed++
                }
            }
        }
    }
}

# Optional M3U sync to playlist folder.
if ($SyncPlaylists) {
    if (-not (Test-Path -LiteralPath $PlaylistDestRoot)) {
        if ($DryRun) {
            Write-Host "[DRY RUN] Would create playlist destination: $PlaylistDestRoot" -ForegroundColor Yellow
        } else {
            New-Item -ItemType Directory -Path $PlaylistDestRoot -Force | Out-Null
            Write-Host "Created playlist destination: $PlaylistDestRoot" -ForegroundColor Green
        }
    }

    $playlistFiles = @()
    if ($effectiveIncludePlaylists.Count -gt 0) {
        foreach ($plName in $effectiveIncludePlaylists) {
            $plPath = Join-Path $Source $plName
            if (-not (Test-Path -LiteralPath $plPath)) {
                Write-Host "WARN: Requested playlist not found, skipping: $plName" -ForegroundColor Yellow
                continue
            }
            $playlistFiles += Get-Item -LiteralPath $plPath
        }
        $playlistFiles = @($playlistFiles | Sort-Object Name -Unique)
    } else {
        $playlistFiles = Get-ChildItem -Path $Source -Filter "*.m3u" | Sort-Object Name
    }

    foreach ($pl in $playlistFiles) {
        $destPl = Join-Path $PlaylistDestRoot $pl.Name
        if ($DryRun) {
            Write-Host "  [M3U]   $($pl.Name)" -ForegroundColor Yellow
        } else {
            try {
                $raw = Get-Content -Raw -LiteralPath $pl.FullName
                $normalized = Normalize-M3UContent -RawText $raw
                Set-Content -LiteralPath $pl.FullName -Value $normalized
                if (Test-Path -LiteralPath $destPl) {
                    Remove-Item -LiteralPath $destPl -Force -ErrorAction Stop
                }
                Copy-Item -LiteralPath $pl.FullName -Destination $destPl -Force
                Write-Host "  M3U     $($pl.Name)" -ForegroundColor Cyan
            } catch {
                Write-Host "  FAILED  $($pl.Name) - $($_.Exception.Message)" -ForegroundColor Red
                $failed++
            }
        }
    }
}

# Summary
Write-Host ""
Write-Host "-------------------------------------" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "DRY RUN complete - no files written"
} else {
    $totalMB = [math]::Round($totalMB, 1)
    Write-Host "Copied : $copied files  ($totalMB MB transferred)"
    Write-Host "Skipped: $skipped files  (already up to date)"
    if ($failed -gt 0) {
        Write-Host "Failed : $failed files" -ForegroundColor Red
    }
    $destCount = (Get-ChildItem -Path $Destination -Filter '*.mp3').Count
    Write-Host "Total in destination: $destCount mp3 files"
}
Write-Host "-------------------------------------" -ForegroundColor Cyan
Write-Host ""
