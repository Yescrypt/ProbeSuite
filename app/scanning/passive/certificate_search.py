#!/usr/bin/env python3
"""
ProBeSuite - Certificate Transparency Search (Fixed)
SSL/TLS Certificate Discovery via crt.sh with rate limiting
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET, REPORTS_DIR
from app.utils import Logger, InputValidator, clear_screen, pause, ReportWriter


class CertificateSearch:
    def __init__(self):
        self.output_dir = Path(REPORTS_DIR) / "scanning" / "passive" / "certificates"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = None
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║          🔐 CERTIFICATE TRANSPARENCY SEARCH 🔐              ║
║            SSL/TLS Certificate Discovery                     ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(f"{C_INFO}{banner}{C_RESET}")
    
    def show_menu(self):
        menu = """
╭─ CERTIFICATE SEARCH OPTIONS ─────────────────────────────────╮
│                                                               │
│  SEARCH METHODS:                                             │
│    [1]  crt.sh Search (Certificate Transparency)            │
│    [2]  SSL Certificate Analysis                            │
│    [3]  Certificate Chain Analysis                          │
│    [4]  Multiple Domain Search                              │
│                                                               │
│  ADVANCED:                                                    │
│    [5]  Export to CSV                                        │
│    [6]  Filter by Date Range                                │
│    [7]  Find Wildcard Certificates                          │
│                                                               │
│  [0]  ← Back                                                 │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
        """
        print(f"{C_OK}{menu}{C_RESET}")
    
    def init_session(self):
        """Initialize requests session with retry logic"""
        try:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
            
            if not self.session:
                self.session = requests.Session()
                
                # Retry strategy
                retry_strategy = Retry(
                    total=3,
                    backoff_factor=2,
                    status_forcelist=[429, 500, 502, 503, 504],
                )
                
                adapter = HTTPAdapter(max_retries=retry_strategy)
                self.session.mount("http://", adapter)
                self.session.mount("https://", adapter)
                
                # Headers to avoid being blocked
                self.session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'application/json',
                    'Accept-Language': 'en-US,en;q=0.9',
                })
            
            return True
        except ImportError:
            Logger.error("'requests' library not installed")
            Logger.info("Install: pip install requests")
            return False
    
    def search_crtsh(self, domain, retry_count=3, delay=5):
        """Search crt.sh with retry and rate limiting"""
        if not self.init_session():
            return None
        
        import requests
        
        Logger.info(f"Searching crt.sh for: {domain}")
        
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        
        for attempt in range(retry_count):
            try:
                if attempt > 0:
                    wait_time = delay * (attempt + 1)
                    Logger.warning(f"Rate limited. Waiting {wait_time} seconds... (Attempt {attempt + 1}/{retry_count})")
                    time.sleep(wait_time)
                
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        Logger.success(f"Retrieved {len(data)} certificates")
                        return data
                    except json.JSONDecodeError:
                        Logger.error("Failed to parse JSON response")
                        return None
                
                elif response.status_code == 429:
                    if attempt < retry_count - 1:
                        continue
                    else:
                        Logger.error("Rate limit exceeded. Please try again later.")
                        Logger.info("Alternative: Use manual search at https://crt.sh")
                        return None
                
                else:
                    Logger.error(f"HTTP Error: {response.status_code}")
                    return None
            
            except requests.exceptions.Timeout:
                Logger.error("Request timeout")
                if attempt < retry_count - 1:
                    continue
                return None
            
            except requests.exceptions.RequestException as e:
                Logger.error(f"Request failed: {e}")
                if attempt < retry_count - 1:
                    continue
                return None
        
        return None
    
    def crtsh_search(self):
        """Main crt.sh search"""
        domain = InputValidator.get_domain()
        if not domain:
            return
        
        output = self.output_dir / f"crtsh_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        output_json = output.with_suffix('.json')
        
        data = self.search_crtsh(domain)
        
        if not data:
            Logger.error("No data retrieved")
            Logger.info("Possible reasons:")
            Logger.info("  1. Rate limiting by crt.sh (try again in a few minutes)")
            Logger.info("  2. Domain has no certificates")
            Logger.info("  3. Network connectivity issues")
            pause()
            return
        
        # Extract unique subdomains
        subdomains = set()
        certificates = []
        
        for cert in data:
            name = cert.get('name_value', '')
            if name:
                for subdomain in name.split('\n'):
                    subdomain = subdomain.strip()
                    if subdomain and domain in subdomain:
                        subdomains.add(subdomain)
            
            certificates.append({
                'common_name': cert.get('common_name', ''),
                'name_value': cert.get('name_value', ''),
                'issuer_name': cert.get('issuer_name', ''),
                'not_before': cert.get('not_before', ''),
                'not_after': cert.get('not_after', ''),
                'serial_number': cert.get('serial_number', '')
            })
        
        # Save text report
        with open(output, 'w') as f:
            f.write(ReportWriter.create_report_header("Certificate Transparency Search", domain))
            f.write(f"Total certificates found: {len(data)}\n")
            f.write(f"Unique subdomains: {len(subdomains)}\n")
            f.write("\n" + "="*80 + "\n")
            f.write("SUBDOMAINS\n")
            f.write("="*80 + "\n\n")
            
            for subdomain in sorted(subdomains):
                f.write(f"{subdomain}\n")
        
        # Save JSON
        with open(output_json, 'w') as f:
            json.dump({
                'domain': domain,
                'timestamp': datetime.now().isoformat(),
                'total_certificates': len(data),
                'unique_subdomains': len(subdomains),
                'subdomains': sorted(list(subdomains)),
                'certificates': certificates
            }, f, indent=2)
        
        # Display results
        print(f"\n{C_OK}{'='*65}{C_RESET}")
        print(f"{C_OK}RESULTS{C_RESET}")
        print(f"{C_OK}{'='*65}{C_RESET}\n")
        print(f"{C_INFO}Total Certificates: {len(data)}{C_RESET}")
        print(f"{C_INFO}Unique Subdomains: {len(subdomains)}{C_RESET}\n")
        
        print(f"{C_INFO}Subdomains:{C_RESET}")
        for subdomain in sorted(subdomains)[:20]:  # Show first 20
            print(f"{C_OK}  [+] {subdomain}{C_RESET}")
        
        if len(subdomains) > 20:
            print(f"\n{C_WARN}  ... and {len(subdomains) - 20} more subdomains{C_RESET}")
        
        Logger.success(f"Report saved: {output}")
        Logger.success(f"JSON saved: {output_json}")
    
    def ssl_analysis(self):
        """Analyze SSL/TLS certificate"""
        domain = InputValidator.get_domain()
        if not domain:
            return
        
        output = self.output_dir / f"ssl_analysis_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        Logger.info(f"Analyzing SSL certificate for: {domain}")
        
        cmd = f"echo | openssl s_client -servername {domain} -connect {domain}:443 2>/dev/null | openssl x509 -text -noout"
        
        Logger.info("Connecting to server...")
        returncode = os.system(f"{cmd} > {output}")
        
        if returncode == 0:
            Logger.success("Certificate analysis completed")
            
            # Display key info
            try:
                with open(output, 'r') as f:
                    content = f.read()
                    print(f"\n{C_INFO}Certificate Information:{C_RESET}")
                    for line in content.split('\n'):
                        if any(kw in line for kw in ['Subject:', 'Issuer:', 'Not Before', 'Not After', 'DNS:', 'Public Key']):
                            print(f"{C_OK}  {line.strip()}{C_RESET}")
            except:
                pass
            
            Logger.success(f"Full report: {output}")
        else:
            Logger.error("Analysis failed - check if port 443 is open")
    
    def certificate_chain(self):
        """Analyze certificate chain"""
        domain = InputValidator.get_domain()
        if not domain:
            return
        
        output = self.output_dir / f"cert_chain_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        Logger.info(f"Analyzing certificate chain for: {domain}")
        
        cmd = f"echo | openssl s_client -servername {domain} -connect {domain}:443 -showcerts 2>/dev/null"
        
        returncode = os.system(f"{cmd} > {output}")
        
        if returncode == 0:
            Logger.success(f"Certificate chain saved: {output}")
        else:
            Logger.error("Failed to retrieve certificate chain")
    
    def multiple_domain_search(self):
        """Search multiple domains"""
        print(f"\n{C_INFO}Enter domains (one per line, empty line to finish):{C_RESET}")
        
        domains = []
        while True:
            domain = input(f"{C_INFO}  Domain: {C_RESET}").strip()
            if not domain:
                break
            domains.append(domain)
        
        if not domains:
            Logger.error("No domains provided")
            return
        
        all_subdomains = {}
        
        for i, domain in enumerate(domains, 1):
            Logger.info(f"Searching: {domain} ({i}/{len(domains)})")
            
            data = self.search_crtsh(domain, retry_count=2, delay=10)
            
            if data:
                subdomains = set()
                for cert in data:
                    name = cert.get('name_value', '')
                    if name:
                        for subdomain in name.split('\n'):
                            subdomain = subdomain.strip()
                            if subdomain and domain in subdomain:
                                subdomains.add(subdomain)
                
                all_subdomains[domain] = sorted(subdomains)
                Logger.success(f"{domain}: {len(subdomains)} subdomains")
            else:
                Logger.warning(f"{domain}: Failed to retrieve data")
                all_subdomains[domain] = []
            
            # Delay between requests to avoid rate limiting
            if i < len(domains):
                Logger.info("Waiting 10 seconds before next request...")
                time.sleep(10)
        
        # Save combined results
        output = self.output_dir / f"multi_domain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'domains': domains,
                'results': all_subdomains
            }, f, indent=2)
        
        # Display summary
        print(f"\n{C_INFO}Summary:{C_RESET}")
        for domain, subs in all_subdomains.items():
            print(f"{C_OK}  {domain}: {len(subs)} subdomains{C_RESET}")
        
        Logger.success(f"Combined results: {output}")
    
    def export_csv(self):
        """Export to CSV"""
        domain = InputValidator.get_domain()
        if not domain:
            return
        
        data = self.search_crtsh(domain)
        
        if not data:
            return
        
        output = self.output_dir / f"crtsh_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            import csv
            
            with open(output, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Common Name', 'Name Value', 'Issuer', 'Not Before', 'Not After', 'Serial Number'])
                
                for cert in data:
                    writer.writerow([
                        cert.get('common_name', ''),
                        cert.get('name_value', '').replace('\n', '; '),
                        cert.get('issuer_name', ''),
                        cert.get('not_before', ''),
                        cert.get('not_after', ''),
                        cert.get('serial_number', '')
                    ])
            
            Logger.success(f"CSV exported: {output}")
        
        except Exception as e:
            Logger.error(f"Export failed: {e}")
    
    def filter_by_date(self):
        """Filter certificates by date range"""
        domain = InputValidator.get_domain()
        if not domain:
            return
        
        print(f"\n{C_INFO}Date Range Filter:{C_RESET}")
        print(f"{C_WARN}Leave empty to skip start/end date{C_RESET}")
        
        start_date_str = input(f"{C_INFO}  Start date (YYYY-MM-DD): {C_RESET}").strip()
        end_date_str = input(f"{C_INFO}  End date (YYYY-MM-DD): {C_RESET}").strip()
        
        data = self.search_crtsh(domain)
        
        if not data:
            return
        
        filtered_certs = []
        
        for cert in data:
            not_before = cert.get('not_before', '')
            not_after = cert.get('not_after', '')
            
            try:
                # Parse dates
                if not_before:
                    cert_start = datetime.fromisoformat(not_before.replace('Z', '+00:00'))
                else:
                    continue
                
                # Apply filters
                if start_date_str:
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                    if cert_start < start_date:
                        continue
                
                if end_date_str:
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                    if cert_start > end_date:
                        continue
                
                filtered_certs.append(cert)
            
            except:
                continue
        
        Logger.info(f"Filtered: {len(filtered_certs)} out of {len(data)} certificates")
        
        if filtered_certs:
            # Extract subdomains from filtered certs
            subdomains = set()
            for cert in filtered_certs:
                name = cert.get('name_value', '')
                if name:
                    for subdomain in name.split('\n'):
                        subdomain = subdomain.strip()
                        if subdomain and domain in subdomain:
                            subdomains.add(subdomain)
            
            print(f"\n{C_INFO}Filtered Subdomains ({len(subdomains)}):{C_RESET}")
            for subdomain in sorted(subdomains)[:20]:
                print(f"{C_OK}  [+] {subdomain}{C_RESET}")
            
            # Save filtered results
            output = self.output_dir / f"filtered_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(output, 'w') as f:
                json.dump({
                    'domain': domain,
                    'timestamp': datetime.now().isoformat(),
                    'filter': {
                        'start_date': start_date_str,
                        'end_date': end_date_str
                    },
                    'total_filtered': len(filtered_certs),
                    'subdomains': sorted(list(subdomains)),
                    'certificates': filtered_certs
                }, f, indent=2)
            
            Logger.success(f"Filtered results saved: {output}")
        else:
            Logger.warning("No certificates match the date filter")
    
    def find_wildcards(self):
        """Find wildcard certificates"""
        domain = InputValidator.get_domain()
        if not domain:
            return
        
        data = self.search_crtsh(domain)
        
        if not data:
            return
        
        wildcards = []
        wildcard_domains = set()
        
        for cert in data:
            name = cert.get('name_value', '')
            if name and '*' in name:
                wildcards.append(cert)
                for subdomain in name.split('\n'):
                    subdomain = subdomain.strip()
                    if subdomain and '*' in subdomain and domain in subdomain:
                        wildcard_domains.add(subdomain)
        
        Logger.info(f"Found {len(wildcards)} wildcard certificates")
        
        if wildcard_domains:
            print(f"\n{C_INFO}Wildcard Certificates:{C_RESET}")
            for wc in sorted(wildcard_domains):
                print(f"{C_OK}  [*] {wc}{C_RESET}")
            
            # Save wildcard results
            output = self.output_dir / f"wildcards_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(output, 'w') as f:
                json.dump({
                    'domain': domain,
                    'timestamp': datetime.now().isoformat(),
                    'total_wildcards': len(wildcards),
                    'wildcard_domains': sorted(list(wildcard_domains)),
                    'certificates': wildcards
                }, f, indent=2)
            
            Logger.success(f"Wildcard results saved: {output}")
        else:
            Logger.warning("No wildcard certificates found")
    
    def run(self):
        while True:
            clear_screen()
            self.print_banner()
            self.show_menu()
            
            choice = InputValidator.get_choice()
            
            if choice == '0':
                break
            elif choice == '1':
                self.crtsh_search()
            elif choice == '2':
                self.ssl_analysis()
            elif choice == '3':
                self.certificate_chain()
            elif choice == '4':
                self.multiple_domain_search()
            elif choice == '5':
                self.export_csv()
            elif choice == '6':
                self.filter_by_date()
            elif choice == '7':
                self.find_wildcards()
            else:
                Logger.error("Invalid option!")
            
            pause()


def main():
    try:
        searcher = CertificateSearch()
        searcher.run()
    except KeyboardInterrupt:
        print(f"\n\n{C_ERR}[!] Interrupted by user{C_RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C_ERR}[!] Error: {e}{C_RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()