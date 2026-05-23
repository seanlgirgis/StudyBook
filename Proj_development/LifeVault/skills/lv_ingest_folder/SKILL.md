# LV_ingest_folder

## Purpose

Ingest a local folder into a controlled onboarding pod as a copy-first workflow.

## Inputs

- Source folder path (operator-provided)
- Intake notes/story context
- Sensitivity hints

## Outputs

- Pod manifest proposal
- Initial metadata records
- Intake report summary

## Constraints

- No delete, move, or rename of source files.
- No extraction of sensitive real content without explicit approval.
- Use config-defined operational paths.