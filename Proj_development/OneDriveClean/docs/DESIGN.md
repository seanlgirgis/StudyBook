# OneDriveClean v0.1 Design

Primary workflow:

source directory
  -> deterministic proposal generation
  -> human approval/edit
  -> onboarding pod (controlled copy)
  -> pod/profile/manifest metadata
  -> local SQLite indexing
  -> duplicate/review reports
  -> later approved copy to clean vault

`staging` remains available, but `onboarding\pods` is the preferred workflow.
