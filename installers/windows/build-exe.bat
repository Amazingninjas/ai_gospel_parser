@echo off
REM ============================================================================
REM Build AI Gospel Parser .exe Installer with Inno Setup
REM ============================================================================

echo ============================================================================
echo   Building AI Gospel Parser .exe Installer
echo ============================================================================
echo.

REM Check if Inno Setup is installed
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%INNO_PATH%" (
    echo [ERROR] Inno Setup not found at: %INNO_PATH%
    echo.
    echo Please install Inno Setup from:
    echo   https://jrsoftware.org/isinfo.php
    echo.
    pause
    exit /b 1
)

echo [1/3] Found Inno Setup
echo.

REM Check if installer.iss exists
if not exist "installer.iss" (
    echo [ERROR] installer.iss not found
    echo.
    echo Please run this script from the installers/windows directory
    echo.
    pause
    exit /b 1
)

echo [2/3] Found installer.iss
echo.

REM Create output directory
if not exist "output" mkdir output

REM Compile the installer
echo [3/3] Compiling installer...
echo.
"%INNO_PATH%" "installer.iss"

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   BUILD SUCCESSFUL!
    echo ============================================
    echo.
    echo Installer created:
    dir /b output\*.exe
    echo.
    echo Location: output\AI-Gospel-Parser-Setup-1.0.1.exe
    echo.
    echo You can now:
    echo   1. Test the installer locally
    echo   2. Upload to GitHub releases
    echo   3. Distribute to users
    echo.
) else (
    echo.
    echo ============================================
    echo   BUILD FAILED
    echo ============================================
    echo.
    echo Check the error messages above.
    echo.
)

pause
exit /b %errorlevel%
