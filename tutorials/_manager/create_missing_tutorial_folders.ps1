# create_missing_tutorial_folders.ps1
# Run from: D:\Workarea\StudyBook

$TutorialRoot = "D:\Workarea\StudyBook\tutorials"

$Topics = @(
    "15_data_anonymization_pii",
    "16_aws_iam",
    "17_postgresql",
    "18_sql_patterns",
    "19_python_testing",
    "20_pydantic",
    "21_aws_redshift",
    "22_aws_athena",
    "23_sqlalchemy",
    "25_numpy",
    "28_data_stubbing",
    "29_streamlit",
    "30_fastapi",
    "31_aws_lambda",
    "32_aws_dynamodb",
    "34_aws_bedrock",
    "35_terraform",
    "37_cicd",
    "38_aws_ecs",
    "39_aws_cloudformation",
    "40_opensearch",
    "41_snowflake_pyiceberg",
    "42_aws_lambda_de",
    "43_terraform_de",
    "44_pyiceberg",
    "45_great_expectations",
    "46_cicd_data",
    "47_redis_de"
)

foreach ($Topic in $Topics) {
    $Path = Join-Path $TutorialRoot $Topic

    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Host "Created: $Path"
    } else {
        Write-Host "Exists:  $Path"
    }

    $ReadmePath = Join-Path $Path "README.md"

    if (-not (Test-Path $ReadmePath)) {
        $Title = $Topic -replace "_", " "
        $Content = @"
# $Title

Status: scaffolded only

Planned files:
- prompt.md
- prompt_READY_TO_PASTE.md
- tutorial/setup Python files
- capstone files
- tests

Notes:
- Folder created during project scaffolding.
- Implementation not started yet.
"@

        Set-Content -Path $ReadmePath -Value $Content -Encoding UTF8
        Write-Host "  Added README.md"
    }
}

Write-Host ""
Write-Host "Done. Missing tutorial folders are now scaffolded."