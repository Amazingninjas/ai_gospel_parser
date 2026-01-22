@echo off
REM ============================================================================
REM AI Gospel Parser - Windows Bootstrap Installer
REM This script checks for Python and installs it automatically if needed
REM ============================================================================

echo ============================================================================
echo AI GOSPEL PARSER - WINDOWS INSTALLER
echo ============================================================================
echo.
echo This installer will:
echo  1. Check if Python is installed
echo  2. Install Python 3.12 if needed (automatic download)
echo  3. Run the main installation script
echo.
echo Press Ctrl+C to cancel, or
pause

REM Create logs directory
if not exist "install_logs" mkdir install_logs
set LOG_FILE=install_logs\bootstrap_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set LOG_FILE=%LOG_FILE: =0%

echo.
echo [1/4] Checking for Python installation...
echo [LOG] Checking for Python installation... >> "%LOG_FILE%" 2>&1

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is already installed!
    python --version
    python --version >> "%LOG_FILE%" 2>&1
    goto :run_installer
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is already installed via 'py' launcher!
    py --version
    py --version >> "%LOG_FILE%" 2>&1
    goto :run_installer_py
)

echo [!] Python is not installed.
echo.

REM Ask user permission to install Python
echo ============================================================================
echo PYTHON INSTALLATION REQUIRED
echo ============================================================================
echo.
echo Python 3.12 is required to run this application.
echo.
echo This installer can automatically download and install Python for you.
echo  - Download size: ~30 MB
echo  - Installation size: ~100 MB
echo  - Will install Python 3.12 (latest stable version)
echo  - Will add Python to your PATH automatically
echo.
set /p INSTALL_PYTHON="Would you like to install Python now? (Y/N): "

if /i "%INSTALL_PYTHON%" neq "Y" (
    echo.
    echo Installation cancelled. You can install Python manually from:
    echo   https://www.python.org/downloads/
    echo.
    echo After installing Python, run this installer again.
    pause
    exit /b 1
)

echo.
echo [2/4] Downloading Python 3.12...
echo [LOG] Downloading Python 3.12... >> "%LOG_FILE%" 2>&1

REM Download Python installer using PowerShell
set PYTHON_URL=https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
set PYTHON_INSTALLER=%TEMP%\python-3.12.0-amd64.exe

echo Downloading from: %PYTHON_URL%
echo Please wait...

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%' -UseBasicParsing}" >> "%LOG_FILE%" 2>&1

if %errorlevel% neq 0 (
    echo [ERROR] Failed to download Python installer.
    echo.
    echo Please install Python manually from: https://www.python.org/downloads/
    echo Then run this installer again.
    echo.
    echo Error details saved to: %LOG_FILE%
    pause
    exit /b 1
)

echo [OK] Python installer downloaded!
echo.

echo [3/4] Installing Python 3.12...
echo [LOG] Installing Python 3.12... >> "%LOG_FILE%" 2>&1
echo.
echo Please wait while Python is installed...
echo (This may take 2-3 minutes)
echo.

REM Install Python silently with all features
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1 Include_tcltk=1 >> "%LOG_FILE%" 2>&1

if %errorlevel% neq 0 (
    echo [ERROR] Python installation failed.
    echo.
    echo Please try installing Python manually from: https://www.python.org/downloads/
    echo.
    echo Error details saved to: %LOG_FILE%
    pause
    exit /b 1
)

echo [OK] Python installed successfully!
echo.

REM Clean up installer
del "%PYTHON_INSTALLER%" >nul 2>&1

REM Refresh PATH (restart cmd to pick up new PATH)
echo [INFO] Refreshing environment variables...
echo Please wait a moment for PATH to update...
timeout /t 3 /nobreak >nul

REM Check if Python is now available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Python was installed but PATH may not be updated yet.
    echo.
    echo Please close this window and run this installer again.
    echo (Python should be available after restarting the installer)
    echo.
    pause
    exit /b 1
)

echo [OK] Python is now available!
python --version
echo.

:run_installer
echo [4/4] Running AI Gospel Parser installer...
echo [LOG] Running install.py >> "%LOG_FILE%" 2>&1
echo.

REM Run the main installer
python install.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed. Check install_log.txt for details.
    echo Bootstrap log saved to: %LOG_FILE%
    pause
    exit /b 1
)

goto :success

:run_installer_py
echo [4/4] Running AI Gospel Parser installer...
echo [LOG] Running install.py with py launcher >> "%LOG_FILE%" 2>&1
echo.

REM Run the main installer with py launcher
py install.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed. Check install_log.txt for details.
    echo Bootstrap log saved to: %LOG_FILE%
    pause
    exit /b 1
)

:success
echo.
echo ============================================================================
echo INSTALLATION COMPLETE!
echo ============================================================================
echo.
echo Next steps:
echo  1. Read GETTING_STARTED.txt for usage instructions
echo  2. Look for the desktop shortcut: "AI Gospel Parser"
echo  3. Double-click the shortcut to launch
echo.
echo Bootstrap log saved to: %LOG_FILE%
echo.
pause
exit /b 0
