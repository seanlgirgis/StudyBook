Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function ConvertTo-NormalizedMachineName {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $normalized = $Name.Trim().ToLowerInvariant()
    $normalized = $normalized -replace "[^a-z0-9\-_. ]", ""
    $normalized = $normalized -replace "[\s_]+", "-"
    return $normalized
}

function Resolve-StudyBookPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot,
        [Parameter(Mandatory = $true)]
        [string]$PathValue
    )

    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return [System.IO.Path]::GetFullPath($PathValue)
    }

    $combined = Join-Path -Path $ProjectRoot -ChildPath $PathValue
    return [System.IO.Path]::GetFullPath($combined)
}

function Expand-TemplateString {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value,
        [Parameter(Mandatory = $true)]
        [hashtable]$Tokens
    )

    $result = $Value
    foreach ($key in $Tokens.Keys) {
        $result = $result.Replace("{$key}", [string]$Tokens[$key])
    }
    return $result
}

function Copy-Hashtable {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$InputObject
    )

    $copy = @{}
    foreach ($key in $InputObject.Keys) {
        $value = $InputObject[$key]
        if ($value -is [hashtable]) {
            $copy[$key] = Copy-Hashtable -InputObject $value
        }
        elseif ($value -is [System.Collections.IList] -and -not ($value -is [string])) {
            $arr = @()
            foreach ($item in $value) {
                if ($item -is [hashtable]) {
                    $arr += ,(Copy-Hashtable -InputObject $item)
                }
                else {
                    $arr += ,$item
                }
            }
            $copy[$key] = $arr
        }
        else {
            $copy[$key] = $value
        }
    }
    return $copy
}

function Merge-Hashtable {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Base,
        [Parameter(Mandatory = $true)]
        [hashtable]$Override
    )

    foreach ($key in $Override.Keys) {
        if ($Base.ContainsKey($key) -and $Base[$key] -is [hashtable] -and $Override[$key] -is [hashtable]) {
            Merge-Hashtable -Base $Base[$key] -Override $Override[$key]
            continue
        }
        $Base[$key] = $Override[$key]
    }
}

function ConvertTo-PlainTextFromSecureString {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$SecureString
    )

    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

function Protect-StudyBookSecretContent {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PlainText,
        [Parameter(Mandatory = $true)]
        [string]$OutputEncryptedPath,
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$Passphrase
    )

    if ([string]::IsNullOrWhiteSpace($PlainText)) {
        throw "Secret content cannot be empty."
    }

    $passphraseText = ConvertTo-PlainTextFromSecureString -SecureString $Passphrase
    $saltBytes = New-Object byte[] 16
    [System.Security.Cryptography.RandomNumberGenerator]::Fill($saltBytes)
    $ivBytes = New-Object byte[] 16
    [System.Security.Cryptography.RandomNumberGenerator]::Fill($ivBytes)

    $derive = New-Object System.Security.Cryptography.Rfc2898DeriveBytes($passphraseText, $saltBytes, 150000, [System.Security.Cryptography.HashAlgorithmName]::SHA256)
    $keyBytes = $derive.GetBytes(32)

    $aes = [System.Security.Cryptography.Aes]::Create()
    try {
        $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
        $aes.KeySize = 256
        $aes.Key = $keyBytes
        $aes.IV = $ivBytes

        $encryptor = $aes.CreateEncryptor()
        $plainBytes = [System.Text.Encoding]::UTF8.GetBytes($PlainText)
        $cipherBytes = $encryptor.TransformFinalBlock($plainBytes, 0, $plainBytes.Length)

        $payload = @{
            version = 1
            algorithm = "AES-256-CBC/PBKDF2-SHA256"
            iterations = 150000
            salt = [Convert]::ToBase64String($saltBytes)
            iv = [Convert]::ToBase64String($ivBytes)
            ciphertext = [Convert]::ToBase64String($cipherBytes)
        }

        $outDir = Split-Path -Path $OutputEncryptedPath -Parent
        if (-not [string]::IsNullOrWhiteSpace($outDir)) {
            New-Item -ItemType Directory -Path $outDir -Force | Out-Null
        }

        $json = $payload | ConvertTo-Json -Depth 8
        Set-Content -LiteralPath $OutputEncryptedPath -Value $json -Encoding UTF8
    }
    finally {
        if ($aes) {
            $aes.Dispose()
        }
    }
}

