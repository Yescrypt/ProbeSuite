#!/usr/bin/env python3
# app/config.py - ProbeSuite Configuration
import os
from colorama import Fore, Style, init

# Colorama init
init(autoreset=True)

# ====================
# VERSION
# ====================
VERSION = "1.61"
BANNER = f"ProbeSuite v{VERSION}"

# ====================
# PATHS
# ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE_DIR, 'app')
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Create directories if not exist
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(TOOLS_DIR, exist_ok=True)
os.makedirs(os.path.join(REPORTS_DIR, 'scanning'), exist_ok=True)
os.makedirs(os.path.join(REPORTS_DIR, 'scanning', 'active'), exist_ok=True)
os.makedirs(os.path.join(REPORTS_DIR, 'scanning', 'passive'), exist_ok=True)
os.makedirs(os.path.join(REPORTS_DIR, 'information_gathering'), exist_ok=True)

# ====================
# API KEYS
# ====================
SHODAN_API_KEY = ""  # https://account.shodan.io/
VIRUSTOTAL_API_KEY = ""  # https://virustotal.com
HUNTER_API_KEY = ""  # https://hunter.io
CENSYS_API_ID = ""  # https://censys.io
CENSYS_API_SECRET = ""

# ====================
# TOOLS PATHS
# ====================
TOOLS = {
    'nmap': 'nmap',
    'nikto': 'nikto',
    'dirsearch': os.path.join(TOOLS_DIR, 'dirsearch/dirsearch.py'),
    'gobuster': 'gobuster',
    'dnsrecon': os.path.join(TOOLS_DIR, 'dnsrecon/dnsrecon.py'),
    'wfuzz': 'wfuzz',
    'sublist3r': os.path.join(TOOLS_DIR, 'sublist3r/sublist3r.py'),
    'findomain': 'findomain',
    'assetfinder': 'assetfinder',
    'whatweb': 'whatweb',
    'feroxbuster': 'feroxbuster',
    'wpscan': 'wpscan',
    'masscan': 'masscan',
    'sqlmap': 'sqlmap',
    'zenmap': 'zenmap',
    'ipscan': 'ipscan',
}

# ====================
# COLORS
# ====================
C_TITLE = Fore.CYAN + Style.BRIGHT
C_OK = Fore.GREEN + Style.BRIGHT
C_WARN = Fore.YELLOW + Style.BRIGHT
C_ERR = Fore.RED + Style.BRIGHT
C_INFO = Fore.BLUE + Style.BRIGHT
C_RESET = Style.RESET_ALL

# ====================
# USER AGENT
# ====================
USER_AGENT = f"ProbeSuite/{VERSION} (Penetration Testing Framework)"

# ====================
# TIMEOUTS
# ====================
REQUEST_TIMEOUT = 10
NMAP_TIMEOUT = 300
SCAN_TIMEOUT = 600

# ====================
# THREADING
# ====================
MAX_THREADS = 10

# ====================
# WORDLISTS
# ====================
WORDLISTS = {
    'directories': '/usr/share/wordlists/dirb/common.txt',
    'subdomains': '/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt',
    'passwords': '/usr/share/wordlists/rockyou.txt',
    'web_content': '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
}

# ====================
# NMAP PROFILES
# ====================
NMAP_PROFILES = {
    'light': '-sV --script vuln -p 1-1000 -T4',
    'medium': '-sV -sC -A -p 1-10000 -T4',
    'aggressive': '-sV -sC -A -p- --script all -T4',
    'stealth': '-sS -p 1-1000 -T2',
}

# ====================
# HEADERS
# ====================
HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# ====================
# SCAN PORTS
# ====================
COMMON_PORTS = "21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080"
WEB_PORTS = "80,443,8000,8001,8008,8080,8443,8888,9000,9001,9090"
DATABASE_PORTS = "1433,1521,3306,5432,5984,6379,27017,27018,27019,28017"