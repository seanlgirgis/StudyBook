@echo off
set "PYW=%~dp0.venv\Scripts\pythonw.exe"
if exist "%PYW%" (
    start /b "" "%PYW%" "%~dp0clipboard_app.py"
) else (
    start /b "" pythonw "%~dp0clipboard_app.py"
)