function ConvertTo-NestedHashtable {
    param(
        [Parameter(Mandatory = $false)]
        $InputObject
    )

    if ($null -eq $InputObject) {
        return $null
    }

    if ($InputObject -is [hashtable]) {
        $out = @{}
        foreach ($k in $InputObject.Keys) {
            $out[$k] = ConvertTo-NestedHashtable -InputObject $InputObject[$k]
        }
        return $out
    }

    if ($InputObject -is [System.Collections.IDictionary]) {
        $out = @{}
        foreach ($k in $InputObject.Keys) {
            $out[$k] = ConvertTo-NestedHashtable -InputObject $InputObject[$k]
        }
        return $out
    }

    if (($InputObject -is [System.Collections.IEnumerable]) -and -not ($InputObject -is [string])) {
        $arr = @()
        foreach ($item in $InputObject) {
            $arr += ,(ConvertTo-NestedHashtable -InputObject $item)
        }
        return $arr
    }

    if ($InputObject -is [psobject]) {
        $out = @{}
        foreach ($prop in $InputObject.PSObject.Properties) {
            $out[$prop.Name] = ConvertTo-NestedHashtable -InputObject $prop.Value
        }
        return $out
    }

    return $InputObject
}

function ConvertFrom-JsonToHashtable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Json
    )

    if ([string]::IsNullOrWhiteSpace($Json)) {
        return @{}
    }

    $convertCmd = Get-Command -Name ConvertFrom-Json -ErrorAction Stop
    if ($convertCmd.Parameters.ContainsKey("AsHashtable")) {
        return $Json | ConvertFrom-Json -AsHashtable
    }

    $obj = $Json | ConvertFrom-Json
    $converted = ConvertTo-NestedHashtable -InputObject $obj
    if ($null -eq $converted) {
        return @{}
    }
    if ($converted -isnot [hashtable]) {
        throw "Expected JSON object at root."
    }
    return $converted
}

function Protect-StudyBookSecretFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InputJsonPath,
        [Parameter(Mandatory = $true)]
        [string]$OutputEncryptedPath,
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$Passphrase
    )

    if (-not (Test-Path -LiteralPath $InputJsonPath)) {
        throw "Secrets input file not found: $InputJsonPath"
    }

    $plainText = Get-Content -LiteralPath $InputJsonPath -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($plainText)) {
        throw "Secrets input file is empty: $InputJsonPath"
    }

    Protect-StudyBookSecretContent -PlainText $plainText -OutputEncryptedPath $OutputEncryptedPath -Passphrase $Passphrase
}

function Unprotect-StudyBookSecretFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$EncryptedPath,
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$Passphrase
    )

    if (-not (Test-Path -LiteralPath $EncryptedPath)) {
        throw "Encrypted secret file not found: $EncryptedPath"
    }

    $raw = Get-Content -LiteralPath $EncryptedPath -Raw -Encoding UTF8
    $payload = ConvertFrom-JsonToHashtable -Json $raw

    $saltBytes = [Convert]::FromBase64String([string]$payload.salt)
    $ivBytes = [Convert]::FromBase64String([string]$payload.iv)
    $cipherBytes = [Convert]::FromBase64String([string]$payload.ciphertext)
    $iterations = [int]$payload.iterations

    $passphraseText = ConvertTo-PlainTextFromSecureString -SecureString $Passphrase
    $derive = New-Object System.Security.Cryptography.Rfc2898DeriveBytes($passphraseText, $saltBytes, $iterations, [System.Security.Cryptography.HashAlgorithmName]::SHA256)
    $keyBytes = $derive.GetBytes(32)

    $aes = [System.Security.Cryptography.Aes]::Create()
    try {
        $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
        $aes.KeySize = 256
        $aes.Key = $keyBytes
        $aes.IV = $ivBytes

        $decryptor = $aes.CreateDecryptor()
        $plainBytes = $decryptor.TransformFinalBlock($cipherBytes, 0, $cipherBytes.Length)
        return [System.Text.Encoding]::UTF8.GetString($plainBytes)
    }
    finally {
        if ($aes) {
            $aes.Dispose()
        }
    }
}

