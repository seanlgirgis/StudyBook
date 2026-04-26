param(
    [switch]$UpdateExisting
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Path $PSCommandPath -Parent
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $scriptDir -ChildPath "..\.."))

$repos = @(
    @{ Name = "jobsearch"; Remote = "https://github.com/seanlgirgis/jobsearch"; RelativePath = "..\jobsearch" },
    @{ Name = "seanlgirgis.github.io"; Remote = "https://github.com/seanlgirgis/seanlgirgis.github.io"; RelativePath = "..\seanlgirgis.github.io" }
)

$results = @()
foreach ($repo in $repos) {
    $targetPath = Join-Path -Path $projectRoot -ChildPath $repo.RelativePath
    $gitDir = Join-Path -Path $targetPath -ChildPath ".git"

    if (Test-Path -LiteralPath $gitDir) {
        if ($UpdateExisting) {
            Write-Host "Updating $($repo.Name) in $targetPath" -ForegroundColor Cyan
            git -C $targetPath pull --ff-only
            $status = "updated"
        }
        else {
            Write-Host "Exists: $($repo.Name) ($targetPath)" -ForegroundColor Gray
            $status = "exists"
        }
    }
    else {
        $parent = Split-Path -Path $targetPath -Parent
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
        Write-Host "Cloning $($repo.Name) into $targetPath" -ForegroundColor Cyan
        git clone $repo.Remote $targetPath
        $status = "cloned"
    }

    $results += [PSCustomObject]@{
        Name = $repo.Name
        Path = $targetPath
        Remote = $repo.Remote
        Status = $status
    }
}

Write-Host "--- Managed Repos ---" -ForegroundColor Yellow
$results | Format-Table -AutoSize
