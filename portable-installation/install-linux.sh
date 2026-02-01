#!/bin/bash
# AI Gospel Parser - Smart Linux Installer
# Run with: bash install-linux.sh

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

# Detect package manager
if command_exists apt-get; then
    PKG_MANAGER="apt-get"
    PKG_UPDATE="sudo apt-get update"
    PKG_INSTALL="sudo apt-get install -y"
elif command_exists dnf; then
    PKG_MANAGER="dnf"
    PKG_UPDATE="sudo dnf check-update || true"
    PKG_INSTALL="sudo dnf install -y"
elif command_exists yum; then
    PKG_MANAGER="yum"
    PKG_UPDATE="sudo yum check-update || true"
    PKG_INSTALL="sudo yum install -y"
else
    echo -e "${RED}Could not detect package manager (apt/dnf/yum)${NC}"
    echo "Please install Docker and Git manually."
    exit 1
fi

echo -e "${CYAN}Detected package manager: $PKG_MANAGER${NC}"
echo ""

# Step 1: Check/Install Docker
echo -e "${YELLOW}[1/5] Checking for Docker...${NC}"
if command_exists docker; then
    echo -e "${GREEN}  ✓ Docker is already installed${NC}"
else
    echo -e "${RED}  ✗ Docker is not installed${NC}"
    echo ""
    read -p "Install Docker now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}  Installing Docker...${NC}"
        
        if [ "$PKG_MANAGER" = "apt-get" ]; then
            # Ubuntu/Debian
            $PKG_UPDATE
            $PKG_INSTALL ca-certificates curl gnupg lsb-release
            
            sudo mkdir -p /etc/apt/keyrings
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
            
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
            
            sudo apt-get update
            $PKG_INSTALL docker-ce docker-ce-cli containerd.io docker-compose-plugin
        else
            # Fedora/RHEL/CentOS
            $PKG_INSTALL dnf-plugins-core
            sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
            $PKG_INSTALL docker-ce docker-ce-cli containerd.io docker-compose-plugin
        fi
        
        # Start Docker service
        sudo systemctl start docker
        sudo systemctl enable docker
        
        # Add current user to docker group
        sudo usermod -aG docker $USER
        
        echo -e "${GREEN}  ✓ Docker installed successfully${NC}"
        echo -e "${YELLOW}  Note: You may need to log out and back in for group changes to take effect${NC}"
        echo -e "${YELLOW}  Or run: newgrp docker${NC}"
        
        # Try to activate group immediately
        newgrp docker << EONG
echo -e "${GREEN}  ✓ Docker group activated${NC}"
EONG
    else
        echo "Please install Docker manually and run this script again."
        exit 1
    fi
fi

# Step 2: Check if Docker is running
echo -e "${YELLOW}[2/5] Checking if Docker is running...${NC}"
if docker info >/dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Docker is running${NC}"
else
    echo -e "${YELLOW}  Starting Docker...${NC}"
    sudo systemctl start docker
    sleep 2
    if docker info >/dev/null 2>&1; then
        echo -e "${GREEN}  ✓ Docker is now running${NC}"
    else
        echo -e "${RED}  ✗ Failed to start Docker${NC}"
        echo "  Please run: sudo systemctl start docker"
        exit 1
    fi
fi

# Step 3: Check/Install Git
echo -e "${YELLOW}[3/5] Checking for Git...${NC}"
if command_exists git; then
    echo -e "${GREEN}  ✓ Git is already installed${NC}"
else
    echo -e "${RED}  ✗ Git is not installed${NC}"
    echo ""
    read -p "Install Git now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}  Installing Git...${NC}"
        $PKG_INSTALL git
        echo -e "${GREEN}  ✓ Git installed successfully${NC}"
    else
        echo "Please install Git manually and run this script again."
        exit 1
    fi
fi

# Step 4: Clone repository
echo -e "${YELLOW}[4/5] Setting up AI Gospel Parser...${NC}"

INSTALL_DIR="$HOME/ai_gospel_parser"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${CYAN}  Directory already exists. Updating...${NC}"
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo -e "${CYAN}  Cloning repository...${NC}"
    cd "$HOME"
    git clone https://github.com/Amazingninjas/ai_gospel_parser.git
    cd "$INSTALL_DIR"
fi

echo -e "${GREEN}  ✓ Repository ready${NC}"

# Step 5: Start application
echo -e "${YELLOW}[5/5] Starting AI Gospel Parser...${NC}"
echo -e "${CYAN}  This may take 5-10 minutes on first run...${NC}"
echo ""

docker compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}   INSTALLATION COMPLETE!${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    echo -e "${YELLOW}Opening browser in 3 seconds...${NC}"
    sleep 3
    
    # Try to open browser
    if command_exists xdg-open; then
        xdg-open "http://localhost:3000"
    elif command_exists firefox; then
        firefox "http://localhost:3000" &
    elif command_exists google-chrome; then
        google-chrome "http://localhost:3000" &
    fi
    
    echo ""
    echo -e "${CYAN}Application URLs:${NC}"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:8000/docs"
    echo ""
    echo -e "${CYAN}Installed to: $INSTALL_DIR${NC}"
    echo ""
    echo -e "${YELLOW}To stop:  docker compose down${NC}"
    echo -e "${YELLOW}To start: docker compose up -d${NC}"
    echo ""
    
    # Create desktop launcher
    cat > "$HOME/start-gospel-parser.sh" << 'LAUNCH'
#!/bin/bash
cd "$HOME/ai_gospel_parser"
docker compose up -d
xdg-open "http://localhost:3000" 2>/dev/null || firefox "http://localhost:3000" &
LAUNCH
    chmod +x "$HOME/start-gospel-parser.sh"
    echo -e "${GREEN}  ✓ Created quick launcher: ~/start-gospel-parser.sh${NC}"
    echo ""
else
    echo -e "${RED}  ✗ Failed to start application${NC}"
    echo ""
    echo -e "${YELLOW}Checking logs...${NC}"
    docker compose logs
    exit 1
fi
