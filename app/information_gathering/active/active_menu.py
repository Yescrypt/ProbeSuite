# app/information_gathering/active/active_menu.py

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from app.config import C_TITLE, C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import Logger, print_header, print_footer, pause, clear_screen


class ActiveMenu:
    def __init__(self):
        self.tools = {
            '1': {
                'name': 'Nmap Scanner',
                'tool': 'Nmap',
                'status': 'Active',
                'function': self.run_nmap,
                'needs_target': False
            },
            '2': {
                'name': 'Nuclei Scanner',
                'tool': 'Nuclei',
                'status': 'Active',
                'function': self.run_nuclei,
                'needs_target': False
            },
            '3': {
                'name': 'Nikto Scanner',
                'tool': 'Nikto',
                'status': 'Active',
                'function': self.run_nikto,
                'needs_target': True
            },
            '4': {
                'name': 'Web Path Scanner',
                'tool': 'Dirsearch',
                'status': 'Active',
                'function': self.run_dirsearch,
                'needs_target': True
            },
            '5': {
                'name': 'Directory Bruteforcer',
                'tool': 'Gobuster',
                'status': 'Active',
                'function': self.run_gobuster,
                'needs_target': True
            },
            '6': {
                'name': 'Content Discovery',
                'tool': 'Feroxbuster',
                'status': 'Active',
                'function': self.run_feroxbuster,
                'needs_target': True
            },
            '7': {
                'name': 'Technology Fingerprint',
                'tool': 'WhatWeb',
                'status': 'Active',
                'function': self.run_whatweb,
                'needs_target': True
            },
            '8': {
                'name': 'Web Application Fuzzer',
                'tool': 'Wfuzz',
                'status': 'Active',
                'function': self.run_wfuzz,
                'needs_target': True
            },
            '9': {
                'name': 'Subdomain Discovery',
                'tool': 'Assetfinder',
                'status': 'Active',
                'function': self.run_assetfinder,
                'needs_target': True
            },
            '10': {
                'name': 'Fast Subdomain Finder',
                'tool': 'Findomain',
                'status': 'Active',
                'function': self.run_findomain,
                'needs_target': True
            },
            '11': {
                'name': 'OSINT Subdomain Enum',
                'tool': 'Sublist3r',
                'status': 'Active',
                'function': self.run_sublist3r,
                'needs_target': True
            },
            '12': {
                'name': 'DNS Information',
                'tool': 'DNSRecon',
                'status': 'Active',
                'function': self.run_dnsrecon,
                'needs_target': True
            },
        }

    def display_menu(self):
        clear_screen()
        
        # Header
        print(f"{C_INFO}╔══════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║{C_RESET}                    {C_OK}ACTIVE INFORMATION GATHERING MENU{C_RESET}                         {C_INFO}║{C_RESET}")
        print(f"{C_INFO}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        # Tools list
        for key, tool in sorted(self.tools.items(), key=lambda x: int(x[0])):
            # Status indicator
            status_color = C_OK if tool['status'] == 'Active' else C_ERR
            status = f"{status_color}● {tool['status']}{C_RESET}"
            
            # Format display
            tool_display = f"{tool['name']} ({tool['tool']})"
            
            # Calculate spacing for alignment
            # Key (2-3 chars) + ". " (2) + tool_display + spaces + status
            key_part = f"  {key}."
            spacing_needed = 65 - len(tool_display)
            
            print(f"{C_INFO}{key_part:5}{C_RESET} {C_OK}{tool['name']}{C_RESET} {C_WARN}({tool['tool']}){C_RESET}{' ' * spacing_needed}{status}")
        
        # Footer
        print(f"\n  {C_INFO}0.{C_RESET} {C_WARN}Back to Information Gathering menu{C_RESET}")
        print(f"{C_INFO}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}")

    def get_target(self):
        """Target olish"""
        print(f"\n{C_INFO}Enter target (domain/URL/IP):{C_RESET}")
        target = input(f"{C_OK}She11> {C_RESET}").strip()
        return target if target else None

    # ==================== TOOL WRAPPERS ====================

    def run_nmap(self, t):
        """Nmap Scanner"""
        from app.information_gathering.active.nmap_scanner import run_nmap_scanner
        run_nmap_scanner()

    def run_nuclei(self, t):
        """Nuclei Vulnerability Scanner"""
        from app.information_gathering.active.nuclei_scanner import run_nuclei_scanner
        run_nuclei_scanner()

    def run_nikto(self, t):
        """Nikto Web Server Scanner"""
        from app.information_gathering.active.nikto_scanner import run_nikto_scanner
        run_nikto_scanner(t.strip())

    def run_dirsearch(self, t):
        """Dirsearch Directory Scanner"""
        from app.information_gathering.active.dirsearch import run_dirsearch_scanner
        run_dirsearch_scanner(t)

    def run_gobuster(self, t):
        """Gobuster Directory/DNS Bruteforcer"""
        from app.information_gathering.active.gobuster import run_gobuster_scanner
        run_gobuster_scanner(t)

    def run_feroxbuster(self, t):
        """Feroxbuster Recursive Content Discovery"""
        from app.information_gathering.active.feroxbuster import run_feroxbuster_scanner
        run_feroxbuster_scanner(t)

    def run_whatweb(self, t):
        """WhatWeb Technology Identifier"""
        from app.information_gathering.active.whatweb import run_whatweb_scanner
        run_whatweb_scanner(t)

    def run_wfuzz(self, t):
        """Wfuzz Web Application Fuzzer"""
        from app.information_gathering.active.wfuzz import run_wfuzz_scanner
        run_wfuzz_scanner(t)

    def run_assetfinder(self, domain):
        """Assetfinder Subdomain Discovery"""
        from app.information_gathering.active.assetfinder import run_assetfinder_scanner
        clear_screen()
        run_assetfinder_scanner()

    def run_findomain(self, domain):
        """Findomain Fast Subdomain Finder"""
        from app.information_gathering.active.findomain import run_findomain_scanner
        run_findomain_scanner(domain)

    def run_sublist3r(self, domain):
        """Sublist3r OSINT Subdomain Enumeration"""
        from app.information_gathering.active.sublist3r import run_sublist3r_scanner
        run_sublist3r_scanner(domain)

    def run_dnsrecon(self, domain):
        """DNSRecon DNS Information Gathering"""
        from app.information_gathering.active.dnsrecon import run_dnsrecon_scanner
        run_dnsrecon_scanner(domain)

    # ==================== MAIN LOOP ====================
    def run(self):
        while True:
            self.display_menu()
            choice = input(f"{C_OK}She11> {C_RESET}").strip()

            if choice == "0":
                return
            
            if choice not in self.tools:
                Logger.error("Invalid selection!")
                time.sleep(1)
                continue

            tool = self.tools[choice]
            
            # Check if tool needs target
            if tool['needs_target']:
                target = self.get_target()
                if not target:
                    Logger.warning("Target not provided!")
                    time.sleep(1)
                    continue
                
                print(f"\n{C_OK}→ Launching {tool['tool']} on target: {C_WARN}{target}{C_RESET}\n")
                time.sleep(0.7)
                tool['function'](target)
            else:
                print(f"\n{C_OK}→ Launching {tool['tool']}...{C_RESET}\n")
                time.sleep(0.5)
                tool['function'](None)
            
            pause()


def run_active_menu():
    """Active menu wrapper"""
    ActiveMenu().run()


if __name__ == "__main__":
    run_active_menu()