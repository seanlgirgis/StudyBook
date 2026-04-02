[CmdletBinding()]
param(
    [string]$TargetHost = "localhost",

    [string]$EnvFile = "D:\StudyBook\_infra\env\.env.local",

    [int]$TcpTimeoutMs = 2500,

    [int]$HttpTimeoutSec = 5,

    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path -Path $PSScriptRoot -ChildPath "lib\ProofUtils.ps1")

function Get-EnvMap {
    param(
        [string]$Path
    )

    $map = @{}
    if (-not (Test-Path -LiteralPath $Path)) {
        return $map
    }

    $lines = Get-Content -Path $Path
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed)) { continue }
        if ($trimmed.StartsWith("#")) { continue }
        if ($trimmed -notmatch "=") { continue }

        $parts = $trimmed.Split("=", 2)
        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"')
        if (-not [string]::IsNullOrWhiteSpace($key)) {
            $map[$key] = $value
        }
    }

    return $map
}

function Resolve-Port {
    param(
        [hashtable]$EnvMap,
        [string]$Key,
        [int]$Fallback
    )

    if ($EnvMap.ContainsKey($Key)) {
        $raw = $EnvMap[$Key]
        [int]$parsed = 0
        if ([int]::TryParse($raw, [ref]$parsed)) {
            return $parsed
        }
    }

    return $Fallback
}

$envMap = Get-EnvMap -Path $EnvFile

$tcpChecks = @(
    @{ Name = "postgres"; Key = "POSTGRES_PORT"; Port = 5432 },
    @{ Name = "redis"; Key = "REDIS_PORT"; Port = 6380 },
    @{ Name = "cassandra"; Key = "CASSANDRA_PORT"; Port = 9042 },
    @{ Name = "neo4j-bolt"; Key = "NEO4J_BOLT_PORT"; Port = 7687 },
    @{ Name = "kafka"; Key = "KAFKA_PORT"; Port = 9092 },
    @{ Name = "spark-master"; Key = "SPARK_MASTER_PORT"; Port = 7077 }
)

$httpChecks = @(
    @{ Name = "neo4j-http"; Key = "NEO4J_HTTP_PORT"; Port = 7474; Path = "/" },
    @{ Name = "kafka-ui"; Key = "KAFKA_UI_PORT"; Port = 8080; Path = "/" },
    @{ Name = "airflow"; Key = "AIRFLOW_PORT"; Port = 8082; Path = "/" },
    @{ Name = "mlflow"; Key = "MLFLOW_PORT"; Port = 5000; Path = "/" },
    @{ Name = "kibana"; Key = "KIBANA_PORT"; Port = 5601; Path = "/" }
)

$results = @()

foreach ($check in $tcpChecks) {
    $port = Resolve-Port -EnvMap $envMap -Key $check.Key -Fallback $check.Port
    $results += Invoke-TcpConnectionProof -Name $check.Name -TargetHost $TargetHost -Port $port -TimeoutMs $TcpTimeoutMs
}

foreach ($check in $httpChecks) {
    $port = Resolve-Port -EnvMap $envMap -Key $check.Key -Fallback $check.Port
    $url = "http://$TargetHost`:$port$($check.Path)"
    $results += Invoke-HttpConnectionProof -Name $check.Name -Url $url -TimeoutSec $HttpTimeoutSec
}

if ($AsJson) {
    $results | ConvertTo-Json -Depth 4
} else {
    Write-Host "Connection proofs (TargetHost=$TargetHost, EnvFile=$EnvFile)"
    $results | Sort-Object Method, Name | Format-Table Name, Method, Target, Success, LatencyMs -AutoSize

    $failed = $results | Where-Object { -not $_.Success }
    if ($failed.Count -gt 0) {
        Write-Host ""
        Write-Host "Failed checks:"
        $failed | Format-Table Name, Target, Detail -AutoSize
    }
}

if (($results | Where-Object { -not $_.Success }).Count -gt 0) {
    exit 1
}
