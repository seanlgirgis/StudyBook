[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$pocRoot = Join-Path -Path $repoRoot -ChildPath "pocs\01_static_site_shell"

$requiredFiles = @(
    "pocs/01_static_site_shell/website/index.html",
    "pocs/01_static_site_shell/website/assets/styles.css",
    "pocs/01_static_site_shell/website/assets/chat-widget.js"
)

$missingFiles = @()
foreach ($relative in $requiredFiles) {
    $abs = Join-Path -Path $repoRoot -ChildPath ($relative -replace "/", "\")
    if (-not (Test-Path -LiteralPath $abs)) {
        $missingFiles += $relative
    }
}

$failures = @()
if ($missingFiles.Count -gt 0) {
    $failures += "Missing required files: $($missingFiles -join ', ')"
}

$indexPath = Join-Path -Path $pocRoot -ChildPath "website\index.html"
if (Test-Path -LiteralPath $indexPath) {
    $indexText = Get-Content -Raw -LiteralPath $indexPath
    if ($indexText -notmatch [regex]::Escape("assets/styles.css")) {
        $failures += "index.html missing reference to assets/styles.css"
    }
    if ($indexText -notmatch [regex]::Escape("assets/chat-widget.js")) {
        $failures += "index.html missing reference to assets/chat-widget.js"
    }
}

$scanTargets = @(
    (Join-Path -Path $pocRoot -ChildPath "website\index.html"),
    (Join-Path -Path $pocRoot -ChildPath "website\assets\styles.css"),
    (Join-Path -Path $pocRoot -ChildPath "website\assets\chat-widget.js")
) | Where-Object { Test-Path -LiteralPath $_ }

$patternMap = @{
    "fetch" = "\bfetch\b"
    "XMLHttpRequest" = "\bXMLHttpRequest\b"
    "axios" = "\baxios\b"
    "/api" = "/api"
    "localhost" = "\blocalhost\b"
    "http://" = "http://"
    "https://" = "https://"
}

foreach ($label in $patternMap.Keys) {
    $regex = $patternMap[$label]
    $matches = Select-String -Path $scanTargets -Pattern $regex
    if ($matches) {
        $locations = $matches | ForEach-Object { "{0}:{1}" -f $_.Path, $_.LineNumber }
        $failures += "Disallowed pattern '$label' found at: $($locations -join '; ')"
    }
}

if ($failures.Count -eq 0) {
    Write-Output "PASS: static site validation succeeded."
    exit 0
}

Write-Output "FAIL: static site validation failed."
foreach ($failure in $failures) {
    Write-Output ("- {0}" -f $failure)
}
exit 1
