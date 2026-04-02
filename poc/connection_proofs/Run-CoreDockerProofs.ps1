[CmdletBinding()]
param(
    [string]$TargetHost = 'localhost',
    [string]$EnvFile = 'D:\StudyBook\_infra\env\.env.local',
    [int]$TcpTimeoutMs = 2500,
    [int]$HttpTimeoutSec = 6,
    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path -Path $PSScriptRoot -ChildPath 'lib\ProofUtils.ps1')
. (Join-Path -Path $PSScriptRoot -ChildPath 'DockerProofUtils.ps1')

$envMap = Get-ConnectionProofEnvMap -Path $EnvFile

$postgresPort = Resolve-EnvPort -EnvMap $envMap -Key 'POSTGRES_PORT' -Fallback 5432
$redisPort = Resolve-EnvPort -EnvMap $envMap -Key 'REDIS_PORT' -Fallback 6380
$cassandraPort = Resolve-EnvPort -EnvMap $envMap -Key 'CASSANDRA_PORT' -Fallback 9042
$neo4jHttpPort = Resolve-EnvPort -EnvMap $envMap -Key 'NEO4J_HTTP_PORT' -Fallback 7474
$influxPort = Resolve-EnvPort -EnvMap $envMap -Key 'INFLUXDB_PORT' -Fallback 8086

$results = @()
$results += Invoke-TcpConnectionProof -Name 'core-postgres-tcp' -TargetHost $TargetHost -Port $postgresPort -TimeoutMs $TcpTimeoutMs
$results += Invoke-DockerExecProof -Name 'core-postgres-pg_isready' -Container 'de_postgres' -ExecCommand @('pg_isready','-U',(Resolve-EnvValue -EnvMap $envMap -Key 'POSTGRES_USER' -Fallback 'de_admin'))

$results += Invoke-TcpConnectionProof -Name 'core-redis-tcp' -TargetHost $TargetHost -Port $redisPort -TimeoutMs $TcpTimeoutMs
$results += Invoke-DockerExecProof -Name 'core-redis-ping' -Container 'de_redis' -ExecCommand @('redis-cli','-a',(Resolve-EnvValue -EnvMap $envMap -Key 'REDIS_PASSWORD' -Fallback 'change_me'),'PING')

$results += Invoke-TcpConnectionProof -Name 'core-cassandra-tcp' -TargetHost $TargetHost -Port $cassandraPort -TimeoutMs $TcpTimeoutMs
$results += Invoke-DockerExecProof -Name 'core-cassandra-describe' -Container 'de_cassandra' -ExecCommand @('cqlsh','-e','DESCRIBE KEYSPACES')

$results += Invoke-HttpConnectionProof -Name 'core-neo4j-http' -Url ("http://$TargetHost`:$neo4jHttpPort/") -TimeoutSec $HttpTimeoutSec -AcceptedStatusCodes @(200,301,302,401)
$results += Invoke-HttpConnectionProof -Name 'core-influxdb-health' -Url ("http://$TargetHost`:$influxPort/health") -TimeoutSec $HttpTimeoutSec -AcceptedStatusCodes @(200,204)

Write-ProofResults -Results $results -AsJson:$AsJson


