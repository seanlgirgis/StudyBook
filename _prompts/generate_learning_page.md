# Reusable Prompt — Generate a Learning Hub Reference Page
> Save path: `D:\StudyBook\temp\seanlgirgis.github.io\learning\_prompts\generate_learning_page.md`
> Use this prompt with any AI agent to generate a new reference page in the same style as `learning/aws-s3.html`

---

## How to use this prompt

1. Fill in the **[VARIABLES]** section below with your topic details
2. Paste the entire prompt (from "YOUR TASK" onwards) into any AI agent
3. The agent returns a complete `.html` file
4. Save it to `D:\StudyBook\temp\seanlgirgis.github.io\learning\[filename].html`
5. Add a card to `components/learning.html`
6. Add the route to `assets/js/router.js`
7. Commit and push

---

## [VARIABLES] — Fill these in before sending

```
TOPIC_TITLE:        AWS Glue                          ← e.g. "AWS Glue", "Amazon Redshift", "Apache Kafka"
TOPIC_SUBTITLE:     ETL, Data Catalog & PySpark       ← short descriptor shown under title
FILENAME:           aws-glue.html                     ← output filename
TAGS:               AWS, Glue, ETL, PySpark, Catalog  ← comma-separated tags shown on page
READ_TIME:          25–35 min                         ← estimated read time
DATE:               2026-04-13                        ← today's date
AUDIO_URL:          https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/FILENAME.m4a
VIDEO_URL:          https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/FILENAME.mp4
                    ← If no media yet, set both to: PLACEHOLDER
EXPERIENCE_CONTEXT: At a large financial institution, used Glue ETL jobs to transform
                    raw telemetry data from S3 raw/ zone into typed Parquet files in
                    the processed/ zone. Crawlers built the Data Catalog consumed by
                    Redshift and Athena. Jobs ran on a schedule and were triggered by
                    S3 event notifications.
                    ← 3–5 sentences of YOUR real hands-on experience with this technology.
                    ← No company names. Generic "large financial institution" or "enterprise pipeline".
SECTIONS:           (list the key topics to cover — see example below)
```

---

## PROMPT — Paste everything below this line into the AI agent

---

YOUR TASK: Generate a complete standalone HTML reference page for **[TOPIC_TITLE]** following the exact structure, CSS, and conventions described below. Output only the raw HTML — no explanation, no markdown code fences, just the file content.

---

### FILE DETAILS

- Output filename: `[FILENAME]`
- Page title tag: `[TOPIC_TITLE] — Master Engineering Reference | Sean Girgis`
- Canonical URL: `https://seanlgirgis.github.io/learning/[FILENAME]`
- Back link goes to: `https://seanlgirgis.github.io/#learning`

---

### CONTENT RULES — READ CAREFULLY

1. **No company names ever.** Never mention specific companies (employers, clients, vendors by proper name in a personal context). Use "a large financial institution", "an enterprise pipeline", "a high-scale production environment" instead.
2. **No the word "interview".** Replace with: "key engineering questions", "common questions", "engineering Q&A", "technical questions worth knowing".
3. **No tool/platform brand names for the audio/video generation tool.** Just say "AI-generated audio overview" or "AI podcast overview".
4. **No "interview prep" framing.** Frame everything as a reference for practitioners: "worth knowing", "engineers are often asked", "important to understand deeply".
5. **Real depth.** Each section should have substance — not bullet lists of marketing copy. Include architecture diagrams in ASCII/pre blocks, code examples, SQL where relevant, gotchas, and anti-patterns.
6. **Your experience woven in naturally.** Use the EXPERIENCE_CONTEXT provided to add concrete "in production this looks like..." paragraphs. Keep it generic — no names, just patterns.

---

### HTML STRUCTURE — Follow exactly

The file must be a **single self-contained HTML file** with all CSS inlined in a `<style>` block. No external CSS files except optionally Google Fonts.

#### CSS variables (copy exactly — these match the site palette):
```css
:root {
    --primary: #004a99;
    --accent:  #e67e22;
    --text:    #222;
    --muted:   #666;
    --bg:      #f4f7f6;
    --line:    #dde3ea;
    --code-bg: #1e2a38;
    --code-fg: #e8edf2;
    --hi-bg:   #e8f4fd;
    --warn-bg: #fff8e6;
}
```

#### Page wrapper:
```css
.doc { max-width: 820px; margin: 0 auto; background: #fff; padding: 48px 52px 80px; min-height: 100vh; }
@media (max-width: 680px) { .doc { padding: 28px 20px 60px; } }
```

