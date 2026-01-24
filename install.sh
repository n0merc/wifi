#!/data/data/com.termux/files/usr/bin/bash
# WiFi Deauth Installation Script

echo "[*] WiFi Deauthentication Attack - Installation"
echo "[*] This will install all required tools and dependencies"

# Check if running as root
if [ "$(whoami)" != "root" ]; then
    echo "[!] Not running as root!"
    echo "[*] Run with: tsu -c './install.sh'"
    exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[+] Root access confirmed${NC}"

# Update packages
echo -e "${YELLOW}[*] Updating packages...${NC}"
pkg update -y && pkg upgrade -y

# Install dependencies
echo -e "${YELLOW}[*] Installing dependencies...${NC}"
pkg install -y python git root-repo tsu
pkg install -y aircrack-ng wireless-tools
pkg install -y net-tools procps iproute2

# Install Python packages
echo -e "${YELLOW}[*] Installing Python packages...${NC}"
pip install --upgrade pip
pip install colorama requests argparse tabulate progress

# Setup storage
echo -e "${YELLOW}[*] Setting up storage...${NC}"
termux-setup-storage

# Create directories
echo -e "${YELLOW}[*] Creating directories...${NC}"
mkdir -p /sdcard/wifi_deauth/{tools,logs,captures,wordlists,scripts,config}

# Download main script
echo -e "${YELLOW}[*] Downloading tools...${NC}"
curl -o /sdcard/wifi_deauth/tools/wifi_deauth.py https://raw.githubusercontent.com/hubaxgpt/wifi-deauth/main/wifi_deauth.py
chmod +x /sdcard/wifi_deauth/tools/wifi_deauth.py

# Create launcher
echo -e "${YELLOW}[*] Creating launcher...${NC}"
cat > /data/data/com.termux/files/usr/bin/wifideauth << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
python3 /sdcard/wifi_deauth/tools/wifi_deauth.py
EOF

chmod +x /data/data/com.termux/files/usr/bin/wifideauth

# Create configuration
echo -e "${YELLOW}[*] Creating configuration...${NC}"
cat > /sdcard/wifi_deauth/config/setup.conf << 'EOF'
# WiFi Deauth Configuration
interface=wlan0
monitor_mode=true
scan_time=30
deauth_packets=100
log_level=INFO
EOF

# Add to bashrc
echo -e "${YELLOW}[*] Updating bashrc...${NC}"
echo "alias deauth='python3 /sdcard/wifi_deauth/tools/wifi_deauth.py'" >> /data/data/com.termux/files/home/.bashrc
echo "export WIFI_DEAUTH_HOME=/sdcard/wifi_deauth" >> /data/data/com.termux/files/home/.bashrc

echo -e "${GREEN}[+] Installation complete!${NC}"
echo ""
echo -e "${YELLOW}[*] Usage:${NC}"
echo "  1. Restart Termux or run: source ~/.bashrc"
echo "  2. Run: wifideauth"
echo "  3. Or: deauth"
echo ""
echo -e "${RED}[!] Important:${NC}"
echo "  - Root access required"
echo "  - WiFi adapter must support monitor mode"
echo "  - Use only on authorized networks"
