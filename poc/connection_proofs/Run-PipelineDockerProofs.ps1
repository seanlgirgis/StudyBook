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

$sparkMasterUi = Resolve-EnvPort -EnvMap $envMap -Key 'SPARK_MASTER_UI_PORT' -Fallback 8081
$sparkWorkerUi = Resolve-EnvPort -EnvMap $envMap -Key 'SPARK_WORKER_UI_PORT' -Fallback 8085
$airflowPort = Resolve-EnvPort -EnvMap $envMap -Key 'AIRFLOW_PORT' -Fallback 8082
$mlflowPort = Resolve-EnvPort -EnvMap $envMap -Key 'MLFLOW_PORT' -Fallback 5000
$jupyterPort = Resolve-EnvPort -EnvMap $envMap -Key 'JUPYTER_PORT' -Fallback 8888

$results = @()
$results += Invoke-HttpConnectionProof -Name 'pipeline-spark-master-ui' -Url ("http://$TargetHost`:$sparkMasterUi/") -TimeoutSec $HttpTimeoutSec -AcceptedStatusCodes @(200,301,302)
$results += Invoke-HttpConnectionProof -Name 'pipeline-spark-worker-ui' -Url ("http://$TargetHost`:$sparkWorkerUi/") -TimeoutSec $HttpTimeoutSec -AcceptedStatusCodes @(200,301,302)

$results += Invoke-TcpConnectionProof -Name 'pipeline-airflow-tcp' -TargetHost $TargetHost -Port $airflowPort
$results += Invoke-DockerExecProof -Name 'pipeline-airflow-dags-list' -Container 'citi_airflow' -ExecCommand @('bash','-lc','airflow dags list --output table | head -n 20')

$results += Invoke-HttpConnectionProof -Name 'pipeline-mlflow-http' -Url ("http://$TargetHost`:$mlflowPort/") -TimeoutSec $HttpTimeoutSec -AcceptedStatusCodes @(200,301,302)
$results += Invoke-HttpConnectionProof -Name 'pipeline-jupyterlab-http' -Url ("http://$TargetHost`:$jupyterPort/lab") -TimeoutSec $HttpTimeoutSec -AcceptedStatusCodes @(200,301,302,403)

Write-ProofResults -Results $results -AsJson:$AsJson