#### Required page elements in order:
1. **`.topnav`** — breadcrumb: `← Learning Hub / [TOPIC_TITLE] — Master Engineering Reference`
2. **`<h1>`** — topic title
3. **`.subtitle`** — `Engineering reference · Senior Data Engineer · Last updated [DATE] · [READ_TIME] read`
4. **`.tag-row`** with `.tag` spans — one per tag from TAGS variable
5. **`.audio-box`** — media section (see media rules below)
6. **`.toc`** — two-column ordered list of section anchor links
7. **Content sections** — `<h2 id="sN">` headings, content, then `<a class="back-top" href="#top">↑ Back to top</a>` after each
8. **Cheat sheet** — dark background `.cheat` div with `.cheat-row` / `.ct` term / `.cd` definition rows

#### Media box rules:
- If AUDIO_URL is not PLACEHOLDER:
```html
<audio controls preload="metadata" style="width:100%;margin-top:6px;">
    <source src="[AUDIO_URL]" type="audio/mp4">
    Your browser does not support the audio element.
</audio>
```
- If VIDEO_URL is not PLACEHOLDER:
```html
<video controls preload="metadata" style="width:100%;max-width:100%;border-radius:4px;margin-top:8px;">
    <source src="[VIDEO_URL]" type="video/mp4">
    Your browser does not support the video tag.
</video>
```
- If either is PLACEHOLDER, show: `<div class="video-hint">🎧 Audio / 🎬 Video: coming soon</div>`
- Label audio as: `🎧 AI-Generated Audio Overview`
- Label video as: `🎬 AI-Generated Video Overview`

#### Back-to-top link (after every section):
```html
<a class="back-top" href="#top">↑ Back to top</a>
```

---

### REQUIRED CSS CLASSES — Include all of these in the `<style>` block

```css
.topnav { font-size:0.88em; margin-bottom:32px; color:var(--muted); }
.topnav a { color:var(--primary); text-decoration:none; }
h1 { color:var(--primary); font-size:2em; margin:0 0 10px; line-height:1.25; }
.subtitle { color:var(--muted); font-size:0.9em; margin:0 0 24px; }
.tag-row { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:32px; }
.tag { background:var(--hi-bg); color:var(--primary); padding:3px 10px; border-radius:12px; font-size:0.82em; font-weight:600; }
.audio-box { border:1px solid var(--line); border-left:5px solid var(--accent); border-radius:6px; padding:18px 22px; margin-bottom:36px; background:#fffdf9; }
.audio-box .audio-label { font-weight:700; color:var(--accent); font-size:0.92em; margin-bottom:10px; }
.video-hint { font-size:0.82em; color:#aaa; margin-top:8px; }
.toc { background:#f7f9fc; border:1px solid var(--line); border-radius:6px; padding:22px 28px; margin-bottom:44px; }
.toc h2 { margin:0 0 14px; font-size:0.82em; text-transform:uppercase; letter-spacing:0.08em; color:var(--muted); font-weight:700; }
.toc ol { margin:0; padding-left:20px; columns:2; column-gap:32px; }
.toc li { margin-bottom:6px; break-inside:avoid; }
.toc a { color:var(--primary); text-decoration:none; font-size:0.93em; }
.doc h2 { color:var(--primary); font-size:1.25em; margin:52px 0 14px; padding-bottom:8px; border-bottom:2px solid var(--line); }
.doc h3 { color:#333; font-size:1.02em; margin:28px 0 10px; }
.back-top { display:block; text-align:right; font-size:0.82em; color:var(--muted); text-decoration:none; margin-top:28px; padding-top:10px; border-top:1px solid var(--line); }
code { background:#eef2f7; color:var(--primary); padding:2px 6px; border-radius:3px; font-size:0.88em; font-family:'Consolas','Courier New',monospace; }
pre { background:var(--code-bg); color:var(--code-fg); padding:18px 22px; border-radius:6px; overflow-x:auto; font-size:0.87em; line-height:1.6; margin:14px 0; font-family:'Consolas','Courier New',monospace; }
pre code { background:none; color:inherit; padding:0; font-size:inherit; }
table { width:100%; border-collapse:collapse; margin:16px 0; font-size:0.91em; }
th { background:var(--primary); color:#fff; padding:9px 14px; text-align:left; font-weight:600; }
td { padding:8px 14px; border-bottom:1px solid #eee; }
tr:nth-child(even) td { background:#f8fafc; }
.hi { background:var(--hi-bg); border-left:4px solid var(--primary); padding:13px 17px; border-radius:0 5px 5px 0; margin:16px 0; font-size:0.95em; }
.warn { background:var(--warn-bg); border-left:4px solid var(--accent); padding:13px 17px; border-radius:0 5px 5px 0; margin:16px 0; font-size:0.95em; }
.qa { margin-bottom:22px; }
.qa-q { font-weight:700; color:var(--primary); margin-bottom:6px; font-size:0.97em; }
.qa-a { border-left:3px solid var(--accent); padding:10px 16px; background:#fffaf5; border-radius:0 5px 5px 0; font-style:italic; color:#444; line-height:1.75; }
.cheat { background:var(--code-bg); color:var(--code-fg); border-radius:6px; padding:22px 26px; }
.cheat-row { display:grid; grid-template-columns:150px 1fr; gap:10px; padding:7px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.9em; }
.cheat-row:last-child { border-bottom:none; }
.ct { color:#f5a623; font-family:monospace; font-weight:bold; }
.cd { color:#c8d8e8; }
```

