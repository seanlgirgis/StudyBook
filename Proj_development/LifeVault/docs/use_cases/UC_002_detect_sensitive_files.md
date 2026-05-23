# UC_002_detect_sensitive_files.md

## Use Case ID

UC_002

## Name

Detect Sensitive Files by Metadata and Filename Rules

## Goal

Classify likely sensitivity using filename/folder/extension/rule signals plus source/story hints, without opening file contents.

## Safety Boundaries

- Must not open full file contents.
- Must not extract full text.
- Must not cache text.
- Must not send file contents to AI.
- Must not upload anything.
- Must not delete/move/rename/copy source files.

## Detection Inputs

- Filename rules
- Folder-name rules
- Extension rules
- Source/story hints

## Sensitivity Levels

- `unknown`
- `public`
- `normal`
- `private`
- `sensitive`
- `highly_sensitive`

## Example Rules

- `W4`, `W-4`, `I9`, `I-9`, `direct deposit`, `direct_deposit`, `ddep`, `payroll`, `bank`, `banking`, `SSN`, `social security`, `passport`, `driver license`, `tax` -> `highly_sensitive`
- `HIPAA`, `medical`, `insurance`, `legal`, `agreement`, `release`, `privacy notice`, `applicant statement` -> `sensitive` (or `highly_sensitive` where combined with stronger terms)
- `onboarding`, `new hire`, `policy/policies`, `manual/helpmanual`, `password reset`, `employee/employer`, `career` -> baseline `private`

Priority:

- `highly_sensitive` overrides `sensitive` and `private`.
- `sensitive` overrides `private`.
- `private` is baseline only.

## Dependencies

UC_001 proposal outputs, sensitivity policy, review workflow.

## Outputs

- `sensitivity_candidates.csv` or JSON
- per-record reasons
- confidence
- recommended next action

## Acceptance Criteria

- Produces sensitivity candidate list with reasons and confidence.
- Supports human override decision path.
- Performs no content extraction.

## v0 Integration Note

- UC_002 v0 filename/rule-based detection is currently embedded in UC_001 proposal generation.
- A separate UC_002 command can be added later if richer review/reporting workflows are needed.
