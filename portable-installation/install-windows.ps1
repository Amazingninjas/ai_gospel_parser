<#
.SYNOPSIS
    AI Gospel Parser - Smart Windows Installer
.DESCRIPTION
    Automatically installs Docker Desktop, Git, and sets up AI Gospel Parser
.NOTES
    Run with: powershell -ExecutionPolicy Bypass -File install-windows.ps1
#>

# Require Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This installer needs to run as Administrator." -ForegroundColor Red
    Write-Host "Please right-click and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   AI GOSPEL PARSER - SMART INSTALLER" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command($command) {
    try {
        if (Get-Command $command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

# Step 1: Check Docker
Write-Host "[1/5] Checking for Docker Desktop..." -ForegroundColor Yellow
if (Test-Command docker) {
    Write-Host "  ✓ Docker is already installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ Docker is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Docker Desktop needs to be installed manually." -ForegroundColor Yellow
    Write-Host "Please follow these steps:" -ForegroundColor Yellow
    Write-Host "  1. Visit: https://www.docker.com/products/docker-desktop" -ForegroundColor White
    Write-Host "  2. Download Docker Desktop for Windows" -ForegroundColor White
    Write-Host "  3. Install and restart your computer" -ForegroundColor White
    Write-Host "  4. Run this installer again" -ForegroundColor White
    Write-Host ""
    $openBrowser = Read-Host "Open Docker Desktop download page now? (Y/N)"
    if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
        Start-Process "https://www.docker.com/products/docker-desktop"
    }
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# Step 2: Check if Docker is running
Write-Host "[2/5] Checking if Docker is running..." -ForegroundColor Yellow
try {
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
    Write-Host "  ✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker is not running" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please start Docker Desktop and wait for it to finish starting." -ForegroundColor Yellow
    Write-Host "You should see the Docker whale icon in your system tray." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# Step 3: Check Git
Write-Host "[3/5] Checking for Git..." -ForegroundColor Yellow
if (Test-Command git) {
    Write-Host "  ✓ Git is already installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ Git is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing Git for Windows..." -ForegroundColor Yellow
    
    # Try to install using winget (Windows Package Manager)
    if (Test-Command winget) {
        Write-Host "  Installing via winget..." -ForegroundColor Cyan
        winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
        
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        if (Test-Command git) {
            Write-Host "  ✓ Git installed successfully" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Git installation failed" -ForegroundColor Red
            Write-Host "  Please install Git manually from: https://git-scm.com/download/win" -ForegroundColor Yellow
            Start-Process "https://git-scm.com/download/win"
            pause
            exit
        }
    } else {
        Write-Host "  Windows Package Manager (winget) not found." -ForegroundColor Yellow
        Write-Host "  Please install Git manually from: https://git-scm.com/download/win" -ForegroundColor Yellow
        Start-Process "https://git-scm.com/download/win"
        pause
        exit
    }
}

# Step 4: Clone repository
Write-Host "[4/5] Setting up AI Gospel Parser..." -ForegroundColor Yellow

$installPath = "$env:USERPROFILE\Documents\ai_gospel_parser"

if (Test-Path $installPath) {
    Write-Host "  Directory already exists. Updating..." -ForegroundColor Cyan
    Set-Location $installPath
    git pull origin main
} else {
    Write-Host "  Cloning repository..." -ForegroundColor Cyan
    Set-Location "$env:USERPROFILE\Documents"
    git clone https://github.com/Amazingninjas/ai_gospel_parser.git
    Set-Location $installPath
}

Write-Host "  ✓ Repository ready" -ForegroundColor Green

# Step 5: Start application
Write-Host "[5/5] Starting AI Gospel Parser..." -ForegroundColor Yellow
Write-Host "  This may take 5-10 minutes on first run..." -ForegroundColor Cyan
Write-Host ""

docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Application started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "   INSTALLATION COMPLETE!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Opening browser in 3 seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:3000"
    Write-Host ""
    Write-Host "Application URLs:" -ForegroundColor Cyan
    Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "  Backend:  http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "Installed to: $installPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To stop:  docker-compose down" -ForegroundColor Yellow
    Write-Host "To start: docker-compose up -d" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "  ✗ Failed to start application" -ForegroundColor Red
    Write-Host ""
    Write-Host "Checking logs..." -ForegroundColor Yellow
    docker-compose logs
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
