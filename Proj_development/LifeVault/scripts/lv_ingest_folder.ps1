param(
  [Parameter(Mandatory = $true)]
  [string]$SourcePath,
  [string]$Story,
  [switch]$AutoApprovePod,
  [string]$OutputRoot,
  [string]$ApprovedPodName,
  [int]$MaxPreviewFiles = 200
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$srcPath = Join-Path $projectRoot "src"

if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "$srcPath;$($env:PYTHONPATH)"
} else {
  $env:PYTHONPATH = $srcPath
}

$storyArg = if ($Story) { $Story } else { "__NONE__" }
$outArg = if ($OutputRoot) { $OutputRoot } else { "__NONE__" }
$podArg = if ($ApprovedPodName) { $ApprovedPodName } else { "__NONE__" }
$approveArg = if ($AutoApprovePod) { "1" } else { "0" }

@"
import json
import sys
from lifevault.lv_ingest_folder import run_lv_ingest_folder

source_path = sys.argv[1]
story = None if sys.argv[2] == "__NONE__" else sys.argv[2]
auto_approve = sys.argv[3] == "1"
output_root = None if sys.argv[4] == "__NONE__" else sys.argv[4]
approved_pod_name = None if sys.argv[5] == "__NONE__" else sys.argv[5]
max_preview = int(sys.argv[6])

result = run_lv_ingest_folder(
    source_path=source_path,
    story=story,
    output_root=output_root,
    auto_approve_pod=auto_approve,
    approved_pod_name=approved_pod_name,
    max_preview_files=max_preview,
)

p = result["proposal"]
print("LV_ingest_folder UC_001 summary")
print(f"proposal_path={p['proposal_path']}")
print(f"file_count={p['file_count']}")
print(f"highest_sensitivity={p['highest_sensitivity']}")
print(f"duplicate_candidate_count={p['duplicate_candidate_count']}")
print(f"recommended_next_action={p['recommended_next_action']}")
print(f"suggested_metadata={json.dumps(p['suggested_metadata'])}")

if "pod" in result:
    pod = result["pod"]
    print("LV_ingest_folder UC_003 summary")
    print(f"pod_path={pod['pod_path']}")
    print(f"file_count={pod['file_count']}")
    print(f"copied_count={pod['copied_count']}")
    print(f"failed_count={pod['failed_count']}")
    print(f"review_csv_path={pod['review_csv_path']}")
    print(f"next_safe_action={pod['next_safe_action']}")
else:
    print("Approval gate: UC_003 not run.")
    print(f"next_uc003_command={result['next_uc003_command']}")
"@ | python - $SourcePath $storyArg $approveArg $outArg $podArg $MaxPreviewFiles

