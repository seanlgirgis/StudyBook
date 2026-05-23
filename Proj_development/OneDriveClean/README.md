# OneDriveClean v0.1

OneDriveClean is a safe local AI/data-engineering workflow for onboarding files from any source directory into controlled pods, indexing metadata, and later promoting approved files to a clean OneDrive vault.

Primary workflow:

source directory
  -> proposal
  -> human approval/edit
  -> onboarding pod
  -> index database
  -> duplicate/review reports
  -> later approved vault copy

Safety:
- copy only
- no delete/move/rename of source files
- no OneDrive upload yet in this phase
- no rclone sync
- metadata only (no real text extraction)

Quick command:

```powershell
.\pod.ps1 "D:\Users\shareuser\Downloads\apod"
```

Alternative:

```powershell
.\scripts\start_pod_intake.ps1 -SourcePath "D:\Users\shareuser\Downloads\apod"
```

The intake flow creates a rules-based proposal, saves it under `D:\AI_Lab\OneDriveClean\onboarding\proposals`, prints it, and asks:
- `A` accept and create pod
- `E` edit fields interactively then create pod
- `S` save proposal only
- `Q` quit
