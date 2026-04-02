param(
    [ValidateSet("all", "core", "streaming", "pipeline", "observability")]
    [string]$Group = "all",
    [switch]$NoDetach,
    [switch]$SkipLegacyCleanup
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $PSCommandPath
$infraRoot = Split-Path -Parent $scriptRoot
$dockerDir = Join-Path $infraRoot "docker"
$envDir = Join-Path $infraRoot "env"

$envLocal = Join-Path $envDir ".env.local"
$envExample = Join-Path $envDir ".env.example"

if (Test-Path $envLocal) {
    $envFile = $envLocal
} elseif (Test-Path $envExample) {
    $envFile = $envExample
    Write-Host "Using .env.example because .env.local was not found." -ForegroundColor Yellow
} else {
    throw "No env file found. Expected $envLocal or $envExample."
}

$composeMap = @{
    all = Join-Path $dockerDir "docker-compose.yml"
    core = Join-Path $dockerDir "core.yml"
    streaming = Join-Path $dockerDir "streaming.yml"
    pipeline = Join-Path $dockerDir "pipeline.yml"
    observability = Join-Path $dockerDir "observability.yml"
}

$composeFile = $composeMap[$Group]
if (-not (Test-Path $composeFile)) {
    throw "Compose file not found: $composeFile"
}

function Get-ContainerInspectObject {
    param([Parameter(Mandatory = $true)][string]$Name)
    $json = & docker inspect $Name 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $json) {
        return $null
    }
    return ($json | ConvertFrom-Json)[0]
}

function Is-LegacyWorkspaceContainer {
    param($Inspect)
    if ($null -eq $Inspect) { return $false }
    $labels = $Inspect.Config.Labels
    if ($null -eq $labels) { return $false }
    $configFiles = $labels."com.docker.compose.project.config_files"
    $workingDir = $labels."com.docker.compose.project.working_dir"
    return (($configFiles -like "*\Workspace\*") -or ($workingDir -like "*\Workspace\*"))
}

function Get-TargetContainerNamesForGroup {
    param([Parameter(Mandatory = $true)][string]$SelectedGroup)
    $groupMap = @{
        core = @("de_postgres", "de_redis", "de_cassandra", "de_neo4j", "de_influxdb")
        streaming = @("citi_zookeeper", "citi_kafka", "citi_kafka_ui")
        pipeline = @("citi_spark", "citi_spark_worker", "citi_airflow", "citi_mlflow", "citi_jupyterlab")
        observability = @("de_elasticsearch", "de_kibana", "citi_splunk")
    }
    if ($SelectedGroup -eq "all") {
        return ($groupMap.Values | ForEach-Object { $_ }) | Sort-Object -Unique
    }
    return $groupMap[$SelectedGroup]
}

if (-not $SkipLegacyCleanup) {
    $targetContainerNames = Get-TargetContainerNamesForGroup -SelectedGroup $Group
    foreach ($name in $targetContainerNames) {
        $inspect = Get-ContainerInspectObject -Name $name
        if ($null -eq $inspect) { continue }
        if (Is-LegacyWorkspaceContainer -Inspect $inspect) {
            $sourceConfig = $inspect.Config.Labels."com.docker.compose.project.config_files"
            Write-Host "Removing legacy workspace container '$name' from '$sourceConfig' before StudyBook startup." -ForegroundColor Yellow
            & docker rm -f $name | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to remove legacy container '$name'."
            }
        }
    }
}

$args = @("compose", "-f", $composeFile, "--env-file", $envFile, "up")
if (-not $NoDetach) {
    $args += "-d"
}

Write-Host "Starting infra group '$Group' using $composeFile" -ForegroundColor Cyan
& docker @args
if ($LASTEXITCODE -ne 0) {
    throw "docker compose up failed for group '$Group'."
}

Write-Host "Infra group '$Group' started successfully." -ForegroundColor Green
