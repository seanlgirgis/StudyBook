[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetHost,

    [Parameter(Mandatory = $true)]
    [int]$Port,

    [string]$Name = "custom-tcp-check",

    [int]$TimeoutMs = 2500,

    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path -Path $PSScriptRoot -ChildPath "lib\ProofUtils.ps1")

$result = Invoke-TcpConnectionProof -Name $Name -TargetHost $TargetHost -Port $Port -TimeoutMs $TimeoutMs

if ($AsJson) {
    $result | ConvertTo-Json -Depth 4
} else {
    $result | Format-List
}

if (-not $result.Success) {
    exit 1
}
