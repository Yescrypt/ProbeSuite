#!/usr/bin/env python3
"""
ProBeSuite - Shodan Scanner Module
Internet-Connected Device Search
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET, REPORTS_DIR, SHODAN_API_KEY
from app.utils import Logger, CommandRunner, InputValidator, clear_screen, pause, ReportWriter


class ShodanScanner:
    def __init__(self):
        self.api_key = SHODAN_API_KEY
        self.output_dir = Path(REPORTS_DIR) / "scanning" / "passive" / "shodan"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                🌐 SHODAN - IOT SCANNER 🌐                   ║
║          Search Engine for Internet-Connected Devices        ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(f"{C_INFO}{banner}{C_RESET}")
    
    def show_menu(self):
        menu = """
╭─ SHODAN SEARCH OPTIONS ──────────────────────────────────────╮
│                                                               │
│  BASIC SEARCHES:                                             │
│    [1]  IP Address Lookup                                    │
│    [2]  Domain/Hostname Search                              │
│    [3]  Search by Query                                      │
│                                                               │
│  ADVANCED SEARCHES:                                           │
│    [4]  Organization Search                                  │
│    [5]  Product/Service Search                              │
│    [6]  Vulnerability Search (CVE)                          │
│    [7]  Port Search                                          │
│    [8]  Country Search                                       │
│                                                               │
│  SHODAN CLI (Requires API):                                  │
│    [9]  Host Information                                     │
│    [10] Count Results                                        │
│    [11] Download Search Results                             │
│                                                               │
│  BROWSER SEARCH:                                              │
│    [12] Open Shodan Website                                  │
│                                                               │
│  CONFIGURATION:                                               │
│    [13] Set API Key                                          │
│    [14] Test API Key                                         │
│                                                               │
│  [0]  ← Back                                                 │
│                                                               │
╰───────────────────────────────────────────────────────────────╯

