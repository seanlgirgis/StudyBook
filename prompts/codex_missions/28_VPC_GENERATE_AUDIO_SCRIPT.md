# MISSION 28 — Generate Audio Script: AWS VPC
# Working directory: D:\Workarea\StudyBook\
# No existing HTML page to read — this is a new topic (Phase 2)
# Output: ..\jobsearch\data\interview_prep\audio_prep\aws-vpc\audio_script_aws-vpc.md

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\Workarea\StudyBook
```
All paths are relative to D:\Workarea\StudyBook\. Use no absolute paths.

---

## PRE-FLIGHT

1. Confirm working directory:
   ```powershell
   Get-Location
   ```

2. Create output folder:
   ```powershell
   New-Item -ItemType Directory -Force -Path "..\jobsearch\data\interview_prep\audio_prep\aws-vpc"
   ```

---

## YOUR TASK

Write a complete HOST+SEAN dialogue script for AWS VPC.

Save to:
`..\jobsearch\data\interview_prep\audio_prep\aws-vpc\audio_script_aws-vpc.md`

Target: ~14-18 speaker blocks, ~10-13 minutes total audio.

---

## OUTPUT LOCATION RULE (MANDATORY)

- Keep only the script in repo:
  - `..\jobsearch\data\interview_prep\audio_prep\aws-vpc\audio_script_aws-vpc.md`
- All generated audio artifacts MUST be outside repo:
  - `C:\temp\studybook_audio\aws-vpc\audio_clips\`
  - `C:\temp\studybook_audio\aws-vpc\final_aws-vpc.mp3`
  - `C:\temp\studybook_audio\aws-vpc\UPLOAD_INSTRUCTIONS.md`
- Never keep `audio_clips`, `.mp3`, `.m4a`, or `filelist.txt` under `D:\Workarea\StudyBook`.

---

## SCRIPT FORMAT (NON-NEGOTIABLE)

File must start with this exact header:
```
## API INSTRUCTIONS

Target model: gpt-4o-mini-audio-preview (preferred) / gpt-4o-mini-tts (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: AWS VPC
Output filename: final_aws-vpc.mp3
Script path: ..\jobsearch\data\interview_prep\audio_prep\aws-vpc\audio_script_aws-vpc.md

---
```

Use exact speaker block format:
```
**[HOST — voice: nova]**

Spoken text...

---

**[SEAN — voice: onyx]**

Spoken text...

---
```

Rules:
- One blank line after speaker label
- `---` after every block
- One speaker per block only
- Chunk size target per block: ~1,200-1,800 chars
- End file with: `## END OF SCRIPT`

---

## SPEAKER STYLE

HOST (nova):
- short prompts, 1-3 sentences
- natural transitions, curious tone

SEAN (onyx):
- senior, calm, concrete
- each answer starts with a varied conversational bridge (do not repeat same bridge consecutively)
- closes clearly with takeaways

---

## TTS NORMALIZATION RULES

- Use contractions in spoken text ("it's", "don't", "you'll", "we've")
- Use punctuation pauses naturally; max 4 `...` per block
- Avoid markdown inside spoken text
- Expand acronyms phonetically where needed:
  - AWS → A-W-S
  - VPC → V-P-C
  - CIDR → C-I-D-R
  - NAT → N-A-T
  - IGW → I-G-W
  - NACL → N-A-C-L
  - ENI → E-N-I
  - EC2 → E-C-2
  - ALB → A-L-B
  - NLB → N-L-B
  - DNS → D-N-S
  - AZ → A-Z

---

## CONTENT OUTLINE (WRITE IN THIS ORDER)

1. What VPC is and why it matters
2. CIDR blocks, subnets, and AZ design
3. Route tables and routing behavior
4. Internet Gateway vs NAT Gateway
5. Public vs private subnets (real workload patterns)
6. Security Groups vs NACLs (stateful vs stateless)
7. VPC endpoints (gateway and interface) and cost/security tradeoffs
8. VPC peering vs Transit Gateway
9. Hybrid networking (VPN + Direct Connect basics)
10. DNS in VPC (Route 53 private hosted zones, resolver behavior)
11. High availability network architecture patterns
12. Common mistakes and debugging checklist
13. Interview recap Q&A (exactly 5 HOST/SEAN rapid-fire pairs)

Include concrete engineering examples throughout (data platform, Glue/Lambda/Redshift connectivity patterns).

---

## POST-WRITE CHECKLIST

- [ ] Header is exact and complete
- [ ] All blocks follow exact speaker format
- [ ] Every block ends with `---`
- [ ] No mixed speakers in one block
- [ ] No markdown formatting in spoken text
- [ ] All required VPC topics covered in order
- [ ] Recap section has exactly 5 rapid-fire Q&A pairs
- [ ] File ends with `## END OF SCRIPT`
- [ ] Saved to correct path

Report:
- `MISSION 28 COMPLETE — script saved — [N] blocks — est. [X] min audio`
- or `MISSION 28 BLOCKED — [reason]`

---

## AFTER THIS MISSION

Run master pipeline with topic slug `aws-vpc`:
`prompts\codex_missions\Existing_work_pipeline_execution_master.md`

Expected script input:
`..\jobsearch\data\interview_prep\audio_prep\aws-vpc\audio_script_aws-vpc.md`

Canonical run command:
```powershell
cd D:\Workarea\StudyBook
.\scripts\run_mission_audio.ps1 "..\jobsearch\data\interview_prep\audio_prep\aws-vpc\audio_script_aws-vpc.md" -ChunkSize 750 -RequestTimeoutSeconds 120
```

Post-run cleanliness check (must be empty):
```powershell
rg --files -g "*.mp3" -g "*.m4a" -g "*filelist.txt" ..\jobsearch\data\interview_prep\audio_prep\aws-vpc
```

After R2 upload confirm URL:
`https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-vpc.mp3`

Then run Mission 29.

