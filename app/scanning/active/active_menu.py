#!/usr/bin/env python3
"""
ProBeSuite - Active Scanning Menu
Integrated with existing framework structure
"""

import os
import sys
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import (
    C_OK, C_ERR, C_WARN, C_INFO, C_RESET, 
    REPORTS_DIR, TOOLS, NMAP_PROFILES
)
from app.utils import (
    Logger, CommandRunner, InputValidator,
    clear_screen, pause, print_header
)

class ActiveScanner:
    """Active reconnaissance and scanning"""
    
    def __init__(self):
        self.reports_dir = Path(REPORTS_DIR) / "scanning" / "active"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def print_banner(self):
        """Display active scanning banner"""
        banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║        🔍 ACTIVE SCANNING & ENUMERATION 🔍            ║
    ║              Professional Port Scanner                ║
    ╚═══════════════════════════════════════════════════════╝
        """
        print(f"{C_INFO}{banner}{C_RESET}")
    
    def show_menu(self):
        """Display main menu"""
        menu = """
    ┌─ ACTIVE SCANNING ────────────────────────────────────┐
    │                                                      │
    │  PROFESSIONAL SCANNERS:                              │
    │    [1]  Nmap Advanced - Professional Scanner         │
    │    [2]  Masscan - Ultra-Fast Scanner                 │
    │                                                      │
    │  QUICK NMAP SCANS:                                   │
    │    [3]  Light Scan (Top 1000 ports + Vuln)           │
    │    [4]  Medium Scan (Full service detection)         │
    │    [5]  Aggressive Scan (All ports + Scripts)        │
    │    [6]  Stealth Scan (SYN scan, slow)                │
    │                                                      │
    │  WEB APPLICATION:                                    │
    │    [7]  WPScan - WordPress Scanner                   │
    │    [8]  Nikto - Web Server Scanner                   │
    │    [9]  Gobuster - Directory Enumeration             │
    │                                                      │
    │  GUI TOOLS:                                          │
    │    [10] Zenmap - Nmap GUI                            │
    │    [11] Angry IP Scanner                             │
    │                                                      │
    │  [0]  ← Back to Main Menu                            │
    │                                                      │
    └──────────────────────────────────────────────────────┘
        """
        print(f"{C_OK}{menu}{C_RESET}")
    
    def get_output_file(self, scan_type, target):
        """Generate output filename"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_target = target.replace('/', '_').replace(':', '_').replace('.', '_')
        
        scan_dir = self.reports_dir / scan_type
        scan_dir.mkdir(exist_ok=True)
        
        filename = f"{safe_target}_{timestamp}.txt"
        return scan_dir / filename
    
    def run_nmap_profile(self, target, profile_name):
        """Run Nmap with predefined profile"""
        if profile_name not in NMAP_PROFILES:
            Logger.error(f"Unknown profile: {profile_name}")
            return
        
        flags = NMAP_PROFILES[profile_name]
        output_file = self.get_output_file("nmap", target)
        
        Logger.info(f"Running Nmap {profile_name} scan...")
        Logger.info(f"Target: {target}")
        Logger.info(f"Flags: {flags}")
        
        # Check if nmap is installed
        if not CommandRunner.check_tool('nmap'):
            Logger.error("Nmap is not installed!")
            Logger.info("Install: sudo apt install nmap")
            return
        
        # Build command
        cmd = f"nmap {flags} {target} -oN {output_file}"
        
        print(f"\n{C_WARN}[*] Executing: {cmd}{C_RESET}\n")
        
        # Run scan
        result = os.system(cmd)
        
        if result == 0:
            Logger.success(f"Scan completed successfully!")
            Logger.success(f"Results saved to: {output_file}")
        else:
            Logger.error(f"Scan failed with exit code: {result}")
    
    def run_nmap_advanced(self):
        """Launch advanced Nmap scanner"""
        try:
            from scanning.active.nmap_advenced import NmapScanner
            scanner = NmapScanner()
            scanner.run()
        except ImportError:
            Logger.error("Nmap Advanced module not found!")
            Logger.info("Using basic Nmap instead...")
            
            target = InputValidator.get_ip()
            if not target:
                return
            
            self.show_nmap_profiles()
            choice = input(f"{C_INFO}Choose profile (1-5): {C_RESET}").strip()
            
            profiles = {
                '1': 'light',
                '2': 'medium',
                '3': 'aggressive',
                '4': 'stealth'
            }
            
            if choice == '5':
                custom_flags = input(f"{C_INFO}Enter custom Nmap flags: {C_RESET}").strip()
                output_file = self.get_output_file("nmap", target)
                cmd = f"nmap {custom_flags} {target} -oN {output_file}"
                os.system(cmd)
            elif choice in profiles:
                self.run_nmap_profile(target, profiles[choice])
    
    def show_nmap_profiles(self):
        """Display Nmap profile options"""
        print(f"\n{C_INFO}    Select Nmap profile:{C_RESET}")
        print(f"      [1]  Light ({NMAP_PROFILES['light']})")
        print(f"      [2]  Medium ({NMAP_PROFILES['medium']})")
        print(f"      [3]  Aggressive ({NMAP_PROFILES['aggressive']})")
        print(f"      [4]  Stealth ({NMAP_PROFILES['stealth']})")
        print(f"      [5]  Custom (enter your options)")
    
    def run_masscan(self):
        """Launch Masscan scanner"""
        try:
            from scanning.active.masscan import MasscanScanner
            scanner = MasscanScanner()
            scanner.run()
        except ImportError:
            Logger.error("Masscan module not found!")
            Logger.info("Using basic Masscan instead...")
            
            target = InputValidator.get_ip()
            if not target:
                return
            
            ports = input(f"{C_INFO}Port range (default: 1-1000): {C_RESET}").strip() or "1-1000"
            rate = input(f"{C_INFO}Scan rate (default: 1000 pps): {C_RESET}").strip() or "1000"
            
            output_file = self.get_output_file("masscan", target)
            
            if not CommandRunner.check_tool('masscan'):
                Logger.error("Masscan is not installed!")
                Logger.info("Install from: https://github.com/robertdavidgraham/masscan")
                return
            
            cmd = f"sudo masscan {target} -p{ports} --rate={rate} -oL {output_file}"
            
            Logger.info("Running Masscan...")
            print(f"\n{C_WARN}[*] Executing: {cmd}{C_RESET}\n")
            
            result = os.system(cmd)
            
            if result == 0:
                Logger.success(f"Scan completed!")
                Logger.success(f"Results: {output_file}")
    
    def run_wpscan(self):
        """Run WPScan"""
        target = InputValidator.get_url()
        if not target:
            return
        
        if not CommandRunner.check_tool('wpscan'):
            Logger.error("WPScan is not installed!")
            Logger.info("Install: gem install wpscan")
            return
        
        output_file = self.get_output_file("wpscan", target)
        
        Logger.info("WPScan - WordPress Security Scanner")
        print(f"\n{C_INFO}Enumeration options:{C_RESET}")
        print("  [1] Basic scan")
        print("  [2] Enumerate users")
        print("  [3] Enumerate plugins")
        print("  [4] Enumerate themes")
        print("  [5] Full enumeration")
        
        choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
        
        enum_flags = {
            '1': '',
            '2': '--enumerate u',
            '3': '--enumerate p',
            '4': '--enumerate t',
            '5': '--enumerate u,p,t'
        }
        
        flags = enum_flags.get(choice, '')
        cmd = f"wpscan --url {target} {flags} --output {output_file}"
        
        Logger.info("Running WPScan...")
        print(f"\n{C_WARN}[*] Executing: {cmd}{C_RESET}\n")
        
        os.system(cmd)
        Logger.success(f"Results saved to: {output_file}")
    
    def run_nikto(self):
        """Run Nikto web scanner"""
        target = InputValidator.get_url()
        if not target:
            return
        
        if not CommandRunner.check_tool('nikto'):
            Logger.error("Nikto is not installed!")
            Logger.info("Install: sudo apt install nikto")
            return
        
        output_file = self.get_output_file("nikto", target)
        
        port = input(f"{C_INFO}Port (default: 80): {C_RESET}").strip() or "80"
        ssl = input(f"{C_INFO}Use SSL? (y/n): {C_RESET}").strip().lower() == 'y'
        
        ssl_flag = '-ssl' if ssl else ''
        cmd = f"nikto -h {target} -p {port} {ssl_flag} -output {output_file}"
        
        Logger.info("Running Nikto...")
        print(f"\n{C_WARN}[*] Executing: {cmd}{C_RESET}\n")
        
        os.system(cmd)
        Logger.success(f"Results saved to: {output_file}")
    
    def run_gobuster(self):
        """Run Gobuster"""
        target = InputValidator.get_url()
        if not target:
            return
        
        if not CommandRunner.check_tool('gobuster'):
            Logger.error("Gobuster is not installed!")
            Logger.info("Install: sudo apt install gobuster")
            return
        
        output_file = self.get_output_file("gobuster", target)
        
        print(f"\n{C_INFO}Mode selection:{C_RESET}")
        print("  [1] Directory brute force")
        print("  [2] DNS subdomain enumeration")
        print("  [3] Virtual host discovery")
        
        mode = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
        
        if mode == '1':
            wordlist = input(f"{C_INFO}Wordlist (default: common.txt): {C_RESET}").strip()
            wordlist = wordlist or "/usr/share/wordlists/dirb/common.txt"
            cmd = f"gobuster dir -u {target} -w {wordlist} -o {output_file}"
        
        elif mode == '2':
            wordlist = input(f"{C_INFO}Wordlist path: {C_RESET}").strip()
            wordlist = wordlist or "/usr/share/wordlists/amass/subdomains-top1mil-5000.txt"
            cmd = f"gobuster dns -d {target} -w {wordlist} -o {output_file}"
        
        elif mode == '3':
            wordlist = input(f"{C_INFO}Wordlist path: {C_RESET}").strip()
            if not wordlist:
                Logger.error("Wordlist required for vhost mode!")
                return
            cmd = f"gobuster vhost -u {target} -w {wordlist} -o {output_file}"
        else:
            Logger.error("Invalid mode!")
            return
        
        Logger.info("Running Gobuster...")
        print(f"\n{C_WARN}[*] Executing: {cmd}{C_RESET}\n")
        
        os.system(cmd)
        Logger.success(f"Results saved to: {output_file}")
    
    def launch_zenmap(self):
        """Launch Zenmap GUI"""
        if not CommandRunner.check_tool('zenmap'):
            Logger.error("Zenmap is not installed!")
            Logger.info("Install: sudo apt install zenmap")
            return
        
        Logger.info("Launching Zenmap GUI...")
        os.system('zenmap &')
    
    def launch_angry_ip(self):
        """Launch Angry IP Scanner"""
        if not CommandRunner.check_tool('ipscan'):
            Logger.error("Angry IP Scanner is not installed!")
            Logger.info("Download from: https://angryip.org")
            return
        
        Logger.info("Launching Angry IP Scanner...")
        os.system('ipscan &')
    
    def run(self):
        """Main menu loop"""
        while True:
            clear_screen()
            self.print_banner()
            self.show_menu()
            
            choice = InputValidator.get_choice()
            
            if choice == '0':
                break
            
            elif choice == '1':
                self.run_nmap_advanced()
                pause()
            
            elif choice == '2':
                self.run_masscan()
                pause()
            
            elif choice == '3':
                target = InputValidator.get_ip()
                if target:
                    self.run_nmap_profile(target, 'light')
                pause()
            
            elif choice == '4':
                target = InputValidator.get_ip()
                if target:
                    self.run_nmap_profile(target, 'medium')
                pause()
            
            elif choice == '5':
                target = InputValidator.get_ip()
                if target:
                    self.run_nmap_profile(target, 'aggressive')
                pause()
            
            elif choice == '6':
                target = InputValidator.get_ip()
                if target:
                    self.run_nmap_profile(target, 'stealth')
                pause()
            
            elif choice == '7':
                self.run_wpscan()
                pause()
            
            elif choice == '8':
                self.run_nikto()
                pause()
            
            elif choice == '9':
                self.run_gobuster()
                pause()
            
            elif choice == '10':
                self.launch_zenmap()
                pause()
            
            elif choice == '11':
                self.launch_angry_ip()
                pause()
            
            else:
                Logger.error("Invalid option!")
                pause()

def main():
    """Entry point"""
    try:
        scanner = ActiveScanner()
        scanner.run()
    except KeyboardInterrupt:
        print(f"\n\n{C_ERR}[!] Interrupted by user{C_RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C_ERR}[!] Error: {e}{C_RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()