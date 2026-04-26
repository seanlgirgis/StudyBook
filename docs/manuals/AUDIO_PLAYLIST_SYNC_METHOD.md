# Audio Playlist + Phone Sync Method (Persisted SOP)

Last updated: 2026-04-26

## Scope

This SOP defines where StudyBook playlists live, how to place new topic audio into playlists, and how to sync MP3 + playlist files to phone.

Linked handoff source:
- `..\..\tutorials\_manager\AUDIO_HANDOFF.md`

## Canonical Locations

Audio root:
- `D:\temp\studybook_audio\`

Playlist files:
- Stored flat at the audio root (not in a `playlists/` subfolder)
- Pattern: `PL-XX <Name>.m3u`

Topic audio folders:
- `D:\temp\studybook_audio\{slug}\final_{slug}.mp3`

Phone sync script:
- `..\..\scripts\sync_studybook_to_phone.ps1`

## Playlist Format Rules

- Use `#EXTM3U` header.
- Use one `#EXTINF` line per track followed by the filename.
- Track path is filename-only, example:
  - `final_aws-eventbridge.mp3`
- Keep playlists flat-reference style because phone destination is also flat.

Example entry:
```text
#EXTINF:-1,AWS EventBridge
final_aws-eventbridge.mp3
```

## Assignment Rule for New Topics

1. Place topic into one or more existing thematic playlists.
2. Optionally add to a short-term "new additions" playlist for immediate listening.
3. Keep naming and style consistent with existing `.m3u` files.

## Latest Applied Updates

Added to existing playlists:
- `PL-04 AWS Data Stack.m3u`
  - `final_aws-eventbridge.mp3`
- `PL-05 Streaming & Real-Time.m3u`
  - `final_apache-flink.mp3`

Created playlist:
- `PL-13 New Additions.m3u`
  - `final_apache-flink.mp3`
  - `final_aws-eventbridge.mp3`

## Phone Sync Method

Run from StudyBook root:

```powershell
cd D:\Workarea\StudyBook
```

Dry run first:

```powershell
.\scripts\sync_studybook_to_phone.ps1 -DryRun
```

Normal smart sync (recommended):

```powershell
.\scripts\sync_studybook_to_phone.ps1
```

Force overwrite all files:

```powershell
.\scripts\sync_studybook_to_phone.ps1 -Force
```

## Preconditions for Sync

- Pixel connected via USB.
- USB mode set to **File Transfer (MTP)**.
- Phone unlocked during copy.

## Quick Verification

After sync, verify destination contains both files and playlist:

```powershell
Get-ChildItem "C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook" -Filter "*eventbridge*"
Get-ChildItem "C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook" -Filter "*flink*"
Get-ChildItem "C:\Users\shareuser\CrossDevice\Pixel 8 Pro\storage\Music\StudyBook" -Filter "PL-13*"
```

## Baseline Confirmation (Persisted)

Confirmed on 2026-04-26:
- `final_apache-flink.mp3` is present on phone destination.
- `final_aws-eventbridge.mp3` is present on phone destination.
- `PL-13 New Additions.m3u` is present on phone destination.
- Smart sync completed successfully via `.\scripts\sync_studybook_to_phone.ps1`.
