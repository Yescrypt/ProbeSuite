# app/information_gathering/osint/osint_menu.py

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

# Import OSINT tools
from app.information_gathering.osint.google_dorking import run_google_dorking
from app.information_gathering.osint.phoneinfoga import run_phoneinfoga
from app.information_gathering.osint.holehe import run_holehe
from app.information_gathering.osint.ignorant import run_ignorant
from app.information_gathering.osint.sherlock import run_sherlock
from app.information_gathering.osint.maigret import run_maigret
from app.information_gathering.osint.blackbird import run_blackbird
from app.information_gathering.osint.inspy import run_inspy
from app.information_gathering.osint.exiftool import run_exiftool

class OSINTMenu:
    """Professional OSINT (Open Source Intelligence) Framework"""
    
    def __init__(self):
        self.tools = {
            '1': {
                'name': 'Google Dorking',
                'tool': 'Google Advanced Search',
                'status': 'Active',
                'function': run_google_dorking
            },
            '2': {
                'name': 'Phone Intelligence',
                'tool': 'PhoneInfoga',
                'status': 'Active',
                'function': run_phoneinfoga
            },
            '3': {
                'name': 'Email Discovery',
                'tool': 'Holehe',
                'status': 'Active',
                'function': run_holehe
            },
            '4': {
                'name': 'Email Validator',
                'tool': 'Ignorant',
                'status': 'Active',
                'function': run_ignorant
            },
            '5': {
                'name': 'Username Hunter',
                'tool': 'Sherlock',
                'status': 'Active',
                'function': run_sherlock
            },
            '6': {
                'name': 'Advanced Profiling',
                'tool': 'Maigret',
                'status': 'Active',
                'function': run_maigret
            },
            '7': {
                'name': 'Social Media Intel',
                'tool': 'BlackBird',
                'status': 'Active',
                'function': run_blackbird
            },
            '8': {
                'name': 'LinkedIn OSINT',
                'tool': 'InSpy',
                'status': 'Active',
                'function': run_inspy
            },
            '9': {
                'name': 'Metadata Extraction',
                'tool': 'ExifTool',
                'status': 'Active',
                'function': run_exiftool
            },
        }
    
    def display_menu(self):
        """Display OSINT menu"""
        clear_screen()
        
        # Header
        print(f"{C_INFO}╔══════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║{C_RESET}                  {C_OK}OSINT - OPEN SOURCE INTELLIGENCE MENU{C_RESET}                       {C_INFO}║{C_RESET}")
        print(f"{C_INFO}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        # Tools list
        for key, tool in sorted(self.tools.items()):
            # Status indicator
            status_color = C_OK if tool['status'] == 'Active' else C_ERR
            status = f"{status_color}● {tool['status']}{C_RESET}"
            
            # Tool name with proper spacing
            tool_display = f"{tool['name']} ({tool['tool']})"
            spacing = 62 - len(tool['name']) - len(tool['tool']) - 3  # -3 for parentheses and space
            
            print(f"  {C_INFO}{key}.{C_RESET} {C_OK}{tool['name']}{C_RESET} {C_WARN}({tool['tool']}){C_RESET}{' ' * spacing}{status}")
        
        # Footer
        print(f"\n  {C_INFO}0.{C_RESET} {C_WARN}Back to Information Gathering menu{C_RESET}")
        print(f"{C_INFO}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}")
    
    def run(self):
        """Main OSINT menu loop"""
        while True:
            self.display_menu()
            choice = input(f"{C_OK}She11> {C_RESET}").strip()
            
            if choice == '0':
                Logger.info("Returning to Information Gathering menu")
                return
            
            if choice not in self.tools:
                Logger.error("Invalid selection!")
                pause()
                continue
            
            tool = self.tools[choice]
            
            # Launch tool
            try:
                Logger.info(f"Launching {tool['tool']}...")
                print()  # Empty line for spacing
                tool['function']()
            except KeyboardInterrupt:
                Logger.warning(f"\n{tool['tool']} interrupted by user")
                pause()
            except Exception as e:
                Logger.error(f"Error running {tool['tool']}: {str(e)}")
                pause()


def run_osint_menu():
    """Entry point for OSINT menu"""
    menu = OSINTMenu()
    menu.run()


if __name__ == "__main__":
    run_osint_menu()