@echo off
REM ============================================================================
REM AI Gospel Parser - Simple Windows Installer (Alternative to VBScript)
REM ============================================================================
REM This is a simpler alternative if the VBScript launcher doesn't work
REM Right-click and select "Run as Administrator"
REM ============================================================================

echo ============================================================================
echo   AI GOSPEL PARSER - WINDOWS INSTALLER
echo ============================================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] This script must be run as Administrator
    echo.
    echo Please:
    echo   1. Right-click this file
    echo   2. Select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo [INFO] Running with Administrator privileges
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if PowerShell script exists
if not exist "install-windows.ps1" (
    echo [ERROR] Could not find install-windows.ps1
    echo.
    echo Please make sure this file is in the same folder as:
    echo   install-windows.ps1
    echo.
    pause
    exit /b 1
)

echo [INFO] Found install-windows.ps1
echo [INFO] Starting PowerShell installer...
echo.

REM Run the PowerShell installer
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0install-windows.ps1"

REM Check exit code
if %errorlevel% equ 0 (
    echo.
    echo ============================================================================
    echo   INSTALLATION COMPLETE!
    echo ============================================================================
    echo.
) else (
    echo.
    echo ============================================================================
    echo   INSTALLATION FAILED
    echo ============================================================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause
exit /b %errorlevel%
