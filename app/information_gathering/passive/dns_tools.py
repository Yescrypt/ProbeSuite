import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
from app.utils import Logger, CommandRunner
from app.config import REPORTS_DIR
from datetime import datetime

def run_dns_tools(domain):
    Logger.info(f"DNS Tools: {domain}")
    
    domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
    
    print("\n[*] HOST Command:")
    _, stdout, _ = CommandRunner.run(f"host {domain}")
    print(stdout if stdout else "[!] Command failed")
    
    print("\n[*] DIG Command:")
    _, stdout, _ = CommandRunner.run(f"dig {domain}")
    print(stdout if stdout else "[!] Command failed")
    
    print("\n[*] NSLOOKUP Command:")
    _, stdout, _ = CommandRunner.run(f"nslookup {domain}")
    print(stdout if stdout else "[!] Command failed")
