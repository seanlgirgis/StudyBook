# Git for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — version control is table stakes, but DE-specific patterns matter

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Git for Data Engineers
Slug: git-data-engineering

Extra coverage required:
- The four zones — working tree (files on disk), staging area (index), local repo (committed history), remote repo (origin); how a change travels through all four
- The commit model — commits as snapshots not diffs; the DAG structure; HEAD pointer, branch pointers, detached HEAD state
- Branching strategy — feature branches vs trunk-based development; when GitFlow is overkill; what teams at scale actually use
- Merge vs rebase — merge preserves history with a merge commit; rebase replays commits onto a new base and rewrites history; the golden rule of never rebasing shared branches
- Pull request workflow — opening a PR, reviewer checklist, squash merge vs merge commit vs rebase merge and when each makes sense
- Conflict resolution — what a conflict marker means, resolving in the file vs using a merge tool, keeping the blame history clean
- .gitignore for data engineering — ignoring data files, .env secrets, __pycache__, virtual environments, large model artifacts; common patterns every DE repo needs
- Git for pipeline code — versioning ETL scripts, SQL files, config YAML; keeping secrets out; large files via Git LFS
- Tagging releases — annotated tags for production deploys, semantic versioning (v1.2.3), deploying a pinned version of a pipeline
- git log and git bisect for debugging — finding the commit that changed pipeline behavior; bisect binary search for regressions
- GitLab CI/CD integration — .gitlab-ci.yml triggers on push/merge; pipeline stages run automatically; only merge to main if CI passes
- Protecting main — required approvals, CI must pass, no force pushes; the single rule that prevents data disasters
- Pre-commit hooks — pre-commit framework runs linters and formatters before every commit; enforces standards locally before CI

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. The Four Zones & The Commit Model
  2. Branching Strategy — feature branches vs trunk-based
  3. Merge vs Rebase — when to use each
  4. Pull Request Workflow & Conflict Resolution
  5. .gitignore for Data Engineering
  6. Tagging Releases & Semantic Versioning
  7. GitLab CI/CD Integration
  8. Debugging with git log & git bisect
  9. Protecting Main & Pre-commit Hooks
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\git-data-engineering.html
