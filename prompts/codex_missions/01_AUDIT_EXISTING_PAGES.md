# MISSION 01 — Audit Existing Learning Pages (One at a Time)
# Working directory: D:\StudyBook\
# Touches: temp\seanlgirgis.github.io\learning\ (READ ONLY — no changes)
# Output: prompts\codex_missions\AUDIT_REPORT.md (built file by file)

---

## WORKING DIRECTORY

```powershell
Get-Location   # must show D:\StudyBook
```

---

## RULE: ONE FILE PER RUN — STOP AND WAIT AFTER EACH

Do NOT audit all 8 files in one shot.
Audit ONE file. Write its section to AUDIT_REPORT.md. STOP.
Wait for Sean to say "confirmed, next" before moving to the next file.

This protects tokens and catches problems early.

---

## FILE QUEUE (audit in this exact order, one at a time)

```
1. temp\seanlgirgis.github.io\learning\aws-ec2.html        ← START HERE
2. temp\seanlgirgis.github.io\learning\aws-athena.html
3. temp\seanlgirgis.github.io\learning\aws-glue.html
4. temp\seanlgirgis.github.io\learning\aws-redshift.html
5. temp\seanlgirgis.github.io\learning\aws-lambda.html
6. temp\seanlgirgis.github.io\learning\aws-s3.html
7. temp\seanlgirgis.github.io\learning\apache-kafka.html
8. temp\seanlgirgis.github.io\learning\aws-ecs.html
```

---

## WHAT TO CHECK (same checklist for every file)

**A. Metadata**
- `<title>` text
- `.subtitle` paragraph — full text including date and read time
- All `.tag` span values

**B. Audio Box**
- Does `<div class="audio-box">` exist?
- Is there an `<audio>` element with a real `src` URL? → copy exact URL
- Is audio type `audio/mp4` (old NotebookLM) or `audio/mpeg` (new pipeline)?
- Or is there only placeholder text with no `<audio>` element? → note the text
- Is there a `<video>` element with a real `src` URL? → copy exact URL

**C. Structure**
- Does `<div class="toc">` exist? How many `<li>` entries?
- List all `<h2 id="...">` section IDs in order
- Does a `.qa` section exist?
- Does a `.cheat` section exist?
- Count `.hi` and `.warn` callout divs

**D. CSS**
- Does `--primary: #004a99` appear in the `<style>` block? (standard CSS check)
- What is the `grid-template-columns` value inside `.cheat-row`?
  Should be `170px 1fr` — flag anything different

**E. Issues**
- Anything broken, missing, or inconsistent

---

## OUTPUT FORMAT — append to AUDIT_REPORT.md after each file

If AUDIT_REPORT.md does not exist yet, create it with this header first:
```markdown
# Audit Report — Learning Hub Existing Pages
Working directory: D:\StudyBook\
Pages location: temp\seanlgirgis.github.io\learning\
Report location: prompts\codex_missions\AUDIT_REPORT.md
```

Then append this block for each file audited:

```markdown
---

## [N]. {filename}

**Title:** [value]
**Subtitle:** [full text]
**Tags:** [list]

**Audio:** LIVE | PLACEHOLDER | NONE
  src: [exact URL — do not truncate]
  type: [audio/mp4 | audio/mpeg | N/A]
**Video:** LIVE | NONE
  src: [exact URL — do not truncate]

**TOC:** YES / NO — [N] entries
**Section IDs:** [#s1, #s2, ...]
**QA section:** YES / NO
**Cheat sheet:** YES / NO
**hi callouts:** [N]
**warn callouts:** [N]

**CSS standard:** MATCH / DEVIATION: [describe]
**cheat-row columns:** [170px 1fr | OTHER: describe]

**Issues:** [list or "None"]

**Status:** READY FOR AUDIO REPLACEMENT | NEEDS AUDIO ADDED | REVIEW NEEDED
```

---

## AFTER EACH FILE — STOP AND REPORT

After writing one file's section to AUDIT_REPORT.md, output this exact message:

```
AUDIT [N/8] COMPLETE — {filename}
Audio: [LIVE/PLACEHOLDER/NONE]  Video: [LIVE/NONE]
Issues: [count or "none"]
AUDIT_REPORT.md updated at prompts\codex_missions\AUDIT_REPORT.md

Waiting for confirmation to audit next file: {next filename}
Say "confirmed, next" to continue.
```

Then STOP. Do not proceed to the next file until Sean responds.

---

## AFTER ALL 8 FILES — APPEND SUMMARY TABLE

Only after Sean confirms all 8 are done, append this to AUDIT_REPORT.md:

```markdown
---

## SUMMARY TABLE

| # | File | Audio | Type | Video | QA | Cheat | Issues |
|---|------|-------|------|-------|----|-------|--------|
| 1 | aws-ec2.html | | | | | | |
| 2 | aws-athena.html | | | | | | |
| 3 | aws-glue.html | | | | | | |
| 4 | aws-redshift.html | | | | | | |
| 5 | aws-lambda.html | | | | | | |
| 6 | aws-s3.html | | | | | | |
| 7 | apache-kafka.html | | | | | | |
| 8 | aws-ecs.html | | | | | | |

## PHASE 1 PROCESSING ORDER
[confirm or adjust based on findings]
1. aws-ec2.html — TEST CASE
2. ...
```

Then report: "MISSION 01 COMPLETE — all 8 files audited — AUDIT_REPORT.md finalized"

---

## START NOW

Audit file 1 of 8: `temp\seanlgirgis.github.io\learning\aws-ec2.html`
Write its section to AUDIT_REPORT.md. Stop. Wait for confirmation.
