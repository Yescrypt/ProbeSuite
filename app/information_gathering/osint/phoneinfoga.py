# app/information_gathering/osint/phoneinfoga.py

import sys
import os
import re
import subprocess
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

class PhoneInfoga:
    """Professional Phone Number OSINT Tool"""
    
    def __init__(self):
        self.tool_path = self.check_installation()
    
    def check_installation(self):
        """Check if phoneinfoga is installed"""
        try:
            result = subprocess.run(['which', 'phoneinfoga'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None
    
    def validate_phone(self, phone):
        """Validate phone number format"""
        # Remove spaces, dashes, parentheses
        phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Check if it starts with + and has 10-15 digits
        if re.match(r'^\+?\d{10,15}$', phone):
            return phone
        return None
    
    def manual_search(self, phone):
        """Manual phone number analysis without external tool"""
        clear_screen()
        print_header("PHONE NUMBER ANALYSIS", 80)
        
        print(f"\n{C_OK}[*] Analyzing: {C_WARN}{phone}{C_RESET}\n")
        
        # Extract country code
        if phone.startswith('+'):
            country_codes = {
                '+1': 'USA/Canada',
                '+7': 'Russia/Kazakhstan',
                '+44': 'United Kingdom',
                '+49': 'Germany',
                '+33': 'France',
                '+86': 'China',
                '+81': 'Japan',
                '+91': 'India',
                '+998': 'Uzbekistan',
                '+996': 'Kyrgyzstan',
                '+992': 'Tajikistan',
                '+993': 'Turkmenistan',
                '+994': 'Azerbaijan',
            }
            
            for code, country in country_codes.items():
                if phone.startswith(code):
                    print(f"{C_OK}[+] Country Code: {C_INFO}{code} ({country}){C_RESET}")
                    break
        
        # Display search suggestions
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  SEARCH SUGGESTIONS                                                       ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        searches = [
            (f'Google Search', f'https://www.google.com/search?q="{phone}"'),
            (f'Reverse Phone Lookup', f'https://www.whitepages.com/phone/{phone}'),
            (f'TrueCaller', f'https://www.truecaller.com/search/{phone}'),
            (f'NumLookup', f'https://www.numlookup.com/?phone={phone}'),
            (f'Facebook Search', f'https://www.facebook.com/search/top?q={phone}'),
            (f'LinkedIn Search', f'https://www.linkedin.com/search/results/all/?keywords={phone}'),
            (f'Twitter Search', f'https://twitter.com/search?q={phone}'),
            (f'Instagram Search', f'https://www.instagram.com/explore/tags/{phone.replace("+", "")}'),
        ]
        
        for i, (name, url) in enumerate(searches, 1):
            print(f"{C_OK}{i}. {name:25}{C_RESET}")
            print(f"   {C_INFO}{url}{C_RESET}\n")
        
        # Google Dorks
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  GOOGLE DORKS FOR PHONE NUMBER                                            ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        dorks = [
            f'"{phone}"',
            f'"{phone}" site:linkedin.com',
            f'"{phone}" site:facebook.com',
            f'"{phone}" filetype:pdf',
            f'"{phone}" filetype:xlsx',
            f'"{phone}" intext:"contact" OR "phone"',
        ]
        
        for i, dork in enumerate(dorks, 1):
            print(f"{C_OK}{i}. {dork}{C_RESET}")
        
        # Save report
        self.save_report(phone, searches, dorks)
    
    def phoneinfoga_scan(self, phone):
        """Run phoneinfoga tool scan"""
        if not self.tool_path:
            Logger.warning("PhoneInfoga not installed!")
            print(f"\n{C_INFO}Install instructions:{C_RESET}")
            print(f"  1. Download from: https://github.com/sundowndev/phoneinfoga")
            print(f"  2. Install: go install github.com/sundowndev/phoneinfoga/v2@latest")
            print(f"  3. Or use Docker: docker pull sundowndev/phoneinfoga:latest\n")
            return False
        
        clear_screen()
        print_header("PHONEINFOGA SCAN", 80)
        
        print(f"\n{C_OK}[*] Scanning with PhoneInfoga: {C_WARN}{phone}{C_RESET}\n")
        
        try:
            # Run phoneinfoga scan
            cmd = ['phoneinfoga', 'scan', '-n', phone]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(result.stdout)
                Logger.success("Scan completed!")
                return True
            else:
                Logger.error(f"Scan failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            Logger.error("Scan timeout!")
            return False
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            return False
    
    def save_report(self, phone, searches, dorks):
        """Save analysis reports"""
        filename = f"reports/osint/phoneinfoga/phone_analysis_{phone.replace('+', '').replace(' ', '_')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("PHONE NUMBER OSINT REPORT\n")
                f.write("="*80 + "\n\n")
                f.write(f"Phone Number: {phone}\n")
                f.write(f"Generated: {os.popen('date').read()}\n")
                f.write("="*80 + "\n\n")
                
                f.write("SEARCH RESOURCES:\n")
                f.write("-"*80 + "\n")
                for name, url in searches:
                    f.write(f"\n{name}:\n{url}\n")
                
                f.write("\n\n" + "="*80 + "\n")
                f.write("GOOGLE DORKS:\n")
                f.write("-"*80 + "\n")
                for dork in dorks:
                    f.write(f"{dork}\n")
                
                f.write("\n" + "="*80 + "\n")
            
            Logger.success(f"Report saved: {filename}")
            
        except Exception as e:
            Logger.error(f"Failed to save report: {str(e)}")
    
    def display_menu(self):
        """Display phone search menu"""
        clear_screen()
        print_header("PHONE NUMBER OSINT", 80)
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  Phone number intelligence gathering tool. Supports international         ║{C_RESET}")
        print(f"{C_INFO}║  phone numbers with country codes.                                        ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        print(f"{C_OK}1. Manual Phone Analysis{C_RESET}     - Search suggestions & dorks")
        print(f"{C_OK}2. PhoneInfoga Scan{C_RESET}          - Automated tool scan")
        print(f"{C_OK}3. Batch Analysis{C_RESET}            - Multiple phone numbers")
        
        print(f"\n{C_WARN}0. Back{C_RESET}")
        print_footer()
    
    def batch_analysis(self):
        """Analyze multiple phone numbers"""
        clear_screen()
        print_header("BATCH PHONE ANALYSIS", 80)
        
        print(f"\n{C_INFO}Enter phone numbers (one per line, empty line to finish):{C_RESET}\n")
        
        phones = []
        while True:
            phone = input(f"{C_INFO}Phone #{len(phones)+1}: {C_RESET}").strip()
            if not phone:
                break
            
            validated = self.validate_phone(phone)
            if validated:
                phones.append(validated)
                Logger.success(f"Added: {validated}")
            else:
                Logger.warning(f"Invalid format: {phone}")
        
        if not phones:
            Logger.warning("No valid phone numbers!")
            return
        
        print(f"\n{C_OK}[*] Processing {len(phones)} phone number(s)...{C_RESET}\n")
        
        for i, phone in enumerate(phones, 1):
            print(f"\n{C_INFO}[{i}/{len(phones)}] Analyzing: {phone}{C_RESET}")
            self.manual_search(phone)
            
            if i < len(phones):
                input(f"\n{C_INFO}Press Enter for next...{C_RESET}")
        
        Logger.success("Batch analysis complete!")
    
    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            
            if choice == '1':
                # Manual analysis
                clear_screen()
                print_header("MANUAL PHONE ANALYSIS", 80)
                
                phone = input(f"\n{C_INFO}Enter phone number (with country code): {C_RESET}").strip()
                
                validated = self.validate_phone(phone)
                if not validated:
                    Logger.error("Invalid phone number format!")
                    Logger.info("Format: +1234567890 or +998901234567")
                    pause()
                    continue
                
                self.manual_search(validated)
                pause()
                
            elif choice == '2':
                # PhoneInfoga scan
                clear_screen()
                print_header("PHONEINFOGA SCAN", 80)
                
                phone = input(f"\n{C_INFO}Enter phone number: {C_RESET}").strip()
                
                validated = self.validate_phone(phone)
                if not validated:
                    Logger.error("Invalid phone number!")
                    pause()
                    continue
                
                self.phoneinfoga_scan(validated)
                pause()
                
            elif choice == '3':
                # Batch analysis
                self.batch_analysis()
                pause()
                
            else:
                Logger.error("Invalid choice!")
                pause()


def run_phoneinfoga():
    """Entry point"""
    tool = PhoneInfoga()
    tool.run()


if __name__ == "__main__":
    run_phoneinfoga()