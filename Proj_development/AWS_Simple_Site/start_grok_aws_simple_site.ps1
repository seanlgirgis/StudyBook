# start_grok_aws_simple_site.ps1
# STABLE - do not modify without explicit request from Sean.
#
# Runtime copy (use this):  C:\scripts\start_grok_aws_simple_site.ps1
# Repo archive (git only):  D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site\start_grok_aws_simple_site.ps1
# Keep both files identical when a change is ever required.
#
# Location-agnostic launcher: AWS_Simple_Site (clipboard → S3) -> Grok Build TUI
#
# Usage (from anywhere):
#   pwsh -ExecutionPolicy Bypass -File "C:\scripts\start_grok_aws_simple_site.ps1"
#
# Opens a new PowerShell window by default. To run in the current shell:
#   ...\start_grok_aws_simple_site.ps1 -NoNewWindow

param(
    [string]$AwsSimpleSiteRoot = 'D:\Workarea\StudyBook\Proj_development\AWS_Simple_Site',
    [switch]$NoNewWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$WindowTitle = 'grok_aws_simple_site'

function Resolve-AwsSimpleSitePaths {
    param([string]$Root)

    if (-not (Test-Path -LiteralPath $Root)) {
        throw "AWS_Simple_Site folder not found: $Root"
    }

    return [ordered]@{
        AwsSimpleSiteRoot = (Resolve-Path -LiteralPath $Root).Path
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
For this AWS_Simple_Site (clipboard → S3 static site) project session:
- Read BOOTSTRAP.md startup order before executing any task.
- Then read PROJECT_GUIDE.md for publish commands and AWS resource names.
- Read Grok_PROJECT_PROFILE.md when boundaries or routing are unclear.
- Read only task files (publish_clipboard.py, etc.); do not scan other Workarea projects.
- Read Grok_CURRENT_STATE.md only for status or planning.
- Read Grok_PROJECT_MEMORY.md only when stable architecture context is needed.
- Use Grok_ prefix for agent files (Grok_PROJECT_PROFILE.md, Grok_PROJECT_MEMORY.md, Grok_CURRENT_STATE.md).
- Preferred publish: python publish_clipboard.py text; local-only: --no-upload.
- Never store or request AWS secret keys in the repo or chat.
- Publisher IAM is limited to bucket aws-comm-site — not general AWS admin work.
- Full Sean context export: D:\Workarea\learning\sean_girgis_memory_context_export_2026-06-15.md (confirm time-sensitive facts).
- Sean has ADD/ADHD: keep every response ~1 page or less; one concept at a time; wait for his reply before continuing.
- Default work mode: bite-sized unless Sean requests feature or maintenance mode.
- When Sean asks for an opinion, give an honest assessment with tradeoffs - not blind agreement.
- Sean manages Git; director syncs via C:\scripts\gitqall.ps1.
- UCM is the local clipboard tray app — not this project; short command nuggets may pointer to local_memory.
'@
}

function Get-GrokBootstrapPrompt {
    param([string]$RootPath)

    @"
New Grok Build session for AWS_Simple_Site (clipboard to S3 static website).

Read BOOTSTRAP.md and follow its startup order before doing any work. Confirm the Grok agent files are loaded and you are operating repository-first in $RootPath. Default to bite-sized work unless Sean requests feature or maintenance mode. Primary ops guide is PROJECT_GUIDE.md.
"@
}

function Start-GrokAwsSimpleSiteSession {
    $paths = Resolve-AwsSimpleSitePaths -Root $AwsSimpleSiteRoot
    $grokExe = Resolve-GrokExecutable

    try {
        $Host.UI.RawUI.WindowTitle = $WindowTitle
    } catch {
        # Some hosts do not support title changes.
    }

    Write-Host "=== $WindowTitle ===" -ForegroundColor Cyan
    Write-Host "AWS_Simple_Site: $($paths.AwsSimpleSiteRoot)" -ForegroundColor DarkGray

    Set-Location -LiteralPath $paths.AwsSimpleSiteRoot
    Write-Host "Working directory: $(Get-Location)" -ForegroundColor Green

    $rules = Get-GrokBootstrapRules
    $prompt = Get-GrokBootstrapPrompt -RootPath $paths.AwsSimpleSiteRoot

    Write-Host "`nStarting Grok Build..." -ForegroundColor Yellow
    & $grokExe --cwd $paths.AwsSimpleSiteRoot --rules $rules $prompt
}

if (-not $NoNewWindow) {
    $pwshExe = Resolve-PwshExecutable
    $paths = Resolve-AwsSimpleSitePaths -Root $AwsSimpleSiteRoot
    $scriptPath = $PSCommandPath

    $argList = @(
        '-NoExit'
        '-ExecutionPolicy', 'Bypass'
        '-File', $scriptPath
        '-AwsSimpleSiteRoot', $paths.AwsSimpleSiteRoot
        '-NoNewWindow'
    )

    Start-Process -FilePath $pwshExe -ArgumentList $argList -WorkingDirectory $paths.AwsSimpleSiteRoot | Out-Null
    return
}

Start-GrokAwsSimpleSiteSession
