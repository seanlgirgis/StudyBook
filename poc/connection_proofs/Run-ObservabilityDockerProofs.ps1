[CmdletBinding()]
param(
    [string]$TargetHost = 'localhost',
    [string]$EnvFile = 'D:\StudyBook\_infra\env\.env.local',
    [int]$HttpTimeoutSec = 8,
    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path -Path $PSScriptRoot -ChildPath 'lib\ProofUtils.ps1')
. (Join-Path -Path $PSScriptRoot -ChildPath 'DockerProofUtils.ps1')

$envMap = Get-ConnectionProofEnvMap -Path $EnvFile

$elasticPort = Resolve-EnvPort -EnvMap $envMap -Key 'ELASTIC_PORT' -Fallback 9200
$kibanaPort = Resolve-EnvPort -EnvMap $envMap -Key 'KIBANA_PORT' -Fallback 5601
$splunkMgtPort = Resolve-EnvPort -EnvMap $envMap -Key 'SPLUNK_PORT_MGT' -Fallback 8089

$elasticPassword = Resolve-EnvValue -EnvMap $envMap -Key 'ELASTIC_PASSWORD' -Fallback 'change_me'
$splunkPassword = Resolve-EnvValue -EnvMap $envMap -Key 'SPLUNK_PASSWORD' -Fallback 'change_me'

$results = @()
$results += Invoke-TcpConnectionProof -Name 'obs-elasticsearch-tcp' -TargetHost $TargetHost -Port $elasticPort
$results += Invoke-DockerExecProof -Name 'obs-elasticsearch-cluster-health' -Container 'de_elasticsearch' -ExecCommand @('bash','-lc',"curl -s -u elastic:$elasticPassword http://localhost:9200/_cluster/health")

$results += Invoke-HttpConnectionProof -Name 'obs-kibana-status' -Url ("http://$TargetHost`:$kibanaPort/api/status") -TimeoutSec $HttpTimeoutSec -AcceptedStatusCodes @(200)

$results += Invoke-TcpConnectionProof -Name 'obs-splunk-mgt-tcp' -TargetHost $TargetHost -Port $splunkMgtPort
$results += Invoke-DockerExecProof -Name 'obs-splunk-server-info' -Container 'citi_splunk' -ExecCommand @('bash','-lc',"curl -sk https://localhost:8089/services/server/info -u admin:$splunkPassword")

Write-ProofResults -Results $results -AsJson:$AsJson


