# CODEX CONTEXT — Read This at the Start of Every Session
# Owner: Sean Girgis | seanlgirgis@gmail.com
# Last updated: 2026-04-24

---

## WORKING DIRECTORY — ALWAYS RUN FROM HERE

All commands in every mission file assume your working directory is the StudyBook root.
Set it once at the start of every Codex session and never change it:

```
WORKING DIRECTORY: D:\StudyBook\
```

All paths below are relative to that root. Never use absolute paths.

---

## THREE REPOSITORIES UNDER THIS ROOT

```
D:\StudyBook\                          ← ROOT (your working directory)
│
│   env_setter.ps1                     ← MUST run this before any Python/OpenAI script
│   playground\                        ← Jupyter notebooks (CodeSignal practice, etc.)
│   prompts\
│       codex_missions\                ← THIS FOLDER — all Codex mission files live here
│
├── temp\jobsearch\                    ← REPO 2: Job search system
│       data\
│           interview_prep\
│               audio_prep\            ← Audio scripts and generated MP3 clips go here
│                   {topic}\
│                       audio_script_{topic}.md
│                       audio_clips\
│                           01_HOST.mp3 ...
│                       final_{topic}.mp3
│       scripts\
│           generate_audio_generic.py  ← TTS pipeline script
│       prompts\
│           AudioPrepForIntrviews\
│               audio_script_master_rules_reliable_tts.md
│           learning_artifact_prompt_template.md
│
└── temp\seanlgirgis.github.io\        ← REPO 3: Personal website
        learning\
            aws-ec2.html               ← Existing learning pages (8 total)
            aws-athena.html
            aws-s3.html
            aws-glue.html
            aws-redshift.html
            aws-lambda.html
            apache-kafka.html
            aws-ecs.html
            _prompts\                  ← Website-specific prompt archive (separate from codex_missions)
```

---

## PYTHON ENVIRONMENT SETUP

The OpenAI API key and all Python environment variables are loaded via:
```
.\env_setter.ps1
```

Run this from the StudyBook root at the start of any session that calls Python scripts.
Verify it worked:
```powershell
python -c "import os; print(bool(os.getenv('OPENAI_API_KEY')))"
```
Expected: `True`. If `False`: stop and report — do not call any OpenAI API.

---

## RELATIVE PATH REFERENCE (from D:\StudyBook\)

| What | Relative Path |
|------|--------------|
| Env setter | `.\env_setter.ps1` |
| Audio pipeline script | `temp\jobsearch\scripts\generate_audio_generic.py` |
| Audio prep output folder | `temp\jobsearch\data\interview_prep\audio_prep\` |
| Jobsearch prompts | `temp\jobsearch\prompts\` |
| Master TTS rules | `temp\jobsearch\prompts\AudioPrepForIntrviews\audio_script_master_rules_reliable_tts.md` |
| Artifact template | `temp\jobsearch\prompts\learning_artifact_prompt_template.md` |
| Website learning pages | `temp\seanlgirgis.github.io\learning\` |
| Codex missions (here) | `prompts\codex_missions\` |
| Playground notebooks | `playground\` |

---

## EXISTING LEARNING PAGES — AUDIO STATUS

| File (relative path) | Audio | Video | Action |
|----------------------|-------|-------|--------|
| temp\seanlgirgis.github.io\learning\aws-ec2.html | NotebookLM .m4a | NotebookLM .mp4 | Replace audio, keep video |
| temp\seanlgirgis.github.io\learning\aws-athena.html | NotebookLM .m4a | NotebookLM .mp4 | Replace audio, keep video |
| temp\seanlgirgis.github.io\learning\aws-s3.html | NotebookLM .m4a | NotebookLM .mp4 | Replace audio, keep video |
| temp\seanlgirgis.github.io\learning\aws-glue.html | NotebookLM .m4a | NotebookLM .mp4 | Replace audio, keep video |
| temp\seanlgirgis.github.io\learning\aws-redshift.html | NotebookLM .m4a | NotebookLM .mp4 | Replace audio, keep video |
| temp\seanlgirgis.github.io\learning\aws-lambda.html | NotebookLM .m4a | NotebookLM .mp4 | Replace audio, keep video |
| temp\seanlgirgis.github.io\learning\apache-kafka.html | ❌ Placeholder | ❌ None | Add new audio |
| temp\seanlgirgis.github.io\learning\aws-ecs.html | ❌ Placeholder | ❌ None | Add new audio |

---

## HTML FRAMEWORK — CSS RULES (DO NOT DEVIATE)

Every learning page uses these exact CSS variables — never change:
```css
--primary: #004a99;   --accent: #e67e22;    --text: #222;
--muted:   #666;      --bg:     #f4f7f6;    --line: #dde3ea;
--code-bg: #1e2a38;   --code-fg:#e8edf2;    --hi-bg:#e8f4fd;
--warn-bg: #fff8e6;
```

Key CSS classes:
- `.hi`        — blue left-border callout (key insight)
- `.warn`      — orange left-border callout (warning/gotcha)
- `.qa` / `.qa-q` / `.qa-a` — interview Q&A blocks
- `.cheat` / `.cheat-row` / `.ct` / `.cd` — quick reference cheat sheet
- `.cheat-row` grid: `grid-template-columns: 170px 1fr` ← exact value, do not change

Audio box — pages WITH existing video (keep video, replace audio only):
```html
<div class="audio-box">
  <div class="audio-label">🎧 Audio Overview</div>
  <audio controls preload="metadata" style="width:100%;margin-top:6px;">
    <source src="https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{topic}.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
  <div class="video-hint" style="margin-top:10px;">🎬 Video Overview (NotebookLM)</div>
  <video controls preload="metadata" style="width:100%;max-width:100%;border-radius:4px;margin-top:8px;">
    <source src="EXISTING_VIDEO_URL_UNCHANGED" type="video/mp4">
  </video>
