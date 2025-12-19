# app/information_gathering/osint/blackbird.py

import sys
import os
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

class Blackbird:
    """Professional Social Media OSINT Tool - Deep Social Network Analysis"""
    
    def __init__(self):
        self.tool_path = self.check_installation()
        self.social_platforms = self.get_social_platforms()
        self.output_dir = "reports/osint/blackbird"
        os.makedirs(self.output_dir, exist_ok=True)  # Umumiy papka avto-yaratiladi
    
    def check_installation(self):
        """Check if blackbird is installed"""
        paths = [
            'blackbird',
            os.path.expanduser('~/blackbird/blackbird.py'),
            '/opt/blackbird/blackbird.py'
        ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def get_social_platforms(self):
        """Comprehensive list of social media platforms"""
        return {
            'Major Social Networks': {
                'Facebook': {'url': 'https://www.facebook.com/{}', 'users': '3B+'},
                'Instagram': {'url': 'https://www.instagram.com/{}', 'users': '2B+'},
                'Twitter/X': {'url': 'https://twitter.com/{}', 'users': '500M+'},
                'LinkedIn': {'url': 'https://www.linkedin.com/in/{}', 'users': '900M+'},
                'TikTok': {'url': 'https://www.tiktok.com/@{}', 'users': '1B+'},
                'Snapchat': {'url': 'https://www.snapchat.com/add/{}', 'users': '750M+'},
            },
            'Video & Streaming': {
                'YouTube': {'url': 'https://www.youtube.com/@{}', 'users': '2.5B+'},
                'Twitch': {'url': 'https://twitch.tv/{}', 'users': '140M+'},
                'Vimeo': {'url': 'https://vimeo.com/{}', 'users': '260M+'},
                'DailyMotion': {'url': 'https://www.dailymotion.com/{}', 'users': '300M+'},
                'Rumble': {'url': 'https://rumble.com/user/{}', 'users': '78M+'},
            },
            'Messaging & Communication': {
                'Telegram': {'url': 'https://t.me/{}', 'users': '800M+'},
                'Discord': {'url': 'https://discord.com/users/{}', 'users': '150M+'},
                'WhatsApp': {'url': 'https://wa.me/{}', 'users': '2B+'},
                'Skype': {'url': 'https://skype.com/{}', 'users': '40M+'},
                'Signal': {'url': 'https://signal.me/#p/{}', 'users': '40M+'},
            },
            'Professional Networks': {
                'AngelList': {'url': 'https://angel.co/u/{}', 'users': '10M+'},
                'Crunchbase': {'url': 'https://www.crunchbase.com/person/{}', 'users': '50M+'},
                'Xing': {'url': 'https://www.xing.com/profile/{}', 'users': '20M+'},
                'About.me': {'url': 'https://about.me/{}', 'users': '5M+'},
            },
            'Content & Blogging': {
                'Medium': {'url': 'https://medium.com/@{}', 'users': '100M+'},
                'Substack': {'url': 'https://{}.substack.com', 'users': '2M+'},
                'WordPress': {'url': 'https://{}.wordpress.com', 'users': '400M+'},
                'Blogger': {'url': 'https://{}.blogspot.com', 'users': '42M+'},
                'Tumblr': {'url': 'https://{}.tumblr.com', 'users': '135M+'},
            },
            'Creative & Design': {
                'Behance': {'url': 'https://www.behance.net/{}', 'users': '50M+'},
                'Dribbble': {'url': 'https://dribbble.com/{}', 'users': '12M+'},
                'DeviantArt': {'url': 'https://www.deviantart.com/{}', 'users': '61M+'},
                'ArtStation': {'url': 'https://www.artstation.com/{}', 'users': '6M+'},
                'Flickr': {'url': 'https://www.flickr.com/people/{}', 'users': '112M+'},
            },
            'Music & Audio': {
                'Spotify': {'url': 'https://open.spotify.com/user/{}', 'users': '550M+'},
                'SoundCloud': {'url': 'https://soundcloud.com/{}', 'users': '76M+'},
                'Bandcamp': {'url': 'https://{}.bandcamp.com', 'users': '5M+'},
                'Apple Music': {'url': 'https://music.apple.com/profile/{}', 'users': '88M+'},
            },
            'Forums & Communities': {
                'Reddit': {'url': 'https://www.reddit.com/user/{}', 'users': '430M+'},
                'Quora': {'url': 'https://www.quora.com/profile/{}', 'users': '300M+'},
                'Stack Overflow': {'url': 'https://stackoverflow.com/users/{}', 'users': '18M+'},
                'HackerNews': {'url': 'https://news.ycombinator.com/user?id={}', 'users': '5M+'},
            },
            'Dating & Social': {
                'Tinder': {'url': 'https://www.gotinder.com/@{}', 'users': '75M+'},
                'Bumble': {'url': 'https://bumble.com/{}', 'users': '42M+'},
                'OkCupid': {'url': 'https://www.okcupid.com/profile/{}', 'users': '50M+'},
                'Match': {'url': 'https://www.match.com/{}', 'users': '8M+'},
            },
            'Gaming': {
                'Steam': {'url': 'https://steamcommunity.com/id/{}', 'users': '120M+'},
                'Xbox': {'url': 'https://xboxgamertag.com/search/{}', 'users': '120M+'},
                'PlayStation': {'url': 'https://psnprofiles.com/{}', 'users': '110M+'},
                'Roblox': {'url': 'https://www.roblox.com/users/profile?username={}', 'users': '200M+'},
            }
        }
    
    def display_menu(self):
        """Display blackbird menu"""
        clear_screen()
        print_header("BLACKBIRD - SOCIAL MEDIA OSINT", 80)
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  Deep dive into social media presence. Find accounts, analyze activity,  ║{C_RESET}")
        print(f"{C_INFO}║  discover connections, and map digital footprints across platforms.       ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        print(f"{C_OK}1. Quick Social Scan{C_RESET}         - Top 20 platforms")
        print(f"{C_OK}2. Comprehensive Scan{C_RESET}        - All social media sites")
        print(f"{C_OK}3. Platform Categories{C_RESET}       - Browse by category")
        print(f"{C_OK}4. Activity Timeline{C_RESET}         - Track posting history")
        print(f"{C_OK}5. Connection Mapper{C_RESET}         - Find related accounts")
        print(f"{C_OK}6. Profile Comparator{C_RESET}        - Compare multiple profiles")
        print(f"{C_OK}7. Automated Blackbird{C_RESET}       - Run blackbird tool")
        
        print(f"\n{C_WARN}0. Back{C_RESET}")
        print_footer()
    
    def quick_social_scan(self, username):
        """Quick scan of top 20 platforms"""
        clear_screen()
        print_header("QUICK SOCIAL MEDIA SCAN", 80)
        
        print(f"\n{C_OK}[*] Scanning top platforms for: {C_WARN}{username}{C_RESET}\n")
        
        top_20 = [
            ('Facebook', f'https://www.facebook.com/{username}'),
            ('Instagram', f'https://www.instagram.com/{username}'),
            ('Twitter/X', f'https://twitter.com/{username}'),
            ('LinkedIn', f'https://www.linkedin.com/in/{username}'),
            ('TikTok', f'https://www.tiktok.com/@{username}'),
            ('YouTube', f'https://www.youtube.com/@{username}'),
            ('GitHub', f'https://github.com/{username}'),
            ('Reddit', f'https://www.reddit.com/user/{username}'),
            ('Medium', f'https://medium.com/@{username}'),
            ('Telegram', f'https://t.me/{username}'),
            ('Pinterest', f'https://www.pinterest.com/{username}'),
            ('Snapchat', f'https://www.snapchat.com/add/{username}'),
            ('Tumblr', f'https://{username}.tumblr.com'),
            ('Twitch', f'https://twitch.tv/{username}'),
            ('Discord', f'https://discord.com/users/{username}'),
            ('Spotify', f'https://open.spotify.com/user/{username}'),
            ('SoundCloud', f'https://soundcloud.com/{username}'),
            ('Steam', f'https://steamcommunity.com/id/{username}'),
            ('Vimeo', f'https://vimeo.com/{username}'),
            ('DeviantArt', f'https://www.deviantart.com/{username}'),
        ]
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  TOP 20 SOCIAL MEDIA PLATFORMS                                            ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        for i, (platform, url) in enumerate(top_20, 1):
            print(f"{C_OK}{i:2}. {platform:15}{C_RESET} {C_INFO}{url}{C_RESET}")
        
        print(f"\n{C_WARN}💡 Tip: Click or paste URLs to check if profiles exist{C_RESET}\n")
        
        self.save_scan_results(username, top_20, "quick")
    
    def comprehensive_scan(self, username):
        """Comprehensive scan across all platforms"""
        clear_screen()
        print_header("COMPREHENSIVE SOCIAL MEDIA SCAN", 80)
        
        print(f"\n{C_OK}[*] Comprehensive scan for: {C_WARN}{username}{C_RESET}\n")
        
        total_platforms = 0
        all_urls = []
        
        for category, platforms in self.social_platforms.items():
            print(f"\n{C_OK}╔═ {category} {('═' * (71 - len(category)))}╗{C_RESET}")
            
            for platform, data in platforms.items():
                url = data['url'].format(username)
                users = data['users']
                all_urls.append((platform, url))
                total_platforms += 1
                print(f"{C_INFO}  • {platform:20} {url:40} [{users}]{C_RESET}")
            
            print(f"{C_OK}╚{'═' * 77}╝{C_RESET}")
        
        print(f"\n{C_OK}[*] Total platforms checked: {total_platforms}{C_RESET}\n")
        
        self.save_scan_results(username, all_urls, "comprehensive")
    
    def browse_categories(self, username):
        """Browse platforms by category"""
        while True:
            clear_screen()
            print_header("SOCIAL MEDIA CATEGORIES", 80)
            
            print(f"\n{C_OK}[*] Username: {C_WARN}{username}{C_RESET}\n")
            
            categories = list(self.social_platforms.keys())
            
            print(f"{C_INFO}Select a category to explore:{C_RESET}\n")
            for i, cat in enumerate(categories, 1):
                print(f"{C_OK}{i}. {cat}{C_RESET}")
            
            print(f"\n{C_INFO}A. Show all categories{C_RESET}")
            print(f"{C_WARN}0. Back to main menu{C_RESET}")
            
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip().lower()
            
            if choice == '0':
                return
            elif choice == 'a':
                self.comprehensive_scan(username)
                pause()
            elif choice.isdigit() and 1 <= int(choice) <= len(categories):
                selected_cat = categories[int(choice)-1]
                self.show_category(username, selected_cat)
            else:
                Logger.warning("Invalid choice!")
                pause()
    
    def show_category(self, username, category):
        """Show specific category platforms"""
        clear_screen()
        print_header(f"{category.upper()}", 80)
        
        print(f"\n{C_OK}[*] Username: {C_WARN}{username}{C_RESET}\n")
        
        platforms = self.social_platforms[category]
        
        for i, (platform, data) in enumerate(platforms.items(), 1):
            url = data['url'].format(username)
            users = data['users']
            print(f"{C_OK}{i:2}. {platform:20}{C_RESET}")
            print(f"    {C_INFO}URL:   {url}{C_RESET}")
            print(f"    {C_INFO}Users: {users}{C_RESET}\n")
        
        pause()
    
    def activity_timeline(self, username):
        """Create activity timeline"""
        while True:
            clear_screen()
            print_header("ACTIVITY TIMELINE BUILDER", 80)
            
            print(f"\n{C_OK}[*] Username: {C_WARN}{username}{C_RESET}\n")
            
            print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
            print(f"{C_INFO}║  TIMELINE INVESTIGATION METHODS                                           ║{C_RESET}")
            print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
            
            print(f"{C_OK}1. Investigation Steps{C_RESET}        - How to build timeline")
            print(f"{C_OK}2. Timeline Tools{C_RESET}             - Recommended tools")
            print(f"{C_OK}3. Platform Analysis{C_RESET}          - Check each platform")
            print(f"{C_OK}4. Export Timeline Data{C_RESET}       - Save investigation notes")
            
            print(f"\n{C_WARN}0. Back{C_RESET}")
            print_footer()
            
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            elif choice == '1':
                self.show_investigation_steps(username)
            elif choice == '2':
                self.show_timeline_tools(username)
            elif choice == '3':
                self.platform_analysis(username)
            elif choice == '4':
                self.export_timeline_data(username)
            else:
                Logger.error("Invalid choice!")
                pause()
    
    def show_investigation_steps(self, username):
        """Show timeline investigation steps"""
        clear_screen()
        print_header("TIMELINE INVESTIGATION STEPS", 80)
        
        print(f"\n{C_OK}[*] Username: {C_WARN}{username}{C_RESET}\n")
        
        steps = [
            ('Check account creation dates', 'Find when accounts were created'),
            ('Review earliest posts', 'Look at first activities on each platform'),
            ('Note major milestones', 'Track followers, achievements, verified status'),
            ('Track content themes', 'Analyze interests and topics over time'),
            ('Identify connections', 'Map when key connections were made'),
            ('Find activity gaps', 'Look for dormant or inactive periods'),
            ('Compare patterns', 'Cross-reference activity across platforms'),
            ('Map location changes', 'Track geographic movements from posts'),
        ]
        
        for i, (step, desc) in enumerate(steps, 1):
            print(f"{C_OK}{i}. {step:30}{C_RESET}")
            print(f"   {C_INFO}{desc}{C_RESET}\n")
        
        pause()
    
    def show_timeline_tools(self, username):
        """Show timeline building tools"""
        clear_screen()
        print_header("TIMELINE TOOLS", 80)
        
        print(f"\n{C_OK}[*] Username: {C_WARN}{username}{C_RESET}\n")
        
        tools = {
            'General Tools': [
                ('Google Sheets', 'Create visual timelines and charts'),
                ('Excel', 'Data organization and analysis'),
                ('Notion', 'Timeline database and notes'),
                ('Airtable', 'Structured timeline tracking'),
            ],
            'Platform-Specific': [
                ('Archive.org', 'View historical versions of profiles'),
                ('Social Bearing', 'Twitter analytics and timeline'),
                ('Stalkscan', 'Facebook timeline analysis'),
                ('Inflact', 'Instagram insights and history'),
                ('TweetDeck', 'Real-time Twitter monitoring'),
            ],
            'OSINT Tools': [
                ('Maltego', 'Visual timeline mapping'),
                ('Spiderfoot', 'Automated timeline collection'),
                ('Recon-ng', 'Data aggregation for timelines'),
            ]
        }
        
        for category, items in tools.items():
            print(f"\n{C_OK}╔═ {category} {('═' * (71 - len(category)))}╗{C_RESET}")
            for tool, desc in items:
                print(f"{C_INFO}  • {tool:20} - {desc}{C_RESET}")
            print(f"{C_OK}╚{'═' * 77}╝{C_RESET}")
        
        print()
        pause()
    
    def platform_analysis(self, username):
        """Analyze each platform for timeline"""
        clear_screen()
        print_header("PLATFORM TIMELINE ANALYSIS", 80)
        
        print(f"\n{C_OK}[*] Username: {C_WARN}{username}{C_RESET}\n")
        
        platforms = [
            ('Facebook', f'https://www.facebook.com/{username}', 'Check About > Work and Education for dates'),
            ('Instagram', f'https://www.instagram.com/{username}', 'Sort posts by oldest to see timeline'),
            ('Twitter/X', f'https://twitter.com/{username}', 'Use advanced search to find earliest tweets'),
            ('LinkedIn', f'https://www.linkedin.com/in/{username}', 'Complete work history with dates'),
            ('GitHub', f'https://github.com/{username}', 'Repository creation dates show activity'),
            ('Reddit', f'https://www.reddit.com/user/{username}', 'Posts and comments sorted by date'),
            ('Medium', f'https://medium.com/@{username}', 'Article publication timeline'),
            ('YouTube', f'https://www.youtube.com/@{username}', 'Video upload dates and history'),
        ]
        
        print(f"{C_INFO}Check these platforms for timeline data:{C_RESET}\n")
        
        for i, (platform, url, tip) in enumerate(platforms, 1):
            print(f"{C_OK}{i}. {platform:15}{C_RESET}")
            print(f"   {C_INFO}URL: {url}{C_RESET}")
            print(f"   {C_WARN}Tip: {tip}{C_RESET}\n")
        
        pause()
    
    def export_timeline_data(self, username):
        """Export timeline investigation data"""
        clear_screen()
        print_header("EXPORT TIMELINE DATA", 80)
        
        print(f"\n{C_OK}[*] Creating timeline template for: {C_WARN}{username}{C_RESET}\n")
        
        # Create reports directory
        filename = f"{self.output_dir}/timeline_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"ACTIVITY TIMELINE - {username.upper()}\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Investigation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target Username: {username}\n\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("TIMELINE TEMPLATE\n")
                f.write("-" * 80 + "\n\n")
                
                platforms = ['Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'GitHub', 
                           'Reddit', 'Medium', 'YouTube', 'TikTok', 'Discord']
                
                for platform in platforms:
                    f.write(f"\n[{platform}]\n")
                    f.write(f"Account Created: ___________\n")
                    f.write(f"First Post Date: ___________\n")
                    f.write(f"Last Active: ___________\n")
                    f.write(f"Total Posts/Activity: ___________\n")
                    f.write(f"Key Milestones:\n")
                    f.write(f"  - \n")
                    f.write(f"  - \n")
                    f.write(f"Notes:\n")
                    f.write(f"  \n\n")
                    f.write("-" * 80 + "\n")
                
                f.write("\n\nCONNECTIONS TIMELINE\n")
                f.write("-" * 80 + "\n")
                f.write("Date | Platform | Event/Connection | Notes\n")
                f.write("-" * 80 + "\n")
                f.write("\n" * 10)
                
                f.write("\nLOCATION TIMELINE\n")
                f.write("-" * 80 + "\n")
                f.write("Date | Location | Source | Notes\n")
                f.write("-" * 80 + "\n")
                f.write("\n" * 10)
                
                f.write("\n" + "=" * 80 + "\n")
            
            Logger.success(f"Timeline template saved: {filename}")
            print(f"\n{C_INFO}Fill in the template with your findings!{C_RESET}\n")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
        
        pause()
    
    def connection_mapper(self, username):
        """Map connections between accounts"""
        clear_screen()
        print_header("CONNECTION MAPPER", 80)
        
        print(f"\n{C_OK}[*] Mapping connections for: {C_WARN}{username}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  CONNECTION DISCOVERY METHODS                                             ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        methods = {
            'Direct Connections': [
                'Followers/Following lists',
                'Friends and connections',
                'Mutual friends',
                'Group memberships',
                'Collaboration tags',
            ],
            'Content-Based': [
                'Mentions and tags',
                'Comments and replies',
                'Shared content',
                'Cross-posted material',
                'Similar hashtags',
            ],
            'Metadata Clues': [
                'Same profile pictures across platforms',
                'Matching bio information',
                'Linked websites/portfolios',
                'Email addresses in profiles',
                'Phone numbers (if public)',
            ],
            'Behavioral Patterns': [
                'Similar posting times',
                'Common interests/topics',
                'Geographic overlap',
                'Language and writing style',
                'Activity correlations',
            ]
        }
        
        for category, items in methods.items():
            print(f"\n{C_OK}{category}:{C_RESET}")
            for item in items:
                print(f"{C_INFO}  • {item}{C_RESET}")
        
        print()
        pause()
    
    def profile_comparator(self, usernames):
        """Compare multiple profiles"""
        while True:
            clear_screen()
            print_header("PROFILE COMPARATOR", 80)
            
            print(f"\n{C_OK}[*] Comparing profiles:{C_RESET}\n")
            
            for i, username in enumerate(usernames, 1):
                print(f"{C_INFO}{i}. {username}{C_RESET}")
            
            print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
            print(f"{C_INFO}║  COMPARISON OPTIONS                                                       ║{C_RESET}")
            print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
            
            print(f"{C_OK}1. Comparison Criteria{C_RESET}        - What to compare")
            print(f"{C_OK}2. Generate URLs{C_RESET}              - Create profile links")
            print(f"{C_OK}3. Visual Comparison{C_RESET}          - Side-by-side analysis")
            print(f"{C_OK}4. Export Comparison{C_RESET}          - Save comparison data")
            
            print(f"\n{C_WARN}0. Back{C_RESET}")
            print_footer()
            
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            elif choice == '1':
                self.show_comparison_criteria(usernames)
            elif choice == '2':
                self.generate_profile_urls(usernames)
            elif choice == '3':
                self.visual_comparison(usernames)
            elif choice == '4':
                self.export_comparison(usernames)
            else:
                Logger.error("Invalid choice!")
                pause()
    
    def show_comparison_criteria(self, usernames):
        """Show comparison criteria"""
        clear_screen()
        print_header("COMPARISON CRITERIA", 80)
        
        print(f"\n{C_OK}[*] Comparing: {C_WARN}{', '.join(usernames)}{C_RESET}\n")
        
        criteria = {
            'Visual Elements': [
                'Profile picture similarity',
                'Cover/banner images',
                'Color schemes and themes',
                'Logo or branding consistency',
            ],
            'Profile Information': [
                'Bio/description matching',
                'Name variations',
                'Location information',
                'Website links',
                'Contact information',
            ],
            'Account Metadata': [
                'Account creation dates',
                'Account verification status',
                'Follower/following counts',
                'Activity frequency',
            ],
            'Content Analysis': [
                'Content themes and topics',
                'Posting frequency patterns',
                'Language and writing style',
                'Hashtag usage',
                'Media types (photo/video/text)',
            ],
            'Network Analysis': [
                'Common followers/friends',
                'Linked accounts',
                'Mentioned accounts',
                'Group memberships',
            ]
        }
        
        for category, items in criteria.items():
            print(f"\n{C_OK}╔═ {category} {('═' * (71 - len(category)))}╗{C_RESET}")
            for item in items:
                print(f"{C_INFO}  • {item}{C_RESET}")
            print(f"{C_OK}╚{'═' * 77}╝{C_RESET}")
        
        print()
        pause()
    
    def generate_profile_urls(self, usernames):
        """Generate URLs for all profiles"""
        clear_screen()
        print_header("PROFILE URLs GENERATOR", 80)
        
        print(f"\n{C_OK}[*] Generating URLs for: {C_WARN}{', '.join(usernames)}{C_RESET}\n")
        
        platforms = [
            ('Facebook', 'https://www.facebook.com/{}'),
            ('Instagram', 'https://www.instagram.com/{}'),
            ('Twitter', 'https://twitter.com/{}'),
            ('LinkedIn', 'https://www.linkedin.com/in/{}'),
            ('GitHub', 'https://github.com/{}'),
            ('TikTok', 'https://www.tiktok.com/@{}'),
            ('YouTube', 'https://www.youtube.com/@{}'),
            ('Reddit', 'https://www.reddit.com/user/{}'),
        ]
        
        for platform, url_template in platforms:
            print(f"\n{C_OK}═══ {platform} ═══{C_RESET}")
            for username in usernames:
                url = url_template.format(username)
                print(f"{C_INFO}  • {username:20} {url}{C_RESET}")
        
        print()
        pause()
    
    def visual_comparison(self, usernames):
        """Visual side-by-side comparison"""
        clear_screen()
        print_header("VISUAL COMPARISON", 80)
        
        print(f"\n{C_OK}[*] Side-by-side comparison:{C_RESET}\n")
        
        print(f"{C_INFO}{'Criteria':<30}", end='')
        for username in usernames:
            print(f"{username:<20}", end='')
        print(f"{C_RESET}\n{'─' * 80}")
        
        criteria = [
            'Profile Picture',
            'Bio Length',
            'Verified Status',
            'Follower Count',
            'Post Frequency',
            'Account Age',
            'Active Platforms',
            'Content Type',
            'Engagement Rate',
            'Last Activity',
        ]
        
        for criterion in criteria:
            print(f"{C_OK}{criterion:<30}{C_RESET}", end='')
            for _ in usernames:
                print(f"{'[MANUAL]':<20}", end='')
            print()
        
        print(f"\n{C_WARN}Note: Fill in [MANUAL] fields by checking each profile{C_RESET}\n")
        pause()
    
    def export_comparison(self, usernames):
        """Export comparison data"""
        clear_screen()
        print_header("EXPORT COMPARISON", 80)
        
        print(f"\n{C_OK}[*] Creating comparison template...{C_RESET}\n")
        
        safe_usernames = '_'.join(usernames[:3]) if len(usernames) > 3 else '_'.join(usernames)
        filename = f"{self.output_dir}/comparison_{safe_usernames}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("PROFILE COMPARISON REPORT\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Profiles: {', '.join(usernames)}\n\n")
                f.write("=" * 80 + "\n\n")
                
                # Generate URLs
                f.write("PROFILE URLs\n")
                f.write("-" * 80 + "\n\n")
                
                platforms = ['Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'GitHub']
                
                for platform in platforms:
                    f.write(f"\n{platform}:\n")
                    for username in usernames:
                        f.write(f"  {username}: [URL]\n")
                
                # Comparison template
                f.write("\n\nCOMPARISON MATRIX\n")
                f.write("-" * 80 + "\n\n")
                
                criteria = ['Profile Picture', 'Bio', 'Location', 'Verified', 
                          'Followers', 'Posts', 'Active Since', 'Last Post']
                
                header = f"{'Criteria':<20}"
                for username in usernames:
                    header += f"{username:<20}"
                f.write(header + "\n")
                f.write("-" * 80 + "\n")
                
                for criterion in criteria:
                    line = f"{criterion:<20}"
                    for _ in usernames:
                        line += f"{'[FILL]':<20}"
                    f.write(line + "\n")
                
                f.write("\n\nSIMILARITIES\n")
                f.write("-" * 80 + "\n")
                f.write("\n" * 5)
                
                f.write("\nDIFFERENCES\n")
                f.write("-" * 80 + "\n")
                f.write("\n" * 5)
                
                f.write("\nCONCLUSION\n")
                f.write("-" * 80 + "\n")
                f.write("\n" * 5)
                
                f.write("\n" + "=" * 80 + "\n")
            
            Logger.success(f"Comparison template saved: {filename}")
            print(f"\n{C_INFO}Fill in the template with your analysis!{C_RESET}\n")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
        
        pause()
    
    def blackbird_automated(self, username):
        """Run automated blackbird tool - FIXED: username parameter added"""
        clear_screen()
        print_header("BLACKBIRD AUTOMATED SCAN", 80)
        
        # Check installation first
        if not self.tool_path:
            Logger.warning("Blackbird tool not installed!")
            print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
            print(f"{C_INFO}║  INSTALLATION INSTRUCTIONS                                                ║{C_RESET}")
            print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
            
            print(f"{C_OK}Step 1: Clone the repository{C_RESET}")
            print(f"{C_INFO}  git clone https://github.com/p1ngul1n0/blackbird{C_RESET}\n")
            
            print(f"{C_OK}Step 2: Navigate to directory{C_RESET}")
            print(f"{C_INFO}  cd blackbird{C_RESET}\n")
            
            print(f"{C_OK}Step 3: Install requirements{C_RESET}")
            print(f"{C_INFO}  pip3 install -r requirements.txt{C_RESET}\n")
            
            print(f"{C_OK}Step 4: Run blackbird{C_RESET}")
            print(f"{C_INFO}  python3 blackbird.py -u USERNAME{C_RESET}\n")
            
            print(f"{C_WARN}After installation, this tool will automatically detect it!{C_RESET}\n")
            
            pause()
            return
        
        print(f"\n{C_OK}[*] Running Blackbird scan for: {C_WARN}{username}{C_RESET}\n")
        print(f"{C_INFO}This may take 1-2 minutes...{C_RESET}\n")
        
        try:
            cmd = ['python3', self.tool_path, '-u', username]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(result.stdout)
                Logger.success("Scan completed!")
            else:
                Logger.error(f"Scan failed!")
                if result.stderr:
                    print(f"\n{C_ERR}{result.stderr}{C_RESET}")
                
        except subprocess.TimeoutExpired:
            Logger.error("Scan timeout! Try again or check tool manually.")
        except Exception as e:
            Logger.error(f"Error: {str(e)}")
        
        print()
        pause()
    
    def save_scan_results(self, username, platforms, scan_type):
        """Save scan results to file"""
        # Create reports directory if it doesn't exist
        
        filename = f"{self.output_dir}/blackbird_{scan_type}_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"BLACKBIRD - {scan_type.upper()} SOCIAL MEDIA SCAN\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Username: {username}\n")
                f.write(f"Scan Type: {scan_type}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Platforms: {len(platforms)}\n")
                f.write("=" * 80 + "\n\n")
                
                for i, (platform, url) in enumerate(platforms, 1):
                    f.write(f"{i}. {platform}\n")
                    f.write(f"   {url}\n\n")
                
                f.write("=" * 80 + "\n")
            
            Logger.success(f"Results saved: {filename}")
            
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            
            if choice in ['1', '2', '3', '4', '5', '7']:
                clear_screen()
                print_header("USERNAME INPUT", 80)
                
                username = input(f"\n{C_INFO}Enter username: {C_RESET}").strip()
                
                if not username:
                    Logger.warning("Username required!")
                    pause()
                    continue
                
                if choice == '1':
                    self.quick_social_scan(username)
                elif choice == '2':
                    self.comprehensive_scan(username)
                elif choice == '3':
                    self.browse_categories(username)
                elif choice == '4':
                    self.activity_timeline(username)
                elif choice == '5':
                    self.connection_mapper(username)
                elif choice == '7':
                    self.blackbird_automated(username)  # FIXED: username passed
                
                pause()
            
            elif choice == '6':
                clear_screen()
                print_header("PROFILE COMPARATOR", 80)
                
                print(f"\n{C_INFO}Enter usernames to compare (one per line, empty to finish):{C_RESET}\n")
                
                usernames = []
                while len(usernames) < 5:
                    username = input(f"{C_INFO}Username #{len(usernames)+1}: {C_RESET}").strip()
                    if not username:
                        break
                    usernames.append(username)
                
                if len(usernames) >= 2:
                    self.profile_comparator(usernames)
                else:
                    Logger.warning("Need at least 2 usernames to compare!")
                    pause()
            
            else:
                Logger.error("Invalid choice!")
                pause()


def run_blackbird():
    """Entry point"""
    tool = Blackbird()
    tool.run()


if __name__ == "__main__":
    run_blackbird()