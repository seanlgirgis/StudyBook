# JOB: SB-AUDIO-CURE-V1

Purpose: Repair weak TTS topic-by-topic using approved voice profile, then republish with the same final filename/key.

Locked profile:
- HOST: `nova`
- SEAN: `echo`
- SEAN post-process: `softC` (gentle soften chain, no pitch shift)

Status values:
- `queued`
- `in_progress`
- `qa`
- `published`
- `done`
- `blocked`

Priority values:
- `urgent`
- `normal`
- `backlog`

## Queue

| topic | priority | status | source_script | final_filename | published_url | last_run_date | notes |
|---|---|---|---|---|---|---|---|
| aws-athena | urgent | queued | D:\Workarea\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md | final_aws-athena.mp3 |  |  | baseline cure job |

## Run Checklist (Per Topic)

1. Regenerate chunks with locked profile.
2. Apply `softC` filter to SEAN chunks only.
3. Stitch to `final_<topic>.mp3`.
4. QA sample listen (start, mid, end).
5. Upload to same key/filename.
6. Verify playback URL.
7. Mark row `done` with date + notes.

## Notes

- Keep original filenames to avoid breaking website/audio links.
- Process urgent topics first; use normal/backlog during free cycles.
