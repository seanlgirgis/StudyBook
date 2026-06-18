# start_grok_lifevault.ps1
# STABLE — do not modify without explicit request from Sean.
#
# Runtime copy (use this):  C:\scripts\start_grok_lifevault.ps1
# Repo archive (git only):  D:\Workarea\StudyBook\Proj_development\LifeVault\start_grok_lifevault.ps1
# Keep both files identical when a change is ever required.
#
# Location-agnostic launcher: StudyBook venv -> LifeVault -> Grok Build TUI
#
# Usage (from anywhere):
#   pwsh -ExecutionPolicy Bypass -File "C:\scripts\start_grok_lifevault.ps1"
#
# Opens a new PowerShell window by default. To run in the current shell:
#   ...\start_grok_lifevault.ps1 -NoNewWindow

param(
    [string]$StudyBookRoot = 'D:\Workarea\StudyBook',
    [string]$LifeVaultRoot,
    [switch]$NoNewWindow,
    [switch]$NonInteractiveEnv
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$WindowTitle = 'grok_lifevault'

function Resolve-LifeVaultPaths {
    param(
        [string]$StudyBook,
        [string]$LifeVault
    )

    if ([string]::IsNullOrWhiteSpace($LifeVault)) {
        $LifeVault = Join-Path -Path $StudyBook -ChildPath 'Proj_development\LifeVault'
    }

    $envSetter = Join-Path -Path $StudyBook -ChildPath 'env_setter.ps1'

    if (-not (Test-Path -LiteralPath $StudyBook)) {
        throw "StudyBook folder not found: $StudyBook"
    }

    if (-not (Test-Path -LiteralPath $LifeVault)) {
        throw "LifeVault folder not found: $LifeVault"
    }

    if (-not (Test-Path -LiteralPath $envSetter)) {
        throw "env_setter.ps1 not found: $envSetter"
    }

    return [ordered]@{
        LifeVaultRoot = (Resolve-Path -LiteralPath $LifeVault).Path
        StudyBookRoot = (Resolve-Path -LiteralPath $StudyBook).Path
        EnvSetter     = (Resolve-Path -LiteralPath $envSetter).Path
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
For this LifeVault guardian session:
- Read GROK_AGENTS.md startup order before executing any task.
- Then read GROK_RUNBOOK.md, GROK_CURRENT_STATE.md, GROK_OPEN_LOOPS.md, and GROK_OPERATING_RULES.md as needed.
- Project root is Grok-only (GROK_*). Codex files live in agents/codex/.
- Dev repo: D:\Workarea\StudyBook\Proj_development\LifeVault
- Operational data: D:\AI_Lab\LifeVault (never commit live DB, pods, secrets, or personal data to Git).
- Run StudyBook env_setter.ps1 before Python commands (..\..\env_setter.ps1 from project root).
- AI suggests; human approves. No delete/move/rename/sync without approved workflow.
- UC_009 is quarantine-only v0. One-writer/many-reader for lifevault.sqlite.
- Codex implements code; Grok scopes tasks and guards architecture.
- Keep responses ~1 page; one step at a time with Sean.
- On session open: brief pending list from GROK_OPEN_LOOPS.md; do not start unless asked.
'@
}

function Get-GrokBootstrapPrompt {
    param([string]$LifeVaultPath)

    @"
New Grok Build session for LifeVault.

Read GROK_AGENTS.md and follow its startup order before doing any work. Confirm the GROK agent files are loaded and you are operating as guardian in $LifeVaultPath.
"@
}

function Start-GrokLifeVaultSession {
    $paths = Resolve-LifeVaultPaths -StudyBook $StudyBookRoot -LifeVault $LifeVaultRoot
    $grokExe = Resolve-GrokExecutable

    try {
        $Host.UI.RawUI.WindowTitle = $WindowTitle
    } catch {
        # Some hosts do not support title changes.
    }

    Write-Host "=== $WindowTitle ===" -ForegroundColor Cyan
    Write-Host "StudyBook: $($paths.StudyBookRoot)" -ForegroundColor DarkGray
    Write-Host "LifeVault: $($paths.LifeVaultRoot)" -ForegroundColor DarkGray

    Write-Host "`nActivating StudyBook environment..." -ForegroundColor Yellow
    $envArgs = @{}
    if ($NonInteractiveEnv) {
        $envArgs['NonInteractive'] = $true
    }
    & $paths.EnvSetter @envArgs

    Set-Location -LiteralPath $paths.LifeVaultRoot
    Write-Host "Working directory: $(Get-Location)" -ForegroundColor Green

    $rules = Get-GrokBootstrapRules
    $prompt = Get-GrokBootstrapPrompt -LifeVaultPath $paths.LifeVaultRoot

    Write-Host "`nStarting Grok Build..." -ForegroundColor Yellow
    & $grokExe --cwd $paths.LifeVaultRoot --rules $rules $prompt
}

if (-not $NoNewWindow) {
    $pwshExe = Resolve-PwshExecutable
    $paths = Resolve-LifeVaultPaths -StudyBook $StudyBookRoot -LifeVault $LifeVaultRoot
    $scriptPath = $PSCommandPath

    $argList = @(
        '-NoExit'
        '-ExecutionPolicy', 'Bypass'
        '-File', $scriptPath
        '-StudyBookRoot', $paths.StudyBookRoot
        '-LifeVaultRoot', $paths.LifeVaultRoot
        '-NoNewWindow'
    )
    if ($NonInteractiveEnv) {
        $argList += '-NonInteractiveEnv'
    }

    Start-Process -FilePath $pwshExe -ArgumentList $argList -WorkingDirectory $paths.LifeVaultRoot | Out-Null
    return
}

Start-GrokLifeVaultSession