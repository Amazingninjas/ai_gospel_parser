@echo off
REM ============================================================================
REM AI Gospel Parser - Stop Script
REM ============================================================================

echo ============================================================================
echo   AI GOSPEL PARSER - STOP
echo ============================================================================
echo.

REM Set the application directory to the user's Documents folder
set "APP_DIR=%USERPROFILE%\Documents\ai_gospel_parser"

REM Check if the application directory exists and change to it
if not exist "%APP_DIR%" (
    echo [!] Error: Application directory not found.
    echo     Searched in: %APP_DIR%
    echo.
    echo     Please ensure the program is installed correctly.
    echo.
    pause
    exit /b 1
)

cd /d "%APP_DIR%"

echo Stopping application...
docker-compose down

if %errorlevel% equ 0 (
    echo [OK] Application stopped successfully
) else (
    echo [!] Failed to stop application
    echo.
    echo Try running manually:
    echo   docker-compose down
)

echo.
pause
exit /b 0
