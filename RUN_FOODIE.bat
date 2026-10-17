@echo off
setlocal
cd /d "%~dp0"
title Foodie - Restaurant Demo

echo.
echo ===================================================
echo   FOODIE - RESTAURANT DISCOVERY DEMO
echo ===================================================
echo.
if not exist ".venv\Scripts\python.exe" (
  echo [1/5] Creating Python virtual environment...
  py -m venv .venv
  if errorlevel 1 goto :python_error
) else (echo [1/5] Python environment already exists.)

echo [2/5] Installing required packages...
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :install_error

echo [3/5] Creating/updating database migrations...
call ".venv\Scripts\python.exe" manage.py makemigrations restaurants
if errorlevel 1 goto :migration_error
call ".venv\Scripts\python.exe" manage.py migrate
if errorlevel 1 goto :migration_error

echo [4/5] Loading 65 demo restaurants and menu data...
call ".venv\Scripts\python.exe" manage.py seed_demo
if errorlevel 1 goto :seed_error

echo [5/5] Starting Foodie...
echo Website: http://127.0.0.1:8000/
echo Keep this window open while using the site. Press Ctrl+C to stop.
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:8000/"
call ".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
goto :eof

:python_error
echo Python was not found. Install Python 3.10+ from https://www.python.org/downloads/ and enable Add Python to PATH.
pause
exit /b 1
:install_error
echo Package installation failed. Check your internet connection and try again.
pause
exit /b 1
:migration_error
echo Database setup failed. Read the error above.
pause
exit /b 1
:seed_error
echo Demo data setup failed. Read the error above.
pause
exit /b 1
