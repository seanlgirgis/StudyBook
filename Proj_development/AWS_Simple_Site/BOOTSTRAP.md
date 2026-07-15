# AWS_Simple_Site Bootstrap

## Project Purpose

AWS_Simple_Site publishes simple clipboard (or file) text to a static website hosted on Amazon S3 (`aws-comm-site`).

## Repository Identity

- Path: `D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site`
- Live site: `http://aws-comm-site.s3-website-us-east-1.amazonaws.com/`
- Bucket: `s3://aws-comm-site/index.html`
- Agent file prefix: `Grok_`
- Primary ops guide: [PROJECT_GUIDE.md](PROJECT_GUIDE.md)

## Scope rule — this project only

**This Grok Build session operates only on `D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site`.**

If Sean asks for work that is not this S3 simple-site publisher — UCM tray app, ALOK ingest, learning courses, kb notes, LifeVault pods, docker labs — decline in one short paragraph and name the correct project.

**In scope:** `publish_clipboard.py`, generated `index.html` behavior, requirements, project docs, `Grok_*` agent files, optional local UX improvements for this site.

**Out of scope:** general AWS account redesign, unrelated apps, secret storage in markdown.

## Startup Rule

For every task:

1. Read this file.
2. Read [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for publish commands and AWS resource names.
3. Read [Grok_PROJECT_PROFILE.md](Grok_PROJECT_PROFILE.md) when boundaries or routing are unclear.
4. Read only the files needed for the task (`publish_clipboard.py`, etc.).
5. Read [Grok_PROJECT_MEMORY.md](Grok_PROJECT_MEMORY.md) only when stable architecture context is needed.
6. Read [Grok_CURRENT_STATE.md](Grok_CURRENT_STATE.md) only for status or planning.
7. Do not scan unrelated Workarea projects.

## Source-of-Truth Order

1. `publish_clipboard.py` (behavior)
2. `PROJECT_GUIDE.md` (ops, AWS resources, safety)
3. `GUIDE.md` / `README.md` (short help)
4. Agent state: `Grok_PROJECT_MEMORY.md`, `Grok_CURRENT_STATE.md`

Do not invent missing AWS facts. Mark uncertainty clearly. Never write secret keys into files.

## Default publish workflow

```powershell
cd D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site
python publish_clipboard.py text
```

Local only (no upload):

```powershell
python publish_clipboard.py text --no-upload
```

If upload fails, check:

```powershell
aws sts get-caller-identity
aws s3 ls s3://aws-comm-site
```

Expected publisher identity:

```text
arn:aws:iam::357811130281:user/aws-comm-site-publisher
```

## Work Modes

### 1. Bite-sized (default)

One fix or one publish-related change — e.g. docs tweak, flag fix, local HTML test.

### 2. Feature

Page design, title prompt, local archive, multi-page notes, Markdown/Python mode improvements.

### 3. Maintenance

Agent files, decommission guide, cost checklist, credential workflow notes (no secrets).

## Hard Rules

- Proportional work: small task → small change set.
- No Git operations unless Sean explicitly delegates.
- Never store AWS access keys or secrets in the repo or chat.
- Prefer plain **text** mode for normal publishing unless Sean asks otherwise.
- Report exactly which files were created, modified, moved, or deleted.
- `index.html` is generated and git-ignored; regenerate via the script.

## Director

For "where does this go?" questions, use Grok Director at `D:\Workarea\Grok_DIRECTOR`.
