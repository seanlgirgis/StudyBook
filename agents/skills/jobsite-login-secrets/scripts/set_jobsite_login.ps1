param(
  [Parameter(Mandatory=$true)][string]$SiteKey,
  [Parameter(Mandatory=$true)][string]$Email,
  [Parameter(Mandatory=$true)][string]$Url,
  [string]$Machine = "asuspc"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$normalizedSite = ($SiteKey.Trim().ToUpperInvariant() -replace "[^A-Z0-9]", "_")
if ([string]::IsNullOrWhiteSpace($normalizedSite)) {
  throw "Invalid SiteKey '$SiteKey'."
}

$userKey = "JOBSITE_${normalizedSite}_USER"
$urlKey = "JOBSITE_${normalizedSite}_URL"
$passKey = "JOBSITE_${normalizedSite}_PASSWORD"

& .\scripts\env\set_secret.ps1 -Machine $Machine -Entry "$urlKey=$Url","$userKey=$Email"
& .\scripts\env\set_secret.ps1 -Machine $Machine -PromptSecretKey $passKey

Write-Host "Saved site login for '$SiteKey' using keys: $urlKey, $userKey, $passKey" -ForegroundColor Green
