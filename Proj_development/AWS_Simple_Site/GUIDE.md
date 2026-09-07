# AWS Simple Site Guide

This project publishes simple clipboard text to a static website hosted on Amazon S3.

## Website Address

Open the site here:

```text
http://aws-comm-site.s3-website-us-east-1.amazonaws.com/
```

If the page does not show the newest version, refresh with:

```text
Ctrl+F5
```

## Publish Clipboard Text

1. Copy the text you want to publish.
2. Open PowerShell.
3. Go to the project folder:

```powershell
cd D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site
```

4. Run:

```powershell
python publish_clipboard.py text
```

The script will:

- Read the current Windows clipboard.
- Rebuild `index.html`.
- Upload `index.html` to:

```text
s3://aws-comm-site/index.html
```

- Print the website address.

## Local Test Without Uploading

Use this when you want to rebuild `index.html` but not send it to AWS:

```powershell
python publish_clipboard.py text --no-upload
```

## AWS CLI Check

If uploading fails, first check that AWS CLI is still configured:

```powershell
aws sts get-caller-identity
```

Then check bucket access:

```powershell
aws s3 ls s3://aws-comm-site
```

The expected publishing user is:

```text
arn:aws:iam::357811130281:user/aws-comm-site-publisher
```

## Modes

Preferred everyday mode:

```powershell
python publish_clipboard.py text
```

Other modes:

```powershell
python publish_clipboard.py md
python publish_clipboard.py json
python publish_clipboard.py html
python publish_clipboard.py python
```

- **md** / **markdown** — render Markdown
- **json** — pretty-print and highlight JSON
- **html** — embed clipboard HTML as live page content
- **python** — syntax-highlight Python

Local test example:

```powershell
python publish_clipboard.py json --from-file .\sample.json --no-upload
```
