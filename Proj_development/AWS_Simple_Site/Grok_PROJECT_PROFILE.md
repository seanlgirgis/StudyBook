# Grok Project Profile — AWS_Simple_Site

**For:** Grok Build director and delegated agents discovering this repository  
**Repository:** `D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site`  
**Profile version:** 2026-07-15

---

## One-Line Summary

Clipboard-to-S3 static site publisher — rebuild `index.html` from Windows clipboard (or a file) and upload to the `aws-comm-site` S3 website bucket.

---

## Project Type

| Field | Value |
|-------|-------|
| Name | `AWS_Simple_Site` |
| Type | Application (Python publish script + static HTML on S3) |
| Path | `D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site` |
| Live site | `http://aws-comm-site.s3-website-us-east-1.amazonaws.com/` |
| Agent file prefix | `Grok_` |

---

## Purpose

AWS_Simple_Site turns text copied on the PC into a simple public HTML page on Amazon S3.

**Does this project:**

- Maintain `publish_clipboard.py` (clipboard/file → `index.html` → optional S3 upload)
- Keep usage docs (`PROJECT_GUIDE.md`, `GUIDE.md`, `README.md`) accurate
- Support text (preferred), markdown, and python publish modes
- Document AWS resources for this site only (bucket, publisher IAM user, region)

**Does not:**

- Act as a general AWS account lab or multi-service infrastructure repo
- Store AWS secret keys or long-lived credentials in files or chat
- Replace **UCM** (clipboard snippet manager app)
- Host work-learning notes (**ALOK**), courses (**learning**), or Obsidian notes (**kb**)
- Replace **LifeVault** file pods or **docker** lab stacks

---

## When to Route Work Here

- Publish clipboard/file content to the S3 simple site
- Fix or extend `publish_clipboard.py`, `index.html` generation, or upload flags
- Improve page design, archive, multi-page notes, or CloudFront/HTTPS for this site
- IAM/S3 checks limited to `aws-comm-site` and `aws-comm-site-publisher`

---

## When Not to Use AWS_Simple_Site

| Instead use | When |
|-------------|------|
| **UCM** | Local clipboard snippets tray app (`clipboard_app.py`) |
| **local_memory** | One-line "how do I publish?" runbook pointer only |
| **docker** | Local container labs, not this S3 site |
| **ALOK** | LTIM/BOA work-learning material |
| **learning** | Course packages / StudyBubbles |

---

## Mandatory Read Order

1. [BOOTSTRAP.md](BOOTSTRAP.md)
2. [PROJECT_GUIDE.md](PROJECT_GUIDE.md) — primary operating guide
3. [Grok_PROJECT_PROFILE.md](Grok_PROJECT_PROFILE.md) when boundaries are unclear
4. Task files only (`publish_clipboard.py`, `requirements.txt`, etc.)
5. [Grok_PROJECT_MEMORY.md](Grok_PROJECT_MEMORY.md) for stable AWS/architecture facts
6. [Grok_CURRENT_STATE.md](Grok_CURRENT_STATE.md) for status / next steps only

Do **not** re-read every doc by default.

---

## Folder Map (Abbreviated)

```text
publish_clipboard.py   Main publisher script
index.html             Generated page (git-ignored)
requirements.txt       Optional Markdown/code formatting deps
PROJECT_GUIDE.md       Full project guide (source of truth for ops)
GUIDE.md               Short publish guide
README.md              Quick start
Grok_*                 Agent files
start_grok_aws_simple_site.ps1
```

---

## Hard Rules

- Preferred publish command: `python publish_clipboard.py text`
- Never paste AWS secret keys into chat or documentation.
- Publishing IAM user is scoped to this bucket — not a general AWS admin.
- `index.html` is generated; do not treat it as hand-edited source of truth.
- Sean manages Git; no Git ops unless delegated.
- Monitor AWS billing for even small S3 use; decommission IAM user when done.

---

## Related Grok Files

| File | Role |
|------|------|
| `Grok_PROJECT_PROFILE.md` | This file |
| `Grok_PROJECT_MEMORY.md` | Stable architecture and AWS resource facts |
| `Grok_CURRENT_STATE.md` | Status and follow-ups |
| `PROJECT_GUIDE.md` | Full human/ops guide |
| `start_grok_aws_simple_site.ps1` | Launcher (repo archive; runtime at `C:\scripts\`) |

---

## Delegation Prompt Template

```text
Project: AWS_Simple_Site (clipboard → S3 static site)
Root: D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site

Read first:
- BOOTSTRAP.md
- PROJECT_GUIDE.md
- Grok_PROJECT_PROFILE.md
- [task paths only]

Work mode: [bite_sized | feature | maintenance]

Task:
[one narrowly scoped publish/script/docs task]

Must not:
- Store or request AWS secret keys in repo/chat
- Expand into unrelated AWS services without Sean approval
- Run Git operations unless delegated

At completion:
- List every file created, modified, moved, or deleted
- Note whether S3 upload was performed or --no-upload only
- Note unresolved ambiguity
```
