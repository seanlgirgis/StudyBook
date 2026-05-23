# Test Plan

- Tests use temporary folders only.
- Tests must not touch real OneDrive.
- Tests must not touch `D:\AI_Lab` unless a future integration test is explicitly added.
- Tests must not run rclone.
- Tests validate config loading, inventory generation, and report outputs.
