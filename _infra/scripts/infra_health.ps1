param(
    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Test-TcpPort {
    param(
        [string]$HostName,
        [int]$Port,
        [int]$TimeoutMs = 2000
    )

    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $iar = $client.BeginConnect($HostName, $Port, $null, $null)
        if (-not $iar.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) {
            return $false
        }
        $client.EndConnect($iar) | Out-Null
        return $true
    }
    catch {
        return $false
    }
    finally {
        $client.Dispose()
    }
}

function Test-HttpEndpoint {
    param(
        [string]$Url,
        [int]$TimeoutSec = 4
    )

    try {
        $response = Invoke-WebRequest -Uri $Url -Method Get -TimeoutSec $TimeoutSec -SkipHttpErrorCheck
        return ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500)
    }
    catch {
        return $false
    }
}

$dockerLines = & docker ps --format "{{json .}}"
if ($LASTEXITCODE -ne 0) {
    throw "Unable to query Docker containers with 'docker ps'."
}

$runningNames = @{}
foreach ($line in $dockerLines) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $obj = $line | ConvertFrom-Json
    $runningNames[$obj.Names] = $true
}

$checks = @(
    @{ Service = "postgres"; Container = "de_postgres"; Ports = @(5432) },
    @{ Service = "redis"; Container = "de_redis"; Ports = @(6380) },
    @{ Service = "cassandra"; Container = "de_cassandra"; Ports = @(9042) },
    @{ Service = "neo4j"; Container = "de_neo4j"; Ports = @(7474, 7687); Http = "http://localhost:7474" },
    @{ Service = "influxdb"; Container = "de_influxdb"; Ports = @(8086); Http = "http://localhost:8086/health" },
    @{ Service = "zookeeper"; Container = "citi_zookeeper"; Ports = @(2181) },
    @{ Service = "kafka"; Container = "citi_kafka"; Ports = @(9092, 29092) },
    @{ Service = "kafka_ui"; Container = "citi_kafka_ui"; Ports = @(8080); Http = "http://localhost:8080" },
    @{ Service = "spark"; Container = "citi_spark"; Ports = @(7077, 8081); Http = "http://localhost:8081" },
    @{ Service = "spark_worker"; Container = "citi_spark_worker"; Ports = @(8085); Http = "http://localhost:8085" },
    @{ Service = "airflow"; Container = "citi_airflow"; Ports = @(8082) },
    @{ Service = "mlflow"; Container = "citi_mlflow"; Ports = @(5000); Http = "http://localhost:5000" },
    @{ Service = "elasticsearch"; Container = "de_elasticsearch"; Ports = @(9200) },
    @{ Service = "kibana"; Container = "de_kibana"; Ports = @(5601) },
    @{ Service = "splunk"; Container = "citi_splunk"; Ports = @(8000, 8088, 8089) }
)

$results = @()
foreach ($check in $checks) {
    $running = $runningNames.ContainsKey($check.Container)

    $portResults = @()
    foreach ($port in $check.Ports) {
        $portResults += [pscustomobject]@{
            Port = $port
            Open = (Test-TcpPort -HostName "localhost" -Port $port)
        }
    }

    $portsOk = @($portResults | Where-Object { -not $_.Open }).Count -eq 0

    $httpOk = $null
    if ($check.ContainsKey("Http")) {
        $httpOk = Test-HttpEndpoint -Url $check.Http
    }

    $overall = $running -and $portsOk -and (($httpOk -eq $null) -or $httpOk)

    $results += [pscustomobject]@{
        Service = $check.Service
        Container = $check.Container
        Running = $running
        PortsOk = $portsOk
        HttpOk = $httpOk
        Overall = $overall
        Ports = ($portResults | ForEach-Object { "{0}:{1}" -f $_.Port, ($(if ($_.Open) { "open" } else { "closed" })) }) -join ", "
    }
}

if ($AsJson) {
    $results | ConvertTo-Json -Depth 4
}
else {
    $results | Sort-Object Service | Format-Table -AutoSize
}

$failed = @($results | Where-Object { -not $_.Overall }).Count
if ($failed -gt 0) {
    exit 1
}

