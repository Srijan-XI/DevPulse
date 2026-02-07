@echo off
REM ============================================================
REM DevPulse Installation Script
REM ============================================================
REM This script checks Python installation and optionally
REM installs documentation requirements.
REM ============================================================

echo.
echo ============================================================
echo DevPulse Installation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Get Python version
echo [INFO] Checking Python version...
python --version
echo.

REM Check Python version (requires 3.10+)
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python 3.10 or higher is recommended
    echo Current version may not be compatible
    echo.
)

echo [SUCCESS] Python is installed and ready!
echo.

REM Main application has no dependencies
echo ============================================================
echo DevPulse Core Application
echo ============================================================
echo.
echo The core DevPulse application requires NO external dependencies!
echo It uses only Python standard library.
echo.
echo You can start using DevPulse right away with:
echo   - start.bat (interactive launcher)
echo   - python devpulse.py scan
echo   - python devpulse_gui.py
echo.

REM Ask about documentation requirements
echo ============================================================
echo Optional: Documentation Requirements
echo ============================================================
echo.
set /p INSTALL_DOCS="Do you want to install documentation tools (MkDocs)? (y/N): "

if /i "%INSTALL_DOCS%"=="y" (
    echo.
    echo [INFO] Installing documentation requirements...
    pip install -r requirements-docs.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install documentation requirements
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [SUCCESS] Documentation tools installed!
    echo You can now build docs with: mkdocs serve
    echo.
) else (
    echo.
    echo [INFO] Skipping documentation tools installation
    echo.
)

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Quick Start:
echo   1. Run "start.bat" for interactive launcher
echo   2. OR run "python devpulse.py scan" for CLI
echo   3. OR run "python devpulse_gui.py" for GUI
echo.
echo For more information, see README.md
echo.
pause
