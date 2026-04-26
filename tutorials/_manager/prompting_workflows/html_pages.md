# Prompting Workflow — HTML Learning Page Generation
# Last updated: 2026-04-25

---

## Overview

Gap prompt file → ChatGPT Project 2 → HTML page → save → commit → push → live

---

## Step 1 — Prepare the Gap Prompt

Gap files live in: `D:\StudyBook\temp\gap\NN_topic_prompts.md`
The **Project 2 section** is the HTML page prompt.

Format recap:
- Numbered section list (sections 1-11)
- Each section: title, focus paragraph, bullet details, code block guidance
- "include a code block where it adds value (20 lines max)"
- SCOPE FENCE at bottom: 5 bullets limiting topic, depth, and length

---

## Step 2 — Generate HTML in ChatGPT Project 2

**Project:** "Project 2 — HTML Page Generator"
**Prompt file:** `D:\users\shareuser\Downloads\Project2_HTML_MAKER.txt`

1. Open ChatGPT → switch to Project 2
2. Start a new conversation
3. Paste the **Project 2 section** from the gap file
4. ChatGPT returns: complete HTML file with styling, all 11 sections

**Quality checks before accepting:**
- 11 sections match what was requested
- Each section has 2-3 focused paragraphs (not a wall of text)
- Code blocks are ≤20 lines and actually illustrate the concept
- No stray "In this section we will..." filler phrases
- Audio player `<audio>` tag is present (even if src is placeholder)
- Meta description and page title are accurate

---

## Step 3 — Save HTML File

Save to: `D:\StudyBook\temp\seanlgirgis.github.io\learning\{slug}.html`

If the file already exists (update scenario):
1. Read the existing file first
2. Replace only the sections that changed
3. Preserve the existing audio `<source src="...">` URL

---

## Step 4 — Commit and Push

```powershell
cd D:\StudyBook\temp\seanlgirgis.github.io
git add learning/{slug}.html
git commit -m "Add/update {topic} learning page"
git push
```

Verify live: `https://seanlgirgis.github.io/learning/{slug}.html`

---

## Step 5 — Update Index (if new page)

If this is a brand new topic (not an update):
1. Open `D:\StudyBook\temp\seanlgirgis.github.io\learning\index.html`
2. Add a link card for the new topic
3. Commit and push index.html

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Sections are walls of text | Ask "tighten each section to 2-3 paragraphs max" |
| Code blocks missing | Ask "add a code block to section N showing X" |
| Code blocks too long (>20 lines) | Ask "trim the code block in section N to 15 lines" |
| Wrong topic scope | Check SCOPE FENCE bullets — may need to be more specific |
| Audio player missing | Add manually: `<audio controls><source src="" type="audio/mpeg"></audio>` |
| ChatGPT truncates output | Ask "continue from section N" or split into two generations |

---

## HTML File Naming Convention

| Topic | Filename |
|---|---|
| AWS Kinesis | aws-kinesis.html |
| Apache Airflow | apache-airflow.html |
| Python Logging | python-logging.html |
| Delta Lake | delta-lake.html |
| SQL Patterns | sql-patterns.html |

Rule: lowercase, hyphens not underscores, match the audio slug exactly.
