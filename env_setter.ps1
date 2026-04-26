param(
    [string]$Machine,
    [switch]$SkipVenvActivation,
    [switch]$NonInteractive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ------------------------------------------------------------
# Java config for PySpark
# ------------------------------------------------------------
# Spark 3.5.x works best with a modern JDK. Your machine already has
# Microsoft JDK 17 installed, so we force PowerShell + Python + Spark
# to use that instead of the Oracle Java 8 shim paths.
$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot"
$javaBin = Join-Path -Path $env:JAVA_HOME -ChildPath "bin"

if (-not (Test-Path -LiteralPath (Join-Path $javaBin "java.exe"))) {
    throw "Java not found at expected path: $javaBin\java.exe"
}

# Preserve critical Windows paths so commands like where.exe still work.
$requiredWindowsPaths = @(
    "C:\Windows\system32",
    "C:\Windows",
    "C:\Windows\System32\Wbem",
    "C:\Windows\System32\WindowsPowerShell\v1.0\",
    "C:\Windows\System32\OpenSSH\"
)

# Remove Java 8 / Oracle shim paths that can hijack java.exe resolution.
$existingPathEntries = @(
    [Environment]::GetEnvironmentVariable("Path", "Process") -split ";" |
    Where-Object {
        -not [string]::IsNullOrWhiteSpace($_) `
        -and $_ -notmatch "Common Files\\Oracle\\Java\\java8path" `
        -and $_ -notmatch "Common Files\\Oracle\\Java\\javapath" `
        -and $_ -notmatch "Program Files\\Java\\jdk1\.8\.0_481\\bin" `
        -and $_ -notmatch "Program Files\\Java\\jre1\.8\.0_481\\bin" `
        -and $_ -notmatch "Program Files\\Microsoft\\jdk-17\.0\.18\.8-hotspot\\bin"
    }
)

# Put JDK 17 first. This is critical for PySpark.
$env:Path = (@($javaBin) + $requiredWindowsPaths + $existingPathEntries | Select-Object -Unique) -join ";"

# ------------------------------------------------------------
# StudyBook environment bootstrap
# ------------------------------------------------------------
$projectRoot = Split-Path -Path $PSCommandPath -Parent
$coreScript = Join-Path -Path $projectRoot -ChildPath "scripts\env\env_core.ps1"

if (-not (Test-Path -LiteralPath $coreScript)) {
    throw "Missing core environment script: $coreScript"
}

. $coreScript

$result = Invoke-StudyBookEnvBootstrap `
    -ProjectRoot $projectRoot `
    -MachineName $Machine `
    -SkipVenvActivation:$SkipVenvActivation `
    -NonInteractive:$NonInteractive

# ------------------------------------------------------------
# Add StudyBook scripts directory to PATH
# ------------------------------------------------------------
$scriptsDir = Join-Path -Path $projectRoot -ChildPath "scripts"
[Environment]::SetEnvironmentVariable("STUDYBOOK_SCRIPTS_DIR", $scriptsDir, "Process")

$pathValue = [Environment]::GetEnvironmentVariable("Path", "Process")
$pathEntries = @($pathValue -split ";" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })

$alreadyPresent = $false
foreach ($entry in $pathEntries) {
    if ($entry.TrimEnd("\") -ieq $scriptsDir.TrimEnd("\")) {
        $alreadyPresent = $true
        break
    }
}

if (-not $alreadyPresent) {
    $newPath = if ([string]::IsNullOrWhiteSpace($pathValue)) {
        $scriptsDir
    } else {
        "$scriptsDir;$pathValue"
    }

    [Environment]::SetEnvironmentVariable("Path", $newPath, "Process")
    $env:Path = $newPath
}

# ------------------------------------------------------------
# Final output
# ------------------------------------------------------------
Write-Host "--- StudyBook Environment ---" -ForegroundColor Yellow
Write-Host "Machine: $($result.Machine)" -ForegroundColor Green
Write-Host "Project Root: $($result.ProjectRoot)" -ForegroundColor Gray
Write-Host "Venv Path: $($result.VenvPath)" -ForegroundColor Gray
Write-Host "Python: $($result.PythonPath)" -ForegroundColor Cyan
Write-Host "Secrets Loaded: $($result.SecretsLoaded)" -ForegroundColor DarkCyan
Write-Host "Scripts On PATH: $scriptsDir" -ForegroundColor DarkGray
Write-Host "JAVA_HOME: $env:JAVA_HOME" -ForegroundColor Cyan
Write-Host "Java Bin: $javaBin" -ForegroundColor Cyan