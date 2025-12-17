#!/usr/bin/env python3
"""
ProBeSuite - Masscan Ultra-Fast Scanner
High-speed port scanning for large networks
"""

import os
import sys
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime

class MasscanScanner:
    def __init__(self):
        self.target = None
        self.resolved_target = None
        self.output_dir = Path("reports/scanning/masscan")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def print_banner(self):
        """Display Masscan banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║              ⚡ MASSCAN ULTRA-FAST SCANNER ⚡                  ║
║             High-Speed Network Port Scanner                  ║
║             Scan Entire Internet in Minutes                  ║
╚══════════════════════════════════════════════════════════════╝
        """
        print("\033[96m" + banner + "\033[0m")
    
    def show_main_menu(self):
        """Display Masscan main menu"""
        menu = """
╭─ MASSCAN SCANNING OPTIONS ────────────────────────────────────╮
│                                                               │
│  QUICK SCANS:                                                 │
│    [1]  Fast Scan (Top 100 ports, 10k pps)                    │
│    [2]  Medium Scan (Top 1000 ports, 5k pps)                  │
│    [3]  Full Scan (All 65535 ports, 1k pps)                   │
│                                                               │
│  SPEED PROFILES:                                              │
│    [4]  Conservative (1,000 packets/sec)                      │
│    [5]  Normal (10,000 packets/sec)                           │
│    [6]  Aggressive (50,000 packets/sec)                       │
│    [7]  Insane (100,000 packets/sec)                          │
│    [8]  Maximum (Custom rate)                                 │
│                                                               │
│  PORT RANGES:                                                 │
│    [9]  Common Ports (80,443,22,21,25,etc)                    │
│    [10] Web Ports (80,443,8000-9000)                          │
│    [11] Database Ports (3306,5432,1433,27017)                 │
│    [12] Mail Ports (25,110,143,465,587,993,995)               │
│    [13] File Transfer (20,21,22,69,115,139,445)               │
│    [14] Custom Port Range                                     │
│                                                               │
│  SCAN TYPES:                                                  │
│    [15] TCP SYN Scan (Default)                                │
│    [16] UDP Scan                                              │
│    [17] TCP + UDP Combined                                    │
│    [18] SCTP Scan                                             │
│                                                               │
│  NETWORK RANGES:                                              │
│    [19] Single IP                                             │
│    [20] CIDR Range (e.g., 192.168.1.0/24)                     │
│    [21] IP Range (e.g., 192.168.1.1-192.168.1.255)            │
│    [22] Multiple Targets                                      │
│    [23] Exclude IPs                                           │
│                                                               │
│  ADVANCED OPTIONS:                                            │
│    [24] Banner Grabbing                                       │
│    [25] Retry Failed Ports                                    │
│    [26] Connection Timeout Config                             │
│    [27] Source Port Spoofing                                  │
│    [28] Interface Selection                                   │
│    [29] Packet Fragmentation                                  │
│                                                               │
│  OUTPUT FORMATS:                                              │
│    [30] List Format (Default)                                 │
│    [31] JSON Format                                           │
│    [32] XML Format                                            │
│    [33] Grepable Format                                       │
│    [34] Binary Format                                         │
│                                                               │
│  PRESET SCANS:                                                │
│    [35] Internet Scan (/0 - Use with caution!)                │
│    [36] Enterprise Network Scan                               │
│    [37] Subnet Discovery                                      │
│    [38] Service Enumeration                                   │
│                                                               │
│  [0]  ← Back to Active Scanning Menu                          │
│                                                               │
╰───────────────────────────────────────────────────────────────╯

\033[93m[!] WARNING: Masscan requires root/sudo privileges\033[0m
\033[93m[!] High-speed scans can be detected by IDS/IPS\033[0m
\033[93m[!] Always get proper authorization before scanning\033[0m
        """
        print("\033[92m" + menu + "\033[0m")
    
    def resolve_domain(self, target):
        """Resolve domain to IP address"""
        # Check if already an IP or CIDR
        if self.is_ip_or_cidr(target):
            return target
        
        # Try to resolve domain
        try:
            print(f"\n\033[96m[*] Resolving domain: {target}\033[0m")
            ip = socket.gethostbyname(target)
            print(f"\033[92m[+] Resolved to: {ip}\033[0m")
            return ip
        except socket.gaierror:
            print(f"\033[91m[!] Failed to resolve domain: {target}\033[0m")
            print(f"\033[93m[~] Please enter IP address directly\033[0m")
            return None
    
    def is_ip_or_cidr(self, target):
        """Check if target is IP address or CIDR notation"""
        # Check for CIDR
        if '/' in target:
            return True
        
        # Check for IP range
        if '-' in target and '.' in target:
            return True
        
        # Check for multiple IPs
        if ',' in target:
            return True
        
        # Check for single IP
        parts = target.split('.')
        if len(parts) == 4:
            try:
                for part in parts:
                    num = int(part)
                    if not 0 <= num <= 255:
                        return False
                return True
            except ValueError:
                return False
        
        return False
    
    def get_target(self):
        """Get target from user"""
        print("\n\033[93m" + "="*65 + "\033[0m")
        print("\033[96m[?] TARGET SPECIFICATION\033[0m")
        print("\033[93m" + "="*65 + "\033[0m")
        print("\nExamples:")
        print("  • Single IP:     192.168.1.1")
        print("  • Domain:        example.com (will be resolved)")
        print("  • CIDR:          192.168.1.0/24")
        print("  • Range:         192.168.1.1-192.168.1.255")
        print("  • Multiple:      192.168.1.0/24,10.0.0.0/8")
        
        target = input("\n[\033[94m?\033[0m] Enter target: ").strip()
        if not target:
            return False
        
        self.target = target
        
        # Resolve domain if needed
        self.resolved_target = self.resolve_domain(target)
        
        if not self.resolved_target:
            self.target = None
            return False
        
        return True
    
    def get_output_file(self, scan_name, format_ext="txt"):
        """Generate output filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_target = self.target.replace('/', '_').replace(':', '_').replace(',', '_').replace('.', '_')
        filename = f"{scan_name}_{safe_target}_{timestamp}.{format_ext}"
        return self.output_dir / filename
    
    def execute_scan(self, command, scan_name):
        """Execute masscan command"""
        print(f"\n\033[93m{'='*65}\033[0m")
        print(f"\033[96m[*] EXECUTING: {scan_name}\033[0m")
        print(f"\033[93m{'='*65}\033[0m")
        print(f"\n\033[96m[+] Original Target:\033[0m {self.target}")
        if self.target != self.resolved_target:
            print(f"\033[96m[+] Resolved IP:\033[0m {self.resolved_target}")
        print(f"\033[96m[+] Command:\033[0m {command}")
        print(f"\n\033[93m[*] Scanning in progress...\033[0m")
        print(f"\033[93m[*] This may take some time depending on the scan rate\033[0m\n")
        
        start_time = time.time()
        result = os.system(command)
        elapsed = time.time() - start_time
        
        if result == 0:
            print(f"\n\033[93m{'='*65}\033[0m")
            print(f"\033[92m[✓] Scan completed successfully in {elapsed:.2f} seconds\033[0m")
            print(f"\033[93m{'='*65}\033[0m")
        else:
            print(f"\n\033[91m[!] Scan failed with exit code: {result}\033[0m")
            print(f"\033[93m[~] Common issues:\033[0m")
            print(f"  • Masscan not installed: sudo apt install masscan")
            print(f"  • Need sudo privileges: Run with sudo")
            print(f"  • Invalid target format")
    
    def quick_scans(self, choice):
        """Handle quick scan presets"""
        output_file = self.get_output_file("quick")
        
        scans = {
            '1': ('Fast Scan', f'sudo masscan {self.resolved_target} --top-ports 100 --rate 10000 -oL {output_file}'),
            '2': ('Medium Scan', f'sudo masscan {self.resolved_target} --top-ports 1000 --rate 5000 -oL {output_file}'),
            '3': ('Full Port Scan', f'sudo masscan {self.resolved_target} -p0-65535 --rate 1000 -oL {output_file}')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            self.execute_scan(cmd, name)
    
    def speed_profiles(self, choice):
        """Handle different speed profiles"""
        output_file = self.get_output_file("speed")
        
        if choice == '8':
            rate = input("[\033[94m?\033[0m] Enter custom rate (packets/sec): ").strip()
            if not rate.isdigit():
                print("\033[91m[!] Invalid rate\033[0m")
                return
        else:
            rates = {
                '4': '1000',
                '5': '10000',
                '6': '50000',
                '7': '100000'
            }
            rate = rates.get(choice, '10000')
        
        ports = input("[\033[94m?\033[0m] Port range (default: 1-65535): ").strip() or "1-65535"
        cmd = f'sudo masscan {self.resolved_target} -p{ports} --rate {rate} -oL {output_file}'
        
        self.execute_scan(cmd, f'Speed Profile ({rate} pps)')
    
    def port_ranges(self, choice):
        """Handle specific port range scans"""
        output_file = self.get_output_file("ports")
        
        port_presets = {
            '9': ('Common Ports', '21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080'),
            '10': ('Web Ports', '80,443,8000,8001,8008,8080,8443,8888,9000,9001,9090'),
            '11': ('Database Ports', '1433,1521,3306,5432,5984,6379,7000,7001,8529,9042,9160,9200,27017,27018,27019,28017'),
            '12': ('Mail Ports', '25,110,143,465,587,993,995,2525'),
            '13': ('File Transfer', '20,21,22,69,115,139,445,2049')
        }
        
        if choice == '14':
            ports = input("[\033[94m?\033[0m] Enter custom port range: ").strip()
            if not ports:
                print("\033[91m[!] No ports specified\033[0m")
                return
            name = 'Custom Ports'
        elif choice in port_presets:
            name, ports = port_presets[choice]
        else:
            return
        
        rate = input("[\033[94m?\033[0m] Scan rate (default: 10000 pps): ").strip() or "10000"
        cmd = f'sudo masscan {self.resolved_target} -p{ports} --rate {rate} -oL {output_file}'
        
        self.execute_scan(cmd, name)
    
    def scan_types(self, choice):
        """Handle different scan types"""
        output_file = self.get_output_file("scantype")
        
        ports = input("[\033[94m?\033[0m] Port range (default: 1-65535): ").strip() or "1-65535"
        rate = input("[\033[94m?\033[0m] Scan rate (default: 10000 pps): ").strip() or "10000"
        
        scan_flags = {
            '15': ('TCP SYN Scan', ''),
            '16': ('UDP Scan', '--udp'),
            '17': ('TCP + UDP', '--udp'),
            '18': ('SCTP Scan', '--sctp')
        }
        
        if choice in scan_flags:
            name, flags = scan_flags[choice]
            cmd = f'sudo masscan {self.resolved_target} -p{ports} {flags} --rate {rate} -oL {output_file}'
            self.execute_scan(cmd, name)
    
    def network_ranges(self, choice):
        """Handle network range configurations"""
        output_file = self.get_output_file("network")
        
        if choice == '23':
            exclude = input("[\033[94m?\033[0m] Enter IPs to exclude (comma-separated): ").strip()
            if exclude:
                ports = input("[\033[94m?\033[0m] Port range: ").strip() or "1-65535"
                rate = input("[\033[94m?\033[0m] Scan rate: ").strip() or "10000"
                cmd = f'sudo masscan {self.resolved_target} -p{ports} --rate {rate} --exclude {exclude} -oL {output_file}'
                self.execute_scan(cmd, 'Scan with Exclusions')
        else:
            ports = input("[\033[94m?\033[0m] Port range: ").strip() or "1-65535"
            rate = input("[\033[94m?\033[0m] Scan rate: ").strip() or "10000"
            cmd = f'sudo masscan {self.resolved_target} -p{ports} --rate {rate} -oL {output_file}'
            self.execute_scan(cmd, 'Network Range Scan')
    
    def advanced_options(self, choice):
        """Handle advanced scanning options"""
        output_file = self.get_output_file("advanced")
        
        base_cmd = f'sudo masscan {self.resolved_target}'
        ports = input("[\033[94m?\033[0m] Port range (default: 1-65535): ").strip() or "1-65535"
        rate = input("[\033[94m?\033[0m] Scan rate (default: 10000): ").strip() or "10000"
        
        if choice == '24':
            cmd = f'{base_cmd} -p{ports} --rate {rate} --banners -oL {output_file}'
            self.execute_scan(cmd, 'Banner Grabbing Scan')
        
        elif choice == '25':
            retries = input("[\033[94m?\033[0m] Number of retries (default: 3): ").strip() or "3"
            cmd = f'{base_cmd} -p{ports} --rate {rate} --retries {retries} -oL {output_file}'
            self.execute_scan(cmd, 'Scan with Retries')
        
        elif choice == '26':
            timeout = input("[\033[94m?\033[0m] Timeout in seconds (default: 10): ").strip() or "10"
            cmd = f'{base_cmd} -p{ports} --rate {rate} --connection-timeout {timeout} -oL {output_file}'
            self.execute_scan(cmd, 'Scan with Custom Timeout')
        
        elif choice == '27':
            src_port = input("[\033[94m?\033[0m] Source port: ").strip()
            if src_port:
                cmd = f'{base_cmd} -p{ports} --rate {rate} --source-port {src_port} -oL {output_file}'
                self.execute_scan(cmd, 'Scan with Source Port')
        
        elif choice == '28':
            interface = input("[\033[94m?\033[0m] Network interface (e.g., eth0): ").strip()
            if interface:
                cmd = f'{base_cmd} -p{ports} --rate {rate} -e {interface} -oL {output_file}'
                self.execute_scan(cmd, f'Scan via {interface}')
        
        elif choice == '29':
            cmd = f'{base_cmd} -p{ports} --rate {rate} --offline -oL {output_file}'
            self.execute_scan(cmd, 'Fragmented Scan')
    
    def output_formats(self, choice):
        """Handle different output formats"""
        ports = input("[\033[94m?\033[0m] Port range: ").strip() or "1-65535"
        rate = input("[\033[94m?\033[0m] Scan rate: ").strip() or "10000"
        
        formats = {
            '30': ('List Format', 'txt', '-oL'),
            '31': ('JSON Format', 'json', '-oJ'),
            '32': ('XML Format', 'xml', '-oX'),
            '33': ('Grepable Format', 'gnmap', '-oG'),
            '34': ('Binary Format', 'bin', '-oB')
        }
        
        if choice in formats:
            name, ext, flag = formats[choice]
            output_file = self.get_output_file("output", ext)
            cmd = f'sudo masscan {self.resolved_target} -p{ports} --rate {rate} {flag} {output_file}'
            self.execute_scan(cmd, name)
    
    def preset_scans(self, choice):
        """Handle preset comprehensive scans"""
        output_file = self.get_output_file("preset")
        
        presets = {
            '35': {
                'name': 'Internet Scan',
                'warning': 'This will scan the ENTIRE internet! Requires authorization!',
                'cmd': 'sudo masscan 0.0.0.0/0 -p80,443 --rate 1000000 --banners -oL'
            },
            '36': {
                'name': 'Enterprise Network',
                'warning': 'Comprehensive scan of enterprise network',
                'cmd': f'sudo masscan {self.resolved_target} -p1-65535 --rate 50000 --banners -oL'
            },
            '37': {
                'name': 'Subnet Discovery',
                'warning': 'Fast discovery scan',
                'cmd': f'sudo masscan {self.resolved_target} --top-ports 100 --rate 10000 -oL'
            },
            '38': {
                'name': 'Service Enumeration',
                'warning': 'Detailed service detection',
                'cmd': f'sudo masscan {self.resolved_target} -p1-65535 --rate 10000 --banners -oL'
            }
        }
        
        if choice in presets:
            preset = presets[choice]
            print(f"\n\033[93m[!] WARNING: {preset['warning']}\033[0m")
            
            if input("[\033[94m?\033[0m] Continue? (yes/no): ").strip().lower() != 'yes':
                print("\033[91m[!] Scan cancelled\033[0m")
                return
            
            cmd = f"{preset['cmd']} {output_file}"
            self.execute_scan(cmd, preset['name'])
    
    def run(self):
        """Main scanner loop"""
        while True:
            os.system('clear')
            self.print_banner()
            
            if not self.target:
                if not self.get_target():
                    print("\033[91m[!] No target specified\033[0m")
                    time.sleep(2)
                    continue
            
            self.show_main_menu()
            
            choice = input("\n\033[93mMasscan>\033[0m ").strip()
            
            if choice == '0':
                break
            
            # Route to handlers
            if choice in ['1', '2', '3']:
                self.quick_scans(choice)
            elif choice in ['4', '5', '6', '7', '8']:
                self.speed_profiles(choice)
            elif choice in ['9', '10', '11', '12', '13', '14']:
                self.port_ranges(choice)
            elif choice in ['15', '16', '17', '18']:
                self.scan_types(choice)
            elif choice in ['19', '20', '21', '22', '23']:
                self.network_ranges(choice)
            elif choice in ['24', '25', '26', '27', '28', '29']:
                self.advanced_options(choice)
            elif choice in ['30', '31', '32', '33', '34']:
                self.output_formats(choice)
            elif choice in ['35', '36', '37', '38']:
                self.preset_scans(choice)
            else:
                print("\033[91m[!] Invalid option\033[0m")
                time.sleep(1)
                continue
            
            input("\n\033[96m[*] Press Enter to continue...\033[0m")
            
            if input("\n[\033[94m?\033[0m] Scan another target? (y/n): ").strip().lower() == 'y':
                self.target = None
                self.resolved_target = None

def main():
    """Main entry point"""
    scanner = MasscanScanner()
    try:
        scanner.run()
    except KeyboardInterrupt:
        print("\n\n\033[91m[!] Scan interrupted by user\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[!] Error: {e}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()