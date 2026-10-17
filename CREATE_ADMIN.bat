@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo First run RUN_FOODIE.bat once.
 pause
 exit /b 1
)
".venv\Scripts\python.exe" manage.py createsuperuser
pause
