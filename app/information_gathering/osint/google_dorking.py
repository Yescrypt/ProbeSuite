# app/information_gathering/osint/google_dorking.py
import sys
import os
import webbrowser
from urllib.parse import quote_plus
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))
from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, InputValidator, clear_screen
import re


class GoogleDorking:
    """Professional Google Dorking Tool"""

    def __init__(self):
        self.dork_categories = {
            '1': ('Document Files', self.documents_dorks),
            '2': ('Login & Admin Pages', self.login_dorks),
            '3': ('Exposed Files & Configs', self.exposed_dorks),
            '4': ('Databases & Backups', self.database_dorks),
            '5': ('Email & Phone Numbers', self.contact_dorks),
            '6': ('Social Media Profiles', self.social_dorks),
            '7': ('Usernames Search', self.username_dorks),
            '8': ('Vulnerability Scanning', self.vuln_dorks),
            '9': ('Custom Dork Builder', self.custom_builder),
        }

    def display_menu(self):
        """Display Google Dorking categories"""
        clear_screen()
        print_header("GOOGLE DORKING - ADVANCED SEARCH", 80)
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║ Google Dorking helps you find specific information using advanced         ║{C_RESET}")
        print(f"{C_INFO}║ search operators. Select a category to generate targeted queries.         ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        for key, (name, _) in self.dork_categories.items():
            print(f" {C_OK}{key}. {name}{C_RESET}")
        print(f"\n {C_WARN}0. Back to OSINT Menu{C_RESET}")
        print_footer()

    def documents_dorks(self, target):
        """Generate document search dorks"""
        clear_screen()
        print_header("DOCUMENT FILES DORKING", 80)
        # Handle wildcard domains (*.uz -> site:.uz)
        site_query = target.replace('*', '') if target.startswith('*') else target
        dorks = [
            (f'site:{site_query} filetype:pdf', 'PDF Documents'),
            (f'site:{site_query} filetype:docx OR filetype:doc', 'Word Documents'),
            (f'site:{site_query} filetype:xlsx OR filetype:xls', 'Excel Spreadsheets'),
            (f'site:{site_query} filetype:pptx OR filetype:ppt', 'PowerPoint Presentations'),
            (f'site:{site_query} filetype:txt', 'Text Files'),
            (f'site:{site_query} filetype:csv', 'CSV Files'),
            (f'site:{site_query} ext:xml OR ext:conf OR ext:cnf OR ext:reg', 'Config Files'),
            (f'site:{site_query} filetype:sql', 'SQL Files'),
            (f'site:{site_query} filetype:log', 'Log Files'),
            (f'site:{site_query} filetype:bak OR filetype:old', 'Backup Files'),
        ]
        self.display_dorks(dorks, target)

    def login_dorks(self, target):
        """Generate login page dorks"""
        clear_screen()
        print_header("LOGIN & ADMIN PAGES DORKING", 80)
        site_query = target.replace('*', '') if target.startswith('*') else target
        dorks = [
            (f'site:{site_query} inurl:admin', 'Admin Pages'),
            (f'site:{site_query} inurl:login', 'Login Pages'),
            (f'site:{site_query} inurl:signin', 'Sign In Pages'),
            (f'site:{site_query} inurl:dashboard', 'Dashboard Pages'),
            (f'site:{site_query} inurl:wp-admin', 'WordPress Admin'),
            (f'site:{site_query} inurl:administrator', 'Administrator Panels'),
            (f'site:{site_query} inurl:moderator', 'Moderator Panels'),
            (f'site:{site_query} intitle:"index of" inurl:admin', 'Admin Directories'),
            (f'site:{site_query} inurl:wp-login.php', 'WordPress Login'),
            (f'site:{site_query} inurl:portal/login', 'Portal Login'),
        ]
        self.display_dorks(dorks, target)

    def exposed_dorks(self, target):
        """Generate exposed files dorks"""
        clear_screen()
        print_header("EXPOSED FILES & CONFIGS DORKING", 80)
        site_query = target.replace('*', '') if target.startswith('*') else target
        dorks = [
            (f'site:{site_query} intitle:"index of"', 'Directory Listings'),
            (f'site:{site_query} inurl:.git', 'Git Repositories'),
            (f'site:{site_query} inurl:.env', 'Environment Files'),
            (f'site:{site_query} inurl:config.php OR inurl:configuration.php', 'PHP Config'),
            (f'site:{site_query} ext:xml | ext:conf | ext:cnf | ext:reg', 'Configuration Files'),
            (f'site:{site_query} intext:"api_key" OR intext:"apikey"', 'API Keys'),
            (f'site:{site_query} intext:"password" OR intext:"passwd"', 'Password Strings'),
            (f'site:{site_query} ext:properties', 'Properties Files'),
            (f'site:{site_query} filetype:yaml OR filetype:yml', 'YAML Configs'),
            (f'site:{site_query} inurl:phpinfo.php', 'PHP Info Pages'),
        ]
        self.display_dorks(dorks, target)

    def database_dorks(self, target):
        """Generate database search dorks"""
        clear_screen()
        print_header("DATABASES & BACKUPS DORKING", 80)
        site_query = target.replace('*', '') if target.startswith('*') else target
        dorks = [
            (f'site:{site_query} inurl:database', 'Database Paths'),
            (f'site:{site_query} inurl:backup', 'Backup Directories'),
            (f'site:{site_query} filetype:sql', 'SQL Dumps'),
            (f'site:{site_query} filetype:db', 'Database Files'),
            (f'site:{site_query} filetype:mdb', 'MS Access DB'),
            (f'site:{site_query} ext:sql intext:password', 'SQL with Passwords'),
            (f'site:{site_query} inurl:"backup.sql"', 'SQL Backups'),
            (f'site:{site_query} intitle:"index of" "database"', 'Database Directories'),
            (f'site:{site_query} ext:sqlite OR ext:sqlite3', 'SQLite Databases'),
            (f'site:{site_query} inurl:dump OR inurl:export', 'DB Dumps/Exports'),
        ]
        self.display_dorks(dorks, target)

    def contact_dorks(self, target):
        """Generate contact information dorks"""
        clear_screen()
        print_header("EMAIL & PHONE NUMBERS DORKING", 80)
        site_query = target.replace('*', '') if target.startswith('*') else target
        if '@' in target:
            # Email-specific search
            email_user = target.split('@')[0]
            email_domain = target.split('@')[1]
            dorks = [
                (f'"{target}"', 'Exact Email Match'),
                (f'"{email_user}*@{email_domain}"', 'Email Variations'),
                (f'site:{email_domain} "{email_user}"', 'On Domain'),
                (f'intext:"{target}"', 'In Page Text'),
                (f'"{target}" site:linkedin.com', 'LinkedIn Profile'),
                (f'"{target}" site:twitter.com', 'Twitter Profile'),
                (f'"{target}" site:facebook.com', 'Facebook Profile'),
                (f'"{target}" filetype:pdf', 'In PDF Documents'),
                (f'"{target}" filetype:docx', 'In Word Docs'),
                (f'"{target}" inurl:contact', 'On Contact Pages'),
            ]
        elif target.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '').isdigit():
            # Phone number search
            phone_clean = target.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            dorks = [
                (f'"{target}"', 'Exact Phone Match'),
                (f'"{phone_clean}"', 'Phone Without Formatting'),
                (f'"{target}" site:linkedin.com', 'LinkedIn'),
                (f'"{target}" site:facebook.com', 'Facebook'),
                (f'"{target}" filetype:pdf', 'In PDFs'),
                (f'"{target}" filetype:xlsx', 'In Excel Files'),
                (f'"{target}" inurl:contact', 'Contact Pages'),
                (f'intext:"{target}" intext:"phone"', 'With Phone Label'),
                (f'intext:"{target}" intext:"mobile"', 'With Mobile Label'),
                (f'"{target}" intext:"whatsapp" OR "telegram"', 'Messaging Apps'),
            ]
        else:
            # Domain or general search
            dorks = [
                (f'site:{site_query} intext:"@" OR intext:"email"', 'Email Addresses'),
                (f'site:{site_query} intext:"phone" OR intext:"tel:"', 'Phone Numbers'),
                (f'site:{site_query} inurl:contact', 'Contact Pages'),
                (f'site:{site_query} intitle:contact', 'Contact Titles'),
                (f'site:{site_query} "@" filetype:pdf', 'Emails in PDFs'),
                (f'site:{site_query} "@" filetype:xlsx', 'Emails in Excel'),
                (f'site:{site_query} intext:"+1" OR intext:"+44" OR intext:"+998"', 'Phone with Code'),
                (f'site:{site_query} "email:" OR "mail:"', 'Email Labels'),
                (f'site:{site_query} intext:"@{site_query}"', 'Domain Emails'),
                (f'site:{site_query} filetype:txt intext:"@"', 'Emails in TXT'),
            ]
        self.display_dorks(dorks, target)

    def social_dorks(self, username):
        """Generate social media profile dorks"""
        clear_screen()
        print_header("SOCIAL MEDIA PROFILES DORKING", 80)
        dorks = [
            (f'"{username}" site:linkedin.com', 'LinkedIn'),
            (f'"{username}" site:twitter.com OR site:x.com', 'Twitter/X'),
            (f'"{username}" site:facebook.com', 'Facebook'),
            (f'"{username}" site:instagram.com', 'Instagram'),
            (f'"{username}" site:github.com', 'GitHub'),
            (f'"{username}" site:reddit.com', 'Reddit'),
            (f'"{username}" site:youtube.com', 'YouTube'),
            (f'"{username}" site:tiktok.com', 'TikTok'),
            (f'"{username}" site:pinterest.com', 'Pinterest'),
            (f'"{username}" site:medium.com', 'Medium'),
        ]
        self.display_dorks(dorks, username)

    def username_dorks(self, username):
        """Generate username search dorks"""
        clear_screen()
        print_header("USERNAME SEARCH DORKING", 80)
        dorks = [
            (f'"{username}"', 'Exact Username'),
            (f'"{username}" -site:linkedin.com -site:facebook.com', 'Exclude Major Sites'),
            (f'intitle:"{username}"', 'In Page Titles'),
            (f'inurl:"{username}"', 'In URLs'),
            (f'"{username}" intext:"joined" OR "member since"', 'Forum Profiles'),
            (f'"{username}" site:github.com', 'GitHub Activity'),
            (f'"{username}" site:stackoverflow.com', 'StackOverflow'),
            (f'"{username}" site:gitlab.com', 'GitLab'),
            (f'"{username}" site:bitbucket.org', 'Bitbucket'),
            (f'"{username}" filetype:pdf OR filetype:docx', 'In Documents'),
        ]
        self.display_dorks(dorks, username)

    def vuln_dorks(self, target):
        """Generate vulnerability scanning dorks"""
        clear_screen()
        print_header("VULNERABILITY SCANNING DORKING", 80)
        site_query = target.replace('*', '') if target.startswith('*') else target
        dorks = [
            (f'site:{site_query} intext:"sql syntax near" OR intext:"mysql_fetch"', 'SQL Errors'),
            (f'site:{site_query} intext:"Warning:" OR "Fatal error:"', 'PHP Errors'),
            (f'site:{site_query} intext:"index of /" OR "parent directory"', 'Directory Browsing'),
            (f'site:{site_query} intitle:"phpMyAdmin"', 'phpMyAdmin'),
            (f'site:{site_query} inurl:phpinfo.php', 'PHP Info Exposure'),
            (f'site:{site_query} ext:action OR ext:do', 'Struts Actions'),
            (f'site:{site_query} inurl:wp-content/uploads/', 'WordPress Uploads'),
            (f'site:{site_query} inurl:install.php OR inurl:setup.php', 'Installation Files'),
            (f'site:{site_query} intitle:"Test Page for Apache"', 'Default Pages'),
            (f'site:{site_query} ext:swf', 'Flash Files'),
        ]
        self.display_dorks(dorks, target)

    def custom_builder(self, target):
        """Custom dork builder"""
        clear_screen()
        print_header("CUSTOM DORK BUILDER", 80)
        print(f"\n{C_INFO}Build your custom Google Dork:{C_RESET}\n")
        operators = {
            '1': ('site:', 'Limit to specific site'),
            '2': ('inurl:', 'URL contains text'),
            '3': ('intitle:', 'Title contains text'),
            '4': ('intext:', 'Body contains text'),
            '5': ('filetype:', 'Specific file type'),
            '6': ('ext:', 'File extension'),
            '7': ('link:', 'Links to page'),
            '8': ('related:', 'Similar pages'),
        }
        print(f"{C_OK}Available Operators:{C_RESET}\n")
        for key, (op, desc) in operators.items():
            print(f" {key}. {op:12} - {desc}")
        print(f"\n{C_INFO}Example: site:example.com filetype:pdf intext:password{C_RESET}\n")
        custom_dork = input(f"{C_INFO}Enter your custom dork: {C_RESET}").strip()
        if custom_dork:
            self.search_google(custom_dork)

    def display_dorks(self, dorks, target):
        """Display generated dorks with persistent loop"""
        target_display = target
        if target.startswith('*'):
            target_display = f"{target} (All {target.replace('*', '')} domains)"

        while True:
            clear_screen()
            print_header(f"GOOGLE DORKS FOR: {target_display.upper()}", 80)
            print(f"\n{C_OK}Generated Dorks:{C_RESET}\n")
            for i, (dork, description) in enumerate(dorks, 1):
                print(f"{C_INFO}{i:2}. {description:30}{C_RESET} {dork}")

            print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
            print(f"{C_INFO}║ Options:                                                                  ║{C_RESET}")
            print(f"{C_INFO}║ • Enter number (1-{len(dorks)}) → open in browser                         ║{C_RESET}")
            print(f"{C_INFO}║ • Enter 'all'                  → save all dorks to file                   ║{C_RESET}")
            print(f"{C_INFO}║ • Press Enter                  → back to category menu                    ║{C_RESET}")
            print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

            choice = input(f"{C_INFO}Your choice: {C_RESET}").strip().lower()

            # 1. Bo'sh Enter → kategoriyaga qaytish
            if choice == '':
                print(f"\n{C_WARN}Returning to category selection...{C_RESET}")
                pause()
                break  # ← Bu yerda faqat break → run() davom etadi, lekin pause() yo'q → to'g'ri

            # 2. 'all' → saqlash
            elif choice == 'all':
                self.save_dorks(dorks, target)
                print(f"\n{C_OK}Dorks saved successfully!{C_RESET}")
                pause()
                # Hech qanday break yo'q → yana ro'yxat chiqadi

            # 3. Raqam tanlash → brauzerda ochish
            elif choice.isdigit() and 1 <= int(choice) <= len(dorks):
                selected_dork = dorks[int(choice) - 1][0]
                self.search_google(selected_dork)

                # Yana qolishni so'raymiz
                while True:
                    stay = input(f"\n{C_INFO}Stay in this dork list? (Y/n): {C_RESET}").strip().lower()
                    if stay in ('', 'y', 'yes'):
                        break  # ← Faqat ichki loopdan chiqamiz → tashqi while davom etadi → ro'yxat qayta chiqadi
                    elif stay == 'n':
                        print(f"{C_WARN}Returning to category selection...{C_RESET}")
                        pause()
                        return  # ← Faqat bu yerda return → kategoriyaga qaytish
                    else:
                        print(f"{C_ERR}Please type Y or N{C_RESET}")

            # 4. Noto'g'ri tanlov
            else:
                Logger.warning("Invalid choice! Try again.")
                pause()
                # Hech qanday break yo'q → yana ro'yxat

    def search_google(self, dork):
        """Open dork in browser"""
        url = f"https://www.google.com/search?q={quote_plus(dork)}"
        try:
            print(f"\n{C_OK}[+] Opening in browser...{C_RESET}")
            webbrowser.open(url)
            Logger.success(f"Dork launched: {dork}")
        except Exception as e:
            Logger.error(f"Failed to open browser: {str(e)}")
            print(f"\n{C_INFO}Copy this URL:{C_RESET}\n{url}\n")

    def save_dorks(self, dorks, target):
        """Save dorks to file"""
        filename = f"reports/osnit/google_dorking/dorks_{target.replace(':', '_').replace('/', '_')}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(f"Google Dorks for: {target}\n")
                f.write(f"Generated: {os.popen('date').read()}\n")
                f.write("="*80 + "\n\n")
                for i, (dork, description) in enumerate(dorks, 1):
                    f.write(f"{i}. {description}\n")
                    f.write(f" {dork}\n\n")
            Logger.success(f"Dorks saved to: {filename}")
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")

    def detect_target_type(self, target):
        """Auto-detect target type"""
        # Email pattern
        if '@' in target and re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
            return 'email'
        # Phone pattern
        if re.match(r'^\+?\d{10,15}$', target.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            return 'phone'
        # Domain pattern (contains dot, no spaces, no @)
        if '.' in target and ' ' not in target and '@' not in target:
            if re.match(r'^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$', target) or target.startswith('*.'):
                return 'domain'
        # Otherwise, treat as username
        return 'username'

    def get_target_with_type(self):
        """Get target and detect its type"""
        clear_screen()
        print_header("TARGET SPECIFICATION", 80)
        print(f"\n{C_INFO}Enter your target (system will auto-detect type):{C_RESET}\n")
        print(f"{C_OK}Examples:{C_RESET}")
        print(f" • Domain: example.com or *.uz")
        print(f" • Email: user@example.com")
        print(f" • Username: john_doe")
        print(f" • Phone: +1234567890\n")
        target = input(f"{C_INFO}Target: {C_RESET}").strip()
        if not target:
            Logger.warning("No target specified!")
            return None, None
        # Detect type
        target_type = self.detect_target_type(target)
        # Display detected type
        type_icons = {
            'domain': 'Domain',
            'email': 'Email',
            'username': 'Username',
            'phone': 'Phone'
        }
        print(f"\n{C_OK}Detected: {type_icons.get(target_type, 'Unknown')} {target_type.upper()}{C_RESET}")
        confirm = input(f"{C_INFO}Is this correct? (Y/n): {C_RESET}").strip().lower()
        if confirm and confirm != 'y':
            print(f"\n{C_INFO}Select target type manually:{C_RESET}")
            print(f" 1. Domain")
            print(f" 2. Email")
            print(f" 3. Username")
            print(f" 4. Phone\n")
            type_choice = input(f"{C_INFO}Choice (1-4): {C_RESET}").strip()
            type_map = {'1': 'domain', '2': 'email', '3': 'username', '4': 'phone'}
            target_type = type_map.get(type_choice, target_type)
        return target, target_type

    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = InputValidator.get_choice()
            if choice == '0':
                return
            if choice not in self.dork_categories:
                Logger.error("Invalid choice!")
                pause()
                continue

            target, target_type = self.get_target_with_type()
            if not target:
                pause()
                continue

            category_name, category_func = self.dork_categories[choice]
            Logger.info(f"Running {category_name} for {target_type}: {target}")

            if choice == '5':
                category_func(target)
            elif choice == '6':
                if target_type != 'username':
                    Logger.warning("Social media search works best with usernames!")
                    proceed = input(f"{C_INFO}Continue anyway? (y/N): {C_RESET}").strip().lower()
                    if proceed != 'y':
                        pause()
                        continue
                category_func(target)
            elif choice == '7':
                if target_type != 'username':
                    Logger.warning("This search is optimized for usernames!")
                    proceed = input(f"{C_INFO}Continue anyway? (y/N): {C_RESET}").strip().lower()
                    if proceed != 'y':
                        pause()
                        continue
                category_func(target)
                       # ...
            else:
                if target_type == 'email' and choice in ['1', '2', '3', '4', '8']:
                    domain = target.split('@')[1]
                    Logger.info(f"Using domain: {domain}")
                    category_func(domain)
                else:
                    category_func(target)


def run_google_dorking():
    """Entry point for Google Dorking"""
    dorking = GoogleDorking()
    dorking.run()


if __name__ == "__main__":
    run_google_dorking()