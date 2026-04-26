# AWS Access & Configuration Manual

This guide serves as the definitive manual for accessing AWS within the StudyBook environment. It explains how your machine is configured, how to run commands, and how our security and portability model works.

## 1. Quick Verification

To verify that your machine is currently authenticated and able to reach AWS, run the following command in PowerShell:

```powershell
aws sts get-caller-identity --profile study
```

**Expected Output:**
You should see a JSON response confirming your `UserId`, `Account` (e.g., `357811130281`), and `Arn` (e.g., `user/sean-study`).

## 2. The `study` Profile

Our canonical AWS profile for all local development and scripting in this repository is named **`study`**. 

When running AWS CLI commands or Python scripts, you should always explicitly reference this profile:
- **AWS CLI:** Append `--profile study` to your commands.
- **Python Scripts (Boto3):** Ensure your connection proofs and scripts specify the `study` profile. We have built-in resolution logic in scripts like `aws_connection_proof.py` to default to this profile.

There is also a `[girgisinv]` profile on this machine, but `[study]` is the designated identity for our cloud learning and infrastructure.

## 3. How Credentials Are Stored (Local vs. Repo)

Your active, plaintext credentials live strictly in your user folder:
* `C:\Users\shareuser\.aws\config`
* `C:\Users\shareuser\.aws\credentials`

**Important Safety Rule:** We *never* commit plaintext AWS keys, `.env` files with keys, or hardcoded credentials into the Git repository.

## 4. Portability: Moving to a New Machine

Because StudyBook is designed to be a reproducible environment, we have a workflow to seamlessly move your AWS access to a new laptop without needing to manually copy plaintext keys.

### Step A: The Encrypted Backup
Your `.aws` credentials have been securely packaged into an encrypted bundle located at:
`D:\StudyBook\config\secrets\aws.profiles.secrets.enc.json`

*(This was done using the `.\scripts\env\package_aws_credentials.ps1` script).*

### Step B: Restoring on a New Machine
If you switch to a new laptop, you can immediately restore your AWS access by doing the following:

1. Open PowerShell and navigate to `D:\StudyBook`.
2. Ensure your local DPAPI seed is registered (which holds your master passphrase).
3. Run the restore script:
   ```powershell
   .\scripts\env\restore_aws_credentials.ps1 -BackupExisting -NonInteractive
   ```
4. This script decrypts the bundle and safely writes it back into `~/.aws/credentials` on the new machine.

## 5. Technical References
For the deep dive on the exact operations, PowerShell scripts, and seed registration commands that power this setup, refer to the underlying architecture doc:
* [AWS Credentials Workflow](../operations/aws_credentials_workflow.md)
