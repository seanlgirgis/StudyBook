# StudyBook Secrets & Passphrase Guide

The StudyBook environment relies on encrypted secrets to securely manage sensitive environment variables and API keys across multiple machines and directories without committing plaintext passwords to version control.

## How It Works

1. **Encrypted Secrets**: Sensitive configuration variables are stored in encrypted JSON files within the `config/secrets/` directory.
2. **The Master Passphrase**: To decrypt these secrets, a master passphrase is required.
3. **The Seed File (Salt)**: Rather than requiring you to type the master passphrase every time you start a new shell, StudyBook uses Windows DPAPI (Data Protection API) to securely encrypt and store your passphrase as a local "seed" file tied specifically to your Windows user account.

## Workflow

### 1. First Run (or Moving to a New Machine/Directory)
When you clone or copy the project to a new location (e.g., a new Workarea folder), the local seed file is typically excluded because it lives in the hidden `.local/` folder (`config/secrets/.local/studybook.secret.seed.dpapi.json`).

When you run `.\env_setter.ps1` for the first time in this new location:
- The script will pause and prompt you to enter the **STUDYBOOK secrets passphrase**.
- Once entered, the script attempts to decrypt your secret files.
- If successful, it automatically generates a new local seed file. 

### 2. Subsequent Runs
From that point on, whenever you open a new shell and run `.\env_setter.ps1`:
- The script automatically detects the local seed file.
- It uses Windows DPAPI to securely unprotect the seed and retrieve the master passphrase without prompting you.
- Your environment variables are loaded instantly.

## Troubleshooting

- **Forgot Passphrase?**: If the passphrase is forgotten and the local seed file is lost, the encrypted secrets cannot be recovered. Ensure you keep the master passphrase securely stored in a password manager.
- **"Padding is invalid" Error**: This usually means the passphrase entered is incorrect, or the encrypted file is corrupted.
- **Moving Across Machines**: You cannot copy the `.local` folder from one machine to another because DPAPI encryption is tied to the specific Windows user profile on that machine. You will simply be prompted to enter the passphrase once on the new machine to generate a new valid seed file.
