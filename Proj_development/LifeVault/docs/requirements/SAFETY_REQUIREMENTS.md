# SAFETY_REQUIREMENTS.md

- No delete by default.
- No move by default.
- No rename by default.
- No sync/upload by default.
- No real DB/backups/exports in Git.
- No real token/secret material in Git.
- Explicit approval gates for publish and cleanup workflows.
- Backup-before-risky-operation rule is mandatory.