# ============================================================================
# AI Gospel Parser - Post-Installation Script
# ============================================================================
# This script runs after the Inno Setup installer completes
# It checks for Docker and guides the user through setup
# ============================================================================

$ErrorActionPreference = "Continue"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  AI GOSPEL PARSER - SETUP" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Get installation directory
$installPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "[INFO] Installation directory: $installPath" -ForegroundColor Gray
Write-Host ""

# Check if Docker is installed and running
Write-Host "[1/4] Checking Docker Desktop..." -ForegroundColor Yellow

try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Docker is installed: $dockerVersion" -ForegroundColor Green

        # Check if Docker is running
        docker info 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Docker is running" -ForegroundColor Green
        } else {
            Write-Host "  [ERROR] Docker is not running" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
            Write-Host "You should see the Docker whale icon in your system tray." -ForegroundColor Yellow
            Write-Host ""
            Write-Host "After Docker starts, run: launch.bat" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "Press any key to exit..."
            $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
            exit 1
        }
    } else {
        throw "Docker not found"
    }
} catch {
    Write-Host "  [ERROR] Docker Desktop is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "AI Gospel Parser requires Docker Desktop to run." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Cyan
    Write-Host "  1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor White
    Write-Host "  2. Install Docker Desktop" -ForegroundColor White
    Write-Host "  3. Restart your computer" -ForegroundColor White
    Write-Host "  4. Run 'AI Gospel Parser' from the Start Menu" -ForegroundColor White
    Write-Host ""

    $response = Read-Host "Open Docker Desktop download page now? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        Start-Process "https://www.docker.com/products/docker-desktop"
    }

    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""

# Check if we need to clone the repository
Write-Host "[2/4] Checking application files..." -ForegroundColor Yellow

$repoPath = "$env:USERPROFILE\Documents\ai_gospel_parser"

if (Test-Path $repoPath) {
    Write-Host "  [OK] Repository already exists at: $repoPath" -ForegroundColor Green
    Write-Host "  Updating..." -ForegroundColor Cyan

    Set-Location $repoPath
    git pull origin main 2>&1 | Out-Null

    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ! Could not update (continuing anyway)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  Cloning repository..." -ForegroundColor Cyan

    # Check if git is installed
    try {
        git --version 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Git not found"
        }
    } catch {
        Write-Host "  [ERROR] Git is not installed" -ForegroundColor Red
        Write-Host ""
        Write-Host "Installing Git..." -ForegroundColor Yellow

        # Try to install via winget
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements

            # Refresh PATH
            $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
        } else {
            Write-Host "  [ERROR] Could not install Git automatically" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please install Git manually:" -ForegroundColor Yellow
            Write-Host "  https://git-scm.com/download/win" -ForegroundColor White
            Write-Host ""
            Write-Host "Press any key to exit..."
            $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
            exit 1
        }
    }

    Set-Location "$env:USERPROFILE\Documents"
    git clone https://github.com/Amazingninjas/ai_gospel_parser.git

    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [ERROR] Failed to clone repository" -ForegroundColor Red
        Write-Host ""
        Write-Host "Press any key to exit..."
        $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
        exit 1
    }

    Write-Host "  [OK] Repository cloned successfully" -ForegroundColor Green
}

Write-Host ""

# Start the application
Write-Host "[3/4] Starting AI Gospel Parser..." -ForegroundColor Yellow
Write-Host "  This may take 5-10 minutes on first run..." -ForegroundColor Cyan
Write-Host ""

Set-Location $repoPath

docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Application started successfully!" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Failed to start application" -ForegroundColor Red
    Write-Host ""
    Write-Host "Checking logs..." -ForegroundColor Yellow
    docker-compose logs
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""

# Open browser
Write-Host "[4/4] Opening browser..." -ForegroundColor Yellow
Write-Host ""

Start-Sleep -Seconds 3
Start-Process "http://localhost:3000"

Write-Host "============================================" -ForegroundColor Green
Write-Host "  INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Application URLs:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Installed to: $repoPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop:  docker-compose down" -ForegroundColor Yellow
Write-Host "To start: docker-compose up -d" -ForegroundColor Yellow
Write-Host ""
Write-Host "You can also use the Start Menu shortcuts!" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
