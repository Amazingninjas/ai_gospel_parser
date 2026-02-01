#!/bin/bash
# AI Gospel Parser - Smart macOS Installer
# Run with: bash install-macos.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}   AI GOSPEL PARSER - SMART INSTALLER${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check Docker
echo -e "${YELLOW}[1/5] Checking for Docker Desktop...${NC}"
if command_exists docker; then
    echo -e "${GREEN}  ✓ Docker is already installed${NC}"
else
    echo -e "${RED}  ✗ Docker is not installed${NC}"
    echo ""
    echo -e "${YELLOW}Docker Desktop needs to be installed.${NC}"
    echo -e "${YELLOW}Opening Docker Desktop download page...${NC}"
    open "https://www.docker.com/products/docker-desktop"
    echo ""
    echo "Please:"
    echo "  1. Download Docker Desktop for Mac"
    echo "  2. Install it (drag to Applications folder)"
    echo "  3. Start Docker Desktop"
    echo "  4. Run this installer again"
    echo ""
    exit 1
fi

# Step 2: Check if Docker is running
echo -e "${YELLOW}[2/5] Checking if Docker is running...${NC}"
if docker info >/dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Docker is running${NC}"
else
    echo -e "${RED}  ✗ Docker is not running${NC}"
    echo ""
    echo -e "${YELLOW}Please start Docker Desktop and wait for it to finish starting.${NC}"
    echo -e "${YELLOW}You should see the whale icon in your menu bar.${NC}"
    echo ""
    exit 1
fi

# Step 3: Check/Install Git
echo -e "${YELLOW}[3/5] Checking for Git...${NC}"
if command_exists git; then
    echo -e "${GREEN}  ✓ Git is already installed${NC}"
else
    echo -e "${RED}  ✗ Git is not installed${NC}"
    echo ""
    echo -e "${YELLOW}Installing Git...${NC}"
    
    # Check if Homebrew is installed
    if command_exists brew; then
        echo -e "${CYAN}  Installing via Homebrew...${NC}"
        brew install git
        echo -e "${GREEN}  ✓ Git installed successfully${NC}"
    else
        echo -e "${YELLOW}  Homebrew not found. Installing Homebrew first...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH
        if [[ $(uname -m) == 'arm64' ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        else
            echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/usr/local/bin/brew shellenv)"
        fi
        
        brew install git
        echo -e "${GREEN}  ✓ Git installed successfully${NC}"
    fi
fi

# Step 4: Clone repository
echo -e "${YELLOW}[4/5] Setting up AI Gospel Parser...${NC}"

INSTALL_DIR="$HOME/Documents/ai_gospel_parser"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${CYAN}  Directory already exists. Updating...${NC}"
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo -e "${CYAN}  Cloning repository...${NC}"
    cd "$HOME/Documents"
    git clone https://github.com/Amazingninjas/ai_gospel_parser.git
    cd "$INSTALL_DIR"
fi

echo -e "${GREEN}  ✓ Repository ready${NC}"

# Step 5: Start application
echo -e "${YELLOW}[5/5] Starting AI Gospel Parser...${NC}"
echo -e "${CYAN}  This may take 5-10 minutes on first run...${NC}"
echo ""

docker-compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}   INSTALLATION COMPLETE!${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    echo -e "${YELLOW}Opening browser in 3 seconds...${NC}"
    sleep 3
    open "http://localhost:3000"
    echo ""
    echo -e "${CYAN}Application URLs:${NC}"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:8000/docs"
    echo ""
    echo -e "${CYAN}Installed to: $INSTALL_DIR${NC}"
    echo ""
    echo -e "${YELLOW}To stop:  docker-compose down${NC}"
    echo -e "${YELLOW}To start: docker-compose up -d${NC}"
    echo ""
    
    # Create quick launch script
    cat > "$HOME/start-gospel-parser.sh" << 'LAUNCH'
#!/bin/bash
cd "$HOME/Documents/ai_gospel_parser"
docker-compose up -d
open "http://localhost:3000"
LAUNCH
    chmod +x "$HOME/start-gospel-parser.sh"
    echo -e "${GREEN}  ✓ Created quick launcher: ~/start-gospel-parser.sh${NC}"
    echo ""
else
    echo -e "${RED}  ✗ Failed to start application${NC}"
    echo ""
    echo -e "${YELLOW}Checking logs...${NC}"
    docker-compose logs
    exit 1
fi
