# Notes

Personal Vault is excluded from early phases.

Reason:
- rclone may fail listing Personal Vault (`invalidResourceId` / `ObjectHandle is Invalid`).
- Personal Vault is high-sensitivity storage and should be out of early automated inventory scope.

Implementation:
- Configure `excluded_remote_paths` in `config/rclone_remotes*.json`.
- Lab 04 applies those excludes to read-only `rclone about` and `rclone lsd` commands.

Full recursive dirty OneDrive inventory is intentionally not part of lab 04 because the dirty drive is large. Recursive inventory will become a later controlled lab with clear scope, filters, and progress logging.

