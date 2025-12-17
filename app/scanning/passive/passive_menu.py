#!/usr/bin/env python3
"""
ProBeSuite - Passive Information Gathering Menu
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET
from app.utils import Logger, InputValidator, clear_screen, pause


def run_passive_menu():
    """Passive information gathering menu"""
    while True:
        clear_screen()
        
        print(f"{C_INFO}")
        print("╔═══════════════════════════════════════════════════════╗")
        print("║    PASSIVE INFORMATION GATHERING                     ║")
        print("╚═══════════════════════════════════════════════════════╝")
        print(f"{C_RESET}\n")
        
        print(f"{C_OK}┌─ PASSIVE RECON ─────────────────────────────────────┐{C_RESET}")
        print(f"{C_INFO}  [1]  WHOIS Lookup{C_RESET}")
        print(f"{C_INFO}  [2]  DNS Records{C_RESET}")
        print(f"{C_INFO}  [3]  Subdomain Enumeration{C_RESET}")
        print(f"{C_INFO}  [4]  Certificate Transparency{C_RESET}")
        print(f"{C_INFO}  [5]  Google Dorking{C_RESET}")
        print(f"{C_INFO}  [6]  Archive.org Lookup{C_RESET}")
        print(f"{C_WARN}  [0]  Back{C_RESET}")
        print(f"{C_OK}└─────────────────────────────────────────────────────┘{C_RESET}\n")
        
        choice = InputValidator.get_choice()
        
        if choice == '0':
            break
        elif choice in ['1', '2', '3', '4', '5', '6']:
            Logger.warning("Module under development")
            pause()
        else:
            Logger.error("Invalid choice!")
            pause()


if __name__ == "__main__":
    run_passive_menu()