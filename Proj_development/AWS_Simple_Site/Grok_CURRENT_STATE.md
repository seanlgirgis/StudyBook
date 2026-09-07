# Grok Current State — AWS_Simple_Site

## Repository

- Path: `D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site`
- Live site: `http://aws-comm-site.s3-website-us-east-1.amazonaws.com/`
- Launcher: `C:\scripts\start_grok_aws_simple_site.ps1` (runtime); `start_grok_aws_simple_site.ps1` (repo archive)
- Onboarded: 2026-07-15 (Grok Director registration)

## Working workflow

| Action | Command |
|--------|---------|
| Publish plain text | `python publish_clipboard.py text` |
| Local build only | `python publish_clipboard.py text --no-upload` |
| Check identity | `aws sts get-caller-identity` |
| List bucket | `aws s3 ls s3://aws-comm-site` |

## Main files

| File | Role |
|------|------|
| `publish_clipboard.py` | Publisher script |
| `index.html` | Generated (git-ignored) |
| `PROJECT_GUIDE.md` | Full ops guide |
| `GUIDE.md` / `README.md` | Short help |
| `requirements.txt` | Markdown/python mode deps |

## Recent actions

- 2026-07-20: Added publish modes `json`, `md` (alias of markdown), and `html` to `publish_clipboard.py`; docs updated in PROJECT_GUIDE.md / GUIDE.md
- 2026-07-15: Grok agent files + launcher pair; registered in Grok Director

## Follow-ups (from PROJECT_GUIDE future list)

- [ ] Improve page design for long notes
- [ ] Optional title prompt per publish
- [ ] Local timestamped archive of uploads
- [ ] Multi-page notes + index links
- [ ] Better Markdown / Python publish modes
- [ ] Simple desktop launcher / `.bat` for publish
- [ ] Cost checklist before new AWS services
- [ ] HTTPS via CloudFront if needed later
- [ ] Prefer temporary credentials over long-lived keys (IAM Identity Center study)
- [ ] Decommission guide (IAM user, bucket contents, bucket)
- [ ] Git init / remote / `gitqall.ps1` when Sean ready

## Last updated

- Date: 2026-07-20
- Reason: Added json / md / html publish modes
