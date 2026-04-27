@echo off
:: This batch file acts as a wrapper to launch the Clipboard Manager.
:: It now uses env_setter.ps1 to ensure the environment (venv and vars) is correctly set.

cd /d "%~dp0"
powershell -WindowStyle Hidden -ExecutionPolicy Bypass -Command "& { . .\env_setter.ps1; & .\run_app.bat }"
exit
