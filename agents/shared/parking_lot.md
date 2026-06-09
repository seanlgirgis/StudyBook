# Parking Lot

Use this file to capture useful findings that are out of scope for the current task.

## Entry Template

- Item ID: PARK-###
- Date: YYYY-MM-DD
- Found During Task: TB-YYYYMMDD-XX
- Observation: short factual note
- Suggested Follow-up: next concrete action
- Priority: low | medium | high

## Items

- Item ID: PARK-001
- Date: 2026-04-27
- Found During Task: TB-20260427-01
- Observation: `tutorials/06_aws_emr/capstone/brief.md` lists `cleanup.py` and `test_capstone.py`, but those files are not present in the current capstone folder.
- Suggested Follow-up: add `capstone/cleanup.py` and `capstone/test_capstone.py` to complete the EMR capstone runnable/testable contract.
- Priority: medium

- Item ID: PARK-002
- Date: 2026-06-07
- Found During Task: TB-20260607-01
- Observation: `study_maps/DataCamp/skill_tracks` currently contains duplicate numeric prefixes across placeholder folders (`06` through `12`), which means the placeholder numbering scheme is not yet reconciled.
- Suggested Follow-up: normalize the placeholder skill-track numbering and folder names before treating the skill-track library as final.
- Priority: medium

- Item ID: PARK-003
- Date: 2026-06-07
- Found During Task: TB-20260607-01
- Observation: `study_maps/DataCamp/career_tracks/index.html` links to `28_java_developer/index.html`, but no matching `career_tracks/28_java_developer` folder exists.
- Suggested Follow-up: either create the missing placeholder folder/page or remove the broken link from the career-track index.
- Priority: low
