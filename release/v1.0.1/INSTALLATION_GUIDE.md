# Installation Guide - AI Gospel Parser v1.0.1

This guide provides detailed installation instructions for all platforms.

---

## Quick Start (Choose Your Platform)

| Platform | Time | Difficulty | Download |
|----------|------|------------|----------|
| **Windows** | 10-15 min | ⭐ Easy | [Download](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.1/AI-Gospel-Parser-Windows-Installer-1.0.1.tar.gz) |
| **macOS** | 10-15 min | ⭐ Easy | [Download](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.1/AI-Gospel-Parser-macOS-Installer-1.0.1.tar.gz) |
| **Linux** | 10-15 min | ⭐ Easy | [Download](https://github.com/Amazingninjas/ai_gospel_parser/releases/download/v1.0.1/AI-Gospel-Parser-Linux-Installer-1.0.1.tar.gz) |

---

## 🪟 Windows Installation

### System Requirements
- Windows 10 (64-bit) or Windows 11
- 8GB RAM (16GB recommended)
- 10GB free disk space
- Internet connection

### Step-by-Step Instructions

1. **Download the installer**
   - Click the download link above
   - Save to your Downloads folder
   - Size: 3.1 KB

2. **Extract the archive**
   - Right-click the downloaded `.tar.gz` file
   - Select "Extract All..."
   - Choose a location (Desktop or Downloads)
   - You should see these files:
     - `AI-Gospel-Parser-Installer.vbs`
     - `install-windows.ps1`
     - `launch.bat`
     - `stop.bat`

3. **Run the installer**
   - **Double-click** `AI-Gospel-Parser-Installer.vbs`
   - Windows may show "Open File - Security Warning" → Click "Open"
   - UAC prompt appears: "Do you want to allow this app to make changes?" → Click **"Yes"**

4. **Wait for installation**
   - PowerShell window opens automatically
   - Installer checks for Docker Desktop
   - If Docker is not installed:
     - Installer asks: "Would you like to open the Docker download page?"
     - Click "Yes" to download Docker Desktop
     - Install Docker Desktop and restart your computer
     - Run the installer again after restart
   - Installer checks for Git
   - If Git is not installed, it will install automatically via winget
   - Installer clones the AI Gospel Parser repository
   - Installer starts Docker containers (first time takes 5-10 minutes)

5. **Application launches**
   - Browser opens automatically to http://localhost:3000
   - You see the AI Gospel Parser login screen
   - Click "Register" to create an account

6. **Quick launch (after first install)**
   - Double-click `launch.bat` to start the application anytime
   - Double-click `stop.bat` to stop the application

### Troubleshooting Windows

**Problem:** "Windows protected your PC"
- **Solution:** Click "More info" → "Run anyway"

**Problem:** PowerShell window closes immediately
- **Solution:** Docker Desktop must be running. Check system tray for Docker whale icon.

**Problem:** Port 3000 or 8000 already in use
- **Solution:** Stop other applications using those ports, or edit `docker-compose.yml` to use different ports

**Problem:** Installation hangs
- **Solution:** Check your antivirus isn't blocking Docker or PowerShell. Add exceptions if needed.

---

## 🍎 macOS Installation

### System Requirements
- macOS 10.13 (High Sierra) or later
- 8GB RAM (16GB recommended)
- 10GB free disk space
- Internet connection

### Step-by-Step Instructions

1. **Download the installer**
   - Click the download link above
   - Save to your Downloads folder
   - Size: 2.9 KB

2. **Extract the archive**
   - Double-click the downloaded `.tar.gz` file
   - macOS extracts it automatically
   - You should see: `AI Gospel Parser Installer.app`

3. **Run the installer**
   - **Double-click** `AI Gospel Parser Installer.app`
   - If macOS shows "unidentified developer" warning:
     - Right-click the app → Select "Open"
     - Click "Open" in the confirmation dialog
     - Or run: `xattr -cr "AI Gospel Parser Installer.app"`
   - Welcome dialog appears → Click **"Install"**

4. **Enter your password**
   - macOS password dialog appears
   - This is a standard macOS security prompt
   - Enter your Mac password → Click **"OK"**

5. **Wait for installation**
   - Terminal may open briefly (this is normal)
   - Installer checks for Docker Desktop
   - If Docker is not installed:
     - Installer opens Docker download page
     - Download and install Docker Desktop for Mac
     - Restart the installer after Docker installation
   - Installer checks for Git
   - If Git is not installed, it installs automatically
   - Installer clones the AI Gospel Parser repository
   - Installer starts Docker containers (first time takes 5-10 minutes)

6. **Application launches**
   - Success dialog appears
   - Browser opens automatically to http://localhost:3000
   - You see the AI Gospel Parser login screen
   - Click "Register" to create an account

### Troubleshooting macOS

**Problem:** "App is damaged and can't be opened"
- **Solution:** This is Gatekeeper blocking unsigned apps
  ```bash
  xattr -cr "/Applications/AI Gospel Parser Installer.app"
  ```
  Then try opening again.

**Problem:** Installation fails
- **Solution:** Check `/tmp/aigospel-install.log` for error messages
  ```bash
  open /tmp/aigospel-install.log
  ```

**Problem:** Docker Desktop won't start
- **Solution:** Make sure your Mac meets Docker's requirements. Check System Preferences → Security & Privacy for blocked applications.

**Problem:** Port 3000 or 8000 already in use
- **Solution:**
  ```bash
  lsof -ti:3000 -ti:8000 | xargs kill
  ```
  Or edit `docker-compose.yml` to use different ports.

---

## 🐧 Linux Installation

### System Requirements
- Ubuntu 18.04+, Debian 10+, Fedora 32+, or any recent Linux distribution
- 8GB RAM (16GB recommended)
- 10GB free disk space
- Internet connection

### Step-by-Step Instructions

1. **Download the installer**
   - Click the download link above
   - Save to your Downloads folder
   - Size: 3.2 KB

2. **Extract the archive**
   ```bash
   cd ~/Downloads
   tar -xzf AI-Gospel-Parser-Linux-Installer-1.0.1.tar.gz
   cd AI-Gospel-Parser-Linux-Installer
   ```

   You should see these files:
   - `ai-gospel-parser-installer.desktop`
   - `install-wrapper.sh`
   - `install-linux.sh`

3. **Make the desktop file executable**

   **Option A: Using File Manager (Easiest)**
   - Right-click `ai-gospel-parser-installer.desktop`
   - Select "Properties"
   - Go to "Permissions" tab
   - Check "Allow executing file as program" or "Executable"
   - Click "OK"

   **Option B: Using Terminal**
   ```bash
   chmod +x ai-gospel-parser-installer.desktop
   ```

4. **Run the installer**
   - **Double-click** `ai-gospel-parser-installer.desktop`
   - Terminal window opens
   - Installer shows welcome message → Type `y` and press Enter
   - Password prompt appears (PolicyKit graphical dialog or sudo in terminal)
   - Enter your password

5. **Wait for installation**
   - Installer checks for Docker Engine
   - If Docker is not installed:
     - Installer installs Docker automatically (Ubuntu/Debian/Fedora/Arch)
     - Adds your user to `docker` group
   - Installer checks for Git
   - If Git is not installed, it installs automatically
   - Installer clones the AI Gospel Parser repository
   - Installer starts Docker containers (first time takes 5-10 minutes)

6. **Application launches**
   - Terminal shows "Installation Complete!"
   - Browser opens automatically to http://localhost:3000
   - You see the AI Gospel Parser login screen
   - Click "Register" to create an account

### Troubleshooting Linux

**Problem:** "Permission denied" when running desktop file
- **Solution:**
  ```bash
  chmod +x ai-gospel-parser-installer.desktop
  chmod +x install-wrapper.sh
  chmod +x install-linux.sh
  ```

**Problem:** pkexec not found
- **Solution:** Install PolicyKit
  ```bash
  # Ubuntu/Debian
  sudo apt install policykit-1

  # Fedora
  sudo dnf install polkit

  # Arch
  sudo pacman -S polkit
  ```

**Problem:** Docker permission denied
- **Solution:** Log out and log back in after installation, or run:
  ```bash
  newgrp docker
  ```

**Problem:** Port 3000 or 8000 already in use
- **Solution:**
  ```bash
  sudo lsof -ti:3000 -ti:8000 | xargs sudo kill
  ```
  Or edit `docker-compose.yml` to use different ports.

**Problem:** Docker won't start
- **Solution:**
  ```bash
  sudo systemctl start docker
  sudo systemctl enable docker
  ```

---

## 🐳 Docker Desktop / Docker Engine

All installations require Docker. The installers will install it automatically, but here's what to expect:

### Windows & macOS (Docker Desktop)
- **Size:** ~500 MB download
- **Installation time:** 5-10 minutes
- **Restart required:** Yes (Windows may require restart)
- **Resource usage:** 2GB RAM minimum (configurable)

### Linux (Docker Engine)
- **Size:** ~100-200 MB
- **Installation time:** 2-5 minutes
- **Restart required:** No (but logout/login needed for group permissions)
- **Resource usage:** Minimal overhead

---

## 📊 First Launch Checklist

After installation completes:

- [ ] Browser opens to http://localhost:3000
- [ ] AI Gospel Parser login screen is visible
- [ ] Click "Register" and create an account
- [ ] Try searching for a verse (e.g., "John 3:16")
- [ ] Click a Greek word to see lexicon entry
- [ ] Try asking AI a question about the verse

If any of these fail, see Troubleshooting section for your platform.

---

## 🔄 Updating AI Gospel Parser

When a new version is released:

1. Stop the current application
   - Windows: Run `stop.bat`
   - macOS/Linux: `docker-compose down`

2. Pull latest changes:
   ```bash
   cd ~/Documents/ai_gospel_parser  # or your installation directory
   git pull origin main
   ```

3. Restart:
   - Windows: Run `launch.bat`
   - macOS/Linux: `docker-compose up -d`

---

## 🗑️ Uninstalling

### Windows
1. Stop the application: Run `stop.bat`
2. Delete installation directory (usually `C:\Users\YourName\Documents\ai_gospel_parser`)
3. (Optional) Uninstall Docker Desktop from Windows Settings

### macOS
1. Stop the application: `docker-compose down`
2. Delete installation directory: `rm -rf ~/Documents/ai_gospel_parser`
3. (Optional) Uninstall Docker Desktop by dragging to Trash

### Linux
1. Stop the application: `docker-compose down`
2. Delete installation directory: `rm -rf ~/Documents/ai_gospel_parser`
3. (Optional) Uninstall Docker:
   ```bash
   # Ubuntu/Debian
   sudo apt remove docker-ce docker-ce-cli containerd.io

   # Fedora
   sudo dnf remove docker-ce docker-ce-cli containerd.io

   # Arch
   sudo pacman -R docker docker-compose
   ```

---

## 🆘 Getting Help

If you're stuck:

1. **Check the logs:**
   - Windows: PowerShell output window
   - macOS: `/tmp/aigospel-install.log`
   - Linux: Terminal output

2. **Check Docker:**
   ```bash
   docker-compose logs
   ```

3. **Search existing issues:**
   - https://github.com/Amazingninjas/ai_gospel_parser/issues

4. **Create a new issue:**
   - Include your OS and version
   - Include error messages
   - Include installation log if available

5. **Join discussions:**
   - https://github.com/Amazingninjas/ai_gospel_parser/discussions

---

## 🎉 Success!

Once installed, AI Gospel Parser provides:

- 13,551 Greek NT verses with instant English translation
- 5,624 Strong's lexicon entries with morphology
- Real-time AI assistance for Bible study
- Conversation history saved automatically
- Mobile-friendly responsive design

**Happy studying!** 📖 α β γ δ ε

---

**Need more help?** Visit the [full documentation](https://github.com/Amazingninjas/ai_gospel_parser#readme)
