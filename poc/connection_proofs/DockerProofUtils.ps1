Set-StrictMode -Version Latest

function Get-ConnectionProofEnvMap {
    param([string]$Path)

    $map = @{}
    if (-not (Test-Path -LiteralPath $Path)) {
        return $map
    }

    foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed)) { continue }
        if ($trimmed.StartsWith('#')) { continue }
        if ($trimmed -notmatch '=') { continue }

        $parts = $trimmed.Split('=', 2)
        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"')
        if (-not [string]::IsNullOrWhiteSpace($key)) {
            $map[$key] = $value
        }
    }

    return $map
}

function Resolve-EnvPort {
    param(
        [hashtable]$EnvMap,
        [string]$Key,
        [int]$Fallback
    )

    if ($EnvMap.ContainsKey($Key)) {
        $raw = [string]$EnvMap[$Key]
        [int]$parsed = 0
        if ([int]::TryParse($raw, [ref]$parsed)) {
            return $parsed
        }
    }

    return $Fallback
}

function Resolve-EnvValue {
    param(
        [hashtable]$EnvMap,
        [string]$Key,
        [string]$Fallback
    )

    if ($EnvMap.ContainsKey($Key)) {
        $value = [string]$EnvMap[$Key]
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return $value
        }
    }

    return $Fallback
}

function Invoke-DockerExecProof {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string]$Container,

        [Parameter(Mandatory = $true)]
        [string[]]$ExecCommand,

        [int]$TimeoutSec = 20
    )

    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $success = $false
    $detail = ''

    try {
        $null = Get-Command docker -ErrorAction Stop

        $output = & docker exec $Container @ExecCommand 2>&1
        $code = $LASTEXITCODE

        $success = ($code -eq 0)
        $detail = ($output | Out-String).Trim()
        if ([string]::IsNullOrWhiteSpace($detail)) {
            $detail = if ($success) { 'docker exec succeeded.' } else { 'docker exec failed.' }
        }
    }
    catch {
        $detail = Set-StrictMode -Version Latest

function Get-ConnectionProofEnvMap {
    param([string]$Path)

    $map = @{}
    if (-not (Test-Path -LiteralPath $Path)) {
        return $map
    }

    foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed)) { continue }
        if ($trimmed.StartsWith('#')) { continue }
        if ($trimmed -notmatch '=') { continue }

        $parts = $trimmed.Split('=', 2)
        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"')
        if (-not [string]::IsNullOrWhiteSpace($key)) {
            $map[$key] = $value
        }
    }

    return $map
}

function Resolve-EnvPort {
    param(
        [hashtable]$EnvMap,
        [string]$Key,
        [int]$Fallback
    )

    if ($EnvMap.ContainsKey($Key)) {
        $raw = [string]$EnvMap[$Key]
        [int]$parsed = 0
        if ([int]::TryParse($raw, [ref]$parsed)) {
            return $parsed
        }
    }

    return $Fallback
}

function Resolve-EnvValue {
    param(
        [hashtable]$EnvMap,
        [string]$Key,
        [string]$Fallback
    )

    if ($EnvMap.ContainsKey($Key)) {
        $value = [string]$EnvMap[$Key]
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return $value
        }
    }

    return $Fallback
}

function Invoke-DockerExecProof {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string]$Container,

        [Parameter(Mandatory = $true)]
        [string[]]$ExecCommand,

        [int]$TimeoutSec = 20
    )

    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $success = $false
    $detail = ''

    try {
        $dockerPath = Get-Command docker -ErrorAction Stop
        $job = Start-Job -ScriptBlock {
            param($containerName, $commandParts)
            & docker exec $containerName @commandParts 2>&1 | Out-String
            $code = $LASTEXITCODE
            [PSCustomObject]@{ Code = $code; Output = $($input | Out-String) }
        } -ArgumentList $Container, $ExecCommand

        if (-not (Wait-Job -Job $job -Timeout $TimeoutSec)) {
            Stop-Job -Job $job -Force | Out-Null
            throw "Timeout after ${TimeoutSec}s"
        }

        $result = Receive-Job -Job $job -Keep
        Remove-Job -Job $job -Force | Out-Null

        $code = [int]$result.Code
        $output = [string]$result.Output

        $success = ($code -eq 0)
        $detail = $output.Trim()
        if ([string]::IsNullOrWhiteSpace($detail)) {
            $detail = if ($success) { 'docker exec succeeded.' } else { 'docker exec failed.' }
        }
    }
    catch {
        $detail = $_.Exception.Message
        $success = $false
    }
    finally {
        $stopwatch.Stop()
    }

    if ($detail.Length -gt 400) {
        $detail = $detail.Substring(0, 400) + '...'
    }

    [PSCustomObject]@{
        Name      = $Name
        Method    = 'DOCKER_EXEC'
        Target    = "container:$Container"
        Success   = $success
        LatencyMs = [int]$stopwatch.ElapsedMilliseconds
        Detail    = $detail
        CheckedAt = (Get-Date).ToString('s')
    }
}

function Write-ProofResults {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.IEnumerable]$Results,
        [switch]$AsJson
    )

    if ($AsJson) {
        $Results | ConvertTo-Json -Depth 5
    }
    else {
        $Results | Sort-Object Method, Name | Format-Table Name, Method, Target, Success, LatencyMs -AutoSize
        $failed = @($Results | Where-Object { -not $_.Success })
        if ($failed.Count -gt 0) {
            Write-Host ''
            Write-Host 'Failed checks:'
            $failed | Format-Table Name, Target, Detail -AutoSize
        }
    }

    if ((@($Results | Where-Object { -not $_.Success })).Count -gt 0) {
        exit 1
    }
}
.Exception.Message
        $success = $false
    }
    finally {
        $stopwatch.Stop()
    }

    if ($detail.Length -gt 400) {
        $detail = $detail.Substring(0, 400) + '...'
    }

    [PSCustomObject]@{
        Name      = $Name
        Method    = 'DOCKER_EXEC'
        Target    = "container:$Container"
        Success   = $success
        LatencyMs = [int]$stopwatch.ElapsedMilliseconds
        Detail    = $detail
        CheckedAt = (Get-Date).ToString('s')
    }
}

function Write-ProofResults {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.IEnumerable]$Results,
        [switch]$AsJson
    )

    if ($AsJson) {
        $Results | ConvertTo-Json -Depth 5
    }
    else {
        $Results | Sort-Object Method, Name | Format-Table Name, Method, Target, Success, LatencyMs -AutoSize
        $failed = @($Results | Where-Object { -not $_.Success })
        if ($failed.Count -gt 0) {
            Write-Host ''
            Write-Host 'Failed checks:'
            $failed | Format-Table Name, Target, Detail -AutoSize
        }
    }

    if ((@($Results | Where-Object { -not $_.Success })).Count -gt 0) {
        exit 1
    }
}

