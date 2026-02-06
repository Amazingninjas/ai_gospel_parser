# Installation Troubleshooting Guide

## Windows SmartScreen Warning

### "Windows protected your PC" Message

**This is expected and safe!** The installer is not digitally signed with a code signing certificate (costs $200+/year). This causes Windows to show warnings, but the software is safe.

#### How to Install on Windows 11:

1. **Download** the installer (.exe file) from GitHub releases
2. **Right-click** the .exe → **Properties**
3. At the bottom, check the box **"Unblock"** → Click **OK**
4. **Double-click** the .exe to run the installer
5. Click **"More info"** on the SmartScreen warning
6. Click **"Run anyway"**
7. Follow the installation wizard

#### How to Install on Windows 10:

Windows 10 is more aggressive with blocks. Try these steps:

**Method 1: Unblock the file**
1. **Right-click** the .exe → **Properties**
2. Check **"Unblock"** at the bottom → **OK**
3. **Right-click** the .exe → **Run as administrator**
4. If still blocked, try Method 2

**Method 2: Add to exclusions**
1. Open **Windows Security** (search in Start menu)
2. Go to **Virus & threat protection**
3. Click **Manage settings** under "Virus & threat protection settings"
4. Scroll down to **Exclusions**
5. Click **Add or remove exclusions**
6. Click **Add an exclusion** → **File**
7. Navigate to the downloaded .exe and select it
8. Now run the installer

**Method 3: Temporarily disable Real-time protection** (not recommended)
1. Open **Windows Security**
2. Go to **Virus & threat protection**
3. Click **Manage settings**
4. Turn off **Real-time protection** (temporary)
5. Install the software
6. Turn **Real-time protection** back on immediately

### Verify File Integrity (Optional but Recommended)

Before running the installer, you can verify it hasn't been tampered with:

**Windows PowerShell:**
```powershell
Get-FileHash AI-Gospel-Parser-Setup-1.0.1.exe -Algorithm SHA256
```

**Command Prompt:**
```cmd
certutil -hashfile AI-Gospel-Parser-Setup-1.0.1.exe SHA256
```

Compare the output with the checksum in `checksums.txt` or the GitHub release notes.

### Why Does Windows Show This Warning?

- The .exe is **not digitally signed** with an expensive code signing certificate
- Windows SmartScreen flags all unsigned executables as "potentially unsafe"
- This is a false positive - the software is open source and safe
- Digital code signing certificates cost $150-400 per year, which is prohibitive for small open-source projects

**Note:** We're working on getting a code signing certificate for future releases to eliminate these warnings.

## Docker Desktop Issues

### "Docker is not installed or not running"

**Solution:**
1. Install Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Restart your computer after installation
3. Wait for Docker Desktop to start (look for whale icon in system tray)
4. Run the installer again

### "WSL 2 installation is incomplete"

Docker Desktop requires WSL 2 (Windows Subsystem for Linux):

1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart your computer
4. Open Docker Desktop settings
5. Ensure "Use the WSL 2 based engine" is checked
6. Run the installer again

## Installation Issues

### "Application directory not found"

This means the Git clone failed during installation.

**Solution:**
1. Install Git from: https://git-scm.com/download/win
2. Restart your computer
3. Run the installer again

**Manual fix:**
1. Open PowerShell
2. Run:
   ```powershell
   cd $env:USERPROFILE\Documents
   git clone https://github.com/Amazingninjas/ai_gospel_parser.git
   ```
3. Click "AI Gospel Parser" from the Start Menu

### "Failed to start application"

**Check Docker is running:**
1. Look for Docker whale icon in system tray
2. Right-click → Check status shows "Docker Desktop is running"
3. If not running, start Docker Desktop

**Check Docker logs:**
```cmd
cd %USERPROFILE%\Documents\ai_gospel_parser
docker-compose logs
```

