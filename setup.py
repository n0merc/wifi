#!/usr/bin/env python3
"""
HUBAXGPT Termux Setup Script
Automates installation and configuration
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class TermuxSetup:
    def __init__(self):
        self.home = Path.home()
        self.termux_home = self.home
        self.sdcard = Path("/sdcard")
        self.is_root = os.geteuid() == 0
        
    def print_banner(self):
        """Print installation banner"""
        banner = """
        ╔══════════════════════════════════════════════════════════╗
        ║            HUBAXGPT - TERMUX HACKING SUITE SETUP         ║
        ║                                                          ║
        ║          ██╗  ██╗██╗   ██╗██████╗  █████╗ ██╗  ██╗       ║
        ║          ██║  ██║██║   ██║██╔══██╗██╔══██╗╚██╗██╔╝       ║
        ║          ███████║██║   ██║██████╔╝███████║ ╚███╔╝        ║
        ║          ██╔══██║██║   ██║██╔══██╗██╔══██║ ██╔██╗        ║
        ║          ██║  ██║╚██████╔╝██████╔╝██║  ██║██╔╝ ██╗       ║
        ║          ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝       ║
        ║                                                          ║
        ║                 Red Team Toolkit for Android             ║
        ╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def check_requirements(self):
        """Check system requirements"""
        print("[*] Checking requirements...")
        
        # Check Android
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
    
    def install_packages(self):
        """Install required packages"""
        print("\n[*] Installing packages...")
        
        packages = [
            "python", "git", "wget", "curl", "nano", "vim",
            "nmap", "hydra", "aircrack-ng", "wireless-tools",
            "bluez", "bluez-utils", "tsu", "root-repo",
            "proot", "proot-distro", "hashcat", "john",
            "sqlmap", "nikto", "dirb", "gobuster",
            "radare2", "gdb", "apktool", "jadx",
            "binwalk", "steghide", "exiftool"
        ]
        
        for pkg in packages:
            print(f"  Installing {pkg}...")
            try:
                subprocess.run(["pkg", "install", "-y", pkg], 
                             capture_output=True, check=True)
                print(f"  [+] {pkg} installed")
            except subprocess.CalledProcessError:
                print(f"  [-] Failed to install {pkg}")
        
        print("[+] Package installation complete")
    
    def setup_directories(self):
        """Create directory structure"""
        print("\n[*] Setting up directories...")
        
        directories = [
            self.sdcard / "hacking",
            self.sdcard / "hacking" / "tools",
            self.sdcard / "hacking" / "logs",
            self.sdcard / "hacking" / "output",
            self.sdcard / "hacking" / "wordlists",
            self.sdcard / "hacking" / "exploits",
            self.sdcard / "hacking" / "scripts",
            self.termux_home / ".hubax"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  [+] Created {directory}")
 # Create symbolic links
        try:
            (self.termux_home / "hacking").symlink_to(self.sdcard / "hacking")
            print("  [+] Created symbolic link: ~/hacking -> /sdcard/hacking")
        except:
            pass
        
        print("[+] Directory structure created")
    
    def install_python_packages(self):
        """Install Python dependencies"""
        print("\n[*] Installing Python packages...")
        
        # Check if requirements.txt exists
        req_file = Path("requirements.txt")
        if req_file.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                          capture_output=True)
        else:
            # Install core packages
            packages = [
                "scapy", "colorama", "requests", "beautifulsoup4", "lxml",
                "pybluez", "bleak", "pyshark", "netifaces", "psutil",
                "argparse", "tabulate", "progress", "pyfiglet", "termcolor",
                "cryptography", "paramiko", "impacket", "pwntools",
                "selenium", "requests-html", "mechanize", "urllib3",
                "python-nmap", "dpkt", "pcapy", "frida", "objection",
                "androguard", "pywifi", "wifi"
            ]
            
            for package in packages:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", package],
                                  capture_output=True, timeout=60)
                    print(f"  [+] Installed {package}")
                except:
                    print(f"  [-] Failed to install {package}")
        
        print("[+] Python packages installed")
    
    def clone_repositories(self):
        """Clone hacking tools from GitHub"""
        print("\n[*] Cloning repositories...")
        
        repos = [
            ("aircrack-ng/aircrack-ng", "wifi/aircrack"),
            ("derv82/wifite2", "wifi/wifite"),
            ("ZerBea/hcxtools", "wifi/hcxtools"),
            ("sqlmapproject/sqlmap", "web/sqlmap"),
            ("sullo/nikto", "web/nikto"),
            ("wpscanteam/wpscan", "web/wpscan"),
            ("ffuf/ffuf", "web/ffuf"),
            ("OJ/gobuster", "web/gobuster"),
            ("hashcat/hashcat", "password/hashcat"),
            ("openwall/john", "password/john"),
            ("sherlock-project/sherlock", "osint/sherlock"),
            ("laramies/theHarvester", "osint/theHarvester"),
            ("MobSF/Mobile-Security-Framework-MobSF", "android/mobsf"),
            ("seemoo-lab/nexmon", "bluetooth/nexmon"),
            ("virtualabs/btlejack", "bluetooth/btlejack")
        ]
        
        for repo, path in repos:
            repo_path = self.sdcard / "hacking" / "tools" / path
            if not repo_path.exists():
                print(f"  Cloning {repo}...")
                try:
                    subprocess.run(["git", "clone", f"https://github.com/{repo}.git", str(repo_path)],
                                  capture_output=True, timeout=300)
                    print(f"  [+] Cloned {repo}")
                except:
                    print(f"  [-] Failed to clone {repo}")
            else:
                print(f"  [*] {repo} already exists")
        
        print("[+] Repositories cloned")
    
    def download_wordlists(self):
        """Download common wordlists"""
        print("\n[*] Downloading wordlists...")
        
        wordlists_dir = self.sdcard / "hacking" / "wordlists"
        
        wordlist_urls = [
            ("https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt", "rockyou.txt"),
            ("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt", "10-million.txt"),
            ("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/rockyou.txt.tar.gz", "rockyou.tar.gz"),
            ("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt", "web-common.txt"),
            ("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/directory-list-2.3-medium.txt", "dir-medium.txt")
        ]
        
        for url, filename in wordlist_urls:
            filepath = wordlists_dir / filename
            if not filepath.exists():
                print(f"  Downloading {filename}...")
                try:
                    subprocess.run(["wget", "-q", "-O", str(filepath), url],
                                  capture_output=True, timeout=300)
                    
                    # Extract if tar.gz
                    if filename.endswith(".tar.gz"):
                        subprocess.run(["tar", "-xzf", str(filepath), "-C", str(wordlists_dir)],
                                      capture_output=True)
                        filepath.unlink()
                    
                    print(f"  [+] Downloaded {filename}")
                except:
                    print(f"  [-] Failed to download {filename}")
        
        print("[+] Wordlists downloaded")
    
    def create_config_files(self):
        """Create configuration files"""
        print("\n[*] Creating configuration files...")
        
        # Create .haxorc
        haxorc_content = """# HUBAXGPT Configuration

# Aliases
alias hax='cd /sdcard/hacking'
alias scan='nmap -sV -sC -O'
alias deauth='python3 /sdcard/hacking/tools/wifi_deauth.py'
alias btspam='python3 /sdcard/hacking/tools/bluetooth_spammer.py'
alias webscan='python3 /sdcard/hacking/tools/web_scanner.py'
alias crack='hashcat -m 2500 -a 0'
alias update-hax='cd /sdcard/hacking && git pull'

# Environment
export PATH=$PATH:/sdcard/hacking/tools
export WORDLISTS=/sdcard/hacking/wordlists
export HACKING_HOME=/sdcard/hacking
export TERMUX_HOME=/data/data/com.termux/files/home

# Colors
export PS1="\\[\\033[1;31m\\]\\u@hax\\[\\033[0m\\]:\\[\\033[1;34m\\]\\w\\[\\033[0m\\]\\$ "

# Tool paths
export AIRCRACK_PATH=/data/data/com.termux/files/usr/bin
export NMAP_PATH=/data/data/com.termux/files/usr/bin
export SQLMAP_PATH=/sdcard/hacking/tools/web/sqlmap

# Python path
export PYTHONPATH=$PYTHONPATH:/sdcard/hacking/tools
"""
        
        haxorc_path = self.termux_home / ".haxorc"
        haxorc_path.write_text(haxorc_content)
        print("  [+] Created ~/.haxorc")
        
        # Create config.json
        config_content = {
            "general": {
                "log_level": "INFO",
                "output_dir": "/sdcard/hacking/output",
                "log_dir": "/sdcard/hacking/logs",
                "auto_update": True
            },
            "wifi": {
                "default_interface": "wlan0",
                "monitor_mode": True,
                "channel_hop": True,
                "scan_time": 30
            },
            "bluetooth": {
                "default_interface": "hci0",
                "scan_time": 60,
                "max_devices": 100
            },
            "web": {
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "timeout": 10,
                "threads": 20
            },
            "password": {
                "default_wordlist": "/sdcard/hacking/wordlists/rockyou.txt",
                "hashcat_path": "/data/data/com.termux/files/usr/bin/hashcat",
                "john_path": "/data/data/com.termux/files/usr/bin/john"
            }
        }
        
        import json
        config_path = self.termux_home / ".hubax" / "config.json"
        config_path.write_text(json.dumps(config_content, indent=2))
        print("  [+] Created ~/.hubax/config.json")
        
        # Create launcher script
        launcher_content = """#!/data/data/com.termux/files/usr/bin/bash
# HUBAXGPT Launcher

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                   HUBAXGPT HACKING SUITE                 ║"
echo "╚══════════════════════════════════════════════════════════╝"

source ~/.haxorc

PS3='Select option: '
options=(
    "WiFi Attacks"
    "Bluetooth Attacks"
    "Web Attacks"
    "Password Attacks"
    "Network Attacks"
    "Android Hacking"
    "OSINT Tools"
    "Exploitation"
    "Reverse Engineering"
    "Update Tools"
    "Exit"
)

select opt in "${options[@]}"
do
    case $opt in
        "WiFi Attacks")
            cd /sdcard/hacking/tools/wifi
            python3 wifi_menu.py
            ;;
        "Bluetooth Attacks")
            cd /sdcard/hacking/tools/bluetooth
            python3 bluetooth_menu.py
            ;;
        "Web Attacks")
            cd /sdcard/hacking/tools/web
            python3 web_menu.py
            ;;
        "Password Attacks")
            cd /sdcard/hacking/tools/password
            python3 password_menu.py
            ;;
        "Network Attacks")
            cd /sdcard/hacking/tools/network
            python3 network_menu.py
            ;;
        "Android Hacking")
            cd /sdcard/hacking/tools/android
            python3 android_menu.py
            ;;
        "OSINT Tools")
            cd /sdcard/hacking/tools/osint
            python3 osint_menu.py
            ;;
        "Exploitation")
            cd /sdcard/hacking/tools/exploitation
            python3 exploit_menu.py
            ;;
        "Reverse Engineering")
            cd /sdcard/hacking/tools/reverse
            python3 reverse_menu.py
            ;;
        "Update Tools")
            echo "[*] Updating tools..."
            cd /sdcard/hacking
            git pull
            pip install -r requirements.txt --upgrade
            echo "[+] Tools updated"
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
        
        launcher_path = self.termux_home / "hax"
        launcher_path.write_text(launcher_content)
        launcher_path.chmod(0o755)
        print("  [+] Created ~/hax launcher")
        
        # Add to bashrc
        bashrc_path = self.termux_home / ".bashrc"
        if bashrc_path.exists():
            with bashrc_path.open("a") as f:
                f.write("\n# HUBAXGPT Configuration\n")
                f.write("source ~/.haxorc\n")
                f.write("alias hax='~/hax'\n")
            print("  [+] Updated ~/.bashrc")
        
        print("[+] Configuration files created")
    
    def setup_permissions(self):
        """Set up permissions"""
        print("\n[*] Setting up permissions...")
        
        # Make scripts executable
        scripts_dir = self.sdcard / "hacking" / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                script.chmod(0o755)
            for script in scripts_dir.glob("*.sh"):
                script.chmod(0o755)
        
        # Set up termux storage
        try:
            subprocess.run(["termux-setup-storage"], capture_output=True)
            print("  [+] Termux storage setup")
        except:
            print("  [-] Failed to setup termux storage")
        
        print("[+] Permissions configured")
    
    def run_tests(self):
        """Run basic tests"""
        print("\n[*] Running tests...")
        
        tests = [
            ("Python", ["python3", "--version"]),
            ("Git", ["git", "--version"]),
            ("Nmap", ["nmap", "--version"]),
            ("Aircrack", ["aircrack-ng", "--version"]),
            ("Hashcat", ["hashcat", "--version"]),
        ]
        
        for name, cmd in tests:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"  [+] {name}: OK")
                else:
                    print(f"  [-] {name}: FAILED")
            except:
                print(f"  [-] {name}: NOT FOUND")
        
        print("[+] Tests completed")
    
    def print_summary(self):
        """Print installation summary"""
        print("\n" + "="*60)
        print("HUBAXGPT - INSTALLATION COMPLETE")
        print("="*60)
        
        summary = """
        ✅ Installation Successful!
        
        📁 Directories:
          • /sdcard/hacking/          - Main hacking directory
          • /sdcard/hacking/tools/    - All hacking tools
          • /sdcard/hacking/wordlists - Password wordlists
          • /sdcard/hacking/logs/     - Log files
          • /sdcard/hacking/output/   - Output files
        
        🚀 Quick Start:
          1. Restart Termux or run: source ~/.bashrc
          2. Launch menu: hax
          3. Or run specific tools from ~/hacking/tools/
        
        🔧 Important Tools:
          • WiFi Deauth: python3 /sdcard/hacking/tools/wifi_deauth.py
          • Bluetooth: python3 /sdcard/hacking/tools/bluetooth_spammer.py
          • Web Scanner: python3 /sdcard/hacking/tools/web_scanner.py
          • Password Crack: hashcat -m 2500 -a 0 hash.txt wordlist.txt
        
        ⚠️  Requirements:
          • Root access for most tools
          • WiFi adapter with monitor mode support
          • USB OTG for external adapters
        
        📚 Documentation:
          • Read the README.md file
          • Check /sdcard/hacking/docs/
          • Join Discord for support
        
        ⚖️  Legal Notice:
          • Use only on authorized systems
          • You are responsible for your actions
          • This is for educational purposes only
        
        🆘 Support:
          • GitHub Issues: https://github.com/hubaxgpt/termux-hacking/issues
          • Discord: https://discord.gg/hubaxgpt
          • Email: hubax@protonmail.com
        """
        
        print(summary)
        print("="*60)
    
    def run(self):
        """Run full setup"""
        self.print_banner()
        
        if not self.check_requirements():
            print("\n[-] Requirements not met. Exiting.")
            sys.exit(1)
        
        if not self.is_root:
            print("\n[!] Warning: Not running as root")
            print("[*] Some features may not work")
            print("[*] Run with: tsu -c 'python3 setup.py'")
            response = input("\nContinue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
        
        try:
            self.install_packages()
            self.setup_directories()
            self.install_python_packages()
            self.clone_repositories()
            self.download_wordlists()
            self.create_config_files()
            self.setup_permissions()
            self.run_tests()
            self.print_summary()
            
            print("\n[+] Setup completed successfully!")
            print("[*] Restart Termux or run: source ~/.bashrc")
            
        except KeyboardInterrupt:
            print("\n\n[!] Installation interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n[-] Installation failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    setup = TermuxSetup()
    setup.run()
