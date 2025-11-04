@echo off
REM Cataclysm: Bright Nights Dialogue Editor - Run Script (Windows)
SETLOCAL

:: Change to the directory where this script lives
cd /d "%~dp0"

echo.
echo Cataclysm: Bright Nights Dialogue Editor
echo =======================================
echo.

:: Check that python is available
where python >nul 2>&1
if ERRORLEVEL 1 (
  echo Error: python is not installed or not in PATH
  echo Please install Python 3.7 or higher
  exit /b 1
)

:: Check Python version (require >= 3.7)
for /f "delims=" %%v in ('python -c "import sys; v=sys.version_info; print('%d.%d' % (v[0], v[1]));\nif v[0]<3 or (v[0]==3 and v[1]<7): sys.exit(1)"') do set PYTHON_VERSION=%%v
if ERRORLEVEL 1 (
  echo Error: Python 3.7 or higher is required (found %PYTHON_VERSION%)
  exit /b 1
)

echo Python version: %PYTHON_VERSION%
echo.

set VENV_DIR=venv

:: Create virtual environment if missing
if not exist "%VENV_DIR%\Scripts\activate.bat" (
  echo Creating virtual environment...
  python -m venv "%VENV_DIR%"
  if ERRORLEVEL 1 (
    echo Failed to create virtual environment
    exit /b 1
  )
) else (
  echo Virtual environment already exists
)

echo.
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

:: Install requirements if present
if exist "requirements.txt" (
  echo Installing requirements...
  pip install -r requirements.txt
) else (
  echo No requirements.txt found (no external dependencies needed)
)

echo.
echo Checking for tkinter...
python -c "import tkinter" >nul 2>&1
if ERRORLEVEL 1 (
  echo Error: tkinter is not available
  echo Please ensure your Python installation includes tkinter (it is usually included on Windows).
  if exist "%VENV_DIR%\Scripts\deactivate.bat" call "%VENV_DIR%\Scripts\deactivate.bat" >nul 2>&1
  exit /b 1
) else (
  echo tkinter is available
)

echo.
echo Starting Dialogue Editor...
echo.

:: Run the application (unbuffered)
python -u main.py
set APP_EXIT=%ERRORLEVEL%

:: Deactivate virtualenv if possible
if exist "%VENV_DIR%\Scripts\deactivate.bat" (
  call "%VENV_DIR%\Scripts\deactivate.bat" >nul 2>&1
)

exit /b %APP_EXIT%
