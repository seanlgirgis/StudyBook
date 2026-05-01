# Audio Generation — Canonical Stand-In Thread

Purpose: operational stand-in for the recovered chat at `recovered_chats/Audio Generation.md`, so future sessions can use this as the canonical quick-reference thread.

## Canonical Source

- Full recovered transcript:
  - `recovered_chats/Audio Generation.md`
- This stand-in is the skim-friendly ops layer; transcript remains turn-level authority.

## Session Identity

- Original thread id: `019de123-ef4d-78f2-8a62-1adc96d6ad41`
- Recovery window in transcript: primarily `2026-04-22` to `2026-04-24`
- Runtime root: `D:\Workarea\StudyBook`

## Objective Arc

This thread established a practical end-to-end audio workflow for interview prep:

1. Configure OpenAI key using StudyBook seed-backed encrypted secrets.
2. Validate model calls and diagnose quota/billing blockers.
3. Standardize chunked generation and stitch/archive flow.
4. Harden prompt files for realistic, safe, reusable TTS script conversion.
5. Lock preflight requirements for future agent runs.

## Major Milestones

1. Key onboarding and secure storage
- User requested encrypted handling.
- Flow aligned to:
  - `.\scripts\env\set_secret.ps1 -Machine asuspc -PromptSecretKey "OPENAI_API_KEY"`
- `env_setter.ps1` confirmed as required load step.

2. First audio smoke test and failure diagnosis
- JS test script executed successfully from correct path.
- API call returned `429 insufficient_quota`, confirming key wiring was correct but billing/quota unavailable at that moment.

3. Git hygiene issue surfaced and corrected
- `node_modules` content was accidentally staged/committed during push flow.
- Session guidance emphasized cleanup and keeping runtime dependencies out of tracked commit scope.

4. Chunked generation pipeline validated
- Multi-chunk MP3 outputs generated into `C:\temp`.
- Stitch flow created final merged MP3.
- Original chunk files archived into `C:\temp\recycle\...`.

5. Prompt hardening and naming normalization
- Improved prompt quality for realistic speech and anti-drift controls.
- Renamed prompt for recognizability:
  - `D:\Workarea\jobsearch\prompts\audio_script_master_rules_reliable_tts.md`
- Refined `convert_prep_to_audio_script.md`, then restored strict no mid-answer split rule per user workflow requirement.

6. Process contract clarified
- Pipeline expectation fixed as:
  - split at speaker-block boundaries only,
  - generate one audio artifact per block,
  - stitch to one final distributable file.
- Mandatory preflight added: run `.\env_setter.ps1`, verify `OPENAI_API_KEY` is loaded, then execute generation.

## Canonical Operating Decisions Captured

1. Secret handling
- Use seed-backed encrypted secret workflow; avoid plaintext key exposure in chat/files/command history.

2. Startup invariant
- Run from StudyBook root and load environment first:
- `cd D:\Workarea\StudyBook`
- `.\env_setter.ps1`

3. Output-location invariant
- Keep generated chunk/final media under temp paths (`C:\temp\...`), not tracked repo content.

4. Split policy
- Never split in the middle of a single speaker answer.
- If chunking is needed, split only between complete dialogue blocks.

5. Reassembly policy
- Default workflow is many chunk MP3s first, then deterministic stitch to one final MP3, then archive chunks.

## Reusable Command Pattern (Condensed)

1. Preflight
- `.\env_setter.ps1`
- verify env key loaded (without printing value)

2. Generate
- run `sbaudio <chunk_file.md> --chunk-chars 6000` for each block file

3. Stitch
- concatenate generated chunk MP3s in sequence into one final file in `C:\temp`

4. Archive
- move source chunk MP3s into `C:\temp\recycle\<timestamped_folder>`

## Canonical Paths

- StudyBook runtime root:
  - `D:\Workarea\StudyBook`
- Prompt files:
  - `D:\Workarea\jobsearch\prompts\convert_prep_to_audio_script.md`
  - `D:\Workarea\jobsearch\prompts\audio_script_master_rules_reliable_tts.md`
- Prep/source docs:
  - `D:\Workarea\jobsearch\data\interview_prep\active_interviews\*.md`
- Chunk/final outputs:
  - `C:\temp\chunk_*.mp3`
  - `C:\temp\*_Final_*.mp3`
  - `C:\temp\recycle\*`

## Known Pain Points Logged

- Billing UI interpretation caused confusion between paid balance and grant credit display.
- Path mismatches (`.\scripts\...` vs repo root) caused avoidable execution errors.
- Mid-answer splitting is unacceptable for later manual edits/restitching.

## Future Reuse Guidance

1. Treat this file as the runbook summary for audio generation onboarding.
2. Keep strict speaker-block split policy unchanged unless user explicitly overrides.
3. Keep env preflight and temp-output policy as hard gates.
4. Fall back to recovered transcript for full turn-by-turn detail.

## Transcript Authority

For complete command/output/message detail:
- `recovered_chats/Audio Generation.md`
