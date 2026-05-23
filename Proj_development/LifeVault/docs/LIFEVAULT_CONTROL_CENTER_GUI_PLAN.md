# LIFEVAULT_CONTROL_CENTER_GUI_PLAN.md

## Goal

Define an operator-facing GUI (`LV_control_center`) for safe ingestion, review, dedupe, and publish workflows.

## Initial Panels

- Intake setup
- LV_ingest_folder v0 operator workflow (UC_001 summary, explicit UC_003 approval, pod summary)
- Pod review queue
- Duplicate review
- Metadata/story editor
- Publish approval gate
- Search memory console

## Safety UX

- Explicit approval actions for publish/move/rename/delete-equivalent operations.
- Strong warning banners for sensitive operations.
- Read-only default posture for remote browsing.
- Separate UI stages for metadata/filename sensitivity vs content sensitivity.
- Content inspection controls must require explicit approval and enforce redaction/logging safeguards.
