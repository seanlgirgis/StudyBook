# Operating Procedure

1. Open PowerShell in project root.
2. Run `..\..\env_setter.ps1`.
3. Run `./scripts/setup_lab_folders.ps1`.
4. Start intake using `./pod.ps1 <SourcePath>`.
5. Review proposal and choose A/E/S/Q.
6. If accepted, pod is created under `onboarding\pods`.
7. Index pod into SQLite with `scripts/index_onboarding_pod.ps1 -PodId <pod_id>`.
8. Run duplicate analysis with `scripts/detect_pod_duplicates.ps1 -PodId <pod_id>`.
9. Do not upload to OneDrive until explicit approval workflow is added.
10. Do not delete, move, or rename source files.
