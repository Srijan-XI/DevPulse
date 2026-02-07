@echo off
REM ============================================================
REM DevPulse Launcher
REM ============================================================
REM Interactive launcher for DevPulse CLI and GUI
REM ============================================================

:MENU
cls
echo.
echo ============================================================
echo DevPulse - Project Health Checker
echo ============================================================
echo.
echo Please select an option:
echo.
echo   1. Launch GUI (Graphical Interface)
echo   2. Scan Current Directory (CLI)
echo   3. Scan Specific Directory (CLI)
echo   4. Fix Issues in Current Directory (CLI)
echo   5. Show Help
echo   6. Exit
echo.
echo ============================================================
echo.

set /p CHOICE="Enter your choice (1-6): "

if "%CHOICE%"=="1" goto GUI
if "%CHOICE%"=="2" goto SCAN_CURRENT
if "%CHOICE%"=="3" goto SCAN_CUSTOM
if "%CHOICE%"=="4" goto FIX
if "%CHOICE%"=="5" goto HELP
if "%CHOICE%"=="6" goto EXIT

echo.
echo [ERROR] Invalid choice. Please enter a number between 1 and 6.
echo.
pause
goto MENU

:GUI
cls
echo.
echo ============================================================
echo Launching DevPulse GUI...
echo ============================================================
echo.
python devpulse_gui.py
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to launch GUI
    echo Make sure Python is installed and in PATH
    echo.
    pause
)
goto MENU

:SCAN_CURRENT
cls
echo.
echo ============================================================
echo Scanning Current Directory...
echo ============================================================
echo.
python devpulse.py scan
echo.
echo ============================================================
echo Scan Complete!
echo ============================================================
echo.
pause
goto MENU

:SCAN_CUSTOM
cls
echo.
echo ============================================================
echo Scan Specific Directory
echo ============================================================
echo.
set /p SCAN_PATH="Enter the path to scan (or press Enter to cancel): "

if "%SCAN_PATH%"=="" (
    echo [INFO] Cancelled
    pause
    goto MENU
)

echo.
echo [INFO] Scanning: %SCAN_PATH%
echo.
python devpulse.py scan --path "%SCAN_PATH%"
echo.
echo ============================================================
echo Scan Complete!
echo ============================================================
echo.
pause
goto MENU

:FIX
cls
echo.
echo ============================================================
echo Fix Issues in Current Directory
echo ============================================================
echo.
echo This will apply safe fixes (generate missing README, LICENSE, .gitignore)
echo.
set /p CONFIRM="Continue? (y/N): "

if /i not "%CONFIRM%"=="y" (
    echo [INFO] Cancelled
    pause
    goto MENU
)

echo.
echo [INFO] Applying safe fixes...
echo.
python devpulse.py fix --safe
echo.
echo ============================================================
echo Fix Complete!
echo ============================================================
echo.
pause
goto MENU

:HELP
cls
echo.
echo ============================================================
echo DevPulse Help
echo ============================================================
echo.
echo DevPulse is a local-first development project health checker
echo that scans your codebase to detect tech stack, check hygiene,
echo find security issues, and suggest improvements.
echo.
echo ============================================================
echo Features:
echo ============================================================
echo   - Tech Stack Detection (Node.js, Python, Docker, etc.)
echo   - Repository Hygiene Checks (README, LICENSE, .gitignore)
echo   - Security Scanning (potential secrets, .env files)
echo   - File Size Analysis (large files detection)
echo   - Auto-Fix Capabilities (safe, non-destructive)
echo.
echo ============================================================
echo Command-Line Usage:
echo ============================================================
echo   Scan current directory:
echo     python devpulse.py scan
echo.
echo   Scan specific directory:
echo     python devpulse.py scan --path C:\my\project
echo.
echo   Output as JSON:
echo     python devpulse.py scan --json
echo.
echo   Apply safe fixes:
echo     python devpulse.py fix --safe
echo.
echo   Interactive fixes:
echo     python devpulse.py fix --interactive
echo.
echo ============================================================
echo For more information, see README.md
echo ============================================================
echo.
pause
goto MENU

:EXIT
cls
echo.
echo Thank you for using DevPulse!
echo.
exit /b 0