---

### CONTENT TO GENERATE — For [TOPIC_TITLE]

Cover these sections (adapt section numbering and add/remove as needed for the topic):

**[SECTIONS]**

Example sections for AWS Glue:
1. What Glue Actually Is (positioning vs Spark, vs Lambda, vs manual ETL)
2. Core Components (Data Catalog, Crawlers, ETL Jobs, Triggers, Workflows)
3. Glue Data Catalog Deep-Dive (databases, tables, partitions, schema versioning)
4. Crawlers (how they work, classifiers, schedule vs trigger, gotchas)
5. ETL Jobs — DynamicFrames vs DataFrames
6. Writing PySpark in Glue (common transforms, resolveChoice, applyMapping)
7. Glue + S3 (reading partitioned data, pushdown predicates, writing Parquet)
8. Glue + Redshift (JDBC connector, temp S3 staging bucket pattern)
9. Glue Workflows and Triggers (orchestration, conditional triggers)
10. Job Bookmarks (incremental processing — what they are, when they break)
11. Performance Tuning (DPU sizing, partitioning reads, enable.s3.parquet.pushdown)
12. Security (IAM roles, VPC, encryption, Lake Formation)
13. Common Gotchas and Anti-Patterns
14. 10 Key Engineering Questions and Answers
15. Production Story Angles (use EXPERIENCE_CONTEXT — no company names)
16. Quick Reference Cheat Sheet

For each section:
- Minimum 3–5 substantial paragraphs or equivalent bullet depth
- At least one `<pre>` code block per technical section (Python, SQL, JSON, or ASCII diagram)
- Use `.hi` boxes for "this is the key insight" moments
- Use `.warn` boxes for gotchas and anti-patterns
- Q&A section must have 10 questions using `.qa` / `.qa-q` / `.qa-a` structure
- Cheat sheet must have 10–15 terms

---

### WHAT NOT TO DO

- Do not use `<div class="container">` — use `.doc` wrapper only
- Do not add external JavaScript
- Do not add navigation sidebars
- Do not mention any AI audio/video generation tool by name
- Do not mention specific employer names or client names
- Do not use the word "interview" anywhere in the document
- Do not add cookie banners, analytics scripts, or tracking

---

### OUTPUT FORMAT

Return only the complete HTML file, starting with `<!DOCTYPE html>` and ending with `</html>`. Nothing else.

---

## Media file naming convention (for your reference when uploading to Cloudflare R2)

```
Audio: [Topic_Snake_Case_Title].m4a        → compressed with ffmpeg to 64k AAC
Video: [Topic_Snake_Case_Title].mp4        → compressed to reasonable size
```

Cloudflare R2 public bucket base URL:
```
https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/
```

ffmpeg compression commands:
```bash
# Audio — compress to 64k AAC (good quality, small file)
ffmpeg -i "input.m4a" -c:a aac -b:a 64k "output_small.m4a"

# Video — compress to web-friendly size
ffmpeg -i "input.mp4" -vcodec libx264 -crf 28 -preset slow -acodec aac -b:a 64k "output_small.mp4"
```

---

## After the file is generated — integration checklist

- [ ] Save file to `D:\StudyBook\temp\seanlgirgis.github.io\learning\[FILENAME]`
- [ ] Add card to `components/learning.html` (copy the S3 card as template)
- [ ] Add route to `assets/js/router.js`: `'[page-key]': ['components/learning.html']`  
      *(learning hub loads from the component, the full page is direct URL only)*
- [ ] Upload audio/video to Cloudflare R2 bucket
- [ ] Update AUDIO_URL and VIDEO_URL placeholders in the HTML file
- [ ] Commit: `git add learning/[FILENAME] components/learning.html assets/js/router.js`
- [ ] Push: `git push origin main`