function Get-StudyBookSecretSeedPath {
    param(
        [string]$ProjectRoot
    )

    if (-not [string]::IsNullOrWhiteSpace($env:STUDYBOOK_SECRET_SEED_PATH)) {
        if (-not [string]::IsNullOrWhiteSpace($ProjectRoot)) {
            return Resolve-StudyBookPath -ProjectRoot $ProjectRoot -PathValue $env:STUDYBOOK_SECRET_SEED_PATH
        }
        return [System.IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($env:STUDYBOOK_SECRET_SEED_PATH))
    }

    if (-not [string]::IsNullOrWhiteSpace($ProjectRoot)) {
        return Join-Path -Path $ProjectRoot -ChildPath "config\secrets\.local\studybook.secret.seed.dpapi.json"
    }

    if (-not [string]::IsNullOrWhiteSpace($env:STUDYBOOK_ROOT)) {
        return Join-Path -Path $env:STUDYBOOK_ROOT -ChildPath "config\secrets\.local\studybook.secret.seed.dpapi.json"
    }

    return Join-Path -Path (Get-Location).Path -ChildPath "config\secrets\.local\studybook.secret.seed.dpapi.json"
}

function Protect-StudyBookSecretSeed {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$Passphrase,
        [Parameter(Mandatory = $true)]
        [string]$SeedPath
    )

    if (-not ([Type]::GetType("System.Security.Cryptography.ProtectedData", $false))) {
        try {
            Add-Type -AssemblyName "System.Security.Cryptography.ProtectedData" -ErrorAction Stop
        }
        catch {
            try {
                Add-Type -AssemblyName "System.Security" -ErrorAction Stop
            }
            catch {
                throw "DPAPI ProtectedData type is unavailable. Use Windows PowerShell 5.1 or ensure System.Security.Cryptography.ProtectedData is installed."
            }
        }
    }

    $passphraseText = ConvertTo-PlainTextFromSecureString -SecureString $Passphrase
    if ([string]::IsNullOrWhiteSpace($passphraseText)) {
        throw "Passphrase cannot be empty."
    }

    $plainBytes = [System.Text.Encoding]::UTF8.GetBytes($passphraseText)
    $entropy = [System.Text.Encoding]::UTF8.GetBytes("StudyBook.SecretSeed.v1")
    $cipherBytes = [System.Security.Cryptography.ProtectedData]::Protect(
        $plainBytes,
        $entropy,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )

    $payload = @{
        version = 1
        algorithm = "DPAPI-CurrentUser"
        created_utc = (Get-Date).ToUniversalTime().ToString("o")
        ciphertext = [Convert]::ToBase64String($cipherBytes)
    }

    $outDir = Split-Path -Path $SeedPath -Parent
    if (-not [string]::IsNullOrWhiteSpace($outDir)) {
        New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    }

    $json = $payload | ConvertTo-Json -Depth 4
    Set-Content -LiteralPath $SeedPath -Value $json -Encoding UTF8
}

function Unprotect-StudyBookSecretSeed {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SeedPath
    )

    if (-not ([Type]::GetType("System.Security.Cryptography.ProtectedData", $false))) {
        try {
            Add-Type -AssemblyName "System.Security.Cryptography.ProtectedData" -ErrorAction Stop
        }
        catch {
            try {
                Add-Type -AssemblyName "System.Security" -ErrorAction Stop
            }
            catch {
                Write-Warning "DPAPI ProtectedData type is unavailable. Use Windows PowerShell 5.1 or install System.Security.Cryptography.ProtectedData."
                return $null
            }
        }
    }

    if (-not (Test-Path -LiteralPath $SeedPath)) {
        return $null
    }

    try {
        $raw = Get-Content -LiteralPath $SeedPath -Raw -Encoding UTF8
        if ([string]::IsNullOrWhiteSpace($raw)) {
            return $null
        }

        $payload = ConvertFrom-JsonToHashtable -Json $raw
        if (-not $payload.ContainsKey("ciphertext")) {
            Write-Warning "Seed file exists but ciphertext is missing: $SeedPath"
            return $null
        }

        $cipherBytes = [Convert]::FromBase64String([string]$payload.ciphertext)
        $entropy = [System.Text.Encoding]::UTF8.GetBytes("StudyBook.SecretSeed.v1")
        $plainBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
            $cipherBytes,
            $entropy,
            [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        )

        $passphraseText = [System.Text.Encoding]::UTF8.GetString($plainBytes)
        if ([string]::IsNullOrWhiteSpace($passphraseText)) {
            return $null
        }

        return ConvertTo-SecureString -String $passphraseText -AsPlainText -Force
    }
    catch {
        Write-Warning "Could not decrypt StudyBook seed file at ${SeedPath}: $($_.Exception.Message)"
        return $null
    }
}

