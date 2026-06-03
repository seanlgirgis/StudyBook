# DataCamp Structure Inventory

Generated: 2026-06-03
Scope inspected: `D:\Workarea\StudyBook\study_maps\DataCamp`

## 1. Top-level files and folders under `study_maps\DataCamp`

### Folders
- `Associate_Data_Engineer_Databricks`
- `associate-data-analyst-in-sql`

### Files
- `DATA_CAMP_DECISIONS.md`
- `DATA_CAMP_PROGRESS_LOG.md`
- `DATA_CAMP_PROJECT_STATE.md`
- `DATA_CAMP_TASK_BOARD.md`
- `index.html`
- `README.md`

## 2. Track folders found

- `Associate_Data_Engineer_Databricks`
- `associate-data-analyst-in-sql`

## 3. Track `study_pages` course folders

### `Associate_Data_Engineer_Databricks`
- `study_pages\01_intro_sql`
- `study_pages\02_intermediate_sql`
- `study_pages\03_joining_data_in_sql`
- `study_pages\04_data_manipulation_in_sql`
- `study_pages\11_intro_pyspark`

### `associate-data-analyst-in-sql`
- `study_pages\03_project_analyzing_students_mental_health`
- `study_pages\05_postgresql_summary_stats_and_window_functions`
- `study_pages\06_functions_for_manipulating_data_in_postgresql`

## 4. Track `source_material` course folders

### `Associate_Data_Engineer_Databricks`
- `source_material\course_01_intro_sql`
- `source_material\course_02_intermediate_sql`
- `source_material\course_03_joining_data_in_sql`
- `source_material\course_04_data_manipulation_in_sql`
- `source_material\course_11_intro_pyspark`

### `associate-data-analyst-in-sql`
- `source_material\course_05_postgresql_summary_stats_and_window_functions`
- `source_material\course_06_functions_for_manipulating_data_in_postgresql`
- `source_material\project_03_analyzing_students_mental_health`

## 5. Existing `index.html` / `README` / `START_HERE` files found

### Root: `study_maps\DataCamp`
- `index.html`
- `README.md`

### `Associate_Data_Engineer_Databricks`
- Track root: `index.html`
- Track root: `README.md`
- `Course_01_Introduction_to_SQL\index.html`
- `Course_01_Introduction_to_SQL\README.md`
- `study_pages\02_intermediate_sql\index.html`
- `study_pages\03_joining_data_in_sql\index.html`
- `study_pages\04_data_manipulation_in_sql\index.html`
- `study_pages\11_intro_pyspark\index.html`
- `source_material\course_01_intro_sql\README.md`
- `source_material\course_02_intermediate_sql\README.md`
- `source_material\course_03_joining_data_in_sql\README.md`
- `source_material\course_04_data_manipulation_in_sql\README.md`
- `source_material\course_11_intro_pyspark\README.md`
- `projects\project_analyzing_students_mental_health\README.md`

### `associate-data-analyst-in-sql`
- `03_project_students_mental_health\README.md`
- `study_pages\05_postgresql_summary_stats_and_window_functions\README.md`
- `source_material\course_05_postgresql_summary_stats_and_window_functions\README.md`
- `source_material\course_06_functions_for_manipulating_data_in_postgresql\README.md`
- `source_material\project_03_analyzing_students_mental_health\README.md`

### `START_HERE`
- No `START_HERE` file was found under `study_maps\DataCamp`.

## 6. Navigation problems found

- Track naming is inconsistent: one track uses `Associate_Data_Engineer_Databricks` and the other uses `associate-data-analyst-in-sql`.
- Course folder naming is inconsistent across areas: examples include `Course_01_Introduction_to_SQL`, `01_intro_sql`, and `course_01_intro_sql` for the same course family.
- Project naming is inconsistent in the analyst track: `03_project_students_mental_health` vs `03_project_analyzing_students_mental_health` vs `project_03_analyzing_students_mental_health`.
- Some track roots are richer navigation hubs than others. `Associate_Data_Engineer_Databricks` has a track `index.html` and `README.md`, while `associate-data-analyst-in-sql` appears much thinner at the root.
- Not every `study_pages` course folder visibly has a matching `index.html` or `README`, which may make click-through navigation uneven.

## 7. Proposed landing page plan

- Keep the existing root `study_maps\DataCamp\index.html` as the main landing page for all DataCamp tracks.
- Add one standardized track landing page pattern per track root that links to:
  - track overview,
  - ordered `study_pages`,
  - matching `source_material`,
  - any projects,
  - progress/state files.
- Standardize display labels in landing pages even if underlying folder names remain unchanged.
- Add a simple crosswalk table on each landing page showing the relationship between `study_pages`, `source_material`, and project folders for each course.
- Reserve `START_HERE` only if a future onboarding layer is needed; otherwise keep `index.html` plus `README.md` as the primary navigation pair.
