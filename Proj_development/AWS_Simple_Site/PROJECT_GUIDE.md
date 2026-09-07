# AWS Simple Site Project Guide

## Local Folder

The local project folder is:

```text
D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site
```

Open PowerShell and move into the folder with:

```powershell
cd D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site
```

## Website Address

The live S3 static website address is:

```text
http://aws-comm-site.s3-website-us-east-1.amazonaws.com/
```

If the browser does not show the newest upload, refresh with:

```text
Ctrl+F5
```

## What This Project Does

This project turns text copied on the Windows clipboard into a new `index.html` file, then uploads that file to an Amazon S3 static website bucket.

The current main workflow is:

```text
Copy text on PC -> run Python script -> rebuild index.html -> upload to S3 -> view from website link
```

For now, the preferred mode is plain text mode.

## Main Files

```text
publish_clipboard.py
```

The Python script that reads clipboard content, builds `index.html`, and uploads it to S3.

```text
index.html
```

The generated website page. This file is rebuilt each time the publish script runs.

```text
requirements.txt
```

Python packages used for optional Markdown and Python code formatting.

```text
README.md
GUIDE.md
PROJECT_GUIDE.md
```

Project notes and usage instructions.

## AWS Resources

S3 bucket:

```text
aws-comm-site
```

S3 object uploaded by the script:

```text
s3://aws-comm-site/index.html
```

Region:

```text
us-east-1
```

Publishing IAM user:

```text
arn:aws:iam::357811130281:user/aws-comm-site-publisher
```

The publishing user should stay limited to this bucket. It should not be used as a general AWS admin user.

## One-Time Setup

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

Configure AWS CLI credentials:

```powershell
aws configure
```

Use:

```text
Default region name: us-east-1
Default output format: json
```

Do not paste AWS secret keys into chat or documentation.

## Check AWS CLI

Confirm the CLI is logged in:

```powershell
aws sts get-caller-identity
```

Confirm access to the S3 bucket:

```powershell
aws s3 ls s3://aws-comm-site
```

Expected result: the command should list `index.html`.

## Publish Plain Text

1. Copy the text you want to publish.
2. Open PowerShell.
3. Run:

```powershell
cd D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site
python publish_clipboard.py text
```

The script should print that it built `index.html`, uploaded to S3, and show the site URL.

## Build Locally Without Uploading

Use this when testing formatting before sending anything to AWS:

```powershell
python publish_clipboard.py text --no-upload
```

This rebuilds the local `index.html` only.

## Optional Modes

Plain **text** is still the preferred everyday mode. Other render modes:

| Mode | Command | What it does |
|------|---------|----------------|
| text | `python publish_clipboard.py text` | Escaped plain text in a `<pre>` block |
| markdown / md | `python publish_clipboard.py md` | Renders Markdown (needs `markdown` package) |
| python | `python publish_clipboard.py python` | Syntax-highlighted Python |
| json | `python publish_clipboard.py json` | Pretty-prints + highlights JSON |
| html | `python publish_clipboard.py html` | Embeds clipboard HTML as live markup |

Markdown (short form):

```powershell
python publish_clipboard.py md
```

Also accepted:

```powershell
python publish_clipboard.py markdown
```

JSON mode:

```powershell
python publish_clipboard.py json
```

HTML mode (clipboard content is inserted as HTML, not escaped):

```powershell
python publish_clipboard.py html
```

Python code mode:

```powershell
python publish_clipboard.py python
```

Read from a file instead of the clipboard:

```powershell
python publish_clipboard.py text --from-file .\my-note.txt
```

## How It Is Made

The script uses PowerShell to read the Windows clipboard:

```text
Get-Clipboard -Raw
```

Then it escapes the copied text so it is safe to place inside HTML.

For text mode, it wraps the content in a `<pre>` block so line breaks and spacing are preserved.

Then it writes a complete HTML page to:

```text
index.html
```

Finally, it uses AWS CLI to upload the generated page:

```powershell
aws s3 cp index.html s3://aws-comm-site/index.html --content-type "text/html; charset=utf-8" --cache-control "no-cache"
```

The S3 bucket is configured for static website hosting, so the uploaded `index.html` becomes visible at the website address.

## Current Operating Rule

Use this command for normal publishing:

```powershell
python publish_clipboard.py text
```

This is the simplest stable workflow.

## Future Development

Possible next steps:

1. Improve the page design for reading long notes.
2. Add a title prompt so each published page can have a custom heading.
3. Add a local archive so every upload is saved with a timestamp.
4. Add multiple pages instead of replacing only `index.html`.
5. Add a small index page that links to all uploaded notes.
6. Improve Markdown publishing for headings, lists, code blocks, and tables.
7. Improve Python code publishing with copy-friendly formatting.
8. Add a simple desktop launcher or `.bat` file so the command is easier to run.
9. Add a cost checklist before using new AWS services.
10. Add HTTPS later using CloudFront if needed.
11. Study IAM Identity Center and replace long-lived access keys with temporary credentials.
12. Add a cleanup/decommission guide for removing the IAM user, bucket contents, and bucket when done.

## Cost And Safety Notes

This project currently uses a very small S3 static website bucket. Costs should be tiny for light personal testing, but AWS billing should still be monitored.

Recommended AWS safety checks:

```text
Billing and Cost Management -> Budgets
Billing and Cost Management -> Cost Explorer
S3 -> aws-comm-site -> Objects
IAM -> aws-comm-site-publisher -> Permissions
IAM -> aws-comm-site-publisher -> Security credentials
```

The publishing IAM user should be deleted when no longer needed.

## Quick Reference

Project folder:

```text
D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site
```

Publish:

```powershell
python publish_clipboard.py text
```

Website:

```text
http://aws-comm-site.s3-website-us-east-1.amazonaws.com/
```
