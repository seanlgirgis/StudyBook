# AWS Simple Site

Build `index.html` from your Windows clipboard and publish it to the S3 static website bucket.

## One-Time Setup

Install the Python packages used for Markdown and Python syntax highlighting:

```powershell
python -m pip install -r requirements.txt
```

Configure AWS CLI credentials before uploading:

```powershell
aws configure
```

If your AWS CLI asks you to use the newer login flow, follow its prompt:

```powershell
aws login
```

## Publish From Clipboard

Copy text, Markdown, or Python code to your clipboard, then run one of these:

```powershell
python publish_clipboard.py text
python publish_clipboard.py markdown
python publish_clipboard.py python
```

The script writes `index.html`, uploads it to:

```text
s3://aws-comm-site/index.html
```

Then you can open:

```text
http://aws-comm-site.s3-website-us-east-1.amazonaws.com/
```

## Local Build Only

Use this when you want to inspect `index.html` before uploading:

```powershell
python publish_clipboard.py markdown --no-upload
```

## Test From A File

```powershell
python publish_clipboard.py python --from-file .\sample.py --no-upload
```
