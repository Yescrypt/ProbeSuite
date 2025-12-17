# app/information_gathering/passive/linkgopher.py
# LINK GOPHER v2.0 — Barcha link, subdomain, domain, email, telefon! (XATOSIZ)

import os
import re
import sys
import requests
import warnings
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

# XATONI YO‘Q QILISH
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# ProbeSuite yo‘lini qo‘shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, C_TITLE, REPORTS_DIR, USER_AGENT
from app.utils import Logger, clear_screen


class LinkGopher:
    def __init__(self):
        self.main_domain = ""
        self.internal_links = set()
        self.external_links = set()
        self.subdomains = set()
        self.external_domains = set()
        self.emails = set()
        self.phones = set()

    def banner(self):
        clear_screen()
        print(f"{C_TITLE}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                               LINK GOPHER v2.0                               ║")
        print("║              Saytdagi barcha link • subdomain • domain • email • tel         ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C_RESET}")

    def extract_from_html(self, url):
        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, timeout=20, verify=False, allow_redirects=True)
            response.raise_for_status()
            html = response.text
            self.main_domain = urlparse(url).netloc.lower()

            soup = BeautifulSoup(html, 'html.parser')

            # Barcha href/src/action/content larni olish
            for tag in soup.find_all(True):
                for attr in ['href', 'src', 'action', 'content']:
                    value = tag.get(attr)
                    if not value:
                        continue
                    value = value.strip()
                    if not value or value.startswith(('#', 'javascript:', 'data:')):
                        continue

                    full_url = urljoin(url, value)
                    parsed = urlparse(full_url)
                    netloc = parsed.netloc.lower()

                    # Email & Tel
                    if value.startswith('mailto:'):
                        email = value[7:].split('?')[0].split('#')[0]
                        if '@' in email:
                            self.emails.add(email.lower())
                        continue
                    if value.startswith('tel:'):
                        phone = value[4:].split('?')[0]
                        self.phones.add(phone)
                        continue

                    # Ichki yoki tashqi
                    if netloc and (netloc == self.main_domain or netloc.endswith('.' + self.main_domain)):
                        self.internal_links.add(full_url)
                        if netloc != self.main_domain:
                            self.subdomains.add(netloc)
                    elif netloc:
                        self.external_links.add(full_url)
                        self.external_domains.add(netloc)

        except Exception as e:
            Logger.error(f"LinkGopher xatosi: {e}")

    def display_results(self):
        total = len(self.internal_links) + len(self.external_links)
        print(f"\n{C_TITLE}══════════════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f"{C_OK}      SKAN MUVOFFAQIYATLI YAKUNLANDI!{C_RESET}")
        print(f"{C_TITLE}══════════════════════════════════════════════════════════════════════════════{C_RESET}\n")

        # LINKLAR
        print(f"{C_INFO}LINKLAR ({total} ta topildi):{C_RESET}")
        print(f"{C_WARN}─────────────────────────────────────────────{C_RESET}")
        for link in sorted(self.internal_links)[:30]:
            print(f"  {C_OK}Link{C_RESET} {link}")
        if len(self.internal_links) > 30:
            print(f"  {C_WARN}... va yana {len(self.internal_links)-30} ta ichki link{C_RESET}\n")

        for link in sorted(self.external_links)[:15]:
            print(f"  {C_ERR}External{C_RESET} {link}")
        if len(self.external_links) > 15:
            print(f"  {C_WARN}... va yana {len(self.external_links)-15} ta tashqi link{C_RESET}\n")

        # SUBDOMAINLAR
        if self.subdomains:
            print(f"{C_INFO}SUBDOMAINLAR ({len(self.subdomains)} ta):{C_RESET}")
            print(f"{C_WARN}─────────────────────────────────────────────{C_RESET}")
            for sub in sorted(self.subdomains):
                print(f"  {C_OK}Subdomain{C_RESET} {sub}")
            print()

        # TASHQI DOMAINLAR
        if self.external_domains:
            print(f"{C_INFO}TASHQI DOMAINLAR ({len(self.external_domains)} ta):{C_RESET}")
            print(f"{C_WARN}─────────────────────────────────────────────{C_RESET}")
            for dom in sorted(self.external_domains)[:25]:
                print(f"  {C_ERR}Domain{C_RESET} {dom}")
            if len(self.external_domains) > 25:
                print(f"  {C_WARN}... va yana {len(self.external_domains)-25} ta{C_RESET}")
            print()

        # EMAIL & TELEFON
        if self.emails:
            print(f"{C_INFO}EMAIL MANZILLAR ({len(self.emails)} ta):{C_RESET}")
            for email in sorted(self.emails):
                print(f"  {C_OK}Email{C_RESET} {email}")
            print()

        if self.phones:
            print(f"{C_INFO}TELEFON RAQAMLAR ({len(self.phones)} ta):{C_RESET}")
            for phone in sorted(self.phones):
                print(f"  {C_OK}Phone{C_RESET} {phone}")
            print()

        # UMUMIY STATISTIKA
        print(f"{C_TITLE}══════════════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f"{C_OK} UMUMIY NATIJA:{C_RESET}")
        print(f"  {C_INFO}Ichki linklar        :{C_RESET} {len(self.internal_links)}")
        print(f"  {C_INFO}Tashqi linklar       :{C_RESET} {len(self.external_links)}")
        print(f"  {C_INFO}Subdomainlar         :{C_RESET} {len(self.subdomains)}")
        print(f"  {C_INFO}Tashqi domainlar     :{C_RESET} {len(self.external_domains)}")
        print(f"  {C_INFO}Email manzillar      :{C_RESET} {len(self.emails)}")
        print(f"  {C_INFO}Telefon raqamlar     :{C_RESET} {len(self.phones)}")
        print(f"{C_TITLE}══════════════════════════════════════════════════════════════════════════════{C_RESET}")

    def save_report(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_domain = re.sub(r'[^\w\-]', '_', self.main_domain)
        filename = f"information_gathering/linkgopher/linkgopher_{safe_domain}_{timestamp}"

        txt_path = os.path.join(REPORTS_DIR, f"{filename}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"LINK GOPHER v2.0 REPORT\n")
            f.write(f"Target: {self.main_domain}\n")
            f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")

            f.write(f"INTERNAL LINKS ({len(self.internal_links)}):\n")
            for l in sorted(self.internal_links):
                f.write(f"• {l}\n")

            f.write(f"\nSUBDOMAINS ({len(self.subdomains)}):\n")
            for s in sorted(self.subdomains):
                f.write(f"• {s}\n")

            f.write(f"\nEXTERNAL DOMAINS ({len(self.external_domains)}):\n")
            for d in sorted(self.external_domains):
                f.write(f"• {d}\n")

            f.write(f"\nEMAILS:\n")
            for e in sorted(self.emails):
                f.write(f"• {e}\n")

            f.write(f"\nPHONES:\n")
            for p in sorted(self.phones):
                f.write(f"• {p}\n")

        print(f"\n{C_OK}[+] Report saqlandi! → {C_INFO}{filename}.txt{C_RESET}")

    def run(self, target):
        url = target.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        self.banner()
        print(f"{C_INFO}[*] Sayt ochilmoqda → {url}{C_RESET}\n")
        self.extract_from_html(url)
        self.display_results()
        self.save_report()
        input(f"\n{C_WARN}Press Enter to continue...{C_RESET}")


# ───────────────────────────────────────
def run_linkgopher(target=""):
    if not target:
        target = input(f"{C_INFO}Enter URL (masalan: darkhunt.uz): {C_RESET}").strip()
    LinkGopher().run(target)


if __name__ == "__main__":
    run_linkgopher()