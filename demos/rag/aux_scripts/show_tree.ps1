[CmdletBinding()]
param(
    [Parameter()]
    [string]$Path = "."
)

$ErrorActionPreference = "Stop"

$excludeDirs = @(
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "node_modules",
    "dist",
    "build"
)

function Get-IsExcludedDirectory {
    param(
        [Parameter(Mandatory = $true)]
        [System.IO.FileSystemInfo]$Item
    )

    return $Item.PSIsContainer -and ($excludeDirs -contains $Item.Name)
}

function Write-Tree {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CurrentPath,
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Prefix
    )

    $children = Get-ChildItem -LiteralPath $CurrentPath -Force |
        Where-Object { -not (Get-IsExcludedDirectory -Item $_) } |
        Sort-Object @{ Expression = { -not $_.PSIsContainer } }, Name

    for ($i = 0; $i -lt $children.Count; $i++) {
        $child = $children[$i]
        $isLast = ($i -eq $children.Count - 1)
        $branch = if ($isLast) { "\-- " } else { "+-- " }

        if ($child.PSIsContainer) {
            Write-Output ("{0}{1}[{2}]" -f $Prefix, $branch, $child.Name)
            $nextPrefix = if ($isLast) { "$Prefix    " } else { "$Prefix|   " }
            Write-Tree -CurrentPath $child.FullName -Prefix $nextPrefix
        } else {
            $sizeKb = [math]::Round(($child.Length / 1KB), 2)
            Write-Output ("{0}{1}{2} ({3} KB)" -f $Prefix, $branch, $child.Name, $sizeKb)
        }
    }
}

$resolvedPath = Resolve-Path -LiteralPath $Path
$root = Get-Item -LiteralPath $resolvedPath

if (-not $root.PSIsContainer) {
    throw "Path must be a directory: $($root.FullName)"
}

Write-Output ("[{0}]" -f $root.FullName)
Write-Tree -CurrentPath $root.FullName -Prefix ""
