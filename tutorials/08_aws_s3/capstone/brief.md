# S3 Data Lake Foundation — Capstone

## Scenario
Manufacturing IoT system:
- Sensors produce CSV files
- Files land in `raw/`
- Pipeline promotes valid data to `bronze/`

## Pipeline Flow
raw/ → validate → bronze/ (tagged) → lifecycle → access → cost reporting

## What You Built

### setup.py
- Create bucket
- Enable:
  - Versioning
  - Encryption (SSE-S3 or SSE-KMS)
  - Block Public Access
- Lifecycle:
  - raw/: 30d → STANDARD_IA → 180d → GLACIER_IR → 730d delete
  - bronze/: no expiration

### ingest.py
- Generate 10 CSV files
- Upload to raw/
- Validate size > 0
- Copy to bronze/ with tags

### access.py
- Generate presigned URLs for last 5 bronze files

### cost_report.py
- Current size + cost
- 12-month projection
- Compare vs all STANDARD

### cleanup.py
- Delete all objects + bucket

## Acceptance Criteria
✔ Versioning, encryption, Block Public Access enabled  
✔ bronze objects tagged  
✔ Presigned URLs valid  
✔ Cost reduction demonstrated  