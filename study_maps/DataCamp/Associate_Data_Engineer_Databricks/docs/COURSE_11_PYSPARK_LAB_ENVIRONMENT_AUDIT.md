# Course 11 PySpark Lab Environment Audit

## Purpose
Diagnose and fix Lab 01 environment enough to run the first Course 11 PySpark lab.

## Commands Run
- `cd D:\Workarea\StudyBook`
- `.\env_setter.ps1`
- `python --version`
- `python -c "import sys; print(sys.executable)"`
- `python -c "import pyspark; print('pyspark ok', pyspark.__version__)"`
- `java -version`
- `echo $env:JAVA_HOME`
- `python -m pip install pyspark`
- `python -c "import pyspark; print('pyspark ok', pyspark.__version__)"`
- `C:\Users\shareuser\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install pyspark`
- `C:\Users\shareuser\AppData\Local\Python\pythoncore-3.14-64\python.exe -c "import pyspark; print('pyspark ok', pyspark.__version__)"`
- `cd ...\01_sparksession_dataframe_basics`
- `python lab_sparksession_dataframe_basics.py`
- `C:\Users\shareuser\AppData\Local\Python\pythoncore-3.14-64\python.exe lab_sparksession_dataframe_basics.py`

## Python Executable
- `C:\Users\shareuser\AppData\Local\Python\pythoncore-3.14-64\python.exe`

## Python Version
- `Python 3.14.3`

## PySpark Installed
- Yes (`pyspark 4.1.1` import succeeded)

## Java Available
- Yes (`java 1.8.0_481` seen)
- `JAVA_HOME` set to `C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot`

## Lab 01 Run Success
- No

## Remaining Issue
- SparkSession startup fails with:
  - `TypeError: Metaclasses with custom tp_new are not supported.`
- Failure occurs inside `google.protobuf` import path during PySpark startup on Python 3.14 runtime.
- `winutils.exe` warning is also present but not the terminal exception.

## Recommended Next Step
- Run labs with a supported Python runtime for current PySpark/dependency compatibility (for example Python 3.11 or 3.12) and then re-run Lab 01.
- Keep this pass limited to diagnosis; do not perform broad environment migration in this prompt.

## 2026-05-21 Stable Runtime Gate Check

- Python 3.14 avoided for SparkSession stability path: Yes
- Python 3.11/3.12 available: No
- Local venv created: No (blocked by missing Python 3.11/3.12)
- Planned venv path (not created): `D:\Workarea\StudyBook\.venvs\datacamp_pyspark`
- Runner created: No (deferred until required interpreter exists)
- Java by JAVA_HOME path: 17
- Java on PATH (`java -version`): 8
- Lab 01 success in required 3.11/3.12 venv: No (not runnable yet)

Remaining issue:
- Install Python 3.11 or 3.12, then proceed with venv + PySpark 4.1.1 + runner + Lab 01 rerun.

Recommended next step:
1. Install Python 3.12 (preferred) or 3.11.
2. Re-run this stabilization prompt from Task C onward.

## Resume Attempt After Python 3.12 Install Claim (2026-05-21)

- Python 3.12 detected: No
- py launcher inventory still shows only 3.14 and 3.13.11
- Local venv created: No
- venv path: `D:\Workarea\StudyBook\.venvs\datacamp_pyspark` (not created)
- PySpark import in venv: Not applicable (venv missing)
- Lab 01 success: No (blocked before rerun)

Remaining blocker:
- Python 3.12/3.11 is still not installed/registered with `py` on this machine.

Recommended next step:
- Install Python 3.12 (or 3.11) and verify with `py -0p`, then rerun from venv creation step.

## 2026-05-21 Resume After Correct Startup Path
- Startup command used correctly: `D:\Workarea\StudyBook\env_setter.ps1`
- Active Python after env setup: `C:\py_venv\proj_educate\Scripts\python.exe`
- Python version: `3.12.9`
- PySpark import: success (`3.5.3`)
- Java: success (`17.0.18` via JAVA_HOME Microsoft JDK 17)
- Lab runner updated to force Python 3.12 env and Java 17 session overrides.

### Lab 01 status
- Spark initializes, but execution fails during first action (`df.show`) with `SocketException: Connection reset` and Python-side WinError 10038 symptom.
- Lab 01 not yet passing end-to-end.

### Recommended next step
- Keep this env as baseline and run a focused Spark local runtime stability pass (Python worker/socket behavior, local Spark config, and Windows Hadoop compatibility checks) before Lab 02+.

## Docker Runner Section (2026-05-21)
- Preferred execution mode: existing Docker PySpark container (`sharkforce-pyspark-lab`).
- Container checks:
  - Python: `3.12.13`
  - PySpark: `3.5.4`
  - Java: `17.0.19`
- Container is running and healthy for Spark tooling.

### Blocker
- Full StudyBook root is not mounted into this container.
- Current mounted project root inside container corresponds to:
  `D:\Workarea\StudyBook\docker\sharkforce-pyspark-lab`
- Therefore Course 11 tutorial lab path is not accessible in-container yet.

### Minimal next command set
- Add mount for `D:/Workarea/StudyBook` to `/workspace/studybook` in compose/container run.
- Then run Lab 01 in-container:
  `docker exec sharkforce-pyspark-lab bash -lc "cd /workspace/studybook/tutorials/DataCamp/Associate_Data_Engineer_Databricks/course_11_intro_pyspark/01_sparksession_dataframe_basics && python lab_sparksession_dataframe_basics.py"`

## 2026-05-21 Docker Compose Mount Update + Lab 01 Verification
- Compose file checked at:
  `D:\Workarea\StudyBook\docker\sharkforce-pyspark-lab\docker-compose.yml`
- Volume mount present and used:
  `D:/Workarea/StudyBook:/workspace/studybook`
- Container update command:
  `docker compose up -d`
- Container status after update:
  `sharkforce-pyspark-lab` running

### Mount verification in container
- `/workspace/studybook` exists
- `/workspace/studybook/tutorials` exists
- `/workspace/studybook/study_maps` exists

### Runtime verification
- Python: `3.12.13`
- PySpark: `3.5.4`
- Java: `openjdk 17.0.19`

### Lab 01 Docker run
```bash
docker exec sharkforce-pyspark-lab bash -lc "cd /workspace/studybook/tutorials/DataCamp/Associate_Data_Engineer_Databricks/course_11_intro_pyspark/01_sparksession_dataframe_basics && python lab_sparksession_dataframe_basics.py"
```
- Result: PASS (`Row count: 4`).

## 2026-05-21 Canonical Runner Confirmation
- Docker is the canonical lab runner.
- Container: `sharkforce-pyspark-lab`.
- Mount: `/workspace/studybook` (host `D:/Workarea/StudyBook`).
- Runtime: PySpark `3.5.4`, Java `openjdk 17.0.19`.
- Labs 01-10 status: PASS in Docker.
