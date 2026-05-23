# 08_local_downloads_staging

Purpose: stage a configured local-source batch (for example Downloads) into lab staging with metadata manifest.
Safety level: copy-only from local source to staging; no delete/move/rename.
Run: .\labs\08_local_downloads_staging\run.ps1 -BatchName "batch_002_boa_ltimindtree_onboarding"
Expected output: staged files under lab_root\staging\<BatchName> and _manifest.csv.
Success: files copied to staging and manifest generated.
Failure: missing source path, missing batch config, or copy error.
Promotable into src\ later: yes.
