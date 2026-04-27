param(
    [string]$Profile = "study",
    [string]$Region = "us-east-1",
    [string]$Bucket = "citi-telemetry-data-lake-dev",
    [string]$RoleName = "StudyBookEMRServerlessExecutionRole"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

function Invoke-Aws {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    $output = & aws @Args 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "AWS CLI command failed: aws $($Args -join ' ')`n$output"
    }
    return $output
}

function Try-GetRoleArn {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TargetRoleName
    )

    $output = & aws iam get-role --profile $Profile --role-name $TargetRoleName --region $Region 2>$null
    if ($LASTEXITCODE -ne 0) {
        return ""
    }

    $parsed = $output | Out-String | ConvertFrom-Json
    return [string]$parsed.Role.Arn
}

$identity = Invoke-Aws -Args @("sts", "get-caller-identity", "--profile", $Profile, "--region", $Region)
$identityObj = $identity | Out-String | ConvertFrom-Json
$accountId = [string]$identityObj.Account

Write-Host "Using AWS profile : $Profile"
Write-Host "AWS account       : $accountId"
Write-Host "Target bucket     : $Bucket"
Write-Host "Target role       : $RoleName"
Write-Host ""

Invoke-Aws -Args @("s3api", "head-bucket", "--profile", $Profile, "--region", $Region, "--bucket", $Bucket) | Out-Null
Write-Host "Bucket check passed." -ForegroundColor Green

$trustPath = Join-Path -Path $env:TEMP -ChildPath "studybook_emr_serverless_trust.json"
$policyPath = Join-Path -Path $env:TEMP -ChildPath "studybook_emr_serverless_policy.json"

@"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "emr-serverless.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
"@ | Set-Content -Path $trustPath -Encoding ASCII

@"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3AccessForCapstoneObjects",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::$Bucket/raw/weblogs/*",
        "arn:aws:s3:::$Bucket/processed/weblogs/*",
        "arn:aws:s3:::$Bucket/emr-scripts/*",
        "arn:aws:s3:::$Bucket/emr-serverless-logs/*"
      ]
    },
    {
      "Sid": "S3ListBucketForCapstone",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::$Bucket"
    }
  ]
}
"@ | Set-Content -Path $policyPath -Encoding ASCII

$roleArn = Try-GetRoleArn -TargetRoleName $RoleName
if ([string]::IsNullOrWhiteSpace($roleArn)) {
    Write-Host "Creating IAM role '$RoleName'..." -ForegroundColor Yellow
    Invoke-Aws -Args @(
        "iam", "create-role",
        "--profile", $Profile,
        "--region", $Region,
        "--role-name", $RoleName,
        "--assume-role-policy-document", "file://$trustPath"
    ) | Out-Null
}
else {
    Write-Host "Role already exists; updating trust policy..." -ForegroundColor Yellow
    Invoke-Aws -Args @(
        "iam", "update-assume-role-policy",
        "--profile", $Profile,
        "--region", $Region,
        "--role-name", $RoleName,
        "--policy-document", "file://$trustPath"
    ) | Out-Null
}

Invoke-Aws -Args @(
    "iam", "put-role-policy",
    "--profile", $Profile,
    "--region", $Region,
    "--role-name", $RoleName,
    "--policy-name", "StudyBookEMRServerlessS3Policy",
    "--policy-document", "file://$policyPath"
) | Out-Null

$roleArn = Try-GetRoleArn -TargetRoleName $RoleName
if ([string]::IsNullOrWhiteSpace($roleArn)) {
    throw "Role creation/update completed but role ARN could not be resolved."
}

$env:AWS_PROFILE = $Profile
$env:AWS_REGION = $Region
$env:EMR_S3_BUCKET = $Bucket
$env:EMR_SERVERLESS_ROLE_ARN = $roleArn

Remove-Item -Path $trustPath -Force -ErrorAction SilentlyContinue
Remove-Item -Path $policyPath -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "EMR Serverless role fix completed." -ForegroundColor Green
Write-Host "Set in current shell:"
Write-Host "  AWS_PROFILE=$($env:AWS_PROFILE)"
Write-Host "  AWS_REGION=$($env:AWS_REGION)"
Write-Host "  EMR_S3_BUCKET=$($env:EMR_S3_BUCKET)"
Write-Host "  EMR_SERVERLESS_ROLE_ARN=$($env:EMR_SERVERLESS_ROLE_ARN)"
Write-Host ""
Write-Host "Next command:"
Write-Host "  python .\capstone\orchestrate.py"