{api_status}
        """
        
        if self.api_key:
            api_status = f"{C_OK}[✓] API Key configured{C_RESET}"
        else:
            api_status = f"{C_WARN}[!] API Key not configured - Limited functionality{C_RESET}"
        
        print(menu.format(api_status=api_status))
    
    def check_shodan_cli(self):
        """Check if Shodan CLI is installed"""
        return CommandRunner.check_tool('shodan')
    
    def get_output_file(self, search_type, query):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = query.replace(' ', '_').replace('/', '_').replace(':', '_')[:50]
        return self.output_dir / f"{search_type}_{safe_query}_{timestamp}.txt"
    
    def browser_search(self, query):
        """Open Shodan in browser"""
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.shodan.io/search?query={encoded_query}"
        
        Logger.info("Opening Shodan in browser...")
        os.system(f"xdg-open '{url}' 2>/dev/null || open '{url}' 2>/dev/null || start '{url}'")
        Logger.success("Browser opened")
    
    def cli_search(self, query, output_file):
        """Search using Shodan CLI"""
        if not self.check_shodan_cli():
            Logger.error("Shodan CLI not installed!")
            Logger.info("Install: pip install shodan")
            return False
        
        if not self.api_key:
            Logger.error("API key not configured!")
            Logger.info("Get API key from: https://account.shodan.io/")
            return False
        
        Logger.info(f"Searching: {query}")
        cmd = f"shodan search '{query}' > {output_file}"
        
        returncode = os.system(cmd)
        
        if returncode == 0:
            Logger.success(f"Results saved: {output_file}")
            
            # Display results
            try:
                with open(output_file, 'r') as f:
                    content = f.read()
                    if content.strip():
                        print(f"\n{C_INFO}Results:{C_RESET}")
                        print(content[:1000])  # First 1000 chars
                        if len(content) > 1000:
                            print(f"\n{C_WARN}... (truncated, see full results in file){C_RESET}")
                    else:
                        Logger.warning("No results found")
            except Exception as e:
                Logger.error(f"Error reading results: {e}")
            
            return True
        else:
            Logger.error("Search failed")
            return False
    
    def ip_lookup(self):
        """Lookup specific IP"""
        ip = InputValidator.get_ip()
        if not ip:
            return
        
        output = self.get_output_file("ip_lookup", ip)
        
        if self.check_shodan_cli() and self.api_key:
            Logger.info(f"Looking up IP: {ip}")
            cmd = f"shodan host {ip}"
            
            returncode, stdout, stderr = CommandRunner.run(cmd, shell=True, timeout=30)
            
            if returncode == 0:
                with open(output, 'w') as f:
                    f.write(ReportWriter.create_report_header("Shodan IP Lookup", ip))
                    f.write(stdout)
                
                print(f"\n{C_INFO}IP Information:{C_RESET}")
                print(stdout)
                Logger.success(f"Results saved: {output}")
            else:
                Logger.error("Lookup failed")
                self.browser_search(ip)
        else:
            self.browser_search(ip)
    
    def domain_search(self):
        """Search by domain"""
        domain = InputValidator.get_domain()
        if not domain:
            return
        
        query = f"hostname:{domain}"
        output = self.get_output_file("domain", domain)
        
        if self.check_shodan_cli() and self.api_key:
            self.cli_search(query, output)
        else:
            self.browser_search(query)
    
    def query_search(self):
        """Custom query search"""
        print(f"\n{C_INFO}[*] Shodan Query Examples:{C_RESET}")
        print("  • product:Apache")
        print("  • port:22")
        print("  • country:US")
        print("  • city:London")
        print("  • os:Windows")
        print("  • vuln:CVE-2021-44228")
        
        query = input(f"\n{C_INFO}Enter Shodan query: {C_RESET}").strip()
        if not query:
            Logger.error("Query cannot be empty")
            return
        
        output = self.get_output_file("query", query)
        
        if self.check_shodan_cli() and self.api_key:
            self.cli_search(query, output)
        else:
            self.browser_search(query)
    
    def organization_search(self):
        """Search by organization"""
        org = input(f"{C_INFO}Enter organization name: {C_RESET}").strip()
        if not org:
            return
        
        query = f"org:\"{org}\""
        output = self.get_output_file("org", org)
        
        if self.check_shodan_cli() and self.api_key:
            self.cli_search(query, output)
        else:
            self.browser_search(query)
    
    def product_search(self):
        """Search by product/service"""
        product = input(f"{C_INFO}Enter product name (e.g., Apache, nginx): {C_RESET}").strip()
        if not product:
            return
        
        query = f"product:{product}"
        output = self.get_output_file("product", product)
        
        if self.check_shodan_cli() and self.api_key:
            self.cli_search(query, output)
        else:
            self.browser_search(query)
    
    def vulnerability_search(self):
        """Search by CVE"""
        cve = input(f"{C_INFO}Enter CVE ID (e.g., CVE-2021-44228): {C_RESET}").strip()
        if not cve:
            return
        
        query = f"vuln:{cve}"
        output = self.get_output_file("vuln", cve)
        
        if self.check_shodan_cli() and self.api_key:
            self.cli_search(query, output)
        else:
            self.browser_search(query)
    
    def port_search(self):
        """Search by port"""
        port = input(f"{C_INFO}Enter port number: {C_RESET}").strip()
        if not port or not port.isdigit():
            Logger.error("Invalid port")
            return
        
        query = f"port:{port}"
        output = self.get_output_file("port", port)
        
        if self.check_shodan_cli() and self.api_key:
            self.cli_search(query, output)
        else:
            self.browser_search(query)
    
    def country_search(self):
        """Search by country"""
        print(f"\n{C_INFO}[*] Use 2-letter country codes (e.g., US, GB, DE, CN){C_RESET}")
        country = input(f"{C_INFO}Enter country code: {C_RESET}").strip().upper()
        if not country or len(country) != 2:
            Logger.error("Invalid country code")
            return
        
        query = f"country:{country}"
        output = self.get_output_file("country", country)
        
        if self.check_shodan_cli() and self.api_key:
            self.cli_search(query, output)
        else:
            self.browser_search(query)
    
    def count_results(self):
        """Count search results"""
        query = input(f"{C_INFO}Enter search query: {C_RESET}").strip()
        if not query:
            return
        
        if not self.check_shodan_cli() or not self.api_key:
            Logger.error("Shodan CLI with API key required")
            return
        
        Logger.info("Counting results...")
        cmd = f"shodan count '{query}'"
        
        returncode, stdout, stderr = CommandRunner.run(cmd, shell=True, timeout=30)
        
        if returncode == 0:
            print(f"\n{C_OK}[+] Results found: {stdout.strip()}{C_RESET}")
        else:
            Logger.error("Count failed")
    
    def download_results(self):
        """Download search results"""
        query = input(f"{C_INFO}Enter search query: {C_RESET}").strip()
        if not query:
            return
        
        if not self.check_shodan_cli() or not self.api_key:
            Logger.error("Shodan CLI with API key required")
            return
        
        output = self.get_output_file("download", query).with_suffix('.json.gz')
        
        Logger.info("Downloading results...")
        Logger.warning("This may take time and consume API credits!")
        
        if not InputValidator.confirm("Continue?"):
            return
        
        cmd = f"shodan download {output} '{query}'"
        
        returncode = os.system(cmd)
        
        if returncode == 0:
            Logger.success(f"Results downloaded: {output}")
        else:
            Logger.error("Download failed")
    
    def open_website(self):
        """Open Shodan website"""
        Logger.info("Opening Shodan website...")
        os.system("xdg-open 'https://www.shodan.io' 2>/dev/null || open 'https://www.shodan.io' 2>/dev/null || start 'https://www.shodan.io'")
    
    def set_api_key(self):
        """Configure API key"""
        Logger.info("Get your API key from: https://account.shodan.io/")
        
        key = input(f"\n{C_INFO}Enter API key: {C_RESET}").strip()
        if not key:
            return
        
        if self.check_shodan_cli():
            cmd = f"shodan init {key}"
            returncode = os.system(cmd)
            
            if returncode == 0:
                self.api_key = key
                Logger.success("API key configured successfully!")
                Logger.info("Also update SHODAN_API_KEY in app/config.py for persistence")
            else:
                Logger.error("Failed to configure API key")
        else:
            Logger.error("Shodan CLI not installed")
            Logger.info("Install: pip install shodan")
    
    def test_api_key(self):
        """Test API key"""
        if not self.check_shodan_cli():
            Logger.error("Shodan CLI not installed")
            return
        
        if not self.api_key:
            Logger.error("API key not configured")
            return
        
        Logger.info("Testing API key...")
        cmd = "shodan info"
        
        returncode, stdout, stderr = CommandRunner.run(cmd, shell=True, timeout=10)
        
        if returncode == 0:
            Logger.success("API key is valid!")
            print(f"\n{C_INFO}Account Info:{C_RESET}")
            print(stdout)
        else:
            Logger.error("API key test failed")
            if stderr:
                print(stderr)
    
    def run(self):
        while True:
            clear_screen()
            self.print_banner()
            self.show_menu()
            
            choice = InputValidator.get_choice()
            
            if choice == '0':
                break
            elif choice == '1':
                self.ip_lookup()
            elif choice == '2':
                self.domain_search()
            elif choice == '3':
                self.query_search()
            elif choice == '4':
                self.organization_search()
            elif choice == '5':
                self.product_search()
            elif choice == '6':
                self.vulnerability_search()
            elif choice == '7':
                self.port_search()
            elif choice == '8':
                self.country_search()
            elif choice == '9':
                self.ip_lookup()
            elif choice == '10':
                self.count_results()
            elif choice == '11':
                self.download_results()
            elif choice == '12':
                self.open_website()
            elif choice == '13':
                self.set_api_key()
            elif choice == '14':
                self.test_api_key()
            else:
                Logger.error("Invalid option!")
            
            pause()


def main():
    try:
        scanner = ShodanScanner()
        scanner.run()
    except KeyboardInterrupt:
        print(f"\n\n{C_ERR}[!] Interrupted by user{C_RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C_ERR}[!] Error: {e}{C_RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()