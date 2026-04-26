# ============================================================
# sync_studybook_to_phone.ps1
# Copies all final_*.mp3 files from D:\temp\studybook_audio\
# to the Pixel 8 Pro Music folder (flat — all in one folder).
#
# Run:  .\scripts\sync_studybook_to_phone.ps1
# Flags: -Force    overwrite all files even if unchanged
#        -DryRun   show what would be copied without doing it
# ============================================================

param(
    [switch]$Force,
    [switch]$DryRun
)

$Source      = "D:\temp\studybook_audio"
$Destination = "C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook"

# ── Validate source ──────────────────────────────────────────
if (-not (Test-Path $Source)) {
    Write-Host "ERROR: Source not found: $Source" -ForegroundColor Red
    exit 1
}

# ── Create destination if missing ────────────────────────────
if (-not (Test-Path $Destination)) {
    if ($DryRun) {
        Write-Host "[DRY RUN] Would create: $Destination" -ForegroundColor Yellow
    } else {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        Write-Host "Created: $Destination" -ForegroundColor Green
    }
}

# ── Collect all final_*.mp3 recursively ─────────────────────
$files = Get-ChildItem -Path $Source -Recurse -Filter "final_*.mp3" | Sort-Object Name

$copied  = 0
$skipped = 0
$failed  = 0
$totalMB = 0

Write-Host ""
Write-Host "StudyBook → Pixel 8 Pro Sync" -ForegroundColor Cyan
Write-Host "Source : $Source"
Write-Host "Dest   : $Destination"
Write-Host "Files  : $($files.Count) found"
if ($DryRun) { Write-Host "Mode   : DRY RUN — no files will be written`n" -ForegroundColor Yellow }
else         { Write-Host "Mode   : $(if ($Force) { 'FORCE (overwrite all)' } else { 'SMART (skip unchanged)' })`n" }

# ── Copy loop ────────────────────────────────────────────────
foreach ($file in $files) {
    $dest = Join-Path $Destination $file.Name
    $sizeMB = [math]::Round($file.Length / 1MB, 1)

    # Skip logic: skip if dest exists, same size, and not -Force
    $needsCopy = $true
    if (-not $Force -and (Test-Path $dest)) {
        $existing = Get-Item $dest
        if ($existing.Length -eq $file.Length) {
            $needsCopy = $false
        }
    }

    if ($needsCopy) {
        if ($DryRun) {
            Write-Host "  [COPY]  $($file.Name)  (${sizeMB} MB)" -ForegroundColor Yellow
        } else {
            try {
                Copy-Item -Path $file.FullName -Destination $dest -Force
                Write-Host "  COPIED  $($file.Name)  (${sizeMB} MB)" -ForegroundColor Green
                $copied++
                $totalMB += $sizeMB
            } catch {
                Write-Host "  FAILED  $($file.Name) — $_" -ForegroundColor Red
                $failed++
            }
        }
    } else {
        Write-Host "  skip    $($file.Name)" -ForegroundColor DarkGray
        $skipped++
    }
}

# ── Sync M3U playlists ───────────────────────────────────────
$playlists = Get-ChildItem -Path $Source -Filter "*.m3u"
foreach ($pl in $playlists) {
    $destPl = Join-Path $Destination $pl.Name
    if ($DryRun) {
        Write-Host "  [M3U]   $($pl.Name)" -ForegroundColor Yellow
    } else {
        Copy-Item -Path $pl.FullName -Destination $destPl -Force
        Write-Host "  M3U     $($pl.Name)" -ForegroundColor Cyan
    }
}

# ── Summary ──────────────────────────────────────────────────
Write-Host ""
Write-Host "─────────────────────────────────────" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "DRY RUN complete — no files written"
} else {
    Write-Host "Copied : $copied files  (${totalMB} MB transferred)"
    Write-Host "Skipped: $skipped files  (already up to date)"
    if ($failed -gt 0) {
        Write-Host "Failed : $failed files" -ForegroundColor Red
    }
    Write-Host "Total in destination: $((Get-ChildItem $Destination -Filter '*.mp3').Count) mp3 files"
}
Write-Host "─────────────────────────────────────" -ForegroundColor Cyan
Write-Host ""
