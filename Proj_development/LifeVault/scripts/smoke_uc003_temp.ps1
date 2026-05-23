param()

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$srcPath = Join-Path $projectRoot "src"

if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "$srcPath;$($env:PYTHONPATH)"
} else {
  $env:PYTHONPATH = $srcPath
}

$base = Join-Path $env:TEMP "lifevault_uc003_smoke"
$source = Join-Path $base "fake_source"
$proposalDir = Join-Path $base "fake_proposal"
$outputRoot = Join-Path $base "uc003_output_root"

New-Item -ItemType Directory -Force -Path $source,$proposalDir,$outputRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $source "nested") | Out-Null

Set-Content -Path (Join-Path $source "alpha.txt") -Value "fake alpha" -Encoding UTF8
Set-Content -Path (Join-Path $source "beta.txt") -Value "fake beta" -Encoding UTF8
Set-Content -Path (Join-Path $source "nested\gamma.txt") -Value "fake gamma" -Encoding UTF8

$utcNow = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

$filePreview = @(
  @{ relative_path = "alpha.txt"; filename = "alpha.txt"; extension = ".txt"; size_bytes = 10; modified_time = $utcNow; file_kind = "document"; filename_sensitivity_level = "normal"; filename_sensitivity_reasons = @("no_sensitive_rule_match"); duplicate_name_group_id = $null; included_in_preview = $true },
  @{ relative_path = "beta.txt"; filename = "beta.txt"; extension = ".txt"; size_bytes = 9; modified_time = $utcNow; file_kind = "document"; filename_sensitivity_level = "normal"; filename_sensitivity_reasons = @("no_sensitive_rule_match"); duplicate_name_group_id = $null; included_in_preview = $true },
  @{ relative_path = "nested/gamma.txt"; filename = "gamma.txt"; extension = ".txt"; size_bytes = 10; modified_time = $utcNow; file_kind = "document"; filename_sensitivity_level = "normal"; filename_sensitivity_reasons = @("no_sensitive_rule_match"); duplicate_name_group_id = $null; included_in_preview = $true }
)

$proposal = @{
  schema_version = "1.0"
  proposal_id = "uc001_smoke_fake"
  created_at = $utcNow
  source_path = $source
  source_exists = $true
  scan_mode = "metadata_only"
  scan_status = "success"
  is_partial = $false
  story = "Fake UC_003 smoke source"
  folder_summary = @{ file_count = 3; folder_count = 1; total_size_bytes = 29; extension_counts = @{ ".txt" = 3 }; largest_files = @(); oldest_modified_time = $utcNow; newest_modified_time = $utcNow; depth_limited = $false; max_depth_used = $null }
  file_preview = $filePreview
  filename_sensitivity_summary = @{ highest_level = "normal"; candidate_count = 0; candidates_by_level = @{ normal = 3 }; rule_version = "filename_rules_v1"; note = "fake" }
  content_scan_status = "not_performed"
  content_scan_reason = "UC_001 does not extract file contents by default."
  content_sensitivity_summary = "not_scanned"
  duplicate_name_summary = @{ duplicate_name_candidate_count = 0; groups = @() }
  suggested_metadata = @{ suggested_pod_name = "pod_uc003_smoke"; suggested_project = "Smoke"; suggested_category = "Test"; suggested_event_name = "uc003_smoke"; suggested_vault_path = "LifeVault/01_Knowledge"; confidence = 0.5; reason = "smoke"; questions_for_user = @() }
  recommended_next_action = "proceed_to_uc_003_after_approval"
  allowed_next_actions = @("create_pod_after_approval")
  forbidden_actions_in_uc_001 = @("copy_files","write_database","call_onedrive_or_rclone","delete_files","move_files","rename_files","extract_full_content","write_text_cache","ai_classify_full_text")
  warnings = @()
  errors = @()
}

$proposalPath = Join-Path $proposalDir "proposal.json"
[System.IO.File]::WriteAllText($proposalPath, ($proposal | ConvertTo-Json -Depth 8), (New-Object System.Text.UTF8Encoding($false)))

python -m lifevault.uc003_cli --proposal-path "$proposalPath" --approved --output-root "$outputRoot"
if ($LASTEXITCODE -ne 0) {
  Write-Host "UC_003 smoke failed with exit code $LASTEXITCODE"
  exit $LASTEXITCODE
}

$podsRoot = Join-Path $outputRoot "onboarding\pods"
if (-not (Test-Path $podsRoot)) {
  throw "Pods root was not created: $podsRoot"
}
$podDir = Get-ChildItem -Directory $podsRoot | Select-Object -First 1
if (-not $podDir) {
  throw "No pod directory created under $podsRoot"
}

Write-Host "Created pod path: $($podDir.FullName)"
Write-Host "\nPod contents:"
Get-ChildItem -Recurse -Force $podDir.FullName | ForEach-Object { $_.FullName }

Write-Host "\n_pod_profile.json:"
Get-Content -Raw (Join-Path $podDir.FullName "_pod_profile.json")

Write-Host "\n_pod_manifest.csv:"
Get-Content -Raw (Join-Path $podDir.FullName "_pod_manifest.csv")

Write-Host "\n_review.csv:"
Get-Content -Raw (Join-Path $podDir.FullName "_review.csv")
