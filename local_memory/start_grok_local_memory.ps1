# start_grok_local_memory.ps1
# STABLE — do not modify without explicit request from Sean.
#
# Runtime copy (use this):  C:\scripts\start_grok_local_memory.ps1
# Repo archive (git only):  D:\Workarea\StudyBook\local_memory\start_grok_local_memory.ps1
# Keep both files identical when a change is ever required.
#
# Location-agnostic launcher: StudyBook venv -> local_memory -> Grok Build TUI
#
# Usage (from anywhere):
#   pwsh -ExecutionPolicy Bypass -File "C:\scripts\start_grok_local_memory.ps1"
#
# Opens a new PowerShell window by default. To run in the current shell:
#   ...\start_grok_local_memory.ps1 -NoNewWindow

param(
    [string]$StudyBookRoot = 'D:\Workarea\StudyBook',
    [string]$LocalMemoryRoot,
    [switch]$NoNewWindow,
    [switch]$NonInteractiveEnv
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$WindowTitle = 'grok_local_memory'

function Resolve-StudyBookPaths {
    param(
        [string]$StudyBook,
        [string]$LocalMemory
    )

    if ([string]::IsNullOrWhiteSpace($LocalMemory)) {
        $LocalMemory = Join-Path -Path $StudyBook -ChildPath 'local_memory'
    }

    $envSetter = Join-Path -Path $StudyBook -ChildPath 'env_setter.ps1'

    if (-not (Test-Path -LiteralPath $StudyBook)) {
        throw "StudyBook folder not found: $StudyBook"
    }

    if (-not (Test-Path -LiteralPath $LocalMemory)) {
        throw "local_memory folder not found: $LocalMemory"
    }

    if (-not (Test-Path -LiteralPath $envSetter)) {
        throw "env_setter.ps1 not found: $envSetter"
    }

    return [ordered]@{
        LocalMemoryRoot = (Resolve-Path -LiteralPath $LocalMemory).Path
        StudyBookRoot   = (Resolve-Path -LiteralPath $StudyBook).Path
        EnvSetter       = (Resolve-Path -LiteralPath $envSetter).Path
    }
}

function Resolve-PwshExecutable {
    $pwshCmd = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($pwshCmd) {
        return $pwshCmd.Source
    }

    $candidates = @(
        (Join-Path $env:ProgramFiles 'PowerShell\7\pwsh.exe')
        (Join-Path $env:ProgramFiles 'PowerShell\6\pwsh.exe')
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    throw "pwsh not found on PATH or under Program Files\PowerShell. Install PowerShell 7+ first."
}

function Resolve-GrokExecutable {
    $grokCmd = Get-Command grok -ErrorAction SilentlyContinue
    if ($grokCmd) {
        return $grokCmd.Source
    }

    $fallback = Join-Path $env:USERPROFILE '.grok\bin\grok.exe'
    if (Test-Path -LiteralPath $fallback) {
        return $fallback
    }

    throw "grok not found on PATH and not at $fallback. Install Grok CLI first."
}

function Get-GrokBootstrapRules {
    @'
For this local_memory vault session:
- Read GROK_AGENTS.md startup order before executing any task.
- Then read GROK_RUNBOOK.md, GROK_CURRENT_STATE.md, GROK_MEMORY.md, LOCAL_MEMORY_HANDOFF.md, and CONTROL_PROTOCOL.md as needed.
- Use GROK_ prefix for Grok-specific memory files (GROK_MEMORY.md, GROK_AGENTS.md, GROK_RUNBOOK.md, GROK_CURRENT_STATE.md).
- Repository files are source of truth; search local files before answering.
- Run StudyBook env_setter.ps1 before any Python commands.
- When Sean asks for an opinion, give an honest assessment with tradeoffs — not blind agreement.
'@
}

function Get-GrokBootstrapPrompt {
    param([string]$LocalMemoryPath)

    @"
New Grok Build session for local_memory.

Read GROK_AGENTS.md and follow its startup order before doing any work. Confirm the GROK agent files are loaded and you are operating repository-first in $LocalMemoryPath.
"@
}

function Start-GrokLocalMemorySession {
    $paths = Resolve-StudyBookPaths -StudyBook $StudyBookRoot -LocalMemory $LocalMemoryRoot
    $grokExe = Resolve-GrokExecutable

    try {
        $Host.UI.RawUI.WindowTitle = $WindowTitle
    } catch {
        # Some hosts do not support title changes.
    }

    Write-Host "=== $WindowTitle ===" -ForegroundColor Cyan
    Write-Host "StudyBook: $($paths.StudyBookRoot)" -ForegroundColor DarkGray
    Write-Host "local_memory: $($paths.LocalMemoryRoot)" -ForegroundColor DarkGray

    Write-Host "`nActivating StudyBook environment..." -ForegroundColor Yellow
    $envArgs = @{}
    if ($NonInteractiveEnv) {
        $envArgs['NonInteractive'] = $true
    }
    & $paths.EnvSetter @envArgs

    Set-Location -LiteralPath $paths.LocalMemoryRoot
    Write-Host "Working directory: $(Get-Location)" -ForegroundColor Green

    $rules = Get-GrokBootstrapRules
    $prompt = Get-GrokBootstrapPrompt -LocalMemoryPath $paths.LocalMemoryRoot

    Write-Host "`nStarting Grok Build..." -ForegroundColor Yellow
    & $grokExe --cwd $paths.LocalMemoryRoot --rules $rules $prompt
}

if (-not $NoNewWindow) {
    $pwshExe = Resolve-PwshExecutable
    $paths = Resolve-StudyBookPaths -StudyBook $StudyBookRoot -LocalMemory $LocalMemoryRoot
    $scriptPath = $PSCommandPath

    $argList = @(
        '-NoExit'
        '-ExecutionPolicy', 'Bypass'
        '-File', $scriptPath
        '-StudyBookRoot', $paths.StudyBookRoot
        '-LocalMemoryRoot', $paths.LocalMemoryRoot
        '-NoNewWindow'
    )
    if ($NonInteractiveEnv) {
        $argList += '-NonInteractiveEnv'
    }

    Start-Process -FilePath $pwshExe -ArgumentList $argList -WorkingDirectory $paths.LocalMemoryRoot | Out-Null
    return
}

Start-GrokLocalMemorySession