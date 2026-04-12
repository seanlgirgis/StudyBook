param(
    [Parameter(Position = 0)]
    [string]$Needle,

    [switch]$CaseSensitive,

    [int]$Limit = 50,

    [Alias("h")]
    [switch]$Usage
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $Root "coding_challenges\scripts\search_index.py"

if (-not (Test-Path $ScriptPath)) {
    throw "search_index.py not found at $ScriptPath"
}

$PreferredPython = "C:\Users\shareuser\AppData\Local\Python\bin\python.exe"
$PythonCmd = if (Test-Path $PreferredPython) { $PreferredPython } else { "python" }

$ArgsList = @($ScriptPath, $Needle, "--limit", $Limit)
if ($CaseSensitive) {
    $ArgsList += "--case-sensitive"
}

if ($Usage) {
    @"
Usage:
  .\search_index.ps1 <needle> [-Limit <n>] [-CaseSensitive] [-h]

Examples:
  .\search_index.ps1 48
  .\search_index.ps1 242 -Limit 20
  .\search_index.ps1 "Valid Anagram" -CaseSensitive
"@ | Write-Output
    exit 0
}

if ([string]::IsNullOrWhiteSpace($Needle)) {
    throw "Needle is required. Use -h for usage."
}

& $PythonCmd @ArgsList
