#!/usr/bin/env python3
"""
ProBeSuite - Advanced Nmap Scanner
Professional port scanning with comprehensive options
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

class NmapScanner:
    def __init__(self):
        self.target = None
        self.output_dir = Path("reports/scanning/nmap")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def print_banner(self):
        """Display Nmap scanner banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                  🎯 NMAP ADVANCED SCANNER 🎯                 ║
║         Professional Network Reconnaissance Tool             ║
║              Comprehensive Port & Service Analysis           ║
╚══════════════════════════════════════════════════════════════╝
        """
        print("\033[96m" + banner + "\033[0m")
    
    def show_main_menu(self):
        """Display main Nmap scanning menu"""
        menu = """  
╭─ NMAP SCANNING CATEGORIES ────────────────────────────────────╮
│                                                               │
│  BASIC SCANS:                                                 │
│    [1]  Ping Sweep (Host Discovery)                           │
│    [2]  Quick Scan (Top 100 ports)                            │
│    [3]  Top Ports Scan (1000 most common)                     │
│    [4]  Full Port Scan (All 65535 ports)                      │
│                                                               │
│  SERVICE DETECTION:                                           │
│    [5]  Service Version Detection (-sV)                       │
│    [6]  Service + Script Scan (-sV -sC)                       │
│    [7]  Aggressive Service Detection (-sV --version-all)      │
│                                                               │
│  OS & FINGERPRINTING:                                         │
│    [8]  OS Detection (-O)                                     │
│    [9]  Aggressive Scan (-A) [OS + Version + Scripts]         │
│    [10] Complete Fingerprint (-A -p-)                         │
│                                                               │
│  STEALTH & EVASION:                                           │
│    [11] SYN Stealth Scan (-sS)                                │
│    [12] FIN Scan (-sF)                                        │
│    [13] NULL Scan (-sN)                                       │
│    [14] XMAS Scan (-sX)                                       │
│    [15] ACK Scan (-sA)                                        │
│    [16] Decoy Scan (Randomize source)                         │
│    [17] Fragment Packets (-f)                                 │
│    [18] Idle/Zombie Scan (-sI)                                │
│                                                               │
│  VULNERABILITY SCANNING:                                      │
│    [19] Vuln Script Scan (--script vuln)                      │
│    [20] Exploit Detection (--script exploit)                  │
│    [21] CVE Detection (--script vulners)                      │
│    [22] SMB Vulnerabilities                                   │
│    [23] Web Vulnerabilities                                   │
│    [24] Database Vulnerabilities                              │
│                                                               │
│  PROTOCOL SPECIFIC:                                           │
│    [25] TCP Connect Scan (-sT)                                │
│    [26] UDP Scan (-sU)                                        │
│    [27] SCTP Scan (-sY)                                       │
│    [28] TCP + UDP Combined                                    │
│                                                               │
│  SPECIALIZED SCANS:                                           │
│    [29] SMB Enumeration                                       │
│    [30] DNS Enumeration                                       │
│    [31] SSL/TLS Analysis                                      │
│    [32] HTTP Service Scan                                     │
│    [33] SSH Audit                                             │
│    [34] FTP Enumeration                                       │
│    [35] SNMP Enumeration                                      │
│                                                               │
│  PERFORMANCE OPTIONS:                                         │
│    [36] Fast Scan (T4)                                        │
│    [37] Insane Scan (T5)                                      │
│    [38] Slow/Paranoid (T0/T1)                                 │
│    [39] Normal Speed (T3)                                     │
│                                                               │
│  ADVANCED OPTIONS:                                            │
│    [40] Custom Script Scan                                    │
│    [41] Custom Port Range                                     │
│    [42] IPv6 Scan                                             │
│    [43] Custom Flags Builder                                  │
│                                                               │
│  NETWORK RANGE SCANS:                                         │
│    [44] Subnet Scan (CIDR)                                    │
│    [45] IP Range Scan                                         │
│    [46] Multiple Targets Scan                                 │
│                                                               │
│  OUTPUT & REPORTING:                                          │
│    [47] All Formats Output (Normal, XML, Grepable)            │
│    [48] XML Output Only                                       │
│    [49] Grepable Output                                       │
│                                                               │
│  COMPREHENSIVE SCANS:                                         │
│    [50] Full Network Audit (Everything)                       │
│    [51] Web Server Full Audit                                 │
│    [52] Internal Network Scan                                 │
│                                                               │
│  [0]  ← Back to Scanning Menu                                 │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
        """
        print("\033[92m" + menu + "\033[0m")
    
    def get_target(self):
        """Get target from user"""
        print("\n\033[93m" + "="*65 + "\033[0m")
        print("\033[96m[?] TARGET SPECIFICATION\033[0m")
        print("\033[93m" + "="*65 + "\033[0m")
        print("\nExamples:")
        print("  • Single IP:     192.168.1.1")
        print("  • Hostname:      scanme.nmap.org")
        print("  • CIDR:          192.168.1.0/24")
        print("  • Range:         192.168.1.1-50")
        print("  • Multiple:      192.168.1.1,192.168.1.5,192.168.1.10")
        
        target = input("\n[\033[94m?\033[0m] Enter target: ").strip()
        if target:
            self.target = target
            return True
        return False
    
    def get_output_file(self, scan_name):
        """Generate output filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_target = self.target.replace('/', '_').replace(':', '_').replace(',', '_')
        filename = f"{scan_name}_{safe_target}_{timestamp}"
        return self.output_dir / filename
    
    def execute_scan(self, command, scan_name):
        """Execute nmap command and save results"""
        print(f"\n\033[93m{'='*65}\033[0m")
        print(f"\033[96m[*] EXECUTING: {scan_name}\033[0m")
        print(f"\033[93m{'='*65}\033[0m")
        print(f"\n\033[96m[+] Target:\033[0m {self.target}")
        print(f"\033[96m[+] Command:\033[0m {command}")
        print(f"\n\033[93m[*] Scanning in progress...\033[0m\n")
        
        start_time = time.time()
        os.system(command)
        elapsed = time.time() - start_time
        
        print(f"\n\033[93m{'='*65}\033[0m")
        print(f"\033[92m[✓] Scan completed in {elapsed:.2f} seconds\033[0m")
        print(f"\033[93m{'='*65}\033[0m")
    
    def basic_scans(self, choice):
        """Handle basic scanning options"""
        output_base = self.get_output_file("basic")
        
        scans = {
            '1': ('Ping Sweep', f'nmap -sn {self.target} -oN {output_base}_ping.txt'),
            '2': ('Quick Scan - Top 100', f'nmap -T4 --top-ports 100 {self.target} -oN {output_base}_quick.txt'),
            '3': ('Top 1000 Ports', f'nmap -T4 --top-ports 1000 {self.target} -oN {output_base}_top1000.txt'),
            '4': ('Full Port Scan', f'nmap -p- -T4 {self.target} -oN {output_base}_fullscan.txt')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            self.execute_scan(cmd, name)
    
    def service_detection(self, choice):
        """Handle service detection scans"""
        output_base = self.get_output_file("service")
        
        scans = {
            '5': ('Service Version Detection', f'nmap -sV -T4 {self.target} -oN {output_base}_version.txt'),
            '6': ('Service + Scripts', f'nmap -sV -sC -T4 {self.target} -oN {output_base}_svc_script.txt'),
            '7': ('Aggressive Version Detection', f'nmap -sV --version-all -T4 {self.target} -oN {output_base}_aggressive_ver.txt')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            self.execute_scan(cmd, name)
    
    def os_fingerprint(self, choice):
        """Handle OS detection scans"""
        output_base = self.get_output_file("os")
        
        scans = {
            '8': ('OS Detection', f'sudo nmap -O -T4 {self.target} -oN {output_base}_os.txt'),
            '9': ('Aggressive Scan', f'sudo nmap -A -T4 {self.target} -oN {output_base}_aggressive.txt'),
            '10': ('Complete Fingerprint', f'sudo nmap -A -p- -T4 {self.target} -oN {output_base}_complete.txt')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            print("\033[93m[!] Note: OS detection requires root privileges\033[0m")
            self.execute_scan(cmd, name)
    
    def stealth_scans(self, choice):
        """Handle stealth and evasion scans"""
        output_base = self.get_output_file("stealth")
        
        scans = {
            '11': ('SYN Stealth Scan', f'sudo nmap -sS -T4 {self.target} -oN {output_base}_syn.txt'),
            '12': ('FIN Scan', f'sudo nmap -sF -T4 {self.target} -oN {output_base}_fin.txt'),
            '13': ('NULL Scan', f'sudo nmap -sN -T4 {self.target} -oN {output_base}_null.txt'),
            '14': ('XMAS Scan', f'sudo nmap -sX -T4 {self.target} -oN {output_base}_xmas.txt'),
            '15': ('ACK Scan', f'sudo nmap -sA -T4 {self.target} -oN {output_base}_ack.txt'),
            '16': ('Decoy Scan', f'sudo nmap -D RND:10 -T4 {self.target} -oN {output_base}_decoy.txt'),
            '17': ('Fragment Packets', f'sudo nmap -f -T4 {self.target} -oN {output_base}_fragment.txt'),
            '18': ('Idle/Zombie Scan', None)  # Requires zombie host
        }
        
        if choice == '18':
            zombie = input("[\033[94m?\033[0m] Enter zombie host IP: ").strip()
            if zombie:
                cmd = f'sudo nmap -sI {zombie} {self.target} -oN {output_base}_zombie.txt'
                self.execute_scan(cmd, 'Idle/Zombie Scan')
        elif choice in scans:
            name, cmd = scans[choice]
            if cmd:
                print("\033[93m[!] Note: Stealth scans require root privileges\033[0m")
                self.execute_scan(cmd, name)
    
    def vulnerability_scans(self, choice):
        """Handle vulnerability scanning options"""
        output_base = self.get_output_file("vuln")
        
        scans = {
            '19': ('Vulnerability Scripts', f'nmap --script vuln -T4 {self.target} -oN {output_base}_vuln.txt'),
            '20': ('Exploit Detection', f'nmap --script exploit -T4 {self.target} -oN {output_base}_exploit.txt'),
            '21': ('CVE Detection', f'nmap --script vulners -T4 {self.target} -oN {output_base}_cve.txt'),
            '22': ('SMB Vulnerabilities', f'nmap --script smb-vuln* -p445 {self.target} -oN {output_base}_smb_vuln.txt'),
            '23': ('Web Vulnerabilities', f'nmap --script http-vuln* -p80,443,8080 {self.target} -oN {output_base}_web_vuln.txt'),
            '24': ('Database Vulnerabilities', f'nmap --script "*vuln*" -p3306,5432,1433 {self.target} -oN {output_base}_db_vuln.txt')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            print("\033[93m[*] Vulnerability scanning may take several minutes...\033[0m")
            self.execute_scan(cmd, name)
    
    def protocol_scans(self, choice):
        """Handle protocol-specific scans"""
        output_base = self.get_output_file("protocol")
        
        scans = {
            '25': ('TCP Connect Scan', f'nmap -sT -T4 {self.target} -oN {output_base}_tcp.txt'),
            '26': ('UDP Scan', f'sudo nmap -sU --top-ports 100 {self.target} -oN {output_base}_udp.txt'),
            '27': ('SCTP Scan', f'sudo nmap -sY -T4 {self.target} -oN {output_base}_sctp.txt'),
            '28': ('TCP + UDP Combined', f'sudo nmap -sS -sU --top-ports 100 {self.target} -oN {output_base}_tcp_udp.txt')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            if choice in ['26', '27', '28']:
                print("\033[93m[!] Note: UDP/SCTP scans require root and take longer\033[0m")
            self.execute_scan(cmd, name)
    
    def specialized_scans(self, choice):
        """Handle specialized protocol scans"""
        output_base = self.get_output_file("specialized")
        
        scans = {
            '29': ('SMB Enumeration', f'nmap --script smb-enum-* -p445 {self.target} -oN {output_base}_smb.txt'),
            '30': ('DNS Enumeration', f'nmap --script dns-brute,dns-zone-transfer -p53 {self.target} -oN {output_base}_dns.txt'),
            '31': ('SSL/TLS Analysis', f'nmap --script ssl-enum-ciphers -p443 {self.target} -oN {output_base}_ssl.txt'),
            '32': ('HTTP Service Scan', f'nmap --script http-enum,http-headers -p80,443,8080 {self.target} -oN {output_base}_http.txt'),
            '33': ('SSH Audit', f'nmap --script ssh2-enum-algos,ssh-auth-methods -p22 {self.target} -oN {output_base}_ssh.txt'),
            '34': ('FTP Enumeration', f'nmap --script ftp-anon,ftp-bounce -p21 {self.target} -oN {output_base}_ftp.txt'),
            '35': ('SNMP Enumeration', f'nmap --script snmp-* -p161 {self.target} -oN {output_base}_snmp.txt')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            self.execute_scan(cmd, name)
    
    def performance_scans(self, choice):
        """Handle performance-tuned scans"""
        output_base = self.get_output_file("performance")
        
        scans = {
            '36': ('Fast Scan (T4)', f'nmap -T4 -F {self.target} -oN {output_base}_fast.txt'),
            '37': ('Insane Speed (T5)', f'nmap -T5 -F {self.target} -oN {output_base}_insane.txt'),
            '38': ('Slow/Paranoid (T0)', f'nmap -T0 --top-ports 100 {self.target} -oN {output_base}_slow.txt'),
            '39': ('Normal Speed (T3)', f'nmap -T3 {self.target} -oN {output_base}_normal.txt')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            self.execute_scan(cmd, name)
    
    def advanced_options(self, choice):
        """Handle advanced scanning options"""
        output_base = self.get_output_file("advanced")
        
        if choice == '40':
            print("\n\033[96m[*] Available script categories:\033[0m")
            print("  auth, broadcast, brute, default, discovery,")
            print("  dos, exploit, external, fuzzer, intrusive,")
            print("  malware, safe, version, vuln")
            scripts = input("\n[\033[94m?\033[0m] Enter script(s) or category: ").strip()
            if scripts:
                cmd = f'nmap --script {scripts} -T4 {self.target} -oN {output_base}_custom_script.txt'
                self.execute_scan(cmd, 'Custom Script Scan')
        
        elif choice == '41':
            ports = input("[\033[94m?\033[0m] Enter port range (e.g., 1-100, 80,443): ").strip()
            if ports:
                cmd = f'nmap -p{ports} -T4 {self.target} -oN {output_base}_custom_ports.txt'
                self.execute_scan(cmd, 'Custom Port Range')
        
        elif choice == '42':
            cmd = f'nmap -6 -T4 {self.target} -oN {output_base}_ipv6.txt'
            self.execute_scan(cmd, 'IPv6 Scan')
        
        elif choice == '43':
            self.custom_flags_builder(output_base)
    
    def custom_flags_builder(self, output_base):
        """Interactive custom scan builder"""
        print("\n\033[96m" + "="*65 + "\033[0m")
        print("\033[96m[*] CUSTOM SCAN BUILDER\033[0m")
        print("\033[96m" + "="*65 + "\033[0m")
        
        flags = []
        
        # Scan type
        print("\n[\033[94m1\033[0m] Scan Type:")
        print("  [a] SYN (-sS)  [b] Connect (-sT)  [c] UDP (-sU)  [d] SCTP (-sY)")
        scan_type = input("  Choice: ").strip().lower()
        scan_map = {'a': '-sS', 'b': '-sT', 'c': '-sU', 'd': '-sY'}
        if scan_type in scan_map:
            flags.append(scan_map[scan_type])
        
        # Port specification
        print("\n[\033[94m2\033[0m] Port Selection:")
        ports = input("  Enter ports (or press Enter for default): ").strip()
        if ports:
            flags.append(f'-p{ports}')
        
        # Timing
        print("\n[\033[94m3\033[0m] Timing Template:")
        print("  [0] Paranoid  [1] Sneaky  [2] Polite  [3] Normal  [4] Fast  [5] Insane")
        timing = input("  Choice: ").strip()
        if timing in '012345':
            flags.append(f'-T{timing}')
        
        # Service detection
        if input("\n[\033[94m4\033[0m] Enable service detection? (y/n): ").strip().lower() == 'y':
            flags.append('-sV')
        
        # OS detection
        if input("\n[\033[94m5\033[0m] Enable OS detection? (y/n): ").strip().lower() == 'y':
            flags.append('-O')
        
        # Scripts
        if input("\n[\033[94m6\033[0m] Run default scripts? (y/n): ").strip().lower() == 'y':
            flags.append('-sC')
        
        # Additional flags
        extra = input("\n[\033[94m7\033[0m] Additional flags (optional): ").strip()
        if extra:
            flags.append(extra)
        
        # Build and execute
        flag_str = ' '.join(flags)
        cmd = f'nmap {flag_str} {self.target} -oN {output_base}_custom.txt'
        
        print(f"\n\033[96m[+] Generated command:\033[0m {cmd}")
        if input("\n[\033[94m?\033[0m] Execute this scan? (y/n): ").strip().lower() == 'y':
            self.execute_scan(cmd, 'Custom Scan')
    
    def network_range_scans(self, choice):
        """Handle network range scans"""
        output_base = self.get_output_file("network")
        
        if choice == '44':
            # CIDR already in target
            cmd = f'nmap -sn {self.target} -oN {output_base}_subnet.txt'
            self.execute_scan(cmd, 'Subnet Scan')
        
        elif choice == '45':
            # Range already in target
            cmd = f'nmap -T4 {self.target} -oN {output_base}_range.txt'
            self.execute_scan(cmd, 'IP Range Scan')
        
        elif choice == '46':
            # Multiple targets
            cmd = f'nmap -T4 {self.target} -oN {output_base}_multiple.txt'
            self.execute_scan(cmd, 'Multiple Targets')
    
    def output_formats(self, choice):
        """Handle different output formats"""
        output_base = self.get_output_file("output")
        
        if choice == '47':
            cmd = f'nmap -T4 {self.target} -oN {output_base}.txt -oX {output_base}.xml -oG {output_base}.gnmap'
            self.execute_scan(cmd, 'All Formats Output')
        
        elif choice == '48':
            cmd = f'nmap -T4 {self.target} -oX {output_base}.xml'
            self.execute_scan(cmd, 'XML Output')
        
        elif choice == '49':
            cmd = f'nmap -T4 {self.target} -oG {output_base}.gnmap'
            self.execute_scan(cmd, 'Grepable Output')
    
    def comprehensive_scans(self, choice):
        """Handle comprehensive audit scans"""
        output_base = self.get_output_file("comprehensive")
        
        scans = {
            '50': ('Full Network Audit', 
                   f'sudo nmap -A -p- -T4 --script=default,vuln {self.target} -oN {output_base}_full_audit.txt'),
            '51': ('Web Server Full Audit', 
                   f'nmap -p80,443,8080,8443 -sV -sC --script=http-* {self.target} -oN {output_base}_web_audit.txt'),
            '52': ('Internal Network Scan', 
                   f'nmap -sS -sU -sV -O -T4 --top-ports 100 {self.target} -oN {output_base}_internal.txt')
        }
        
        if choice in scans:
            name, cmd = scans[choice]
            print("\033[93m[!] Warning: Comprehensive scans can take 30+ minutes\033[0m")
            if input("[\033[94m?\033[0m] Continue? (y/n): ").strip().lower() == 'y':
                self.execute_scan(cmd, name)
    
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
            
            choice = input("\n\033[93mNmap>\033[0m ").strip()
            
            if choice == '0':
                break
            
            # Route to appropriate handler
            if choice in ['1', '2', '3', '4']:
                self.basic_scans(choice)
            elif choice in ['5', '6', '7']:
                self.service_detection(choice)
            elif choice in ['8', '9', '10']:
                self.os_fingerprint(choice)
            elif choice in ['11', '12', '13', '14', '15', '16', '17', '18']:
                self.stealth_scans(choice)
            elif choice in ['19', '20', '21', '22', '23', '24']:
                self.vulnerability_scans(choice)
            elif choice in ['25', '26', '27', '28']:
                self.protocol_scans(choice)
            elif choice in ['29', '30', '31', '32', '33', '34', '35']:
                self.specialized_scans(choice)
            elif choice in ['36', '37', '38', '39']:
                self.performance_scans(choice)
            elif choice in ['40', '41', '42', '43']:
                self.advanced_options(choice)
            elif choice in ['44', '45', '46']:
                self.network_range_scans(choice)
            elif choice in ['47', '48', '49']:
                self.output_formats(choice)
            elif choice in ['50', '51', '52']:
                self.comprehensive_scans(choice)
            else:
                print("\033[91m[!] Invalid option\033[0m")
                time.sleep(1)
                continue
            
            input("\n\033[96m[*] Press Enter to continue...\033[0m")
            
            # Ask if want to scan another target
            if input("\n[\033[94m?\033[0m] Scan another target? (y/n): ").strip().lower() == 'y':
                self.target = None

def main():
    """Main entry point"""
    scanner = NmapScanner()
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