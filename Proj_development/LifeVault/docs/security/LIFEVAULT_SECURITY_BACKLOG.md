# LIFEVAULT_SECURITY_BACKLOG.md

## Purpose

Track deferred-but-required security phases while LifeVault proceeds with v0 local workflows.

## Current Decision

- Encryption is deferred for v0 delivery speed.
- Encryption is not removed from scope.
- v0 publish remains local/plaintext copy to local vault paths.
- Cloud/OneDrive publish should wait for encryption design completion.

## Deferred Security Backlog

1. Encryption/decryption architecture design for LifeVault artifacts.
2. rclone crypt evaluation for remote vault copies.
3. Cryptomator evaluation for operator-managed encrypted vault workflow.
4. Encrypted DB backup archives before any cloud synchronization.
5. Controlled `secure_view` workflow for temporary sensitive review access.
6. Policy: no decrypted sensitive files in `Downloads` or other unmanaged locations.
7. Explicit handling model for `sensitive` and `highly_sensitive` file publishing.
8. Metadata leakage risk assessment (filenames, paths, tags, reports, logs).
9. Key management and recovery planning:
   - key ownership
   - recovery escrow/backup
   - rotation process
   - loss scenarios

## Immediate v0 Guardrails

- No encryption implementation in current bite.
- No OneDrive upload/publish in UC_007 v0 design.
- No rclone calls in UC_007 v0 workflow.
- Sensitive/highly_sensitive files require explicit review and approval gates.
