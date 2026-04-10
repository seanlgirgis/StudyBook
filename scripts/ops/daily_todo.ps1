param(
    [ValidateSet('summary', 'list', 'add', 'done')]
    [string]$Action = 'summary',
    [string]$Title,
    [string]$DueDate,
    [string]$Id,
    [string]$Notes,
    [string]$Context,
    [string]$Date = (Get-Date).ToString('yyyy-MM-dd'),
    [switch]$IncludeDone
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Parse-DateStrict {
    param([Parameter(Mandatory = $true)][string]$Value)
    return [datetime]::ParseExact($Value, 'yyyy-MM-dd', [System.Globalization.CultureInfo]::InvariantCulture)
}

function New-State {
    return [pscustomobject]@{
        next_id = 1
        tasks   = @()
    }
}

function Save-State {
    param(
        [Parameter(Mandatory = $true)]$State,
        [Parameter(Mandatory = $true)][string]$Path
    )
    $State | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Ensure-StateFile {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        $parent = Split-Path -Path $Path -Parent
        if (-not (Test-Path -LiteralPath $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        Save-State -State (New-State) -Path $Path
    }
}

function Load-State {
    param([Parameter(Mandatory = $true)][string]$Path)
    Ensure-StateFile -Path $Path
    $raw = Get-Content -Raw -LiteralPath $Path
    if ([string]::IsNullOrWhiteSpace($raw)) {
        $state = New-State
        Save-State -State $state -Path $Path
        return $state
    }
    $state = $raw | ConvertFrom-Json
    if (-not $state.tasks) {
        $state.tasks = @()
    }
    if (-not $state.next_id) {
        $state.next_id = 1
    }
    return $state
}

function Print-TaskList {
    param(
        [Parameter(Mandatory = $true)][string]$Header,
        [Parameter(Mandatory = $true)]$Items
    )
    Write-Host ""
    Write-Host $Header -ForegroundColor Cyan
    if ($Items.Count -eq 0) {
        Write-Host "  (none)" -ForegroundColor DarkGray
        return
    }
    foreach ($item in $Items) {
        $context = if ([string]::IsNullOrWhiteSpace($item.context)) { '' } else { " | $($item.context)" }
        Write-Host ("  [{0}] {1} (due {2}){3}" -f $item.id, $item.title, $item.due_date, $context)
    }
}

$scriptDir = Split-Path -Path $PSCommandPath -Parent
$projectRoot = (Resolve-Path (Join-Path -Path $scriptDir -ChildPath '..\..')).Path
$dataPath = Join-Path -Path $projectRoot -ChildPath 'agents\shared\daily_todo.json'
$state = Load-State -Path $dataPath

switch ($Action) {
    'add' {
        if ([string]::IsNullOrWhiteSpace($Title)) {
            throw 'For -Action add, provide -Title.'
        }
        if ([string]::IsNullOrWhiteSpace($DueDate)) {
            throw 'For -Action add, provide -DueDate in yyyy-MM-dd.'
        }
        $null = Parse-DateStrict -Value $DueDate
        $id = 'TODO-{0:D4}' -f [int]$state.next_id
        $state.next_id = [int]$state.next_id + 1
        $createdOn = (Get-Date).ToString('yyyy-MM-dd')

        $task = [pscustomobject]@{
            id           = $id
            title        = $Title.Trim()
            due_date     = $DueDate
            status       = 'open'
            created_on   = $createdOn
            completed_on = $null
            context      = $Context
            notes        = $Notes
        }
        $state.tasks += $task
        Save-State -State $state -Path $dataPath
        Write-Host ("Added {0}: {1} (due {2})" -f $id, $task.title, $task.due_date) -ForegroundColor Green
        break
    }
    'done' {
        if ([string]::IsNullOrWhiteSpace($Id)) {
            throw 'For -Action done, provide -Id (example: TODO-0001).'
        }
        $task = $state.tasks | Where-Object { $_.id -eq $Id } | Select-Object -First 1
        if (-not $task) {
            throw "Task not found: $Id"
        }
        if ($task.status -eq 'done') {
            Write-Host ("Task already done: {0}" -f $Id) -ForegroundColor Yellow
            break
        }
        $task.status = 'done'
        $task.completed_on = (Get-Date).ToString('yyyy-MM-dd')
        Save-State -State $state -Path $dataPath
        Write-Host ("Completed {0}: {1}" -f $task.id, $task.title) -ForegroundColor Green
        break
    }
    'list' {
        $items = if ($IncludeDone) { $state.tasks } else { $state.tasks | Where-Object { $_.status -eq 'open' } }
        $sorted = $items | Sort-Object due_date, id
        Print-TaskList -Header 'Task List' -Items $sorted
        break
    }
    'summary' {
        $today = Parse-DateStrict -Value $Date
        $todayStr = $today.ToString('yyyy-MM-dd')
        $tomorrowStr = $today.AddDays(1).ToString('yyyy-MM-dd')

        $openTasks = $state.tasks | Where-Object { $_.status -eq 'open' }
        $dueToday = @($openTasks | Where-Object { $_.due_date -eq $todayStr } | Sort-Object id)
        $dueTomorrow = @($openTasks | Where-Object { $_.due_date -eq $tomorrowStr } | Sort-Object id)
        $leftover = @($openTasks | Where-Object { $_.due_date -lt $todayStr } | Sort-Object due_date, id)

        Write-Host ("Daily Todo Summary for {0}" -f $todayStr) -ForegroundColor Yellow
        Print-TaskList -Header 'Due Today' -Items $dueToday
        Print-TaskList -Header 'Due Tomorrow' -Items $dueTomorrow
        Print-TaskList -Header 'Leftover (Overdue)' -Items $leftover

        Write-Host ""
        Write-Host ("Open Tasks Total: {0}" -f @($openTasks).Count) -ForegroundColor Gray
        break
    }
}