function Get-SecretPassphrase {
    param(
        [switch]$NonInteractive,
        [string]$ProjectRoot
    )

    if (-not [string]::IsNullOrWhiteSpace($env:STUDYBOOK_SECRET_PASSPHRASE)) {
        return ConvertTo-SecureString -String $env:STUDYBOOK_SECRET_PASSPHRASE -AsPlainText -Force
    }

    $seedPath = Get-StudyBookSecretSeedPath -ProjectRoot $ProjectRoot
    $seedPassphrase = Unprotect-StudyBookSecretSeed -SeedPath $seedPath
    if ($seedPassphrase) {
        return $seedPassphrase
    }

    if ($NonInteractive) {
        return $null
    }

    return Read-Host -AsSecureString "Enter STUDYBOOK secrets passphrase"
}
function Resolve-MachineConfigPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot,
        [Parameter(Mandatory = $true)]
        [string]$MachineName
    )

    $machineFolder = Join-Path -Path $ProjectRoot -ChildPath "config\machines"
    $candidates = @(
        (Join-Path -Path $machineFolder -ChildPath "$MachineName.psd1"),
        (Join-Path -Path $machineFolder -ChildPath "$($MachineName.ToLowerInvariant()).psd1"),
        (Join-Path -Path $machineFolder -ChildPath "$($MachineName.ToUpperInvariant()).psd1")
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }
    return $null
}

