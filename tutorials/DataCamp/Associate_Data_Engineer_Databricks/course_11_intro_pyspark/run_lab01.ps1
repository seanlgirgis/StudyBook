$ErrorActionPreference = 'Stop'
$env:JAVA_HOME = 'C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot'
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
$pythonExe = 'C:\py_venv\proj_educate\Scripts\python.exe'
Write-Host "Python executable: $pythonExe"
& $pythonExe --version
& $pythonExe -c "import sys; print(sys.executable)"
Write-Host 'java -version:'
java -version
Write-Host 'JAVA_HOME java -version:'
& "$env:JAVA_HOME\bin\java.exe" -version
Set-Location 'D:\Workarea\StudyBook\tutorials\DataCamp\Associate_Data_Engineer_Databricks\course_11_intro_pyspark\01_sparksession_dataframe_basics'
& $pythonExe 'lab_sparksession_dataframe_basics.py'