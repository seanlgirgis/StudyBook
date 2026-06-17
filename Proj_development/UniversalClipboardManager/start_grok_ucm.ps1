# start_grok_ucm.ps1
# STABLE — do not modify without explicit request from Sean.
#
# Runtime copy (use this):  C:\scripts\start_grok_ucm.ps1
# Repo archive (git only):  D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager\start_grok_ucm.ps1
# Keep both files identical when a change is ever required.
#
# Location-agnostic launcher: StudyBook venv -> UCM project venv -> Grok Build TUI
#
# Usage (from anywhere):
#   pwsh -ExecutionPolicy Bypass -File "C:\scripts\start_grok_ucm.ps1"
#
# Opens a new PowerShell window by default. To run in the current shell:
#   ...\start_grok_ucm.ps1 -NoNewWindow

param(
    [string]$ProjectRoot = 'D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager',
    [string]$StudyBookEnvSetter = 'D:\Workarea\StudyBook\env_setter.ps1',
    [switch]$NoNewWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$WindowTitle = 'grok_ucm'

function Resolve-UcmPaths {
    param(
        [string]$Project,
        [string]$StudyBookEnvScript
    )

    if (-not (Test-Path -LiteralPath $Project)) {
        throw "Universal Clipboard Manager folder not found: $Project"
    }

    if (-not (Test-Path -LiteralPath $StudyBookEnvScript)) {
        throw "StudyBook env_setter.ps1 not found: $StudyBookEnvScript"
    }

    $projectEnvSetter = Join-Path $Project 'env_setter.ps1'
    if (-not (Test-Path -LiteralPath $projectEnvSetter)) {
        throw "Project env_setter.ps1 not found: $projectEnvSetter"
    }

    return [ordered]@{
        ProjectRoot          = (Resolve-Path -LiteralPath $Project).Path
        StudyBookEnvSetter   = (Resolve-Path -LiteralPath $StudyBookEnvScript).Path
        ProjectEnvSetter     = (Resolve-Path -LiteralPath $projectEnvSetter).Path
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
For this Universal Clipboard Manager session:
- Read .agent/GROK_INDEX.md startup order before executing any task.
- Then read GROK_AGENT_STATUS.md, GROK_PENDING_TASK.md, GROK_OPEN_LOOPS.md, and GROK_OPERATING_RULES.md as needed.
- Use GROK_ prefix for Grok-specific memory files under .agent/ (GROK_INDEX.md, GROK_MEMORY.md, GROK_CONTEXT.md, etc.).
- Full project history: PROJECT_FULL_CONTEXT_AND_HISTORY.md at project root.
- Run D:\Workarea\StudyBook\env_setter.ps1 first (StudyBook venv: proj_educate) before any StudyBook-wide Python work.
- Then run the project env_setter.ps1 (local .venv + KB_INBOX_PATH) before app-specific Python commands.
- Source repo: D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
- Deployed runtime: C:\scripts\UniversalClipboardManager (changes need deploy.ps1 + app restart).
- Treat clipboard_data.json as user data — do not wipe casually.
- Hotkeys live in settings.json (F10 show/hide, F11 capture); restart app after hotkey edits.
- Execute commands yourself; keep responses concise and focused.
- On every session open: read GROK_OPEN_LOOPS.md and remind Sean of pending enhancements (backlog table); mark items done there when completed — no separate todo file.
'@
}

function Get-GrokBootstrapPrompt {
    param([string]$UcmPath)

    @"
New Grok Build session for Universal Clipboard Manager.

Read .agent/GROK_INDEX.md and follow its startup order before doing any work. Confirm the GROK agent files are loaded and you are operating repository-first in $UcmPath.
"@
}

function Start-GrokUcmSession {
    $paths = Resolve-UcmPaths -Project $ProjectRoot -StudyBookEnvScript $StudyBookEnvSetter
    $grokExe = Resolve-GrokExecutable

    try {
        $Host.UI.RawUI.WindowTitle = $WindowTitle
    } catch {
        # Some hosts do not support title changes.
    }

    Write-Host "=== $WindowTitle ===" -ForegroundColor Cyan
    Write-Host "project: $($paths.ProjectRoot)" -ForegroundColor DarkGray

    Write-Host "`nActivating StudyBook environment (proj_educate venv)..." -ForegroundColor Yellow
    . $paths.StudyBookEnvSetter -NonInteractive

    Write-Host "`nActivating Universal Clipboard Manager environment (local .venv)..." -ForegroundColor Yellow
    . $paths.ProjectEnvSetter

    Set-Location -LiteralPath $paths.ProjectRoot
    Write-Host "Working directory: $(Get-Location)" -ForegroundColor Green

    $rules = Get-GrokBootstrapRules
    $prompt = Get-GrokBootstrapPrompt -UcmPath $paths.ProjectRoot

    Write-Host "`nStarting Grok Build..." -ForegroundColor Yellow
    & $grokExe --cwd $paths.ProjectRoot --rules $rules $prompt
}

if (-not $NoNewWindow) {
    $pwshExe = Resolve-PwshExecutable
    $paths = Resolve-UcmPaths -Project $ProjectRoot -StudyBookEnvScript $StudyBookEnvSetter
    $scriptPath = $PSCommandPath

    $argList = @(
        '-NoExit'
        '-ExecutionPolicy', 'Bypass'
        '-File', $scriptPath
        '-ProjectRoot', $paths.ProjectRoot
        '-StudyBookEnvSetter', $paths.StudyBookEnvSetter
        '-NoNewWindow'
    )

    Start-Process -FilePath $pwshExe -ArgumentList $argList -WorkingDirectory $paths.ProjectRoot | Out-Null
    return
}

Start-GrokUcmSession