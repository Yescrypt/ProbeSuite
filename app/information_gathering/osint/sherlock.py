# app/information_gathering/osint/sherlock.py

import sys
import os
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

class Sherlock:
    """Professional Username OSINT Tool - Hunt Across 300+ Sites"""
    
    def __init__(self):
        self.tool_path = self.check_installation()
        self.platforms = self.get_platform_categories()
        # <<< YANGI: Reports papkasini avto yaratamiz >>>
        self.reports_dir = "reports/osint/sherlock"
        os.makedirs(self.reports_dir, exist_ok=True)

    def check_installation(self):
        """Check if sherlock is installed"""
        try:
            result = subprocess.run(['which', 'sherlock'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None
    
    def get_platform_categories(self):
        """Categorized social media and online platforms"""
        return {
            'Social Networks': {
                'platforms': ['Facebook', 'Twitter/X', 'Instagram', 'LinkedIn', 
                            'TikTok', 'Snapchat', 'Pinterest', 'Reddit'],
                'urls': [
                    'https://www.facebook.com/{}',
                    'https://twitter.com/{}',
                    'https://www.instagram.com/{}',
                    'https://www.linkedin.com/in/{}',
                    'https://www.tiktok.com/@{}',
                    'https://www.snapchat.com/add/{}',
                    'https://www.pinterest.com/{}',
                    'https://www.reddit.com/user/{}',
                ]
            },
            'Developer Platforms': {
                'platforms': ['GitHub', 'GitLab', 'Bitbucket', 'StackOverflow',
                            'CodePen', 'HackerRank', 'LeetCode', 'Replit'],
                'urls': [
                    'https://github.com/{}',
                    'https://gitlab.com/{}',
                    'https://bitbucket.org/{}',
                    'https://stackoverflow.com/users/{}',
                    'https://codepen.io/{}',
                    'https://www.hackerrank.com/{}',
                    'https://leetcode.com/{}',
                    'https://replit.com/@{}',
                ]
            },
            'Gaming Platforms': {
                'platforms': ['Steam', 'Xbox', 'PlayStation', 'Discord',
                            'Twitch', 'Epic Games', 'Roblox', 'Minecraft'],
                'urls': [
                    'https://steamcommunity.com/id/{}',
                    'https://xboxgamertag.com/search/{}',
                    'https://psnprofiles.com/{}',
                    'https://discord.com/users/{}',
                    'https://twitch.tv/{}',
                    'https://www.epicgames.com/id/{}',
                    'https://www.roblox.com/users/profile?username={}',
                    'https://namemc.com/profile/{}',
                ]
            },
            'Creative Platforms': {
                'platforms': ['Behance', 'Dribbble', 'DeviantArt', '500px',
                            'SoundCloud', 'Spotify', 'YouTube', 'Vimeo'],
                'urls': [
                    'https://www.behance.net/{}',
                    'https://dribbble.com/{}',
                    'https://www.deviantart.com/{}',
                    'https://500px.com/p/{}',
                    'https://soundcloud.com/{}',
                    'https://open.spotify.com/user/{}',
                    'https://www.youtube.com/@{}',
                    'https://vimeo.com/{}',
                ]
            },
            'Professional Networks': {
                'platforms': ['AngelList', 'Crunchbase', 'Product Hunt', 'Medium',
                            'Substack', 'Patreon', 'Ko-fi', 'Buy Me a Coffee'],
                'urls': [
                    'https://angel.co/u/{}',
                    'https://www.crunchbase.com/person/{}',
                    'https://www.producthunt.com/@{}',
                    'https://medium.com/@{}',
                    'https://{}.substack.com',
                    'https://www.patreon.com/{}',
                    'https://ko-fi.com/{}',
                    'https://www.buymeacoffee.com/{}',
                ]
            },
            'Forums & Communities': {
                'platforms': ['HackerNews', 'Dev.to', 'Hashnode', 'Telegram',
                            'Quora', 'AboutMe', 'Linktree', 'Keybase'],
                'urls': [
                    'https://news.ycombinator.com/user?id={}',
                    'https://dev.to/{}',
                    'https://hashnode.com/@{}',
                    'https://t.me/{}',
                    'https://www.quora.com/profile/{}',
                    'https://about.me/{}',
                    'https://linktr.ee/{}',
                    'https://keybase.io/{}',
                ]
            }
        }
    
    def display_menu(self):
        """Display sherlock menu"""
        clear_screen()
        print_header("SHERLOCK - USERNAME OSINT", 80)
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  Hunt social media accounts by username across 300+ websites.             ║{C_RESET}")
        print(f"{C_INFO}║  Find digital footprints, profiles, and online presence.                  ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        print(f"{C_OK}1. Quick Username Check{C_RESET}      - Manual platform links")
        print(f"{C_OK}2. Sherlock Automated Scan{C_RESET}   - Scan 300+ sites automatically")
        print(f"{C_OK}3. Browse by Category{C_RESET}        - Check specific platform types")
        print(f"{C_OK}4. Generate Profile URLs{C_RESET}     - Build direct profile links")
        print(f"{C_OK}5. Google Dorks{C_RESET}              - Advanced username searches")
        print(f"{C_OK}6. Batch Username Search{C_RESET}     - Multiple usernames")
        
        print(f"\n{C_WARN}0. Back{C_RESET}")
        print_footer()
    
    def quick_check(self, username):
        """Quick manual username check"""
        clear_screen()
        print_header("QUICK USERNAME CHECK", 80)
        
        print(f"\n{C_OK}[*] Checking username: {C_WARN}{username}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  TOP PLATFORMS TO CHECK                                                   ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        top_platforms = [
            ('Instagram', f'https://www.instagram.com/{username}'),
            ('Twitter/X', f'https://twitter.com/{username}'),
            ('Facebook', f'https://www.facebook.com/{username}'),
            ('LinkedIn', f'https://www.linkedin.com/in/{username}'),
            ('GitHub', f'https://github.com/{username}'),
            ('TikTok', f'https://www.tiktok.com/@{username}'),
            ('YouTube', f'https://www.youtube.com/@{username}'),
            ('Reddit', f'https://www.reddit.com/user/{username}'),
            ('Medium', f'https://medium.com/@{username}'),
            ('Telegram', f'https://t.me/{username}'),
        ]
        
        for i, (platform, url) in enumerate(top_platforms, 1):
            print(f"{C_OK}{i:2}. {platform:15}{C_RESET} {C_INFO}{url}{C_RESET}")
        
        print(f"\n{C_INFO}Tip: Open these URLs in browser to verify if accounts exist{C_RESET}\n")
        
        self.save_quick_report(username, top_platforms)
    
    def sherlock_scan(self, username):
        """Run sherlock automated scan"""
        if not self.tool_path:
            Logger.warning("Sherlock not installed!")
            print(f"\n{C_INFO}Installation instructions:{C_RESET}")
            print(f"  pip3 install sherlock-project")
            print(f"  OR")
            print(f"  git clone https://github.com/sherlock-project/sherlock.git")
            print(f"  cd sherlock && pip3 install -r requirements.txt\n")
            return False
        
        clear_screen()
        print_header("SHERLOCK AUTOMATED SCAN", 80)
        
        print(f"\n{C_OK}[*] Scanning 300+ sites for username: {C_WARN}{username}{C_RESET}")
        print(f"{C_INFO}[*] This may take 3-5 minutes...{C_RESET}\n")
        
        try:
            # Natijani reports/sherlock ga saqlaymiz
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.reports_dir, f"sherlock_{username}_{timestamp}.txt")
            
            cmd = ['sherlock', username, '--timeout', '10', '--output', output_file]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=400)
            
            if result.returncode == 0:
                print(result.stdout)
                Logger.success(f"Full results saved → {output_file}")
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
    
    def browse_categories(self, username):
        """Browse platforms by category"""
        clear_screen()
        print_header("BROWSE BY CATEGORY", 80)
        
        print(f"\n{C_OK}[*] Username: {C_WARN}{username}{C_RESET}\n")
        
        for category, data in self.platforms.items():
            print(f"\n{C_OK}╔═ {category} {('═' * (71 - len(category)))}╗{C_RESET}")
            
            for i, (platform, url) in enumerate(zip(data['platforms'], data['urls'])):
                profile_url = url.format(username)
                print(f"{C_INFO}  {i+1}. {platform:20}{C_RESET} {profile_url}")
            
            print(f"{C_OK}╚{'═' * 77}╝{C_RESET}")
        
        print(f"\n{C_INFO}Visit these URLs to check if accounts exist{C_RESET}\n")

        # <<< Category natijasini ham saqlaymiz >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"categories_{username}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Username Category Check - {username}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            for category, data in self.platforms.items():
                f.write(f"{category}\n")
                f.write("-"*50 + "\n")
                for platform, url_template in zip(data['platforms'], data['urls']):
                    f.write(f"{platform}: {url_template.format(username)}\n")
                f.write("\n")
        Logger.success(f"Category links saved → {filename}")
    
    def generate_profile_urls(self, username):
        """Generate all profile URLs"""
        clear_screen()
        print_header("PROFILE URL GENERATOR", 80)
        
        print(f"\n{C_OK}[*] Generating URLs for: {C_WARN}{username}{C_RESET}\n")
        
        for category, data in self.platforms.items():
            print(f"\n{C_OK}═══ {category} {'═' * (65 - len(category))}{C_RESET}")
            for platform, url_template in zip(data['platforms'], data['urls']):
                url = url_template.format(username)
                print(f"{C_INFO}{url}{C_RESET}")

        # <<< Saqlash >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"profile_urls_{username}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"All Profile URLs for: {username}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            for category, data in self.platforms.items():
                f.write(f"{category}\n")
                f.write("-"*80 + "\n")
                for platform, url_template in zip(data['platforms'], data['urls']):
                    f.write(f"{platform}: {url_template.format(username)}\n")
                f.write("\n")
        Logger.success(f"All URLs saved → {filename}")
    
    def generate_dorks(self, username):
        """Generate Google dorks for username"""
        clear_screen()
        print_header("GOOGLE DORKS FOR USERNAME", 80)
        
        print(f"\n{C_OK}[*] Username: {C_WARN}{username}{C_RESET}\n")
        
        dorks = [
            (f'"{username}"', 'Exact username match'),
            (f'"{username}" site:linkedin.com', 'LinkedIn profiles'),
            (f'"{username}" site:github.com', 'GitHub accounts'),
            (f'"{username}" site:twitter.com OR site:x.com', 'Twitter/X'),
            (f'"{username}" site:instagram.com', 'Instagram'),
            (f'"{username}" site:facebook.com', 'Facebook'),
            (f'"{username}" site:reddit.com', 'Reddit posts'),
            (f'intitle:"{username}"', 'In page titles'),
            (f'inurl:"{username}"', 'In URLs'),
            (f'"{username}" "profile" OR "account"', 'Profile pages'),
            (f'"{username}" site:medium.com', 'Medium articles'),
            (f'"{username}" site:youtube.com', 'YouTube channels'),
            (f'"{username}" site:twitch.tv', 'Twitch streams'),
            (f'"{username}" site:stackoverflow.com', 'StackOverflow'),
            (f'"{username}" filetype:pdf', 'In documents'),
        ]
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  GOOGLE DORKS - COPY TO SEARCH                                            ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        for i, (dork, desc) in enumerate(dorks, 1):
            print(f"{C_OK}{i:2}. {desc:30}{C_RESET}")
            print(f"    {dork}\n")

        # <<< Saqlash >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"dorks_{username}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Google Dorks for username: {username}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            for dork, desc in dorks:
                f.write(f"{desc}:\n{dork}\n\n")
        Logger.success(f"Dorks saved → {filename}")
    
    def batch_search(self):
        """Search multiple usernames"""
        clear_screen()
        print_header("BATCH USERNAME SEARCH", 80)
        
        print(f"\n{C_INFO}Enter usernames (one per line, empty to finish):{C_RESET}\n")
        
        usernames = []
        while True:
            username = input(f"{C_INFO}Username #{len(usernames)+1}: {C_RESET}").strip()
            if not username:
                break
            usernames.append(username)
            Logger.success(f"Added: {username}")
        
        if not usernames:
            Logger.warning("No usernames provided!")
            return
        
        print(f"\n{C_OK}[*] Processing {len(usernames)} username(s)...{C_RESET}\n")
        
        for i, username in enumerate(usernames, 1):
            print(f"\n{C_INFO}{'='*80}{C_RESET}")
            print(f"{C_INFO}[{i}/{len(usernames)}] Checking: {username}{C_RESET}")
            print(f"{C_INFO}{'='*80}{C_RESET}\n")
            
            self.quick_check(username)
            
            if i < len(usernames):
                input(f"\n{C_INFO}Press Enter for next username...{C_RESET}")
        
        Logger.success("Batch search complete!")
    
    def save_quick_report(self, username, platforms):
        """Save quick check report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"quick_check_{username}_{timestamp}.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("USERNAME OSINT QUICK CHECK\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Username: {username}\n")
                f.write(f"Date: {datetime.now()}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("CHECK THESE PLATFORMS:\n")
                f.write("-" * 80 + "\n\n")
                
                for platform, url in platforms:
                    f.write(f"{platform}:\n{url}\n\n")
                
                f.write("=" * 80 + "\n")
            
            Logger.success(f"Quick report saved → {filename}")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            
            if choice in ['1', '2', '3', '4', '5']:
                clear_screen()
                print_header("USERNAME INPUT", 80)
                
                username = input(f"\n{C_INFO}Enter username: {C_RESET}").strip()
                
                if not username:
                    Logger.warning("Username required!")
                    pause()
                    continue
                
                if choice == '1':
                    self.quick_check(username)
                elif choice == '2':
                    self.sherlock_scan(username)
                elif choice == '3':
                    self.browse_categories(username)
                elif choice == '4':
                    self.generate_profile_urls(username)
                elif choice == '5':
                    self.generate_dorks(username)
                
                pause()
                
            elif choice == '6':
                self.batch_search()
                pause()
                
            else:
                Logger.error("Invalid choice!")
                pause()


def run_sherlock():
    """Entry point"""
    tool = Sherlock()
    tool.run()


if __name__ == "__main__":
    run_sherlock()