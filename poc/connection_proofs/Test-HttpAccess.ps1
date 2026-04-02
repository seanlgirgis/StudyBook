[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Url,

    [string]$Name = "custom-http-check",

    [int]$TimeoutSec = 5,

    [int[]]$AcceptedStatusCodes = @(200, 201, 202, 204, 301, 302, 307, 308),

    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path -Path $PSScriptRoot -ChildPath "lib\ProofUtils.ps1")

$result = Invoke-HttpConnectionProof -Name $Name -Url $Url -TimeoutSec $TimeoutSec -AcceptedStatusCodes $AcceptedStatusCodes

if ($AsJson) {
    $result | ConvertTo-Json -Depth 4
} else {
    $result | Format-List
}

if (-not $result.Success) {
    exit 1
}