</div>
```

Audio box — pages WITHOUT video (kafka, ecs, all new pages):
```html
<div class="audio-box">
  <div class="audio-label">🎧 Audio Overview</div>
  <audio controls preload="metadata" style="width:100%;margin-top:6px;">
    <source src="https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{topic}.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
</div>
```

R2 bucket base URL: `https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/`

---

## AUDIO PIPELINE — OVERVIEW

Audio script source files live under:
`temp\jobsearch\data\interview_prep\audio_prep\{topic-slug}\`

Generated clips/final files live under:
`C:\temp\studybook_audio\{topic-slug}\`

```
Step 1  Codex writes HOST+SEAN dialogue script
        → saves to: temp\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md

Step 2  Load environment
        → .\env_setter.ps1

Step 3  Run fail-fast mission runner (preferred)
        → .\scripts\run_mission_audio.ps1 "temp\jobsearch\data\interview_prep\audio_prep\{slug}\audio_script_{slug}.md" -ChunkSize 750
        → clips: C:\temp\studybook_audio\{slug}\audio_clips\
        → final: C:\temp\studybook_audio\{slug}\final_{slug}.mp3
        → upload guide: C:\temp\studybook_audio\{slug}\UPLOAD_INSTRUCTIONS.md

Step 4  Upload final_{slug}.mp3 to R2 (Sean does this manually)

Step 5  Codex updates the HTML src in temp\seanlgirgis.github.io\learning\{file}.html
```

---

## TTS SCRIPT FORMAT — MANDATORY

Every audio script file structure:

```
## API INSTRUCTIONS
Target model: gpt-4o-mini-tts / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova | SEAN voice: onyx
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.
---

**[HOST — voice: nova]**

Spoken text...

---

**[SEAN — voice: onyx]**

Spoken text...

---

## END OF SCRIPT
```

TTS rules (apply without exception in every script):
- Contractions mandatory: "It is" → "It's" | "Do not" → "Don't" | "I am" → "I'm"
- Pausing: `,` micro | `...` thoughtful (max 4/block) | `......` topic shift | `—` contrast
- ALL CAPS emphasis: key metrics/contrast only — max 3 per block
- Phonetic normalization — every acronym:
  AWS→A-W-S | API→A-P-I | ETL→E-T-L | ECS→E-C-S | CI/CD→C-I-C-D | SQL→S-Q-L
  IAM→I-A-M | JWT→J-W-T | REST→R-E-S-T | VPC→V-P-C | EBS→E-B-S | AMI→A-M-I
  ASG→A-S-G | ALB→A-L-B | NLB→N-L-B | MSK→M-S-K | SQS→S-Q-S | ECR→E-C-R
  HCL→H-C-L | IaC→I-A-C | FastAPI→Fast-A-P-I | PySpark→Pie-Spark
- No markdown inside spoken text (no **, #, backticks, bullet points)
- Chunk size: ~1,200–1,800 characters per block
- SEAN opens every answer with a rotating bridge (never repeat twice in a row):
  "So... basically..." | "Here's the thing..." | "Here's the key insight..."
  "Right... so the way I think about this..." | "Let me give you a concrete example..."
  "Two things matter here..." | "Now... the important distinction is..."

---

## WORK ORDER

PHASE 1 — Fix audio on existing 8 pages (EC2 is test case — do first)
PHASE 2 — Create new learning pages: Terraform, FastAPI, CI/CD, CloudFormation, MSK, Snowflake+PyIceberg, OpenSearch
PHASE 3 — Tutorials + Capstone projects per topic

Full queue: see prompts\codex_missions\README.md
