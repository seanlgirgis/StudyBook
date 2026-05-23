# UC_001_REAL_APOD_ACCEPTANCE.md

## Validation Context

- Source folder: `D:\Users\shareuser\Downloads\apod`
- Proposal output folder: `D:\AI_Lab\LifeVault\onboarding\proposals\uc001_20260523_061147_apod`
- Command used:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc001_proposal.ps1 -SourcePath "D:\Users\shareuser\Downloads\apod"`

## Artifacts Created

- `proposal.json`
- `summary.md`
- `file_preview.csv`
- `filename_sensitivity_candidates.csv`
- `duplicate_name_candidates.csv`

## Observed Result Summary

- `scan_status = success`
- Story preserved:
  - `BOA / LTIMindtree onboarding paperwork from May 2026.`
- 17 files detected
- 16 PDFs and 1 JPG detected
- filename sensitivity candidates produced
- duplicate-name candidates produced

## Sensitivity Results Summary

- `DDep.pdf` -> `highly_sensitive` (`matched:ddep`)
- `i9form PDF` -> `highly_sensitive` (`matched:i9`)
- `W4.pdf` -> `highly_sensitive` (`matched:w4`)
- `HIPAA Notice` -> `sensitive` (`matched:hipaa`)
- `Privacy notice` -> `sensitive` (`matched:privacy notice`)
- `Applicant Statement` -> `sensitive` (`matched:applicant statement`)
- `Mutual Agreement` -> `sensitive` (`matched:agreement`)
- `Name and Likeness Release` -> `sensitive` (`matched:release`)

## Duplicate Results Summary

- `Template parta cover letter_2026.pdf`
- `Template parta cover letter_2026 (1).pdf`

## Safety Confirmation

- No DB write
- No file copy
- No OneDrive/rclone call
- No delete/move/rename
- No content extraction

## Acceptance Verdict

`UC_001` real apod test accepted for v0.

## v0 Scope Clarification

- UC_001 v0 includes embedded UC_002-lite behavior:
  - metadata/filename/story-based sensitivity hints
  - duplicate-name candidate hints
- UC_011 remains future gated content-based sensitivity detection.