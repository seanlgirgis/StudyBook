Use ODC_folder_onboarding.

Source folder:
{{source_path}}

Story/context:
{{story}}

Steps:
1. Run deterministic intake proposal and show it.
2. Ask for human action: Accept/Edit/Save/Quit.
3. On approval, create onboarding pod.
4. Index pod metadata in SQLite.
5. Run duplicate detection report.
6. Stop before vault publish.

Safety:
- copy only
- no delete/move/rename
- no upload
- no sync
- metadata only
