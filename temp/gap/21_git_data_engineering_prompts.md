# Git for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — version control is table stakes, but DE-specific patterns matter

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Git for Data Engineers
Slug: git-data-engineering
Extra coverage required: core concepts — working tree, staging area, local repo, remote repo — the four zones,
the commit model — commits as snapshots not diffs, the DAG structure, HEAD and branch pointers,
branching strategy — feature branches, main/develop, GitFlow vs trunk-based development — what teams actually use,
merge vs rebase — when to use each, what rebase does to history, the golden rule of rebase,
pull request workflow — opening a PR, review process, squash merge vs merge commit vs rebase merge,
conflict resolution — understanding what a conflict is, resolving in the file vs using a merge tool,
.gitignore for data engineering — ignoring data files, .env secrets, __pycache__, virtual environments, large outputs,
git for pipeline code — versioning ETL scripts, config files, SQL files, keeping secrets out of the repo,
tagging releases — semantic versioning, annotated tags, deploying a specific version of a pipeline,
git log and git diff for debugging — finding when a pipeline behavior changed, bisect for regression hunting,
GitLab CI/CD integration — .gitlab-ci.yml, triggering pipeline runs on merge to main,
protecting main branch — required approvals, CI must pass before merge, preventing force pushes,
git blame and git log --follow — understanding the history of a specific transformation function,
monorepo vs polyrepo for data teams — trade-offs for teams managing multiple pipelines,
pre-commit hooks — running linting and tests before every commit, pre-commit framework,
real scenario: GitLab repository structure for a production ETL pipeline — what lives in the repo, what doesn't.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug git-data-engineering -ChunkSize 750
```

Upload final_git-data-engineering.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_git-data-engineering.mp3` is live on R2.

```
Topic: Git for Data Engineers
Slug: git-data-engineering
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_git-data-engineering.mp3
Today's date: 2026-04-25

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\git-data-engineering.html
