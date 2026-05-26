param()

$ErrorActionPreference = 'Stop'
$taskName = 'LifeVault Streamlit Help Console'

try {
    $existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($null -eq $existing) {
        Write-Host "Scheduled task not found: $taskName"
        exit 0
    }

    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Removed scheduled task: $taskName"
    Write-Host "Note: This does not stop running containers. Use stop script separately if needed."
    exit 0
}
catch {
    Write-Error "Failed to remove scheduled task '$taskName': $_"
    exit 1
}
