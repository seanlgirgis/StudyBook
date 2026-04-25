# MISSION 01 — Audit Existing Learning Pages
# Working directory: D:\StudyBook\
# Touches: temp\seanlgirgis.github.io\learning\ (read only)
# Output: prompts\codex_missions\AUDIT_REPORT.md

---

## WORKING DIRECTORY REMINDER

All paths below are relative to D:\StudyBook\.
Confirm your working directory before running any command:
```powershell
Get-Location   # must show D:\StudyBook
```

---

## YOUR TASK

Read all 8 existing HTML files in `temp\seanlgirgis.github.io\learning\`
and produce a structured audit report.

Save the report to:
`prompts\codex_missions\AUDIT_REPORT.md`

This is a READ-ONLY mission. Do not modify any HTML file.

---

## FILES TO AUDIT (in this exact order)

```
temp\seanlgirgis.github.io\learning\aws-ec2.html
temp\seanlgirgis.github.io\learning\aws-athena.html
temp\seanlgirgis.github.io\learning\aws-glue.html
temp\seanlgirgis.github.io\learning\aws-redshift.html
temp\seanlgirgis.github.io\learning\aws-lambda.html
temp\seanlgirgis.github.io\learning\aws-s3.html
temp\seanlgirgis.github.io\learning\apache-kafka.html
temp\seanlgirgis.github.io\learning\aws-ecs.html
```

---

## WHAT TO CHECK FOR EACH FILE

### A. Metadata
- Page `<title>` text
- `.subtitle` paragraph text
- All `.tag` span values
- Read time from subtitle

### B. Audio Box
- Does `<div class="audio-box">` exist?
- Is there an `<audio>` element with a real `src` URL? Copy exact URL.
- Is the audio type `audio/mp4` (old NotebookLM) or `audio/mpeg` (new pipeline)?
- Is there placeholder text instead of a real `<audio>` element? Note the text.
- Is there a `<video>` element with a real `src` URL? Copy exact URL.

### C. Structure
- Does `<div class="toc">` exist? How many `<li>` entries?
- List all `<h2 id="...">` section IDs in order
- Does a `.qa` section exist?
- Does a `.cheat` section exist?
- Count `.hi` and `.warn` callout divs

### D. CSS Check
- Does the file contain `--primary: #004a99` in its `<style>` block?
- What is the `grid-template-columns` value in `.cheat-row`?
  (should be `170px 1fr` — flag anything different)

### E. Issues
- Anything broken, missing, or inconsistent

---

## OUTPUT FORMAT

Save exactly this structure to `prompts\codex_missions\AUDIT_REPORT.md`:

```markdown
# Audit Report — Learning Hub Existing Pages
Date: [today]
Audited from: temp\seanlgirgis.github.io\learning\
Report saved to: prompts\codex_missions\AUDIT_REPORT.md

---

## aws-ec2.html

**Title:** [value]
**Subtitle:** [value]
**Tags:** [list]
**Read time:** [value]

**Audio status:** LIVE | PLACEHOLDER | NONE
**Audio src:** [exact URL or N/A]
**Audio type:** [audio/mp4 | audio/mpeg | N/A]
**Video status:** LIVE | NONE
**Video src:** [exact URL or N/A]

**TOC:** YES/NO — [N] entries
**Section IDs:** [#s1, #s2, ...]
**QA section:** YES/NO
**Cheat sheet:** YES/NO
**hi callouts:** [N]
**warn callouts:** [N]
**CSS standard:** MATCH / DEVIATION: [describe]
**cheat-row columns:** [170px 1fr / OTHER: describe]

**Issues:** [list or "None"]

---

[repeat for all 8 files]

---

## SUMMARY TABLE

| File | Audio | Type | Video | QA | Cheat | CSS | Issues |
|------|-------|------|-------|----|-------|-----|--------|
| aws-ec2.html | | | | | | | |
| aws-athena.html | | | | | | | |
| aws-glue.html | | | | | | | |
| aws-redshift.html | | | | | | | |
| aws-lambda.html | | | | | | | |
| aws-s3.html | | | | | | | |
| apache-kafka.html | | | | | | | |
| aws-ecs.html | | | | | | | |

---

## PHASE 1 PROCESSING ORDER

Based on audit (confirm or adjust from default):
1. aws-ec2.html — TEST CASE
2. [next]
...
```

---

## VERIFICATION CHECKLIST

- [ ] Working directory confirmed as D:\StudyBook\ before starting
- [ ] All 8 files read (not skipped)
- [ ] Every audio src URL copied exactly (not paraphrased or truncated)
- [ ] Every video src URL copied exactly
- [ ] CSS check done by inspecting the actual `<style>` block in each file
- [ ] Summary table complete — all 8 rows filled
- [ ] Report saved to `prompts\codex_missions\AUDIT_REPORT.md`

Report: "MISSION 01 COMPLETE — AUDIT_REPORT.md saved — [N] issues found across [N] files"
Or:     "MISSION 01 BLOCKED — [specific problem]"
