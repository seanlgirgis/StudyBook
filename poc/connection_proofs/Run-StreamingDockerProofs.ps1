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

$zkPort = Resolve-EnvPort -EnvMap $envMap -Key 'ZOOKEEPER_PORT' -Fallback 2181
$kafkaPort = Resolve-EnvPort -EnvMap $envMap -Key 'KAFKA_PORT' -Fallback 9092
$kafkaUiPort = Resolve-EnvPort -EnvMap $envMap -Key 'KAFKA_UI_PORT' -Fallback 8080

$results = @()
$results += Invoke-TcpConnectionProof -Name 'streaming-zookeeper-tcp' -TargetHost $TargetHost -Port $zkPort -TimeoutMs $TcpTimeoutMs
$results += Invoke-DockerExecProof -Name 'streaming-zookeeper-ready' -Container 'citi_zookeeper' -ExecCommand @('bash','-lc','cub zk-ready localhost:2181 10')

$results += Invoke-TcpConnectionProof -Name 'streaming-kafka-tcp' -TargetHost $TargetHost -Port $kafkaPort -TimeoutMs $TcpTimeoutMs
$results += Invoke-DockerExecProof -Name 'streaming-kafka-list-topics' -Container 'citi_kafka' -ExecCommand @('bash','-lc','kafka-topics --bootstrap-server localhost:9092 --list')

$results += Invoke-HttpConnectionProof -Name 'streaming-kafka-ui-http' -Url ("http://$TargetHost`:$kafkaUiPort/") -TimeoutSec $HttpTimeoutSec -AcceptedStatusCodes @(200,301,302)

Write-ProofResults -Results $results -AsJson:$AsJson


