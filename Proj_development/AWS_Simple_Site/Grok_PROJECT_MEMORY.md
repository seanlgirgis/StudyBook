# Grok Project Memory — AWS_Simple_Site

Stable architecture and durable decisions. Update when AWS resources, publish workflow, or scope change.

---

## Stable decisions

- **Project path:** `D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site`
- **Agent prefix:** `Grok_`
- **Type:** application — clipboard/file → static HTML → S3 website
- **Primary human guide:** `PROJECT_GUIDE.md`
- **Preferred mode:** plain text (`python publish_clipboard.py text`)
- **Git:** Sean manages; not auto-registered to `gitqall.ps1` until he opts in

## AWS resources (public / non-secret)

| Resource | Value |
|----------|--------|
| Bucket | `aws-comm-site` |
| Object | `s3://aws-comm-site/index.html` |
| Region | `us-east-1` |
| Website URL | `http://aws-comm-site.s3-website-us-east-1.amazonaws.com/` |
| Publisher IAM user | `arn:aws:iam::357811130281:user/aws-comm-site-publisher` |

Credentials live in AWS CLI config on the machine — **never** in this repo.

## Publish pipeline

```text
Clipboard (or --from-file) → publish_clipboard.py → index.html → aws s3 cp → website URL
```

- Clipboard read via PowerShell `Get-Clipboard -Raw`
- Text mode wraps content in HTML `<pre>` with escaping
- Upload uses AWS CLI with `content-type text/html; charset=utf-8` and `cache-control no-cache`
- `--no-upload` rebuilds local `index.html` only

## Optional modes (existing; text preferred)

- `markdown` — Markdown formatting path
- `python` — Python code formatting path
- Both need `requirements.txt` packages installed when used

## Safety

- Publisher IAM user should stay limited to this bucket
- Watch Billing → Budgets / Cost Explorer for light personal use
- Decommission user + bucket contents when the experiment ends
- Do not expand to general AWS admin tooling in this folder

## Not this project

| Concern | Project |
|---------|---------|
| Local tray clipboard snippets | UCM |
| One-line publish reminder | local_memory (pointer only) |
| Work onboarding / training | ALOK |
