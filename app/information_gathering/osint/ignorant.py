# app/information_gathering/osint/ignorant.py

import sys
import os
import re
import subprocess
import socket
import smtplib
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, print_header, print_footer, pause, clear_screen

class Ignorant:
    """Professional Email Validation and Verification Tool"""
    
    def __init__(self):
        self.tool_path = self.check_installation()
        # <<< YANGI QOʻSHILDI >>> Papkani oldindan yaratamiz
        self.reports_dir = "reports/osint/ignorant"
        os.makedirs(self.reports_dir, exist_ok=True)

    def check_installation(self):
        """Check if ignorant is installed"""
        try:
            result = subprocess.run(['which', 'ignorant'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None
    
    def display_menu(self):
        """Display ignorant menu"""
        clear_screen()
        print_header("IGNORANT - EMAIL VALIDATION & VERIFICATION", 80)
        
        print(f"\n{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  Advanced email validation, verification, and intelligence gathering.     ║{C_RESET}")
        print(f"{C_INFO}║  Check email validity, existence, and gather associated information.      ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        print(f"{C_OK}1. Email Format Validator{C_RESET}    - Syntax and RFC compliance check")
        print(f"{C_OK}2. Domain Verification{C_RESET}       - MX records and DNS lookup")
        print(f"{C_OK}3. SMTP Verification{C_RESET}         - Check if mailbox exists")
        print(f"{C_OK}4. Disposable Email Detector{C_RESET} - Identify temp/fake emails")
        print(f"{C_OK}5. Email Reputation{C_RESET}          - Check spam/blacklist status")
        print(f"{C_OK}6. Breach Database Check{C_RESET}     - Search data leaks")
        print(f"{C_OK}7. Comprehensive Analysis{C_RESET}    - Full email intelligence")
        print(f"{C_OK}8. Batch Validation{C_RESET}          - Multiple email check")
        
        print(f"\n{C_WARN}0. Back{C_RESET}")
        print_footer()
    
    def validate_email_format(self, email):
        """Validate email format"""
        clear_screen()
        print_header("EMAIL FORMAT VALIDATION", 80)
        
        print(f"\n{C_OK}[*] Validating: {C_WARN}{email}{C_RESET}\n")
        
        # RFC 5322 regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  FORMAT ANALYSIS                                                          ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        checks = []
        
        # Basic format
        if re.match(pattern, email):
            checks.append((True, 'RFC 5322 Compliant', 'OK'))
        else:
            checks.append((False, 'RFC 5322 Compliant', 'ERROR'))
        
        # @ symbol
        if email.count('@') == 1:
            checks.append((True, 'Single @ Symbol', 'OK'))
        else:
            checks.append((False, 'Single @ Symbol', 'ERROR'))
        
        # Local part
        local = email.split('@')[0] if '@' in email else ''
        if len(local) > 0 and len(local) <= 64:
            checks.append((True, 'Valid Local Part Length', 'OK'))
        else:
            checks.append((False, 'Valid Local Part Length', 'ERROR'))
        
        # Domain part
        domain = email.split('@')[1] if '@' in email else ''
        if len(domain) > 0 and len(domain) <= 255:
            checks.append((True, 'Valid Domain Length', 'OK'))
        else:
            checks.append((False, 'Valid Domain Length', 'ERROR'))
        
        # TLD check
        if '.' in domain and len(domain.split('.')[-1]) >= 2:
            checks.append((True, 'Valid TLD', 'OK'))
        else:
            checks.append((False, 'Valid TLD', 'ERROR'))
        
        # No spaces
        if ' ' not in email:
            checks.append((True, 'No Whitespace', 'OK'))
        else:
            checks.append((False, 'No Whitespace', 'ERROR'))
        
        # Display results
        for status, check, symbol in checks:
            color = C_OK if status else C_ERR
            print(f"{color}{symbol} {check:40}{C_RESET}")
        
        # Overall verdict
        all_pass = all(check[0] for check in checks)
        print(f"\n{C_INFO}{'─' * 77}{C_RESET}")
        
        if all_pass:
            print(f"{C_OK}OK Email format is VALID{C_RESET}\n")
        else:
            print(f"{C_ERR}ERROR Email format is INVALID{C_RESET}\n")

        # <<< YANGI: Natija saqlanadi >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"format_check_{email.replace('@', '_at_')}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Email Format Validation - {email}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            for status, check, symbol in checks:
                f.write(f"{symbol} {check}\n")
            f.write(f"\nVerdict: {'VALID' if all_pass else 'INVALID'}\n")
        Logger.success(f"Format report saved: {filename}")

        return all_pass
    
    def verify_domain(self, email):
        """Verify email domain"""
        clear_screen()
        print_header("DOMAIN VERIFICATION", 80)
        
        if '@' not in email:
            Logger.error("Invalid email format!")
            return False
        
        domain = email.split('@')[1]
        
        print(f"\n{C_OK}[*] Verifying domain: {C_WARN}{domain}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  DNS & MX RECORDS                                                         ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        result_text = ""
        success = False
        
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            
            print(f"{C_OK}OK MX Records Found:{C_RESET}\n")
            result_text += "MX Records Found:\n"
            for i, mx in enumerate(mx_records, 1):
                line = f"  {i}. {mx.exchange} (Priority: {mx.preference})\n"
                print(line.strip())
                result_text += line
            print(f"\n{C_OK}OK Domain is configured for email{C_RESET}\n")
            result_text += "\nDomain accepts email\n"
            success = True
            
        except ImportError:
            Logger.warning("dnspython not installed - using socket")
            try:
                socket.gethostbyname(domain)
                print(f"{C_OK}OK Domain exists{C_RESET}")
                print(f"{C_WARN}WARNING Install dnspython for MX record check{C_RESET}\n")
                result_text += "Domain exists (A record)\nMX check unavailable (dnspython missing)\n"
                success = True
            except socket.gaierror:
                print(f"{C_ERR}ERROR Domain does not exist{C_RESET}\n")
                result_text += "Domain does not exist\n"
                
        except Exception as e:
            print(f"{C_ERR}ERROR No MX records found{C_RESET}")
            print(f"{C_WARN}Domain may not accept emails{C_RESET}\n")
            result_text += f"No MX records: {str(e)}\n"

        # <<< Saqlash >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"domain_check_{email.replace('@', '_at_')}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Domain Verification - {email}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            f.write(result_text)
        Logger.success(f"Domain report saved: {filename}")

        return success
    
    def smtp_verification(self, email):
        """SMTP mailbox verification"""
        clear_screen()
        print_header("SMTP MAILBOX VERIFICATION", 80)
        
        print(f"\n{C_OK}[*] Checking: {C_WARN}{email}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  SMTP VERIFICATION                                                        ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        domain = email.split('@')[1]
        result_text = f"Target: {email}\nDomain: {domain}\n\n"
        exists = None
        
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_host = str(mx_records[0].exchange).rstrip('.')
            
            print(f"{C_INFO}Connecting to mail server: {mx_host}{C_RESET}")
            result_text += f"Mail server: {mx_host}\n\n"
            
            server = smtplib.SMTP(timeout=10)
            server.set_debuglevel(0)
            server.connect(mx_host)
            server.helo("localhost")
            server.mail('test@example.com')
            code, message = server.rcpt(email)
            server.quit()
            
            msg = message.decode('utf-8', errors='ignore')
            result_text += f"Response Code: {code}\nResponse: {msg}\n\n"
            
            if code == 250:
                print(f"{C_OK}OK Mailbox EXISTS{C_RESET}")
                print(f"{C_INFO}Response: {msg}{C_RESET}\n")
                result_text += "VERDICT: Mailbox exists\n"
                exists = True
            else:
                print(f"{C_ERR}ERROR Mailbox does NOT exist{C_RESET}")
                print(f"{C_INFO}Response: {msg}{C_RESET}\n")
                result_text += "VERDICT: Mailbox does not exist\n"
                exists = False
                
        except ImportError:
            print(f"{C_WARN}dnspython required for SMTP verification{C_RESET}")
            print(f"{C_INFO}Install: pip install dnspython{C_RESET}\n")
            result_text += "ERROR: dnspython not installed\n"
        except Exception as e:
            err = str(e)
            print(f"{C_WARN}WARNING SMTP verification inconclusive{C_RESET}")
            print(f"{C_INFO}Reason: {err}{C_RESET}\n")
            result_text += f"ERROR: {err}\nVERDICT: Unknown\n"

        # <<< Saqlash >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"smtp_check_{email.replace('@', '_at_')}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"SMTP Verification - {email}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            f.write(result_text)
        Logger.success(f"SMTP report saved: {filename}")

        return exists
    
    def detect_disposable(self, email):
        """Detect disposable/temporary email"""
        clear_screen()
        print_header("DISPOSABLE EMAIL DETECTION", 80)
        
        print(f"\n{C_OK}[*] Analyzing: {C_WARN}{email}{C_RESET}\n")
        
        disposable_domains = [
            'tempmail.com', 'guerrillamail.com', '10minutemail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org',
            'maildrop.cc', 'sharklasers.com', 'guerrillamail.info',
            'grr.la', 'guerrillamail.biz', 'guerrillamail.de',
            'spam4.me', 'trash-mail.com', 'yopmail.com'
        ]
        
        domain = email.split('@')[1]
        is_disposable = domain.lower() in disposable_domains
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  DISPOSABLE EMAIL ANALYSIS                                                ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        if is_disposable:
            print(f"{C_ERR}ERROR DISPOSABLE EMAIL DETECTED{C_RESET}")
            print(f"{C_INFO}Domain: {domain} is a known temporary email service{C_RESET}\n")
        else:
            print(f"{C_OK}OK Not a known disposable domain{C_RESET}\n")
            print(f"{C_INFO}Online verification resources:{C_RESET}")
            print(f"  • https://www.validator.pizza/email/{email}")
            print(f"  • https://disposable.debounce.io/?email={email}")
            print(f"  • https://block-temporary-email.com/check/{domain}\n")

        # <<< Saqlash >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"disposable_check_{email.replace('@', '_at_')}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Disposable Email Check - {email}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            f.write(f"Domain: {domain}\n")
            f.write(f"Known disposable: {'Yes' if is_disposable else 'No'}\n")
        Logger.success(f"Disposable report saved: {filename}")

        return is_disposable
    
    def check_reputation(self, email):
        """Check email reputation"""
        clear_screen()
        print_header("EMAIL REPUTATION CHECK", 80)
        
        print(f"\n{C_OK}[*] Checking reputation: {C_WARN}{email}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  REPUTATION RESOURCES                                                     ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        resources = [
            ('EmailRep.io', f'https://emailrep.io/{email}'),
            ('Spamhaus', 'https://www.spamhaus.org/lookup/'),
            ('Barracuda', 'https://www.barracudacentral.org/lookups'),
            ('MXToolbox', f'https://mxtoolbox.com/SuperTool.aspx?action=blacklist:{email}'),
            ('Talos Intelligence', 'https://talosintelligence.com/reputation'),
        ]
        
        for i, (service, url) in enumerate(resources, 1):
            print(f"{C_OK}{i}. {service:20}{C_RESET}")
            print(f"   {C_INFO}{url}{C_RESET}\n")
        
        print(f"{C_WARN}Visit these services to check if email is blacklisted{C_RESET}\n")

        # <<< Saqlash >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"reputation_check_{email.replace('@', '_at_')}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Email Reputation Resources - {email}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            for service, url in resources:
                f.write(f"{service}: {url}\n")
        Logger.success(f"Reputation links saved: {filename}")
    
    def check_breaches(self, email):
        """Check data breach databases"""
        clear_screen()
        print_header("BREACH DATABASE CHECK", 80)
        
        print(f"\n{C_OK}[*] Checking breaches: {C_WARN}{email}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  DATA BREACH DATABASES                                                    ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        databases = [
            ('Have I Been Pwned', f'https://haveibeenpwned.com/account/{email}'),
            ('DeHashed', f'https://www.dehashed.com/search?query={email}'),
            ('LeakCheck', f'https://leakcheck.io/search/{email}'),
            ('IntelX', f'https://intelx.io/?s={email}'),
            ('Snusbase', 'https://snusbase.com/'),
        ]
        
        for i, (db, url) in enumerate(databases, 1):
            print(f"{C_OK}{i}. {db:20}{C_RESET}")
            print(f"   {C_INFO}{url}{C_RESET}\n")
        
        print(f"{C_WARN}Check if email appears in data breaches{C_RESET}\n")

        # <<< Saqlash >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"breach_check_{email.replace('@', '_at_')}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Data Breach Check Links - {email}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            for db, url in databases:
                f.write(f"{db}: {url}\n")
        Logger.success(f"Breach links saved: {filename}")
    
    def comprehensive_analysis(self, email):
        """Full email intelligence analysis"""
        clear_screen()
        print_header("COMPREHENSIVE EMAIL ANALYSIS", 80)
        
        print(f"\n{C_OK}[*] Analyzing: {C_WARN}{email}{C_RESET}\n")
        
        results = {}
        
        print(f"{C_INFO}[1/5] Validating format...{C_RESET}")
        results['format'] = self.validate_email_format(email)
        pause()
        
        print(f"{C_INFO}[2/5] Verifying domain...{C_RESET}")
        results['domain'] = self.verify_domain(email)
        pause()
        
        print(f"{C_INFO}[3/5] Checking disposable...{C_RESET}")
        results['disposable'] = self.detect_disposable(email)
        pause()
        
        print(f"{C_INFO}[4/5] SMTP verification...{C_RESET}")
        results['smtp'] = self.smtp_verification(email)
        pause()
        
        clear_screen()
        print_header("ANALYSIS SUMMARY", 80)
        
        print(f"\n{C_OK}Email: {C_WARN}{email}{C_RESET}\n")
        
        print(f"{C_INFO}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_INFO}║  RESULTS                                                                  ║{C_RESET}")
        print(f"{C_INFO}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        summary_lines = []
        for check, result in results.items():
            if result is True:
                print(f"{C_OK}OK {check.capitalize():20} PASS{C_RESET}")
                summary_lines.append(f"{check.capitalize():20} PASS")
            elif result is False:
                print(f"{C_ERR}ERROR {check.capitalize():20} FAIL{C_RESET}")
                summary_lines.append(f"{check.capitalize():20} FAIL")
            else:
                print(f"{C_WARN}? {check.capitalize():20} UNKNOWN{C_RESET}")
                summary_lines.append(f"{check.capitalize():20} UNKNOWN")

        # <<< Umumiy report >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"comprehensive_{email.replace('@', '_at_')}_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"COMPREHENSIVE EMAIL ANALYSIS - {email}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            for line in summary_lines:
                f.write(line + "\n")
        Logger.success(f"Full report saved: {filename}")
    
    def batch_validation(self):
        """Validate multiple emails"""
        clear_screen()
        print_header("BATCH EMAIL VALIDATION", 80)
        
        print(f"\n{C_INFO}Enter emails (one per line, empty to finish):{C_RESET}\n")
        
        emails = []
        while True:
            email = input(f"{C_INFO}Email #{len(emails)+1}: {C_RESET}").strip()
            if not email:
                break
            emails.append(email)
        
        if not emails:
            Logger.warning("No emails provided!")
            return
        
        print(f"\n{C_OK}[*] Validating {len(emails)} email(s)...{C_RESET}\n")
        
        results = []
        
        for i, email in enumerate(emails, 1):
            print(f"{C_INFO}[{i}/{len(emails)}] {email}{C_RESET}")
            
            valid_format = self.validate_email_format(email)
            valid_domain = self.verify_domain(email)
            
            results.append({
                'email': email,
                'format': 'PASS' if valid_format else 'FAIL',
                'domain': 'PASS' if valid_domain else 'FAIL'
            })
        
        print(f"\n{C_OK}╔═══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_OK}║  BATCH RESULTS                                                            ║{C_RESET}")
        print(f"{C_OK}╚═══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
        
        for r in results:
            status = "OK" if r['format'] == 'PASS' and r['domain'] == 'PASS' else "ERROR"
            color = C_OK if status == "OK" else C_ERR
            print(f"{color}{status} {r['email']}{C_RESET}")

        # <<< Batch report >>>
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"batch_validation_{timestamp}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"BATCH EMAIL VALIDATION - {len(results)} emails\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("="*80 + "\n\n")
            for r in results:
                f.write(f"{r['email']}\n")
                f.write(f"  Format: {r['format']}\n")
                f.write(f"  Domain: {r['domain']}\n\n")
        Logger.success(f"Batch report saved: {filename}")
    
    def run(self):
        """Main run loop"""
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
            
            if choice == '0':
                return
            
            if choice == '8':
                self.batch_validation()
                pause()
                continue
            
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                clear_screen()
                print_header("EMAIL INPUT", 80)
                
                email = input(f"\n{C_INFO}Enter email address: {C_RESET}").strip()
                
                if not email:
                    Logger.warning("Email required!")
                    pause()
                    continue
                
                if choice == '1':
                    self.validate_email_format(email)
                elif choice == '2':
                    self.verify_domain(email)
                elif choice == '3':
                    self.smtp_verification(email)
                elif choice == '4':
                    self.detect_disposable(email)
                elif choice == '5':
                    self.check_reputation(email)
                elif choice == '6':
                    self.check_breaches(email)
                elif choice == '7':
                    self.comprehensive_analysis(email)
                
                pause()
            else:
                Logger.error("Invalid choice!")
                pause()


def run_ignorant():
    """Entry point"""
    tool = Ignorant()
    tool.run()


if __name__ == "__main__":
    run_ignorant()