function Invoke-StudyBookEnvBootstrap {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot,
        [string]$MachineName,
        [switch]$SkipVenvActivation,
        [switch]$NonInteractive
    )

    $projectRootFull = [System.IO.Path]::GetFullPath($ProjectRoot)
    $defaultMachine = if (-not [string]::IsNullOrWhiteSpace($MachineName)) { $MachineName } elseif (-not [string]::IsNullOrWhiteSpace($env:STUDYBOOK_MACHINE)) { $env:STUDYBOOK_MACHINE } else { $env:COMPUTERNAME }
    $normalizedMachine = ConvertTo-NormalizedMachineName -Name $defaultMachine

    $baseConfigPath = Join-Path -Path $projectRootFull -ChildPath "config\env\base.psd1"
    if (-not (Test-Path -LiteralPath $baseConfigPath)) {
        throw "Base environment config not found: $baseConfigPath"
    }

    $baseConfig = Import-PowerShellDataFile -Path $baseConfigPath
    $mergedConfig = Copy-Hashtable -InputObject $baseConfig

    $machineConfigPath = Resolve-MachineConfigPath -ProjectRoot $projectRootFull -MachineName $normalizedMachine
    if ($machineConfigPath) {
        $machineConfig = Import-PowerShellDataFile -Path $machineConfigPath
        Merge-Hashtable -Base $mergedConfig -Override $machineConfig
    }

    $localMachineConfigPath = Join-Path -Path $projectRootFull -ChildPath "config\machines\$normalizedMachine.local.psd1"
    if (Test-Path -LiteralPath $localMachineConfigPath) {
        $localMachineConfig = Import-PowerShellDataFile -Path $localMachineConfigPath
        Merge-Hashtable -Base $mergedConfig -Override $localMachineConfig
    }

    $tokenMap = @{
        PROJECT_ROOT = $projectRootFull
        MACHINE = $normalizedMachine
        COMPUTERNAME = $env:COMPUTERNAME
        USERPROFILE = $env:USERPROFILE
    }

    [Environment]::SetEnvironmentVariable("STUDYBOOK_ROOT", $projectRootFull, "Process")
    [Environment]::SetEnvironmentVariable("STUDYBOOK_MACHINE", $normalizedMachine, "Process")

    if ($mergedConfig.ContainsKey("Environment")) {
        foreach ($key in $mergedConfig.Environment.Keys) {
            $rawValue = [string]$mergedConfig.Environment[$key]
            $expanded = Expand-TemplateString -Value $rawValue -Tokens $tokenMap
            [Environment]::SetEnvironmentVariable($key, $expanded, "Process")
        }
    }

    if ($mergedConfig.ContainsKey("Paths")) {
        foreach ($key in $mergedConfig.Paths.Keys) {
            $rawPath = [string]$mergedConfig.Paths[$key]
            $expandedPath = Expand-TemplateString -Value $rawPath -Tokens $tokenMap
            $fullPath = Resolve-StudyBookPath -ProjectRoot $projectRootFull -PathValue $expandedPath
            [Environment]::SetEnvironmentVariable($key, $fullPath, "Process")
        }
    }

    $venvPath = $null
    $activateScript = $null
    if ($mergedConfig.ContainsKey("Venv")) {
        if ($mergedConfig.Venv.ContainsKey("Path")) {
            $venvPathRaw = Expand-TemplateString -Value ([string]$mergedConfig.Venv.Path) -Tokens $tokenMap
            $venvPath = Resolve-StudyBookPath -ProjectRoot $projectRootFull -PathValue $venvPathRaw
            [Environment]::SetEnvironmentVariable("STUDYBOOK_VENV_PATH", $venvPath, "Process")
        }
        if ($venvPath -and $mergedConfig.Venv.ContainsKey("ActivateScript")) {
            $activateScript = Join-Path -Path $venvPath -ChildPath ([string]$mergedConfig.Venv.ActivateScript)
            [Environment]::SetEnvironmentVariable("STUDYBOOK_VENV_ACTIVATE", $activateScript, "Process")
        }
    }

    if (-not $SkipVenvActivation -and $activateScript) {
        if (-not (Test-Path -LiteralPath $activateScript)) {
            throw "Activation script not found at $activateScript"
        }
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
        . $activateScript
    }

    $passphrase = $null
    $secretsRequired = $false
    if ($mergedConfig.ContainsKey("Secrets")) {
        if ($mergedConfig.Secrets.ContainsKey("Required")) {
            $secretsRequired = [bool]$mergedConfig.Secrets.Required
        }

        if ($mergedConfig.Secrets.ContainsKey("Files")) {
            $secretFiles = @($mergedConfig.Secrets.Files)
            $existingSecretFiles = @()
            foreach ($secretFile in $secretFiles) {
                $expandedSecretPath = Expand-TemplateString -Value ([string]$secretFile) -Tokens $tokenMap
                $resolvedSecretPath = Resolve-StudyBookPath -ProjectRoot $projectRootFull -PathValue $expandedSecretPath
                if (Test-Path -LiteralPath $resolvedSecretPath) {
                    $existingSecretFiles += ,$resolvedSecretPath
                }
            }

            if ($existingSecretFiles.Count -gt 0) {
                $passphrase = Get-SecretPassphrase -NonInteractive:$NonInteractive -ProjectRoot $projectRootFull
                if (-not $passphrase) {
                    if ($secretsRequired) {
                        throw "Secrets are required but no passphrase was provided. Set STUDYBOOK_SECRET_PASSPHRASE or run interactively."
                    }
                    Write-Warning "Encrypted secrets exist but no passphrase is available. Skipping secret import."
                }
                else {
                    foreach ($secretPath in $existingSecretFiles) {
                        try {
                            $secretJson = Unprotect-StudyBookSecretFile -EncryptedPath $secretPath -Passphrase $passphrase
                            $secretData = ConvertFrom-JsonToHashtable -Json $secretJson
                            foreach ($secretKey in $secretData.Keys) {
                                [Environment]::SetEnvironmentVariable($secretKey, [string]$secretData[$secretKey], "Process")
                            }
                        }
                        catch {
                            $message = $_.Exception.Message
                            if ($message -match "Padding is invalid") {
                                $message = "Failed to decrypt $secretPath. This usually means the passphrase does not match the encrypted file or the file is corrupted."
                            }

                            if ($secretsRequired) {
                                throw $message
                            }

                            Write-Warning $message
                        }
                    }
                }
            }
        }
    }

    $pythonPath = $null
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $pythonPath = (Get-Command python).Source
    }
    if ($pythonPath) {
        [Environment]::SetEnvironmentVariable("STUDYBOOK_PYTHON", $pythonPath, "Process")
    }

    [PSCustomObject]@{
        ProjectRoot = $projectRootFull
        Machine = $normalizedMachine
        MachineConfigPath = $machineConfigPath
        VenvPath = $venvPath
        PythonPath = $pythonPath
        SecretsLoaded = [bool]($passphrase)
    }
}




