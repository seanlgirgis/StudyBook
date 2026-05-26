param(
    [int]$DelaySeconds = 45
)

$ErrorActionPreference = 'Stop'
$taskName = 'LifeVault Streamlit Help Console'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$startScript = Join-Path $projectRoot "scripts\start_streamlit_help_console_docker.ps1"

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-ExecutionPolicy Bypass -File `"$startScript`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
if ($DelaySeconds -gt 0) {
    $trigger.Delay = "PT${DelaySeconds}S"
}
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    $existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }

    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description 'Starts LifeVault Streamlit Help Console docker stack at user logon.'
    Write-Host "Installed scheduled task: $taskName"
    Write-Host "Action: powershell.exe -ExecutionPolicy Bypass -File `"$startScript`""
    Write-Host "Trigger: At logon with ${DelaySeconds}s delay"
    Write-Host "Admin rights are typically not required when registering under current user context."
    exit 0
}
catch {
    Write-Error "Failed to install scheduled task '$taskName': $_"
    Write-Host "If registration fails due to policy, try running this installer in an elevated PowerShell session."
    exit 1
}
