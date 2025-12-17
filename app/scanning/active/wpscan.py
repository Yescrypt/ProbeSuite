#!/usr/bin/env python3
"""
ProBeSuite - WPScan Module
WordPress Security Scanner
"""

import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET, REPORTS_DIR
from app.utils import Logger, CommandRunner, InputValidator, clear_screen, pause


class WPScanner:
    def __init__(self):
        self.target = None
        self.output_dir = Path(REPORTS_DIR) / "scanning" / "active" / "wpscan"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║              🔍 WPSCAN - WORDPRESS SCANNER 🔍                ║
║             WordPress Security Assessment Tool               ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(f"{C_INFO}{banner}{C_RESET}")
    
    def show_menu(self):
        menu = """
╭─ WPSCAN OPTIONS ──────────────────────────────────────────────╮
│                                                               │
│  BASIC SCANS:                                                 │
│    [1]  Quick Scan (Basic enumeration)                        │
│    [2]  Standard Scan (Plugins + Themes)                      │
│    [3]  Aggressive Scan (Full enumeration)                    │
│                                                               │
│  ENUMERATION:                                                 │
│    [4]  Enumerate Users                                       │
│    [5]  Enumerate Plugins (All)                               │
│    [6]  Enumerate Vulnerable Plugins                          │
│    [7]  Enumerate Themes                                      │
│    [8]  Enumerate Timthumbs                                   │
│    [9]  Enumerate Config Backups                              │
│    [10] Enumerate DB Exports                                  │
│                                                               │
│  ADVANCED:                                                    │
│    [11] Password Attack (Brute Force)                         │
│    [12] Custom Scan (Manual options)                          │
│    [13] API Token Scan                                        │
│                                                               │
│  [0]  ← Back                                                  │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
        """
        print(f"{C_OK}{menu}{C_RESET}")
    
    def check_wpscan(self):
        """Check if WPScan is installed"""
        if not CommandRunner.check_tool('wpscan'):
            Logger.error("WPScan is not installed!")
            Logger.info("Install: gem install wpscan")
            Logger.info("Or: sudo apt install wpscan")
            return False
        return True
    
    def get_output_file(self, scan_type):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = self.target.replace('https://', '').replace('http://', '').replace('/', '_')
        return self.output_dir / f"{scan_type}_{domain}_{timestamp}.txt"
    
    def execute_scan(self, command, scan_name):
        print(f"\n{C_WARN}{'='*65}{C_RESET}")
        print(f"{C_INFO}[*] Executing: {scan_name}{C_RESET}")
        print(f"{C_WARN}{'='*65}{C_RESET}")
        print(f"\n{C_INFO}[+] Target: {self.target}{C_RESET}")
        print(f"{C_INFO}[+] Command: {command}{C_RESET}\n")
        
        Logger.warning("This may take several minutes...")
        
        returncode = CommandRunner.run_live(command, shell=True)
        
        if returncode == 0:
            Logger.success("Scan completed successfully!")
        else:
            Logger.error(f"Scan failed with code: {returncode}")
    
    def quick_scan(self):
        output = self.get_output_file("quick")
        cmd = f"wpscan --url {self.target} -o {output} --random-user-agent"
        self.execute_scan(cmd, "Quick Scan")
    
    def standard_scan(self):
        output = self.get_output_file("standard")
        cmd = f"wpscan --url {self.target} --enumerate p,t -o {output} --random-user-agent"
        self.execute_scan(cmd, "Standard Scan")
    
    def aggressive_scan(self):
        output = self.get_output_file("aggressive")
        cmd = f"wpscan --url {self.target} --enumerate ap,at,u,m -o {output} --plugins-detection aggressive --random-user-agent"
        self.execute_scan(cmd, "Aggressive Scan")
    
    def enumerate_users(self):
        output = self.get_output_file("users")
        cmd = f"wpscan --url {self.target} --enumerate u -o {output} --random-user-agent"
        self.execute_scan(cmd, "User Enumeration")
    
    def enumerate_plugins(self):
        output = self.get_output_file("plugins")
        cmd = f"wpscan --url {self.target} --enumerate ap --plugins-detection aggressive -o {output} --random-user-agent"
        self.execute_scan(cmd, "Plugin Enumeration")
    
    def enumerate_vulnerable_plugins(self):
        output = self.get_output_file("vuln_plugins")
        cmd = f"wpscan --url {self.target} --enumerate vp -o {output} --random-user-agent"
        self.execute_scan(cmd, "Vulnerable Plugins")
    
    def enumerate_themes(self):
        output = self.get_output_file("themes")
        cmd = f"wpscan --url {self.target} --enumerate at -o {output} --random-user-agent"
        self.execute_scan(cmd, "Theme Enumeration")
    
    def enumerate_timthumbs(self):
        output = self.get_output_file("timthumbs")
        cmd = f"wpscan --url {self.target} --enumerate tt -o {output} --random-user-agent"
        self.execute_scan(cmd, "Timthumb Enumeration")
    
    def enumerate_config_backups(self):
        output = self.get_output_file("config_backups")
        cmd = f"wpscan --url {self.target} --enumerate cb -o {output} --random-user-agent"
        self.execute_scan(cmd, "Config Backup Enumeration")
    
    def enumerate_db_exports(self):
        output = self.get_output_file("db_exports")
        cmd = f"wpscan --url {self.target} --enumerate dbe -o {output} --random-user-agent"
        self.execute_scan(cmd, "DB Export Enumeration")
    
    def password_attack(self):
        output = self.get_output_file("bruteforce")
        
        print(f"\n{C_INFO}[*] Password Attack Configuration{C_RESET}")
        username = input(f"{C_INFO}  Username (or leave empty to enumerate): {C_RESET}").strip()
        
        if not username:
            Logger.info("Enumerating users first...")
            cmd_enum = f"wpscan --url {self.target} --enumerate u --random-user-agent"
            os.system(cmd_enum)
            username = input(f"\n{C_INFO}  Enter username to attack: {C_RESET}").strip()
            if not username:
                Logger.error("Username required!")
                return
        
        wordlist = input(f"{C_INFO}  Wordlist path (default: rockyou.txt): {C_RESET}").strip()
        if not wordlist:
            wordlist = "/usr/share/wordlists/rockyou.txt"
        
        if not os.path.exists(wordlist):
            Logger.error(f"Wordlist not found: {wordlist}")
            return
        
        cmd = f"wpscan --url {self.target} -U {username} -P {wordlist} -o {output} --random-user-agent"
        
        Logger.warning("This may take a VERY long time!")
        if InputValidator.confirm("Start password attack?"):
            self.execute_scan(cmd, "Password Attack")
    
    def custom_scan(self):
        output = self.get_output_file("custom")
        
        print(f"\n{C_INFO}[*] Custom Scan Builder{C_RESET}")
        print(f"\n{C_INFO}Available enumeration options:{C_RESET}")
        print("  vp  - Vulnerable plugins")
        print("  ap  - All plugins")
        print("  p   - Popular plugins")
        print("  vt  - Vulnerable themes")
        print("  at  - All themes")
        print("  t   - Popular themes")
        print("  tt  - Timthumbs")
        print("  cb  - Config backups")
        print("  dbe - Db exports")
        print("  u   - Users")
        print("  m   - Media")
        
        enum_opts = input(f"\n{C_INFO}  Enter options (comma-separated): {C_RESET}").strip()
        
        additional = input(f"{C_INFO}  Additional WPScan flags (optional): {C_RESET}").strip()
        
        enum_flag = f"--enumerate {enum_opts}" if enum_opts else ""
        cmd = f"wpscan --url {self.target} {enum_flag} {additional} -o {output} --random-user-agent"
        
        self.execute_scan(cmd, "Custom Scan")
    
    def api_token_scan(self):
        output = self.get_output_file("api_scan")
        
        Logger.info("WPScan API provides vulnerability data")
        Logger.info("Get token from: https://wpscan.com/api")
        
        token = input(f"\n{C_INFO}  Enter API token: {C_RESET}").strip()
        if not token:
            Logger.warning("Scanning without API token (limited vulnerability data)")
            cmd = f"wpscan --url {self.target} --enumerate vp,vt -o {output} --random-user-agent"
        else:
            cmd = f"wpscan --url {self.target} --api-token {token} --enumerate vp,vt -o {output} --random-user-agent"
        
        self.execute_scan(cmd, "API Token Scan")
    
    def run(self):
        if not self.check_wpscan():
            pause()
            return
        
        while True:
            clear_screen()
            self.print_banner()
            
            if not self.target:
                self.target = InputValidator.get_url()
                if not self.target:
                    return
            
            print(f"{C_OK}[+] Target: {self.target}{C_RESET}\n")
            
            self.show_menu()
            choice = InputValidator.get_choice()
            
            if choice == '0':
                break
            elif choice == '1':
                self.quick_scan()
            elif choice == '2':
                self.standard_scan()
            elif choice == '3':
                self.aggressive_scan()
            elif choice == '4':
                self.enumerate_users()
            elif choice == '5':
                self.enumerate_plugins()
            elif choice == '6':
                self.enumerate_vulnerable_plugins()
            elif choice == '7':
                self.enumerate_themes()
            elif choice == '8':
                self.enumerate_timthumbs()
            elif choice == '9':
                self.enumerate_config_backups()
            elif choice == '10':
                self.enumerate_db_exports()
            elif choice == '11':
                self.password_attack()
            elif choice == '12':
                self.custom_scan()
            elif choice == '13':
                self.api_token_scan()
            else:
                Logger.error("Invalid option!")
                pause()
                continue
            
            pause()
            
            if InputValidator.confirm("Scan another target?"):
                self.target = None


def main():
    try:
        scanner = WPScanner()
        scanner.run()
    except KeyboardInterrupt:
        print(f"\n\n{C_ERR}[!] Interrupted by user{C_RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C_ERR}[!] Error: {e}{C_RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()