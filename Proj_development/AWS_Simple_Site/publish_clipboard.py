from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_BUCKET = "aws-comm-site"
DEFAULT_REGION = "us-east-1"
DEFAULT_OUTPUT = "index.html"


def read_clipboard() -> str:
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "Could not read clipboard.")
    return completed.stdout


def read_source(args: argparse.Namespace) -> str:
    if args.from_file:
        return Path(args.from_file).read_text(encoding="utf-8")
    return read_clipboard()


def render_markdown(content: str) -> str:
    try:
        import markdown  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "Markdown mode needs the 'markdown' package. Run: python -m pip install -r requirements.txt"
        ) from exc

    return markdown.markdown(
        content,
        extensions=["fenced_code", "tables", "nl2br", "sane_lists"],
        output_format="html5",
    )


def render_python(content: str) -> str:
    try:
        from pygments import highlight  # type: ignore
        from pygments.formatters import HtmlFormatter  # type: ignore
        from pygments.lexers import PythonLexer  # type: ignore
    except ImportError:
        escaped = html.escape(content)
        return f'<pre class="code-block"><code>{escaped}</code></pre>'

    formatter = HtmlFormatter(nowrap=False, cssclass="highlight")
    return highlight(content, PythonLexer(), formatter)


def render_text(content: str) -> str:
    return f'<pre class="plain-text">{html.escape(content)}</pre>'


def render_body(content: str, mode: str) -> str:
    if mode == "text":
        return render_text(content)
    if mode == "markdown":
        return f'<article class="markdown-body">{render_markdown(content)}</article>'
    if mode == "python":
        return render_python(content)
    raise ValueError(f"Unsupported mode: {mode}")


def build_html(content: str, mode: str, title: str) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = render_body(content, mode)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f4;
      --ink: #1f2933;
      --muted: #607080;
      --panel: #ffffff;
      --line: #d9dfd6;
      --accent: #256f5c;
      --code-bg: #101820;
      --code-ink: #eef6f4;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 16px/1.55 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{
      width: min(960px, calc(100% - 32px));
      margin: 32px auto;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: clamp(20px, 4vw, 42px);
      box-shadow: 0 14px 40px rgba(31, 41, 51, 0.08);
    }}
    header {{
      border-bottom: 1px solid var(--line);
      margin-bottom: 24px;
      padding-bottom: 14px;
    }}
    h1 {{
      margin: 0 0 4px;
      font-size: clamp(1.6rem, 4vw, 2.5rem);
      line-height: 1.15;
    }}
    .meta {{
      color: var(--muted);
      font-size: 0.92rem;
    }}
    .plain-text {{
      margin: 0;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      font: 1rem/1.55 Consolas, "Courier New", monospace;
    }}
    pre, .highlight {{
      overflow-x: auto;
      background: var(--code-bg);
      color: var(--code-ink);
      border-radius: 8px;
      padding: 18px;
    }}
    code {{
      font-family: Consolas, "Courier New", monospace;
      font-size: 0.95rem;
    }}
    .markdown-body h1,
    .markdown-body h2,
    .markdown-body h3 {{
      line-height: 1.2;
      margin-top: 1.5em;
    }}
    .markdown-body a {{ color: var(--accent); }}
    .markdown-body table {{
      border-collapse: collapse;
      width: 100%;
    }}
    .markdown-body th,
    .markdown-body td {{
      border: 1px solid var(--line);
      padding: 8px 10px;
      text-align: left;
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{html.escape(title)}</h1>
      <div class="meta">Mode: {html.escape(mode)} | Generated: {generated_at}</div>
    </header>
    {body}
  </main>
</body>
</html>
"""


def write_index(html_text: str, output: str) -> Path:
    output_path = Path(output).resolve()
    output_path.write_text(html_text, encoding="utf-8", newline="\n")
    return output_path


def upload_to_s3(output_path: Path, bucket: str) -> None:
    aws = shutil.which("aws")
    if not aws:
        raise RuntimeError("AWS CLI was not found on PATH.")

    destination = f"s3://{bucket}/index.html"
    completed = subprocess.run(
        [
            aws,
            "s3",
            "cp",
            str(output_path),
            destination,
            "--content-type",
            "text/html; charset=utf-8",
            "--cache-control",
            "no-cache",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "Upload failed.")


def website_url(bucket: str, region: str) -> str:
    if region == "us-east-1":
        return f"http://{bucket}.s3-website-us-east-1.amazonaws.com/"
    return f"http://{bucket}.s3-website-{region}.amazonaws.com/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build index.html from clipboard text and optionally upload it to an S3 static site."
    )
    parser.add_argument("mode", choices=["text", "markdown", "python"], help="How to render the clipboard content.")
    parser.add_argument("--title", default="Study Note", help="Page title shown at the top of the page.")
    parser.add_argument("--bucket", default=DEFAULT_BUCKET, help="S3 bucket name.")
    parser.add_argument("--region", default=DEFAULT_REGION, help="AWS region used for the website URL.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output HTML file.")
    parser.add_argument("--from-file", help="Read content from a file instead of the clipboard.")
    parser.add_argument("--no-upload", action="store_true", help="Build index.html without uploading to S3.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        content = read_source(args)
        if not content.strip():
            raise RuntimeError("The source content is empty.")

        html_text = build_html(content, args.mode, args.title)
        output_path = write_index(html_text, args.output)
        print(f"Built {output_path}")

        if args.no_upload:
            print("Skipped upload because --no-upload was used.")
        else:
            upload_to_s3(output_path, args.bucket)
            print(f"Uploaded to s3://{args.bucket}/index.html")

        print(f"Site: {website_url(args.bucket, args.region)}")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
