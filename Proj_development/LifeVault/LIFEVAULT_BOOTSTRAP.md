# LIFEVAULT_BOOTSTRAP.md

## Project Identity

- Active project name: `LifeVault`
- Deprecated name: `OneDriveClean`
- Mission: build a personal knowledge memory and file-governance system.

## Environment

- Project root: `D:\Workarea\StudyBook\Proj_development\LifeVault`
- Operational root: `D:\AI_Lab\LifeVault`
- Initialize Python/test environment from project root with:
  - `..\..\env_setter.ps1`

## Core Laws

- AI suggests; human approves.
- No delete by default.
- No move by default.
- No rename by default.
- Copy only during early phases.
- No rclone sync.
- No file enters the clean vault outside LifeVault.
- The database is the searchable map.
- The clean vault is the final file source of truth.
- Onboarding pods are controlled working copies.
- Real personal data stays outside Git.
- Secrets and rclone tokens must never be committed.
- Support search without hydrating all OneDrive files locally.