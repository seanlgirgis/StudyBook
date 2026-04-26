$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$lessons = @(
    "01_cluster_connection.py",
    "02_dataframe_operations.py",
    "03_sql_and_views.py",
    "04_joins_and_broadcast.py",
    "05_shuffle_partitions_cache.py",
    "06_bronze_silver_gold_pipeline.py",
    "07_spark_ui_experiments.py"
)

foreach ($lesson in $lessons) {
    Write-Host "\n=== Running $lesson ===" -ForegroundColor Cyan
    python -u (Join-Path $root "..\$lesson")
}