**Common issues:**
- Port 3000 or 8000 already in use by another application
- Docker out of memory (allocate more in Docker Desktop settings)
- Firewall blocking Docker

## Runtime Issues

### "Cannot connect to Ollama"

The AI features require Ollama to be running:

**Install Ollama:**
1. Download from: https://ollama.ai
2. Run `ollama serve` in a terminal
3. Run `ollama pull mixtral` to download the model
4. Restart the application

**Check Ollama is running:**
```cmd
curl http://localhost:11434/api/tags
```

### "Frontend won't load"

**Check containers are running:**
```cmd
docker ps
```

You should see two containers:
- `gospel-parser-frontend`
- `gospel-parser-backend`

**Restart containers:**
```cmd
cd %USERPROFILE%\Documents\ai_gospel_parser
docker-compose down
docker-compose up -d
```

### "AI chat not responding"

1. Verify Ollama is running: http://localhost:11434
2. Check backend logs:
   ```cmd
   docker-compose logs backend
   ```
3. Try restarting containers (see above)

## Browser Issues

### "localhost:3000 refused to connect"

**Wait for containers to start:**
- First-time startup takes 5-10 minutes
- Docker must download and build images

**Check status:**
```cmd
docker-compose ps
```

Both containers should show "Up" status.

### "Blank page or errors in browser"

1. **Clear browser cache:** Ctrl+Shift+Delete
2. **Hard refresh:** Ctrl+Shift+R (or Ctrl+F5)
3. **Try incognito/private mode**
4. **Try a different browser** (Chrome, Firefox, Edge)

## Uninstallation

### Clean uninstall:

1. **Stop containers:**
   - Start Menu → "Stop AI Gospel Parser"
   - Or run: `docker-compose down` in the application directory

2. **Uninstall program:**
   - Settings → Apps → AI Gospel Parser → Uninstall
   - Or: Control Panel → Programs → Uninstall AI Gospel Parser

3. **Remove data (optional):**
   ```cmd
   rmdir /s /q "%USERPROFILE%\Documents\ai_gospel_parser"
   ```

4. **Remove Docker images (optional):**
   ```cmd
   docker image rm aigospelparser-frontend aigospelparser-backend
   ```

## Still Having Issues?

1. **Check the logs:**
   - Docker: `docker-compose logs`
   - Installer: Look for `install_logs` directory

2. **Report an issue:**
   - GitHub: https://github.com/Amazingninjas/ai_gospel_parser/issues
   - Include:
     - Windows version (10 or 11)
     - Error messages
     - Steps you've tried
     - Relevant log files

3. **Ask for help:**
   - Open a GitHub discussion
   - Provide system information and error details

## System Requirements

**Minimum:**
- Windows 10 64-bit (version 1903+) or Windows 11
- 8 GB RAM
- 20 GB free disk space
- Docker Desktop installed
- Internet connection (for initial setup)

**Recommended:**
- Windows 11
- 16 GB RAM
- 50 GB free disk space
- SSD storage
- Fast internet connection

## FAQ

**Q: Is this software safe?**
A: Yes! It's open source. You can review all the code at: https://github.com/Amazingninjas/ai_gospel_parser

**Q: Why does Windows think it's a virus?**
A: The installer is not digitally signed (certificate costs $200+/year). Windows blocks all unsigned executables by default.

**Q: Can I trust this?**
A: Verify the file hash (see "Verify File Integrity" above), check the GitHub repository, and review the code if desired.

**Q: Will you get a code signing certificate?**
A: We're considering it for future releases if there's enough demand and usage.

**Q: Can I use a different AI provider besides Ollama?**
A: Yes! The application supports Google Gemini as an alternative. Configure in the `.env` file.

**Q: Do I need an internet connection?**
A: Only for initial setup. After installation, the app works offline (except for Gemini AI option).

**Q: How do I update to a new version?**
A: Download the new installer and run it. It will update the existing installation.
