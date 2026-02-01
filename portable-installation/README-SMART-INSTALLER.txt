AI GOSPEL PARSER - SMART ALL-IN-ONE INSTALLER
==============================================

WHAT ARE THESE?
===============
These smart installers automatically:
✓ Check if Docker is installed (install if needed)
✓ Check if Git is installed (install if needed)
✓ Clone the repository
✓ Start the application
✓ Open your browser to http://localhost:3000

NO COMMAND LINE KNOWLEDGE REQUIRED!

CHOOSE YOUR OPERATING SYSTEM:
==============================

┌─────────────────────────────────────────────────────┐
│  WINDOWS                                             │
│  Right-click: install-windows.ps1                   │
│  Select: "Run with PowerShell"                      │
│  (May need to "Run as Administrator")               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  macOS                                               │
│  Open Terminal (Cmd+Space, type "Terminal")        │
│  Drag install-macos.sh to Terminal window          │
│  Press Enter                                         │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  LINUX                                               │
│  Open Terminal                                       │
│  Navigate to this folder                            │
│  Run: bash install-linux.sh                         │
└─────────────────────────────────────────────────────┘

DETAILED INSTRUCTIONS:
======================

WINDOWS:
--------
1. Right-click on "install-windows.ps1"
2. Select "Run with PowerShell"
   (If you get a security warning, click "More info" then "Run anyway")
3. If prompted, click "Yes" to run as Administrator
4. Follow the on-screen prompts
5. Wait for installation (may take 10-15 minutes first time)
6. Browser will open automatically when ready!

ALTERNATE WINDOWS METHOD:
1. Press Windows key + X
2. Select "Windows PowerShell (Admin)"
3. Navigate to this folder:
   cd "C:\path\to\portable-installation"
4. Run:
   powershell -ExecutionPolicy Bypass -File install-windows.ps1

macOS:
------
1. Open Finder and navigate to this folder
2. Right-click on "install-macos.sh"
3. Select "Open With" → "Terminal"
   (Or drag the file into an open Terminal window)
4. Follow the on-screen prompts
5. Wait for installation (may take 10-15 minutes first time)
6. Browser will open automatically when ready!

LINUX:
------
1. Open Terminal (Ctrl+Alt+T)
2. Navigate to this folder:
   cd ~/Downloads/portable-installation
3. Run the installer:
   bash install-linux.sh
4. Follow the on-screen prompts
5. Enter your password when asked (for installing Docker/Git)
6. Wait for installation (may take 10-15 minutes first time)
7. Browser will open automatically when ready!

WHAT GETS INSTALLED:
====================
✓ Docker Desktop (if not already installed)
✓ Git (if not already installed)
✓ AI Gospel Parser application

WHERE IS IT INSTALLED:
======================
Windows: C:\Users\YourName\Documents\ai_gospel_parser
macOS:   /Users/YourName/Documents/ai_gospel_parser
Linux:   /home/yourname/ai_gospel_parser

AFTER INSTALLATION:
===================
The application runs at: http://localhost:3000

To STOP the app:
  cd to installation folder
  Run: docker-compose down

To START the app later:
  Windows: Run ~/Documents/ai_gospel_parser/setup.bat
  macOS:   Run ~/start-gospel-parser.sh
  Linux:   Run ~/start-gospel-parser.sh
  
  OR just run the smart installer again!

TROUBLESHOOTING:
================

"Execution Policy Error" (Windows):
  Right-click PowerShell → Run as Administrator
  Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  
"Docker is not running":
  Start Docker Desktop and wait for it to finish loading
  Look for the whale icon in system tray/menu bar
  
"Permission denied" (macOS/Linux):
  Make sure the script is executable:
  chmod +x install-macos.sh  (or install-linux.sh)
  
"Port already in use":
  Another app is using port 3000 or 8000
  Stop that app or change ports in docker-compose.yml

SYSTEM REQUIREMENTS:
====================
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space
- Internet connection (first install only)
- Windows 10/11, macOS 10.14+, or modern Linux

SUPPORT:
========
GitHub: https://github.com/Amazingninjas/ai_gospel_parser
Issues: https://github.com/Amazingninjas/ai_gospel_parser/issues

MANUAL INSTALLATION:
====================
If the smart installer doesn't work, see:
- INSTALL-WINDOWS.txt
- INSTALL-MACOS.txt  
- INSTALL-LINUX.txt
