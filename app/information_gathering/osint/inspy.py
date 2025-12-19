# app/information_gathering/osint/inspy.py

import sys
import os
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

class Inspy:
    """Professional LinkedIn OSINT Tool - Corporate Intelligence"""
    
    def __init__(self):
        self.tool_path = self.check_installation()
        # <<< YANGI >>> Umumiy reports papkasi
        self.reports_dir = "reports/osint/inspy"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def check_installation(self):
        """Check if inspy is installed"""
        try:
            result = subprocess.run(['which', 'inspy'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None
    
    def display_menu(self):
        """Display inspy menu"""
        clear_screen()
        print_header("INSPY - LINKEDIN OSINT", 80)
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  LinkedIn intelligence gathering for corporate reconnaissance.            ║{C_RESET}")
        print(f"{C_INFO}║  Find employees, map org structure, discover email patterns.              ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        print(f"{C_OK}1. Company Employee Search{C_RESET}   - Find all employees")
        print(f"{C_OK}2. Email Pattern Discovery{C_RESET}   - Company email formats")
        print(f"{C_OK}3. Department Mapping{C_RESET}        - Org chart structure")
        print(f"{C_OK}4. Technology Stack{C_RESET}          - Tech skills analysis")
        print(f"{C_OK}5. Executive Intelligence{C_RESET}    - Leadership profiles")
        print(f"{C_OK}6. Manual LinkedIn OSINT{C_RESET}     - Investigation guide")
        print(f"{C_OK}7. LinkedIn Dorks{C_RESET}            - Advanced search queries")
        
        print(f"\n{C_WARN}0. Back{C_RESET}")
        print_footer()
    
    def company_employee_search(self, company):
        """Search for company employees and save results"""
        clear_screen()
        print_header("COMPANY EMPLOYEE SEARCH", 80)
        
        print(f"\n{C_OK}[*] Searching employees for: {C_WARN}{company}{C_RESET}\n")
        
        results = []
        
        if self.tool_path:
            Logger.info("Running InSpy automated search...")
            try:
                cmd = ['inspy', '--company', company]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                print(result.stdout)
                results.append(result.stdout)
            except Exception as e:
                Logger.error(f"Error: {str(e)}")
        else:
            self.manual_employee_search(company)
        
        # Natijalarni faylga saqlash
        self.save_employee_results(company, results)

    def save_employee_results(self, company, results):
        """Save employee search results to file"""
        safe_company = company.replace(' ', '_').lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/employees_{safe_company}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Employee Search Results for: {company}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                if results:
                    for result in results:
                        f.write(result + "\n")
                else:
                    f.write("Use manual search methods:\n\n")
                    f.write(f"1. LinkedIn: https://www.linkedin.com/search/results/people/?keywords={company}\n")
                    f.write(f"2. Google: site:linkedin.com/in/ \"{company}\"\n")
                    f.write(f"3. Hunter.io: https://hunter.io/search/{company}\n")
            
            Logger.success(f"Results saved: {filename}")
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def manual_employee_search(self, company):
        """Manual employee search guide"""
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  MANUAL EMPLOYEE DISCOVERY METHODS                                        ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        methods = [
            ('LinkedIn Search', f'https://www.linkedin.com/search/results/people/?keywords={company}'),
            ('Google Dork', f'site:linkedin.com/in/ "{company}"'),
            ('LinkedIn Sales Nav', 'https://www.linkedin.com/sales/'),
            ('Hunter.io', f'https://hunter.io/search/{company}'),
            ('RocketReach', f'https://rocketreach.co/search/company?name={company}'),
        ]
        
        for i, (method, info) in enumerate(methods, 1):
            print(f"{C_OK}{i}. {method:20}{C_RESET}")
            print(f"   {C_INFO}{info}{C_RESET}\n")
        
        print(f"{C_INFO}💡 Tips:{C_RESET}")
        print(f"  • Use LinkedIn's 'People' filter")
        print(f"  • Sort by 'Most Recent' for current employees")
        print(f"  • Check 'Past Company' for ex-employees")
        print(f"  • Use boolean search: (company OR company_name)\n")
    
    def email_pattern_discovery(self, company):
        """Discover email patterns with real company domain"""
        clear_screen()
        print_header("EMAIL PATTERN DISCOVERY", 80)
        
        print(f"\n{C_OK}[*] Analyzing email patterns for: {C_WARN}{company}{C_RESET}\n")
        
        # Real domain name input
        print(f"{C_INFO}Enter company domain (e.g., tesla.com, google.com):{C_RESET}")
        domain = input(f"{C_INFO}Domain: {C_RESET}").strip()
        
        if not domain:
            # Auto-generate domain
            domain = company.lower().replace(' ', '').replace(',', '').replace('.', '') + '.com'
            print(f"{C_WARN}Using auto-generated domain: {domain}{C_RESET}\n")
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  COMMON EMAIL PATTERNS FOR: {company:44} ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        # Real employee names for examples
        print(f"{C_WARN}Enter a sample employee name (e.g., John Doe):{C_RESET}")
        sample_name = input(f"{C_INFO}Name: {C_RESET}").strip()
        
        if sample_name:
            parts = sample_name.lower().split()
            if len(parts) >= 2:
                first = parts[0]
                last = parts[-1]
            else:
                first = "john"
                last = "doe"
        else:
            first = "john"
            last = "doe"
        
        patterns = [
            (f'{first}.{last}@', f'{first}.{last}@{domain}', 'First.Last'),
            (f'{first}@', f'{first}@{domain}', 'First'),
            (f'{first[0]}{last}@', f'{first[0]}{last}@{domain}', 'FLast'),
            (f'{first}{last}@', f'{first}{last}@{domain}', 'FirstLast'),
            (f'{first}_{last}@', f'{first}_{last}@{domain}', 'First_Last'),
            (f'{first[0]}.{last}@', f'{first[0]}.{last}@{domain}', 'F.Last'),
            (f'{last}{first[0]}@', f'{last}{first[0]}@{domain}', 'LastF'),
        ]
        
        print(f"\n{'Pattern Type':<20} {'Example':<40}")
        print(f"{C_INFO}{'─' * 77}{C_RESET}")
        for pattern_type, example, desc in patterns:
            print(f"{C_OK}{desc:<20}{C_RESET} {C_INFO}{example:<40}{C_RESET}")
        
        # Email validation tools
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  EMAIL VALIDATION & VERIFICATION TOOLS                                    ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        tools = [
            ('Hunter.io', 'https://hunter.io/email-verifier', 'Verify email existence'),
            ('EmailHippo', 'https://tools.emailhippo.com/', 'Email validation'),
            ('NeverBounce', 'https://neverbounce.com/', 'Bulk email verification'),
            ('Holehe', f'holehe {first}.{last}@{domain}', 'Check email in data breaches'),
            ('h8mail', f'h8mail -t {first}.{last}@{domain}', 'Find leaked passwords'),
        ]
        
        for i, (tool, info, desc) in enumerate(tools, 1):
            print(f"{C_OK}{i}. {tool:<15}{C_RESET} - {desc}")
            print(f"   {C_INFO}{info}{C_RESET}\n")
        
        # Save to file
        self.save_email_patterns(company, domain, patterns)
    
    def department_mapping(self, company):
        """Map organization departments and save to file"""
        clear_screen()
        print_header("DEPARTMENT MAPPING", 80)
        
        print(f"\n{C_OK}[*] Mapping departments for: {C_WARN}{company}{C_RESET}\n")
        
        departments = {
            'Executive Leadership': ['CEO', 'CTO', 'CFO', 'COO', 'CMO', 'CISO'],
            'Engineering': ['Software Engineer', 'DevOps Engineer', 'QA Engineer', 'Solutions Architect', 'Tech Lead'],
            'Security': ['Security Engineer', 'Security Analyst', 'Penetration Tester', 'SOC Analyst', 'CISO'],
            'Sales': ['Sales Manager', 'Account Executive', 'BDR', 'Sales Engineer', 'VP Sales'],
            'Marketing': ['Marketing Manager', 'Content Writer', 'SEO Specialist', 'Graphic Designer', 'CMO'],
            'Human Resources': ['HR Manager', 'Recruiter', 'Talent Acquisition', 'People Operations', 'HR Director'],
            'Finance': ['Financial Analyst', 'Accountant', 'Controller', 'FP&A Manager', 'CFO'],
            'Operations': ['Operations Manager', 'Project Manager', 'Scrum Master', 'Product Manager', 'COO'],
        }
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  ORGANIZATION STRUCTURE & SEARCH QUERIES                                  ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        all_searches = []
        
        for dept, roles in departments.items():
            print(f"\n{C_OK}■ {dept}{C_RESET}")
            print(f"{C_INFO}{'─' * 77}{C_RESET}")
            for role in roles:
                linkedin_search = f'site:linkedin.com/in/ "{company}" "{role}"'
                google_search = f'"{company}" "{role}" site:linkedin.com'
                
                print(f"{C_INFO}  • {role:<35}{C_RESET}")
                print(f"    LinkedIn: {linkedin_search}")
                
                all_searches.append({
                    'department': dept,
                    'role': role,
                    'linkedin_query': linkedin_search,
                    'google_query': google_search
                })
        
        print(f"\n{C_WARN}💡 Copy these searches to find employees in each department{C_RESET}\n")
        
        # Save to file
        self.save_department_mapping(company, departments, all_searches)

    def save_department_mapping(self, company, departments, searches):
        """Save department mapping to file"""
        safe_company = company.replace(' ', '_').lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/departments_{safe_company}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Department Mapping for: {company}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                for search in searches:
                    f.write(f"Department: {search['department']}\n")
                    f.write(f"Role: {search['role']}\n")
                    f.write(f"LinkedIn Search: {search['linkedin_query']}\n")
                    f.write(f"Google Search: {search['google_query']}\n")
                    f.write("-" * 80 + "\n\n")
            
            Logger.success(f"Department mapping saved: {filename}")
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def technology_stack(self, company):
        """Analyze technology stack with actionable steps"""
        clear_screen()
        print_header("TECHNOLOGY STACK ANALYSIS", 80)
        
        print(f"\n{C_OK}[*] Discovering technology stack for: {C_WARN}{company}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  HOW TO DISCOVER COMPANY TECHNOLOGIES                                     ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        methods = {
            '1. Automated Tools (Recommended)': [
                ('BuiltWith', f'https://builtwith.com/{company}.com', 'Detects web technologies'),
                ('Wappalyzer', 'Browser extension', 'Shows tech stack on any website'),
                ('StackShare', f'https://stackshare.io/companies/{company}', 'Community-driven tech profiles'),
                ('Crunchbase', f'https://www.crunchbase.com/organization/{company}', 'Company tech overview'),
            ],
            '2. LinkedIn Investigation': [
                ('Job Postings', f'site:linkedin.com/jobs/ "{company}" (Python OR Java OR AWS)', 'Find required skills'),
                ('Employee Skills', f'site:linkedin.com/in/ "{company}" (AWS OR Azure OR Docker)', 'Check employee profiles'),
                ('Job Descriptions', 'Read "Requirements" sections', 'Note programming languages'),
            ],
            '3. GitHub & Code Repositories': [
                ('GitHub Org', f'https://github.com/{company}', 'Public repositories'),
                ('GitHub Search', f'user:{company} language:Python', 'Find programming languages'),
                ('GitLab/Bitbucket', 'Search company repos', 'Alternative code hosting'),
            ],
            '4. Job Boards Analysis': [
                ('Indeed', f'site:indeed.com "{company}" developer', 'Job requirements'),
                ('Glassdoor', f'site:glassdoor.com "{company}" engineer interview', 'Interview questions reveal tech'),
                ('AngelList', f'https://angel.co/company/{company}', 'Startup tech stacks'),
            ],
        }
        
        tech_findings = []
        
        for category, items in methods.items():
            print(f"\n{C_OK}{category}{C_RESET}")
            print(f"{C_INFO}{'─' * 77}{C_RESET}")
            for item in items:
                if len(item) == 3:
                    name, url, desc = item
                    print(f"{C_INFO}  • {name:<20} {desc}{C_RESET}")
                    print(f"    {url}\n")
                    tech_findings.append(f"{name}: {url} - {desc}")
                else:
                    print(f"{C_INFO}  • {item}{C_RESET}")
        
        print(f"\n{C_WARN}💡 Action Steps:{C_RESET}")
        print(f"{C_INFO}  1. Visit BuiltWith and Wappalyzer first (fastest results)")
        print(f"  2. Check GitHub for open-source projects")
        print(f"  3. Review 5-10 LinkedIn job postings")
        print(f"  4. Analyze employee skills on LinkedIn profiles{C_RESET}\n")
        
        # Save findings
        self.save_tech_stack(company, tech_findings)

    def save_tech_stack(self, company, findings):
        """Save technology stack findings"""
        safe_company = company.replace(' ', '_').lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/tech_stack_{safe_company}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Technology Stack Analysis for: {company}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                f.write("Discovery Resources:\n\n")
                
                for finding in findings:
                    f.write(f"• {finding}\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("Manual Research Checklist:\n")
                f.write("[ ] Check BuiltWith.com\n")
                f.write("[ ] Install Wappalyzer extension\n")
                f.write("[ ] Search GitHub repos\n")
                f.write("[ ] Review LinkedIn job posts\n")
                f.write("[ ] Analyze employee skills\n")
            
            Logger.success(f"Tech stack guide saved: {filename}")
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def executive_intelligence(self, company):
        """Gather executive intelligence with structured approach"""
        clear_screen()
        print_header("EXECUTIVE INTELLIGENCE GATHERING", 80)
        
        print(f"\n{C_OK}[*] Researching executives for: {C_WARN}{company}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  EXECUTIVE DISCOVERY STRATEGY                                             ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        # Step 1: Find executives
        print(f"{C_OK}STEP 1: Find Executive Names{C_RESET}")
        print(f"{C_INFO}{'─' * 77}{C_RESET}\n")
        
        resources = [
            ('LinkedIn Leadership', f'site:linkedin.com/in/ "{company}" (CEO OR CTO OR CFO OR COO OR CMO)', 'Find C-level executives'),
            ('Company Website', f'{company}.com/about OR {company}.com/team', 'Official leadership page'),
            ('Crunchbase', f'https://www.crunchbase.com/organization/{company}/people', 'Founders & executives'),
            ('Bloomberg', f'https://www.bloomberg.com/profile/company/{company}', 'Executive profiles'),
            ('ZoomInfo', f'https://www.zoominfo.com/c/{company}/executives', 'Contact information'),
        ]
        
        for i, (source, query, desc) in enumerate(resources, 1):
            print(f"{C_OK}{i}. {source:<20}{C_RESET} - {desc}")
            print(f"   {C_INFO}{query}{C_RESET}\n")
        
        # Step 2: Gather information
        print(f"\n{C_OK}STEP 2: Information to Collect{C_RESET}")
        print(f"{C_INFO}{'─' * 77}{C_RESET}\n")
        
        info_categories = {
            'Professional': [
                'Full name and current title',
                'Work email (if public)',
                'Phone number (if available)',
                'Professional bio/summary',
            ],
            'Background': [
                'Previous companies and roles',
                'Education (degree, university)',
                'Years of experience',
                'Career timeline',
            ],
            'Public Presence': [
                'LinkedIn profile URL',
                'Twitter/X handle',
                'Personal website/blog',
                'Public speaking events',
                'Published articles/interviews',
            ],
            'Network': [
                'Board memberships',
                'Advisory roles',
                'Key connections',
                'Professional associations',
            ],
        }
        
        for category, items in info_categories.items():
            print(f"{C_OK}{category}:{C_RESET}")
            for item in items:
                print(f"{C_INFO}  □ {item}{C_RESET}")
            print()
        
        # Step 3: Advanced searches
        print(f"\n{C_OK}STEP 3: Advanced Search Queries{C_RESET}")
        print(f"{C_INFO}{'─' * 77}{C_RESET}\n")
        
        print(f"{C_WARN}CEO Search:{C_RESET}")
        print(f'{C_INFO}  site:linkedin.com/in/ "{company}" CEO{C_RESET}\n')
        
        print(f"{C_WARN}CTO Search:{C_RESET}")
        print(f'{C_INFO}  site:linkedin.com/in/ "{company}" "Chief Technology Officer"{C_RESET}\n')
        
        print(f"{C_WARN}Contact Info:{C_RESET}")
        print(f'{C_INFO}  "{company}" CEO email OR contact{C_RESET}\n')
        
        # Save template
        self.save_executive_template(company)

    def save_executive_template(self, company):
        """Save executive research template"""
        safe_company = company.replace(' ', '_').lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/executive_template_{safe_company}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Executive Intelligence Report for: {company}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("EXECUTIVE PROFILE TEMPLATE\n")
                f.write("-" * 80 + "\n\n")
                
                f.write("Name: _____________________\n")
                f.write("Title: _____________________\n")
                f.write("Email: _____________________\n")
                f.write("Phone: _____________________\n")
                f.write("LinkedIn: _____________________\n\n")
                
                f.write("BACKGROUND:\n")
                f.write("- Previous Company: _____________________\n")
                f.write("- Education: _____________________\n")
                f.write("- Years of Experience: _____________________\n\n")
                
                f.write("PUBLIC PRESENCE:\n")
                f.write("- Twitter: _____________________\n")
                f.write("- Personal Website: _____________________\n")
                f.write("- Recent Articles: _____________________\n\n")
                
                f.write("SEARCH QUERIES USED:\n")
                f.write(f'- site:linkedin.com/in/ "{company}" CEO\n')
                f.write(f'- site:crunchbase.com "{company}" founders\n')
                f.write(f'- "{company}" executive team\n')
            
            Logger.success(f"Executive template saved: {filename}")
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def manual_linkedin_osint(self, target):
        """Complete LinkedIn OSINT investigation guide"""
        clear_screen()
        print_header("MANUAL LINKEDIN OSINT INVESTIGATION", 80)
        
        print(f"\n{C_OK}[*] Target: {C_WARN}{target}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  STEP-BY-STEP LINKEDIN INVESTIGATION GUIDE                                ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        investigation_steps = {
            'PHASE 1: Profile Discovery': {
                'objective': 'Find the target\'s LinkedIn profile',
                'methods': [
                    ('Direct LinkedIn Search', f'https://www.linkedin.com/search/results/people/?keywords={target}'),
                    ('Google Search', f'site:linkedin.com/in/ "{target}"'),
                    ('Company Filter', 'Use LinkedIn filters: Location, Company, School'),
                    ('Mutual Connections', 'Check "People Also Viewed" section'),
                ]
            },
            'PHASE 2: Profile Analysis': {
                'objective': 'Extract all public information from profile',
                'data_points': [
                    'Current job title and company',
                    'Work history (previous companies)',
                    'Education (universities, degrees, years)',
                    'Skills and endorsements (technical skills)',
                    'Recommendations (who endorsed them)',
                    'Volunteer experience',
                    'Languages spoken',
                    'Contact info (email, phone if public)',
                    'Profile summary/bio',
                ]
            },
            'PHASE 3: Network Mapping': {
                'objective': 'Map connections and relationships',
                'actions': [
                    'View all connections (if profile is public)',
                    'Identify key connections (colleagues, managers)',
                    'Note mutual connections (shared network)',
                    'Check group memberships (professional groups)',
                    'Follow company page for updates',
                    'Track connection count over time',
                ]
            },
            'PHASE 4: Activity Monitoring': {
                'objective': 'Monitor target\'s online activity',
                'tracking': [
                    'Recent posts and articles (opinions, interests)',
                    'Likes and comments (engagement patterns)',
                    'Shared content (what they care about)',
                    'Posting frequency (how active they are)',
                    'Professional interests (topics they discuss)',
                    'Job changes (profile updates)',
                ]
            },
            'PHASE 5: Data Extraction & Documentation': {
                'objective': 'Save and organize collected intelligence',
                'methods': [
                    'Screenshot profile (save as image)',
                    'Copy profile URL (bookmark)',
                    'Save post links (archive important posts)',
                    'Document connection changes (track network)',
                    'Export to spreadsheet (organize data)',
                    'Set up alerts (monitor changes)',
                ]
            },
        }
        
        investigation_log = []
        
        for phase, details in investigation_steps.items():
            print(f"\n{C_OK}{'=' * 77}{C_RESET}")
            print(f"{C_OK}{phase}{C_RESET}")
            print(f"{C_INFO}Objective: {details['objective']}{C_RESET}")
            print(f"{C_OK}{'=' * 77}{C_RESET}\n")
            
            if 'methods' in details:
                for i, (method, info) in enumerate(details['methods'], 1):
                    print(f"{C_INFO}{i}. {method}{C_RESET}")
                    print(f"   → {info}\n")
                    investigation_log.append(f"{phase} - {method}: {info}")
            
            elif 'data_points' in details:
                print(f"{C_WARN}Data to Collect:{C_RESET}")
                for point in details['data_points']:
                    print(f"{C_INFO}  □ {point}{C_RESET}")
                    investigation_log.append(f"{phase} - {point}")
                print()
            
            elif 'actions' in details:
                for action in details['actions']:
                    print(f"{C_INFO}  • {action}{C_RESET}")
                    investigation_log.append(f"{phase} - {action}")
                print()
            
            elif 'tracking' in details:
                for item in details['tracking']:
                    print(f"{C_INFO}  ▸ {item}{C_RESET}")
                    investigation_log.append(f"{phase} - {item}")
                print()
        
        # Pro Tips
        print(f"\n{C_OK}{'=' * 77}{C_RESET}")
        print(f"{C_WARN}PRO TIPS FOR EFFECTIVE OSINT:{C_RESET}")
        print(f"{C_OK}{'=' * 77}{C_RESET}\n")
        
        tips = [
            'Use incognito mode to avoid being detected',
            'Create a fake LinkedIn account for advanced searches',
            'Use Sales Navigator for advanced filtering (30-day trial)',
            'Check archived versions of profiles (Wayback Machine)',
            'Cross-reference info with other platforms (Twitter, GitHub)',
            'Document everything with timestamps',
            'Respect privacy and legal boundaries',
        ]
        
        for i, tip in enumerate(tips, 1):
            print(f"{C_INFO}{i}. {tip}{C_RESET}")
        
        print()
        
        # Save investigation checklist
        self.save_investigation_checklist(target, investigation_log)

    def save_investigation_checklist(self, target, log):
        """Save LinkedIn investigation checklist"""
        safe_target = target.replace(' ', '_').lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/linkedin_osint_{safe_target}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"LinkedIn OSINT Investigation Checklist\n")
                f.write(f"Target: {target}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("INVESTIGATION CHECKLIST:\n")
                f.write("-" * 80 + "\n\n")
                
                for item in log:
                    f.write(f"[ ] {item}\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("FINDINGS TEMPLATE:\n")
                f.write("-" * 80 + "\n\n")
                f.write("Profile URL: _____________________\n")
                f.write("Current Title: _____________________\n")
                f.write("Current Company: _____________________\n")
                f.write("Location: _____________________\n")
                f.write("Email: _____________________\n")
                f.write("Connection Count: _____________________\n")
                f.write("Key Skills: _____________________\n")
                f.write("Education: _____________________\n\n")
                f.write("NOTES:\n")
                f.write("_" * 80 + "\n")
            
            Logger.success(f"Investigation checklist saved: {filename}")
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def linkedin_dorks(self, target):
        """Generate LinkedIn Google dorks"""
        clear_screen()
        print_header("LINKEDIN GOOGLE DORKS", 80)
        
        print(f"\n{C_OK}[*] Target: {C_WARN}{target}{C_RESET}\n")
        
        dorks = [
            (f'site:linkedin.com/in/ "{target}"', 'Find profiles'),
            (f'site:linkedin.com/in/ "{target}" AND "email"', 'Profiles with email'),
            (f'site:linkedin.com/in/ "{target}" AND "phone"', 'Profiles with phone'),
            (f'site:linkedin.com/company/{target}', 'Company page'),
            (f'site:linkedin.com/in/ "{target}" AND "CEO"', 'CEO profiles'),
            (f'site:linkedin.com/in/ "{target}" AND "engineer"', 'Engineers'),
            (f'site:linkedin.com/pulse "{target}"', 'Published articles'),
            (f'site:linkedin.com/in/ "{target}" filetype:pdf', 'PDFs with target'),
            (f'site:linkedin.com intext:"{target}" intext:"@"', 'Email mentions'),
            (f'site:linkedin.com/jobs "{target}"', 'Job listings'),
        ]
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  LINKEDIN GOOGLE DORKS                                                    ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        for i, (dork, desc) in enumerate(dorks, 1):
            print(f"{C_OK}{i:2}. {desc:30}{C_RESET}")
            print(f"    {dork}\n")
        
        self.save_dorks(target, dorks)
    
    def save_email_patterns(self, company, domain, patterns):
        """Save email patterns to file"""
        safe_company = company.replace(' ', '_').lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/email_patterns_{safe_company}_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"Email Patterns for: {company}\n")
                f.write(f"Domain: {domain}\n")
                f.write("=" * 80 + "\n\n")
                
                for pattern, example in patterns:
                    f.write(f"{pattern:20} {example}\n")
            
            Logger.success(f"Patterns saved: {filename}")
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def save_dorks(self, target, dorks):
        """Save dorks to file"""
        safe_target = target.replace(' ', '_').lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/linkedin_dorks_{safe_target}_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"LinkedIn Dorks for: {target}\n")
                f.write("=" * 80 + "\n\n")
                
                for dork, desc in dorks:
                    f.write(f"{desc}:\n{dork}\n\n")
            
            Logger.success(f"Dorks saved: {filename}")
        except Exception as e:
            Logger.error(f"Failed to save: {str(e)}")
    
    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            
            clear_screen()
            print_header("TARGET INPUT", 80)
            
            if choice in ['1', '2', '3', '4', '5']:
                target = input(f"\n{C_INFO}Enter company name: {C_RESET}").strip()
            else:
                target = input(f"\n{C_INFO}Enter target (company/person): {C_RESET}").strip()
            
            if not target:
                Logger.warning("Target required!")
                pause()
                continue
            
            if choice == '1':
                self.company_employee_search(target)
            elif choice == '2':
                self.email_pattern_discovery(target)
            elif choice == '3':
                self.department_mapping(target)
            elif choice == '4':
                self.technology_stack(target)
            elif choice == '5':
                self.executive_intelligence(target)
            elif choice == '6':
                self.manual_linkedin_osint(target)
            elif choice == '7':
                self.linkedin_dorks(target)
            else:
                Logger.error("Invalid choice!")
            
            pause()


def run_inspy():
    """Entry point"""
    tool = Inspy()
    tool.run()


if __name__ == "__main__":
    run_inspy()