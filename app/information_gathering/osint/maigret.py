import sys
import os
import subprocess
import threading
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

class Maigret:
    """Professional Multi-Search OSINT Tool"""
    
    def __init__(self):
        self.tool_path = self.check_installation()
        self.reports_dir = "reports/osint/maigret"
        self.scanning = False
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def check_installation(self):
        """Check if maigret is installed"""
        try:
            result = subprocess.run(['which', 'maigret'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def display_menu(self):
        """Display maigret menu"""
        clear_screen()
        print_header("MAIGRET - ADVANCED MULTI-SEARCH OSINT", 80)
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  Maigret collects dossiers about people by username across 2500+ sites.   ║{C_RESET}")
        print(f"{C_INFO}║  More powerful than Sherlock with advanced filtering and reporting.       ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        print(f"{C_OK}1. Username Hunt{C_RESET}             - Search 2500+ sites by username")
        print(f"{C_OK}2. Email Pattern Search{C_RESET}      - Find email-related accounts")
        print(f"{C_OK}3. Advanced Dossier{C_RESET}          - Comprehensive profile building")
        print(f"{C_OK}4. Manual Search Guide{C_RESET}       - Manual investigation guide")
        
        print(f"\n{C_WARN}0. Back{C_RESET}")
        print_footer()
    
    def loading_animation(self):
        """Display loading animation while scanning"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        idx = 0
        while self.scanning:
            print(f"\r{C_INFO}[{frames[idx]}] Scanning... Please wait...{C_RESET}", end='', flush=True)
            idx = (idx + 1) % len(frames)
            time.sleep(0.1)
        print(f"\r{' ' * 50}\r", end='', flush=True)  # Clear line
    
    def username_hunt(self, username):
        """Search username - direct terminal execution with detailed TXT reporting"""
        
        if not self.tool_path:
            Logger.warning("Maigret not installed!")
            print(f"\n{C_INFO}Installation:{C_RESET}")
            print(f"  pip3 install maigret\n")
            self.manual_username_search(username)
            return
        
        clear_screen()
        print_header("MAIGRET USERNAME HUNT", 80)
        
        print(f"\n{C_OK}[*] Target: {C_WARN}{username}{C_RESET}\n")
        
        # Scan options menu
        print(f"{C_INFO}Scan Options:{C_RESET}")
        print(f"  {C_OK}1.{C_RESET} Quick Scan (Top 500 sites) - Fast")
        print(f"  {C_OK}2.{C_RESET} Full Scan (All 2500+ sites) - Comprehensive")
        print(f"  {C_OK}3.{C_RESET} Custom Timeout (Default: 10s)")
        
        option = input(f"\n{C_INFO}Choose option [1]: {C_RESET}").strip() or '1'
        
        # Build command
        cmd = ['maigret', username]
        
        if option == '2':
            cmd.append('-a')  # All sites
            Logger.info("Full scan selected (2500+ sites)")
        elif option == '3':
            timeout = input(f"{C_INFO}Enter timeout in seconds [10]: {C_RESET}").strip() or '10'
            cmd.extend(['--timeout', timeout])
            Logger.info(f"Custom timeout: {timeout}s")
        else:
            cmd.extend(['--timeout', '10'])
            Logger.info("Quick scan selected (Top 500 sites)")
        
        print(f"\n{C_INFO}═══════════════════════════════════════════════════════════════════════════{C_RESET}\n")
        input(f"{C_WARN}Press Enter to start scan...{C_RESET}")
        print()
        
        try:
            # Start loading animation in separate thread
            self.scanning = True
            loader_thread = threading.Thread(target=self.loading_animation)
            loader_thread.daemon = True
            loader_thread.start()
            
            # Run maigret and capture output for report
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            
            # Stop animation
            self.scanning = False
            loader_thread.join(timeout=0.5)
            
            # Display results with colors intact (parse and reformat)
            print(f"\n{C_INFO}═══════════════════════════════════════════════════════════════════════════{C_RESET}\n")
            self.display_colored_results(result.stdout)
            
            print(f"\n{C_INFO}═══════════════════════════════════════════════════════════════════════════{C_RESET}\n")
            
            # Ask if user wants TXT report
            save = input(f"{C_INFO}Generate detailed TXT report? (y/n): {C_RESET}").strip().lower()
            
            if save == 'y':
                txt_path = os.path.join(self.reports_dir, f"report_{username}.txt")
                self.create_detailed_txt_report(username, result.stdout, txt_path)
            else:
                Logger.info("Report skipped")
                
        except KeyboardInterrupt:
            self.scanning = False
            print(f"\n\n{C_WARN}[!] Scan interrupted{C_RESET}")
        except Exception as e:
            self.scanning = False
            Logger.error(f"Error: {str(e)}")

    def display_colored_results(self, output):
        """Display results with colored formatting"""
        for line in output.split('\n'):
            # Skip progress and noise
            if any(x in line for x in ['Searching |', '▁▃▅', '▂▄▆', 'in 0s', '[0%]', '[1%]']):
                continue
            
            line = line.strip()
            if not line:
                continue
            
            # Color formatting
            if line.startswith('[+]'):
                print(f"{C_OK}{line}{C_RESET}")
            elif line.startswith('[-]'):
                if 'Starting' in line or 'Extracted' in line or 'report' in line:
                    print(f"{C_INFO}{line}{C_RESET}")
            elif line.startswith('[!]'):
                if 'You can run' not in line:
                    print(f"{C_WARN}{line}{C_RESET}")
            elif line.startswith('[*]'):
                print(f"{C_INFO}{line}{C_RESET}")
            elif '├─' in line or '└─' in line:
                print(f"{C_INFO}    {line}{C_RESET}")
            else:
                # Other informational lines
                if any(x in line for x in ['Countries:', 'Interests', 'Search by', 'Extended']):
                    print(f"{C_INFO}{line}{C_RESET}")
    
    def create_detailed_txt_report(self, username, output_text, txt_path):
        """Create detailed TXT report with styled header and parsed results"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Parse output for profiles with ALL details
            profiles = []
            current_profile = None
            stats = {
                'total_accounts': 0,
                'extended_info': 0,
                'countries': [],
                'tags': []
            }
            
            lines = output_text.split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # Parse statistics
                if 'returned' in line and 'accounts' in line:
                    try:
                        stats['total_accounts'] = int(line.split('returned')[1].split('accounts')[0].strip())
                    except:
                        pass
                
                if 'Extended info extracted' in line:
                    try:
                        stats['extended_info'] = int(line.split('from')[1].split('accounts')[0].strip())
                    except:
                        pass
                
                if line.startswith('Countries:'):
                    stats['countries'] = [c.strip() for c in line.replace('Countries:', '').split(',')]
                
                if line.startswith('Interests (tags):'):
                    stats['tags'] = [t.strip() for t in line.replace('Interests (tags):', '').split(',')]
                
                # Detect profile line [+] Platform: URL
                if line.startswith('[+]'):
                    if current_profile:
                        profiles.append(current_profile)
                    
                    # Parse platform and URL
                    parts = line[3:].split(':', 1)
                    if len(parts) >= 2:
                        platform = parts[0].strip()
                        url = ':'.join(parts[1:]).strip()
                        current_profile = {
                            'platform': platform,
                            'url': url,
                            'details': []
                        }
                
                # Parse all detail lines (├─, └─, or indented lines after [+])
                elif current_profile:
                    # Check if this is a detail line
                    if ('├─' in line or '└─' in line or 
                        (line and not line.startswith('[') and i > 0 and 
                         (lines[i-1].strip().startswith('[+]') or '├─' in lines[i-1] or '└─' in lines[i-1]))):
                        
                        # Clean the line
                        detail = line.replace('├─', '').replace('└─', '').strip()
                        
                        if detail and not any(x in detail for x in ['Searching', 'in 0s', '[0%]']):
                            current_profile['details'].append(detail)
                
                i += 1
            
            # Add last profile
            if current_profile:
                profiles.append(current_profile)
            
            # Write styled report
            with open(txt_path, 'w', encoding='utf-8') as f:
                # Styled Header
                f.write("=" * 80 + "\n")
                f.write(" " * 20 + "MAIGRET USERNAME HUNT — ProbeSuite\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Target Username: {username}\n")
                f.write(f"Scan Date: {timestamp}\n")
                f.write(f"Command: maigret {username} --timeout 10\n")
                f.write("\n" + "=" * 80 + "\n\n")
                
                # Summary Statistics
                total_found = len(profiles)
                f.write(f"SCAN STATISTICS\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total Accounts Found: {stats.get('total_accounts', total_found)}\n")
                f.write(f"Profiles with Extended Info: {stats.get('extended_info', 0)}\n")
                
                if stats['countries']:
                    f.write(f"Countries: {', '.join(stats['countries'])}\n")
                
                if stats['tags']:
                    f.write(f"Interest Tags: {', '.join(stats['tags'])}\n")
                
                f.write("\n" + "=" * 80 + "\n\n")
                
                if total_found == 0:
                    f.write("No profiles found for this username.\n\n")
                else:
                    f.write(f"FOUND PROFILES ({total_found})\n")
                    f.write("=" * 80 + "\n\n")
                    
                    # Write each profile with ALL details
                    for idx, profile in enumerate(profiles, 1):
                        f.write(f"[{idx}] {profile['platform']}\n")
                        f.write(f"    URL: {profile['url']}\n")
                        
                        # Write ALL extended information
                        if profile['details']:
                            f.write(f"\n    Extended Information:\n")
                            f.write(f"    {'-' * 70}\n")
                            for detail in profile['details']:
                                f.write(f"    {detail}\n")
                        
                        f.write("\n")
                
                # Footer
                f.write("=" * 80 + "\n")
                f.write(f"Report saved to: {txt_path}\n")
                f.write("=" * 80 + "\n")
            
            Logger.success(f"TXT report saved: {txt_path}")
            
        except Exception as e:
            Logger.error(f"Failed to create report: {str(e)}")
    
    def email_pattern_search(self, email):
        """Email pattern analysis with username search"""
        try:
            username = email.split('@')[0]
            domain = email.split('@')[1]
        except:
            Logger.error("Invalid email format!")
            return
        
        while True:  # Loop to stay in this menu
            clear_screen()
            print_header("EMAIL PATTERN SEARCH", 80)
            
            print(f"\n{C_OK}[*] Analyzing: {C_WARN}{email}{C_RESET}\n")
            
            print(f"{C_INFO}Email Components:{C_RESET}")
            print(f"  Username: {C_OK}{username}{C_RESET}")
            print(f"  Domain:   {C_OK}{domain}{C_RESET}\n")
            
            print(f"{C_INFO}What would you like to do?{C_RESET}")
            print(f"  {C_OK}1.{C_RESET} Search username '{username}' on Maigret (Recommended)")
            print(f"  {C_OK}2.{C_RESET} Generate manual investigation guide")
            print(f"  {C_OK}3.{C_RESET} Show Google search queries")
            print(f"  {C_WARN}0.{C_RESET} Back to Main Menu")
            
            choice = input(f"\n{C_INFO}Choose option: {C_RESET}").strip()
            
            if choice == '0':
                break  # Exit loop and return to main menu
            elif choice == '1':
                # Automatically run Maigret username search
                Logger.info(f"Searching for username: {username}")
                time.sleep(1)
                self.username_hunt(username)
                pause()  # Wait before returning to this menu
            elif choice == '2':
                # Generate investigation guide
                self.manual_username_search(username)
                pause()
            elif choice == '3':
                # Show Google search queries
                clear_screen()
                print_header("GOOGLE SEARCH QUERIES", 80)
                print(f"\n{C_INFO}Copy and paste these queries into Google:{C_RESET}\n")
                print(f"{C_OK}  • \"{email}\"{C_RESET}")
                print(f"{C_OK}  • \"{username}\" email{C_RESET}")
                print(f"{C_OK}  • site:linkedin.com \"{email}\"{C_RESET}")
                print(f"{C_OK}  • site:twitter.com \"{email}\"{C_RESET}")
                print(f"{C_OK}  • site:github.com \"{email}\"{C_RESET}")
                print(f"{C_OK}  • \"{email}\" profile{C_RESET}")
                print(f"{C_OK}  • \"{email}\" contact{C_RESET}\n")
                pause()
            else:
                Logger.error("Invalid option!")
                time.sleep(1)
    
    def advanced_dossier(self, target):
        """Build comprehensive dossier with interactive data collection"""
        
        while True:  # Loop to stay in this menu
            clear_screen()
            print_header("ADVANCED DOSSIER BUILDER", 80)
            
            print(f"\n{C_OK}[*] Building dossier for: {C_WARN}{target}{C_RESET}\n")
            
            print(f"{C_INFO}Dossier Options:{C_RESET}")
            print(f"  {C_OK}1.{C_RESET} Auto-collect from Maigret + Generate Report")
            print(f"  {C_OK}2.{C_RESET} View Investigation Template Guide")
            print(f"  {C_WARN}0.{C_RESET} Back to Main Menu")
            
            choice = input(f"\n{C_INFO}Choose option: {C_RESET}").strip()
            
            if choice == '0':
                break  # Exit loop and return to main menu
            elif choice == '1':
                # Run comprehensive Maigret search and auto-generate dossier
                Logger.info("Running comprehensive OSINT collection...")
                print(f"\n{C_INFO}This will:{C_RESET}")
                print(f"  • Search username '{target}' on 2500+ platforms")
                print(f"  • Collect all available profile data")
                print(f"  • Generate comprehensive dossier report\n")
                
                proceed = input(f"{C_WARN}Proceed? (y/n): {C_RESET}").strip().lower()
                if proceed == 'y':
                    self.auto_generate_dossier(target)
                pause()
            elif choice == '2':
                # Show investigation template guide
                self.show_investigation_guide(target)
                pause()
            else:
                Logger.error("Invalid option!")
                time.sleep(1)
    
    def auto_generate_dossier(self, target):
        """Auto-generate comprehensive dossier from Maigret results"""
        clear_screen()
        print_header("AUTO-GENERATING DOSSIER", 80)
        
        print(f"\n{C_INFO}[*] Step 1: Running Maigret scan...{C_RESET}\n")
        
        # Build command
        cmd = ['maigret', target, '--timeout', '10']
        
        try:
            # Start loading animation
            self.scanning = True
            loader_thread = threading.Thread(target=self.loading_animation)
            loader_thread.daemon = True
            loader_thread.start()
            
            # Run maigret
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            
            # Stop animation
            self.scanning = False
            loader_thread.join(timeout=0.5)
            
            print(f"\n{C_OK}[✓] Scan complete!{C_RESET}\n")
            print(f"{C_INFO}[*] Step 2: Parsing results and generating dossier...{C_RESET}\n")
            
            # Parse results into structured dossier
            dossier = self.parse_maigret_to_dossier(target, result.stdout)
            
            # Save dossier
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            target_safe = target.replace(' ', '_').replace('@', '_at_')
            filename = os.path.join(self.reports_dir, f"dossier_{target_safe}_{timestamp}.txt")
            
            self.save_auto_dossier(dossier, filename)
            
            # Show summary
            print(f"\n{C_OK}[✓] Dossier generated successfully!{C_RESET}\n")
            print(f"{C_INFO}Summary:{C_RESET}")
            print(f"  • Total Platforms Found: {len(dossier['platforms'])}")
            print(f"  • Profiles with Details: {dossier['profiles_with_details']}")
            print(f"  • Countries: {', '.join(dossier['countries']) if dossier['countries'] else 'N/A'}")
            print(f"  • Saved to: {filename}\n")
            
        except Exception as e:
            self.scanning = False
            Logger.error(f"Error: {str(e)}")
    
    def parse_maigret_to_dossier(self, target, output):
        """Parse Maigret output into structured dossier"""
        dossier = {
            'target': target,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'platforms': [],
            'profiles_with_details': 0,
            'countries': [],
            'tags': [],
            'usernames': set(),
            'emails': set(),
            'locations': set(),
            'names': set(),
            'urls': set()
        }
        
        current_profile = None
        
        for line in output.split('\n'):
            line = line.strip()
            
            # Parse statistics
            if line.startswith('Countries:'):
                dossier['countries'] = [c.strip() for c in line.replace('Countries:', '').split(',')]
            
            if line.startswith('Interests (tags):'):
                dossier['tags'] = [t.strip() for t in line.replace('Interests (tags):', '').split(',')]
            
            # Parse profiles
            if line.startswith('[+]'):
                if current_profile:
                    dossier['platforms'].append(current_profile)
                    if current_profile['details']:
                        dossier['profiles_with_details'] += 1
                
                parts = line[3:].split(':', 1)
                if len(parts) >= 2:
                    platform = parts[0].strip()
                    url = ':'.join(parts[1:]).strip()
                    dossier['urls'].add(url)
                    current_profile = {
                        'platform': platform,
                        'url': url,
                        'details': {}
                    }
            
            # Parse extended info
            elif current_profile and ('├─' in line or '└─' in line):
                detail = line.replace('├─', '').replace('└─', '').strip()
                if ':' in detail:
                    key, value = detail.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    current_profile['details'][key] = value
                    
                    # Extract useful info
                    if key in ['fullname', 'name']:
                        dossier['names'].add(value)
                    elif key == 'location':
                        dossier['locations'].add(value)
        
        # Add last profile
        if current_profile:
            dossier['platforms'].append(current_profile)
            if current_profile['details']:
                dossier['profiles_with_details'] += 1
        
        return dossier
    
    def save_auto_dossier(self, dossier, filename):
        """Save auto-generated dossier"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write("=" * 80 + "\n")
                f.write(" " * 20 + "COMPREHENSIVE OSINT DOSSIER — ProbeSuite\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Target: {dossier['target']}\n")
                f.write(f"Generated: {dossier['timestamp']}\n")
                f.write(f"Total Platforms Found: {len(dossier['platforms'])}\n")
                f.write("\n" + "=" * 80 + "\n\n")
                
                # Executive Summary
                f.write("EXECUTIVE SUMMARY\n")
                f.write("-" * 80 + "\n")
                f.write(f"Profiles Found: {len(dossier['platforms'])}\n")
                f.write(f"Profiles with Extended Data: {dossier['profiles_with_details']}\n")
                
                if dossier['names']:
                    f.write(f"Known Names: {', '.join(dossier['names'])}\n")
                
                if dossier['locations']:
                    f.write(f"Locations: {', '.join(dossier['locations'])}\n")
                
                if dossier['countries']:
                    f.write(f"Countries: {', '.join(dossier['countries'])}\n")
                
                if dossier['tags']:
                    f.write(f"Interest Tags: {', '.join(dossier['tags'])}\n")
                
                f.write("\n" + "=" * 80 + "\n\n")
                
                # Detailed Profiles
                f.write(f"DETAILED PLATFORM PROFILES ({len(dossier['platforms'])})\n")
                f.write("=" * 80 + "\n\n")
                
                for idx, profile in enumerate(dossier['platforms'], 1):
                    f.write(f"[{idx}] {profile['platform']}\n")
                    f.write(f"    URL: {profile['url']}\n")
                    
                    if profile['details']:
                        f.write(f"\n    Profile Information:\n")
                        f.write(f"    {'-' * 70}\n")
                        for key, value in profile['details'].items():
                            f.write(f"    {key}: {value}\n")
                    
                    f.write("\n")
                
                # All URLs
                if dossier['urls']:
                    f.write("=" * 80 + "\n")
                    f.write("ALL PROFILE URLS\n")
                    f.write("-" * 80 + "\n")
                    for url in sorted(dossier['urls']):
                        f.write(f"• {url}\n")
                    f.write("\n")
                
                # Footer
                f.write("=" * 80 + "\n")
                f.write(f"Report saved to: {filename}\n")
                f.write("=" * 80 + "\n")
            
            Logger.success(f"Dossier saved: {filename}")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def show_investigation_guide(self, target):
        """Show investigation template guide"""
        clear_screen()
        print_header("INVESTIGATION GUIDE", 80)
        
        print(f"\n{C_OK}[*] Investigation guide for: {C_WARN}{target}{C_RESET}\n")
        
        guide_sections = {
            'Basic Information': [
                'Full name (check profile bios)',
                'Username variations (check similar usernames)',
                'Email addresses (look in profile descriptions)',
                'Phone numbers (check contact info)',
                'Location (check profile locations)'
            ],
            'Online Activity': [
                'Social media accounts (Facebook, Instagram, Twitter)',
                'Professional networks (LinkedIn, AngelList)',
                'Developer platforms (GitHub, GitLab, StackOverflow)',
                'Gaming profiles (Steam, Xbox, PlayStation)',
                'Content creation (YouTube, Medium, Patreon)'
            ],
            'Investigation Tips': [
                'Use Google: "username" site:platform.com',
                'Check Wayback Machine for old profiles',
                'Look for connections between accounts',
                'Note posting patterns and timestamps',
                'Document all findings with screenshots'
            ]
        }
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  OSINT INVESTIGATION CHECKLIST                                            ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        for section, items in guide_sections.items():
            print(f"\n{C_OK}═══ {section} ═══{C_RESET}\n")
            for item in items:
                print(f"  {C_INFO}☐ {item}{C_RESET}")
        
        print(f"\n{C_WARN}⚠ Always follow legal and ethical guidelines!{C_RESET}\n")
        
        # Save guide
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_safe = target.replace(' ', '_').replace('@', '_at_')
        filename = os.path.join(self.reports_dir, f"guide_{target_safe}_{timestamp}.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("OSINT INVESTIGATION GUIDE\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Target: {target}\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for section, items in guide_sections.items():
                    f.write(f"{section.upper()}\n")
                    f.write("-" * 80 + "\n")
                    for item in items:
                        f.write(f"☐ {item}\n")
                    f.write("\n")
                
                f.write("=" * 80 + "\n")
            
            Logger.success(f"Guide saved: {filename}")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    
    def manual_username_search(self, username):
        """Manual search guide"""
        clear_screen()
        print_header("MANUAL USERNAME INVESTIGATION", 80)
        
        print(f"\n{C_OK}[*] Target username: {C_WARN}{username}{C_RESET}\n")
        
        categories = {
            'Social Media Giants': [
                ('Facebook', f'https://www.facebook.com/{username}'),
                ('Instagram', f'https://www.instagram.com/{username}'),
                ('Twitter/X', f'https://twitter.com/{username}'),
                ('LinkedIn', f'https://www.linkedin.com/in/{username}'),
                ('TikTok', f'https://www.tiktok.com/@{username}'),
                ('YouTube', f'https://www.youtube.com/@{username}'),
            ],
            'Developer Platforms': [
                ('GitHub', f'https://github.com/{username}'),
                ('GitLab', f'https://gitlab.com/{username}'),
                ('StackOverflow', f'https://stackoverflow.com/users/{username}'),
                ('Dev.to', f'https://dev.to/{username}'),
                ('CodePen', f'https://codepen.io/{username}'),
                ('HackerRank', f'https://www.hackerrank.com/{username}'),
            ],
            'Gaming & Streaming': [
                ('Twitch', f'https://twitch.tv/{username}'),
                ('Steam', f'https://steamcommunity.com/id/{username}'),
                ('Discord', f'https://discord.com/users/{username}'),
                ('Xbox', f'https://xboxgamertag.com/search/{username}'),
                ('PlayStation', f'https://psnprofiles.com/{username}'),
                ('Roblox', f'https://www.roblox.com/users/profile?username={username}'),
            ],
            'Content Creation': [
                ('Medium', f'https://medium.com/@{username}'),
                ('Substack', f'https://{username}.substack.com'),
                ('Patreon', f'https://www.patreon.com/{username}'),
                ('Ko-fi', f'https://ko-fi.com/{username}'),
                ('SoundCloud', f'https://soundcloud.com/{username}'),
                ('Spotify', f'https://open.spotify.com/user/{username}'),
            ],
            'Creative & Design': [
                ('Behance', f'https://www.behance.net/{username}'),
                ('Dribbble', f'https://dribbble.com/{username}'),
                ('DeviantArt', f'https://www.deviantart.com/{username}'),
                ('ArtStation', f'https://www.artstation.com/{username}'),
                ('Flickr', f'https://www.flickr.com/people/{username}'),
                ('500px', f'https://500px.com/p/{username}'),
            ],
            'Forums & Communities': [
                ('Reddit', f'https://www.reddit.com/user/{username}'),
                ('Quora', f'https://www.quora.com/profile/{username}'),
                ('HackerNews', f'https://news.ycombinator.com/user?id={username}'),
                ('Telegram', f'https://t.me/{username}'),
                ('Keybase', f'https://keybase.io/{username}'),
                ('AboutMe', f'https://about.me/{username}'),
            ]
        }
        
        for category, platforms in categories.items():
            print(f"\n{C_OK}╔═ {category} {('═' * (71 - len(category)))}╗{C_RESET}")
            for platform, url in platforms:
                print(f"{C_INFO}  • {platform:20} {url}{C_RESET}")
            print(f"{C_OK}╚{'═' * 77}╝{C_RESET}")
        
        # Save guide
        self.save_investigation_guide(username, categories)
    
    def save_investigation_guide(self, username, categories):
        """Save investigation guide"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"manual_guide_{username}_{timestamp}.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("MANUAL INVESTIGATION GUIDE\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Target: {username}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for category, platforms in categories.items():
                    f.write(f"{category.upper()}\n")
                    f.write("-" * 80 + "\n")
                    for platform, url in platforms:
                        f.write(f"{platform:20} → {url}\n")
                    f.write("\n")
                
                f.write("=" * 80 + "\n")
            
            Logger.success(f"Guide saved: {filename}")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def save_dossier_template(self, target, sections):
        """Save dossier template"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"dossier_{target.replace(' ', '_')}_{timestamp}.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("PROFESSIONAL OSINT DOSSIER\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Target: {target}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")
                
                for section, items in sections.items():
                    f.write(f"{section.upper()}\n")
                    f.write("-" * 80 + "\n\n")
                    for item in items:
                        f.write(f"☐ {item}\n")
                        f.write(f"   Notes: _________________________________\n\n")
                    f.write("\n")
                
                f.write("=" * 80 + "\n")
            
            Logger.success(f"Template saved: {filename}")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            
            if choice in ['1', '2', '4']:
                clear_screen()
                print_header("TARGET INPUT", 80)
                
                if choice == '1' or choice == '4':
                    target = input(f"\n{C_INFO}Enter username: {C_RESET}").strip()
                else:
                    target = input(f"\n{C_INFO}Enter email: {C_RESET}").strip()
                
                if not target:
                    Logger.warning("Target required!")
                    pause()
                    continue
                
                if choice == '1':
                    self.username_hunt(target)
                elif choice == '2':
                    self.email_pattern_search(target)
                elif choice == '4':
                    self.manual_username_search(target)
                
                pause()
                
            elif choice == '3':
                clear_screen()
                print_header("DOSSIER TARGET", 80)
                target = input(f"\n{C_INFO}Enter target (name/username/email): {C_RESET}").strip()
                if target:
                    self.advanced_dossier(target)
                pause()
                
            else:
                Logger.error("Invalid choice!")
                pause()


def run_maigret():
    """Entry point"""
    tool = Maigret()
    tool.run()


if __name__ == "__main__":
    run_maigret()