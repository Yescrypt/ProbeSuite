# app/information_gathering/osint/holehe.py

import sys
import os
import re
import subprocess
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

class Holehe:
    """Professional Email OSINT Tool - Account Detection"""
    
    def __init__(self):
        self.tool_path = self.check_installation()
        self.services = self.get_popular_services()
    
    def check_installation(self):
        """Check if holehe is installed"""
        try:
            result = subprocess.run(['which', 'holehe'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None
    
    def get_popular_services(self):
        """List of popular services to check"""
        return {
            'Social Media': [
                'Facebook', 'Twitter', 'Instagram', 'LinkedIn',
                'TikTok', 'Snapchat', 'Pinterest', 'Reddit',
                'Tumblr', 'VK', 'Telegram'
            ],
            'Professional': [
                'GitHub', 'GitLab', 'Bitbucket', 'StackOverflow',
                'Medium', 'DeviantArt', 'Behance', 'Dribbble'
            ],
            'Gaming': [
                'Steam', 'Epic Games', 'Battle.net', 'Xbox Live',
                'PlayStation Network', 'Discord', 'Twitch'
            ],
            'Shopping': [
                'Amazon', 'eBay', 'PayPal', 'Stripe',
                'Shopify', 'Etsy', 'AliExpress'
            ],
            'Communication': [
                'Gmail', 'Outlook', 'Yahoo', 'ProtonMail',
                'Zoom', 'Skype', 'WhatsApp', 'Signal'
            ],
            'Entertainment': [
                'Spotify', 'Netflix', 'Hulu', 'Disney+',
                'YouTube', 'SoundCloud', 'Vimeo'
            ],
            'Other': [
                'Dropbox', 'Google Drive', 'Adobe', 'Canva',
                'WordPress', 'Blogger', 'Patreon'
            ]
        }
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def display_menu(self):
        """Display holehe menu"""
        clear_screen()
        print_header("HOLEHE - EMAIL ACCOUNT DETECTION", 80)
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  Check if an email address is registered on 120+ websites and services.   ║{C_RESET}")
        print(f"{C_INFO}║  Discovers accounts across social media, gaming, and other platforms.     ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        print(f"{C_OK}1. Quick Email Check{C_RESET}         - Fast manual analysis")
        print(f"{C_OK}2. Holehe Tool Scan{C_RESET}          - Automated deep scan (120+ sites)")
        print(f"{C_OK}3. Service Categories{C_RESET}        - Browse by category")
        print(f"{C_OK}4. Google Dorks{C_RESET}              - Email search queries")
        print(f"{C_OK}5. Batch Email Check{C_RESET}         - Multiple emails")
        
        print(f"\n{C_WARN}0. Back{C_RESET}")
        print_footer()
    
    def quick_check(self, email):
        """Quick manual email check"""
        clear_screen()
        print_header("QUICK EMAIL CHECK", 80)
        
        print(f"\n{C_OK}[*] Analyzing: {C_WARN}{email}{C_RESET}\n")
        
        # Extract domain
        domain = email.split('@')[1]
        username = email.split('@')[0]
        
        print(f"{C_INFO}Email Components:{C_RESET}")
        print(f"  Username: {C_OK}{username}{C_RESET}")
        print(f"  Domain:   {C_OK}{domain}{C_RESET}\n")
        
        # Common email patterns
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  MANUAL CHECK RESOURCES                                                   ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        resources = [
            ('Google Search', f'https://www.google.com/search?q="{email}"'),
            ('Email Reputation', f'https://emailrep.io/{email}'),
            ('Have I Been Pwned', f'https://haveibeenpwned.com/account/{email}'),
            ('LinkedIn', f'https://www.linkedin.com/search/results/all/?keywords={email}'),
            ('GitHub', f'https://github.com/search?q={email}&type=users'),
            ('Twitter', f'https://twitter.com/search?q={email}'),
            ('Facebook', f'https://www.facebook.com/search/top?q={email}'),
            ('Instagram', f'https://www.instagram.com/explore/tags/{username}'),
        ]
        
        for i, (name, url) in enumerate(resources, 1):
            print(f"{C_OK}{i}. {name:20}{C_RESET}")
            print(f"   {C_INFO}{url}{C_RESET}\n")
        
        # Search suggestions
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  SUGGESTED SEARCHES                                                       ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        suggestions = [
            f'Try username "{username}" on social media sites',
            f'Search for "{username}" on GitHub, GitLab, Bitbucket',
            f'Check gaming platforms: Steam, Discord, Xbox',
            f'Look for professional profiles on LinkedIn, AngelList',
            f'Search forums and communities with the username',
        ]
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{C_OK}{i}. {suggestion}{C_RESET}")
        
        self.save_quick_report(email, resources)
    
    def holehe_scan(self, email):
        """Run holehe tool scan"""
        if not self.tool_path:
            Logger.warning("Holehe not installed!")
            print(f"\n{C_INFO}Installation instructions:{C_RESET}")
            print(f"  pip3 install holehe")
            print(f"  OR")
            print(f"  git clone https://github.com/megadose/holehe.git")
            print(f"  cd holehe && python3 setup.py install\n")
            return False
        
        clear_screen()
        print_header("HOLEHE AUTOMATED SCAN", 80)
        
        print(f"\n{C_OK}[*] Scanning 120+ services for: {C_WARN}{email}{C_RESET}")
        print(f"{C_INFO}[*] This may take 2-3 minutes...{C_RESET}\n")
        
        try:
            # Run holehe
            cmd = ['holehe', email, '--only-used']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print(result.stdout)
                
                # Save results
                output_file = f"reports/osint/holehe/holehe_{email.replace('@', '_at_').replace('.', '_')}.txt"
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                
                Logger.success(f"Results saved: {output_file}")
                return True
            else:
                Logger.error(f"Scan failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            Logger.error("Scan timeout! Try again.")
            return False
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
            return False
    
    def browse_categories(self, email):
        """Browse services by category"""
        clear_screen()
        print_header("SERVICE CATEGORIES", 80)
        
        print(f"\n{C_INFO}Checking email: {C_WARN}{email}{C_RESET}\n")
        
        for category, services in self.services.items():
            print(f"\n{C_OK}╔═ {category} {('═' * (73 - len(category)))}╗{C_RESET}")
            
            for service in services:
                print(f"{C_INFO}  • {service}{C_RESET}")
            
            print(f"{C_OK}╚{'═' * 77}╝{C_RESET}")
        
        print(f"\n{C_INFO}Manual Check Instructions:{C_RESET}")
        print(f"  1. Visit each service's website")
        print(f"  2. Try 'Forgot Password' or 'Sign Up' with the email")
        print(f"  3. Look for 'Email already exists' or similar messages\n")
    
    def generate_dorks(self, email):
        """Generate Google dorks for email"""
        clear_screen()
        print_header("GOOGLE DORKS FOR EMAIL", 80)
        
        username = email.split('@')[0]
        domain = email.split('@')[1]
        
        print(f"\n{C_OK}[*] Target: {C_WARN}{email}{C_RESET}\n")
        
        dorks = [
            (f'"{email}"', 'Exact email match'),
            (f'"{username}" site:{domain}', 'Username on domain'),
            (f'"{email}" site:linkedin.com', 'LinkedIn profile'),
            (f'"{email}" site:github.com', 'GitHub account'),
            (f'"{email}" site:twitter.com', 'Twitter mentions'),
            (f'"{email}" site:facebook.com', 'Facebook presence'),
            (f'"{email}" filetype:pdf', 'In PDF documents'),
            (f'"{email}" filetype:xlsx', 'In spreadsheets'),
            (f'"{email}" filetype:docx', 'In Word documents'),
            (f'"{email}" inurl:contact OR inurl:about', 'Contact pages'),
            (f'"{username}@*" site:{domain}', 'Email variations'),
            (f'intext:"{email}" intext:password', 'Password leaks'),
            (f'"{email}" site:pastebin.com', 'Pastebin dumps'),
            (f'"{email}" site:reddit.com', 'Reddit mentions'),
            (f'"{email}" site:stackoverflow.com', 'StackOverflow'),
        ]
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  COPY THESE DORKS TO GOOGLE SEARCH                                        ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        for i, (dork, desc) in enumerate(dorks, 1):
            print(f"{C_OK}{i:2}. {desc:30}{C_RESET}")
            print(f"    {dork}\n")
        
        # Save dorks
        filename = f"reports/osint/holehe/email_dorks_{email.replace('@', '_at_')}.txt"
        with open(filename, 'w') as f:
            f.write(f"Google Dorks for: {email}\n")
            f.write("=" * 80 + "\n\n")
            for dork, desc in dorks:
                f.write(f"{desc}:\n{dork}\n\n")
        
        Logger.success(f"Dorks saved: {filename}")
    
    def batch_check(self):
        """Check multiple emails"""
        clear_screen()
        print_header("BATCH EMAIL CHECK", 80)
        
        print(f"\n{C_INFO}Enter email addresses (one per line, empty to finish):{C_RESET}\n")
        
        emails = []
        while True:
            email = input(f"{C_INFO}Email #{len(emails)+1}: {C_RESET}").strip()
            if not email:
                break
            
            if self.validate_email(email):
                emails.append(email)
                Logger.success(f"Added: {email}")
            else:
                Logger.warning(f"Invalid format: {email}")
        
        if not emails:
            Logger.warning("No valid emails!")
            return
        
        print(f"\n{C_OK}[*] Processing {len(emails)} email(s)...{C_RESET}\n")
        
        for i, email in enumerate(emails, 1):
            print(f"\n{C_INFO}{'='*80}{C_RESET}")
            print(f"{C_INFO}[{i}/{len(emails)}] Checking: {email}{C_RESET}")
            print(f"{C_INFO}{'='*80}{C_RESET}\n")
            
            self.quick_check(email)
            
            if i < len(emails):
                input(f"\n{C_INFO}Press Enter for next email...{C_RESET}")
        
        Logger.success("Batch check complete!")
    
    def save_quick_report(self, email, resources):
        """Save quick check report"""
        filename = f"reports/osint/holehe/email_check_{email.replace('@', '_at_').replace('.', '_')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("EMAIL OSINT QUICK CHECK REPORT\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Email: {email}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("CHECK THESE RESOURCES:\n")
                f.write("-" * 80 + "\n\n")
                
                for name, url in resources:
                    f.write(f"{name}:\n{url}\n\n")
                
                f.write("=" * 80 + "\n")
            
            Logger.success(f"Report saved: {filename}")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            
            if choice in ['1', '2', '3', '4']:
                clear_screen()
                print_header("EMAIL INPUT", 80)
                
                email = input(f"\n{C_INFO}Enter email address: {C_RESET}").strip()
                
                if not self.validate_email(email):
                    Logger.error("Invalid email format!")
                    pause()
                    continue
                
                if choice == '1':
                    self.quick_check(email)
                elif choice == '2':
                    self.holehe_scan(email)
                elif choice == '3':
                    self.browse_categories(email)
                elif choice == '4':
                    self.generate_dorks(email)
                
                pause()
                
            elif choice == '5':
                self.batch_check()
                pause()
                
            else:
                Logger.error("Invalid choice!")
                pause()


def run_holehe():
    """Entry point"""
    tool = Holehe()
    tool.run()


if __name__ == "__main__":
    run_holehe()