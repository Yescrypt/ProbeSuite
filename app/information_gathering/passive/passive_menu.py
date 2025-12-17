# app/information_gathering/passive/passive_menu.py

import sys
import os
import time

# ProbeSuite root yo‘lini qo‘shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO
from app.utils import Logger, clear_screen, pause

# ──────────────────────────────────────────────────────────────────────────────
# TOOLLAR IMPORT (Xatoliklarga chidamli qilingan)
# ──────────────────────────────────────────────────────────────────────────────

# 1. Wappalyzer
try:
    from app.information_gathering.passive.wappalyzer import run_wappalyzer
except ImportError:
    def run_wappalyzer(*args, **kwargs): print(f"{C_ERR}wappalyzer.py topilmadi!{C_RESET}")

# 2. Link Gopher
try:
    from app.information_gathering.passive.linkgopher import run_linkgopher
except ImportError:
    def run_linkgopher(*args, **kwargs): print(f"{C_ERR}linkgopher.py topilmadi!{C_RESET}")

# 3. Redirect Path
try:
    from app.information_gathering.passive.redirect_path import run_redirect_path
except ImportError:
    def run_redirect_path(*args, **kwargs): print(f"{C_ERR}redirect_path.py topilmadi!{C_RESET}")

# 4. Security Headers
try:
    from app.information_gathering.passive.security_headers import run_security_headers
except ImportError:
    def run_security_headers(*args, **kwargs): print(f"{C_WARN}security_headers.py hali tayyor emas{C_RESET}")

# 5. DNS Lookup
try:
    from app.information_gathering.passive.dns_lookup import run_dns_lookup
except ImportError:
    def run_dns_lookup(*args, **kwargs): print(f"{C_ERR}dns_lookup.py topilmadi!{C_RESET}")

# 6. Shodan.io
try:
    from app.information_gathering.passive.shodan_lookup import run_shodan_lookup
except ImportError:
    def run_shodan_lookup(*args, **kwargs): print(f"{C_WARN}shodan_lookup.py hali tayyor emas{C_RESET}")

# 7. Wayback URLs
try:
    from app.information_gathering.passive.waybackurls import run_wayback_urls
except ImportError:
    def run_wayback_urls(*args, **kwargs): print(f"{C_WARN}waybackurls.py hali tayyor emas{C_RESET}")

# 8. WHOIS LOOKUP – ENDI XAVFSIZ!
try:
    from app.information_gathering.passive.whois_lookup import run_whois
except ImportError as e:
    print(f"{C_ERR}[!] whois_lookup.py da xato yoki run_whois funksiyasi yo‘q → {e}{C_RESET}")
    # Agar fayl buzilgan bo‘lsa – oddiy funksiya yaratamiz
    def run_whois(target=""):
        print(f"{C_ERR}WHOIS tool topilmadi yoki ishlamayapti!{C_RESET}")
        print(f"{C_WARN}whois_lookup.py faylini yangilang.{C_RESET}")
        pause()

# ──────────────────────────────────────────────────────────────────────────────

class PassiveMenu:
    def __init__(self):
        self.tools = {
            '1': ('Wappalyzer',          self.wappalyzer_tool),
            '2': ('Link Gopher',         self.linkgopher_tool),
            '3': ('Redirect Path',       self.redirect_path_tool),
            '4': ('Security Headers',    self.security_headers_tool),
            '5': ('DNS Lookup',          self.dns_lookup_tool),
            '6': ('Shodan.io',           self.shodan_tool),
            '7': ('Wayback URLs',        self.waybackurls_tool),
            '9': ('WHOIS Lookup',        self.whois_tool),          # ← 9-raqam to‘g‘ri
        }

    def display_menu(self):
        clear_screen()
        print(f"{C_INFO}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                     PASSIVE INFORMATION GATHERING MENU                       ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C_RESET}\n")

        for key, (name, _) in sorted(self.tools.items(), key=lambda x: x[0]):
            status = f"{C_OK}● Active{C_RESET}" if key in ['1','2','3','4','5','6','7','9'] else f"{C_WARN}○ Soon{C_RESET}"
            print(f"  {C_INFO}{key}. {C_RESET}{name:<30} {status}")

        print(f"\n  {C_WARN}0. Back to main menu{C_RESET}")
        print(f"{C_INFO}╚{'═' * 78}╝{C_RESET}")

    # ─── TOOLLAR ──────────────────────────────────────────────────────────────
    def wappalyzer_tool(self, url):      run_wappalyzer(url)
    def linkgopher_tool(self, url):      run_linkgopher(url)
    def redirect_path_tool(self, url):   run_redirect_path(url)
    def security_headers_tool(self, url):run_security_headers(url)
    def dns_lookup_tool(self, domain):   run_dns_lookup(domain)
    def shodan_tool(self, query):        run_shodan_lookup(query)
    def waybackurls_tool(self, domain):  run_wayback_urls(domain)

    def whois_tool(self, domain):
        Logger.info(f"WHOIS Lookup → {domain}")
        run_whois(domain)                # ← Bu endi har doim ishlaydi!

    # ─── ASOSIY SIKL ───────────────────────────────────────────────────────────
    def run(self):
        while True:
            self.display_menu()
            choice = input(f"\n{C_INFO}She11> {C_RESET}").strip()

            if choice == '0':
                return

            if choice not in self.tools:
                print(f"{C_ERR}Noto‘g‘ri tanlov!{C_RESET}")
                time.sleep(1)
                continue

            tool_name, tool_func = self.tools[choice]

            # Domen so‘raladigan toollar
            if choice in ['5', '7', '9']:        # DNS, Wayback, WHOIS
                target = input(f"{C_INFO}Domen kiriting (masalan: google.com): {C_RESET}").strip()
                if not target:
                    continue
                tool_func(target)
            else:
                target = input(f"{C_INFO}URL kiriting (masalan: https://example.com): {C_RESET}").strip()
                if not target:
                    continue
                if not target.startswith(('http://', 'https://')):
                    target = 'https://' + target
                tool_func(target)

            pause()   # Har qanday tool ishlagandan keyin pauza

# ──────────────────────────────────────────────────────────────────────────────
def run_passive_menu():
    try:
        PassiveMenu().run()
    except KeyboardInterrupt:
        print(f"\n{C_WARN}Menudan chiqildi.{C_RESET}")
    except Exception as e:
        Logger.error(f"Passive menu xatosi: {e}")

if __name__ == "__main__":
    run_passive_menu()