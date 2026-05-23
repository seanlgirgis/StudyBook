# ODC Control Center (Streamlit)

`app/odc_control_center.py` is the first implemented ODC Control Center UI.

Purpose:
- project-native GUI for folder onboarding
- proposal -> human edits -> pod create -> index -> duplicate detect

Safety constraints enforced by workflow:
- no delete / move / rename
- no `rclone sync`
- no OneDrive upload
- no vault publishing
- no real text extraction yet

Run:
```powershell
.\scripts\run_control_center.ps1
```

Direct:
```powershell
streamlit run app\odc_control_center.py
```

Notes:
- App calls existing project scripts with safe subprocess usage.
- Real outputs remain under `D:\AI_Lab\OneDriveClean`, not in repo.
