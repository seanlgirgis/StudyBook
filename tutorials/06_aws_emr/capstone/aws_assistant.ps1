param(
    [string]$Profile,
    [string]$Region,
    [string]$Bucket,
    [string]$RoleArn,
    [switch]$PersistUserEnv,
    [switch]$WriteEnvFile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-AwsJson {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    $raw = & aws @Args 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "AWS CLI command failed: aws $($Args -join ' ')`n$raw"
    }
    if ([string]::IsNullOrWhiteSpace(($raw | Out-String))) {
        return $null
    }
    return ($raw | Out-String | ConvertFrom-Json)
}

function Get-AwsProfiles {
    $raw = & aws configure list-profiles 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to list AWS profiles. Is AWS CLI installed and configured?`n$raw"
    }

    $profiles = @(
        ($raw -split "`r?`n" | ForEach-Object { $_.Trim() }) |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    )

    return $profiles
}

function Get-CallerIdentityOrNull {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CandidateProfile
    )

    $raw = & aws sts get-caller-identity --profile $CandidateProfile 2>&1
    if ($LASTEXITCODE -ne 0) {
        return $null
    }
    try {
        return ($raw | Out-String | ConvertFrom-Json)
    }
    catch {
        return $null
    }
}

function Select-WorkingProfile {
    param(
        [string[]]$Profiles,
        [string]$RequestedProfile
    )

    if ($RequestedProfile) {
        if ($Profiles -notcontains $RequestedProfile) {
            throw "Requested profile '$RequestedProfile' not found. Available: $($Profiles -join ', ')"
        }
        $identity = Get-CallerIdentityOrNull -CandidateProfile $RequestedProfile
        if (-not $identity) {
            throw "Requested profile '$RequestedProfile' cannot call sts get-caller-identity."
        }
        return @{
            Profile = $RequestedProfile
            Identity = $identity
        }
    }

    if ($env:AWS_PROFILE -and ($Profiles -contains $env:AWS_PROFILE)) {
        $identity = Get-CallerIdentityOrNull -CandidateProfile $env:AWS_PROFILE
        if ($identity) {
            return @{
                Profile = $env:AWS_PROFILE
                Identity = $identity
            }
        }
    }

    if ($Profiles -contains "study") {
        $identity = Get-CallerIdentityOrNull -CandidateProfile "study"
        if ($identity) {
            return @{
                Profile = "study"
                Identity = $identity
            }
        }
    }

    foreach ($candidate in $Profiles) {
        $identity = Get-CallerIdentityOrNull -CandidateProfile $candidate
        if ($identity) {
            return @{
                Profile = $candidate
                Identity = $identity
            }
        }
    }

    throw "No AWS profile could successfully call sts get-caller-identity."
}

function Resolve-Region {
    param(
        [string]$SelectedProfile,
        [string]$RequestedRegion
    )

    if ($RequestedRegion) {
        return $RequestedRegion
    }

    if ($env:AWS_REGION) {
        return $env:AWS_REGION
    }

    $configured = (& aws configure get region --profile $SelectedProfile 2>$null)
    if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($configured)) {
        return $configured.Trim()
    }

    return "us-east-1"
}

function Resolve-Bucket {
    param(
        [string]$SelectedProfile,
        [string]$SelectedRegion,
        [string]$RequestedBucket
    )

    if ($RequestedBucket) {
        return $RequestedBucket
    }
    if ($env:EMR_S3_BUCKET) {
        return $env:EMR_S3_BUCKET
    }

    $bucketsObj = Invoke-AwsJson -Args @("s3api", "list-buckets", "--profile", $SelectedProfile, "--region", $SelectedRegion)
    $names = @()
    if ($bucketsObj -and $bucketsObj.Buckets) {
        $names = @($bucketsObj.Buckets | ForEach-Object { $_.Name })
    }
    if ($names.Count -eq 0) {
        return ""
    }

    $preferred = $names | Where-Object { $_ -match "studybook|emr" } | Select-Object -First 1
    if ($preferred) {
        return $preferred
    }
    return ""
}

function Resolve-EmrRoleArn {
    param(
        [string]$SelectedProfile,
        [string]$SelectedRegion,
        [string]$RequestedRoleArn
    )

    if ($RequestedRoleArn) {
        return $RequestedRoleArn
    }
    if ($env:EMR_SERVERLESS_ROLE_ARN) {
        return $env:EMR_SERVERLESS_ROLE_ARN
    }

    try {
        $rolesObj = Invoke-AwsJson -Args @("iam", "list-roles", "--profile", $SelectedProfile, "--region", $SelectedRegion)
        if (-not $rolesObj -or -not $rolesObj.Roles) {
            return ""
        }
        $match = $rolesObj.Roles |
            Where-Object { $_.RoleName -match "(?i)emr.*serverless|serverless.*emr" } |
            Select-Object -First 1
        if ($match) {
            return [string]$match.Arn
        }
    }
    catch {
        return ""
    }

    return ""
}

function Set-EnvVar {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [string]$Value,
        [switch]$PersistUser
    )

    Set-Item -Path "Env:$Name" -Value $Value
    if ($PersistUser) {
        [Environment]::SetEnvironmentVariable($Name, $Value, "User")
    }
}

$profiles = Get-AwsProfiles
if ($profiles.Count -eq 0) {
    throw "No AWS profiles found. Run 'aws configure' first."
}

$selected = Select-WorkingProfile -Profiles $profiles -RequestedProfile $Profile
$selectedProfile = [string]$selected.Profile
$identity = $selected.Identity

$selectedRegion = Resolve-Region -SelectedProfile $selectedProfile -RequestedRegion $Region
$selectedBucket = Resolve-Bucket -SelectedProfile $selectedProfile -SelectedRegion $selectedRegion -RequestedBucket $Bucket
$selectedRoleArn = Resolve-EmrRoleArn -SelectedProfile $selectedProfile -SelectedRegion $selectedRegion -RequestedRoleArn $RoleArn

Set-EnvVar -Name "AWS_PROFILE" -Value $selectedProfile -PersistUser:$PersistUserEnv
Set-EnvVar -Name "AWS_REGION" -Value $selectedRegion -PersistUser:$PersistUserEnv
if (-not [string]::IsNullOrWhiteSpace($selectedBucket)) {
    Set-EnvVar -Name "EMR_S3_BUCKET" -Value $selectedBucket -PersistUser:$PersistUserEnv
}
if (-not [string]::IsNullOrWhiteSpace($selectedRoleArn)) {
    Set-EnvVar -Name "EMR_SERVERLESS_ROLE_ARN" -Value $selectedRoleArn -PersistUser:$PersistUserEnv
}

$envFilePath = Join-Path -Path $PSScriptRoot -ChildPath ".emr_env.ps1"
if ($WriteEnvFile) {
    $lines = @()
    $lines += ('$env:AWS_PROFILE="' + $selectedProfile + '"')
    $lines += ('$env:AWS_REGION="' + $selectedRegion + '"')
    if (-not [string]::IsNullOrWhiteSpace($selectedBucket)) {
        $lines += '$env:EMR_S3_BUCKET="' + $selectedBucket + '"'
    }
    if (-not [string]::IsNullOrWhiteSpace($selectedRoleArn)) {
        $lines += '$env:EMR_SERVERLESS_ROLE_ARN="' + $selectedRoleArn + '"'
    }
    Set-Content -Path $envFilePath -Value $lines -Encoding UTF8
}

Write-Host ""
Write-Host "AWS Assistant Summary" -ForegroundColor Cyan
Write-Host "====================="
Write-Host "Available profiles : $($profiles -join ', ')"
Write-Host "Selected profile   : $selectedProfile"
Write-Host "AWS account        : $($identity.Account)"
Write-Host "AWS ARN            : $($identity.Arn)"
Write-Host "AWS region         : $selectedRegion"
Write-Host "EMR_S3_BUCKET      : $(if ($selectedBucket) { $selectedBucket } else { '<not-set>' })"
Write-Host "EMR role ARN       : $(if ($selectedRoleArn) { $selectedRoleArn } else { '<not-set>' })"
Write-Host ""

if ($PersistUserEnv) {
    Write-Host "Saved to user environment variables for future shells." -ForegroundColor Green
}
else {
    Write-Host "Set for current PowerShell process only." -ForegroundColor Yellow
    Write-Host "Tip: Dot-source to keep vars in your current shell:"
    Write-Host "  . .\capstone\aws_assistant.ps1 -WriteEnvFile"
}

if ($WriteEnvFile) {
    Write-Host "Wrote env helper file: $envFilePath" -ForegroundColor Green
    Write-Host "Load later with:"
    Write-Host "  . .\capstone\.emr_env.ps1"
}
