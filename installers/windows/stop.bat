@echo off
REM ============================================================================
REM AI Gospel Parser - Stop Script
REM ============================================================================

echo ============================================================================
echo   AI GOSPEL PARSER - STOP
echo ============================================================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

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
