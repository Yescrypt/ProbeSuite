# app/information_gathering/passive/security_headers.py

import os
import sys
import requests
import warnings
from urllib.parse import urlparse
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

# InsecureRequestWarning ni yo‘q qilish
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# ProbeSuite yo‘lini qo‘shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, C_TITLE, USER_AGENT
from app.utils import Logger, clear_screen


class SecurityHeadersChecker:
    def __init__(self):
        self.headers_to_check = {
            "Strict-Transport-Security": "HSTS - HTTPS ni majburlaydi",
            "Content-Security-Policy": "XSS va injection hujumlaridan himoya",
            "X-Content-Type-Options": "MIME sniffing oldini oladi",
            "X-Frame-Options": "Clickjacking oldini oladi",
            "X-XSS-Protection": "Eski brauzerlarda XSS filtri",
            "Referrer-Policy": "Referer ma'lumotlarini nazorat qiladi",
            "Permissions-Policy": "Brauzer funksiyalarini cheklaydi",
            "Cross-Origin-Opener-Policy": "COOP - Xizmatlar izolyatsiyasi",
            "Cross-Origin-Embedder-Policy": "COEP - Xavfsiz kontekst",
            "Cross-Origin-Resource-Policy": "CORP - Resurslar himoyasi",
        }
        self.found = {}
        self.missing = {}
        # <<< YANGI >>> Umumiy reports papkasi
        self.reports_dir = "reports/information_gathering/passive/securityheaders"
        os.makedirs(self.reports_dir, exist_ok=True)

    def banner(self):
        clear_screen()
        print(f"{C_TITLE}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                       SECURITY HEADERS ANALYZER v2.0                         ║")
        print("║        Bor bo‘lsa Present • Yo‘q bo‘lsa Missing • Tavsiyalar bilan           ║")
        print("║         Natija → reports/passive/securityheaders/securityheaders_*.txt       ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C_RESET}")

    def check(self, url):
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        self.banner()
        print(f"{C_INFO}[*] Sayt tekshirilmoqda → {url}{C_RESET}\n")

        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, timeout=20, verify=False, allow_redirects=True)
            response.raise_for_status()
            resp_headers = response.headers

            print(f"{C_OK}Status: {response.status_code} | Final URL: {response.url}{C_RESET}\n")

            # Case-insensitive tekshirish
            for header in self.headers_to_check:
                found = False
                for h, v in resp_headers.items():
                    if h.lower() == header.lower():
                        value = v[:120] + ("..." if len(v) > 120 else "")
                        self.found[header] = value
                        found = True
                        break
                if not found:
                    self.missing[header] = self.headers_to_check[header]

            self.display_table()
            self.show_recommendations()
            self.save_report(url, response.url)

        except Exception as e:
            print(f"{C_ERR}Xato: {e}{C_RESET}")

    def display_table(self):
        width = 98
        border = C_TITLE
        reset = C_RESET

        print(f"{border}╔{'═' * width}╗{reset}")
        print(f"{border}║{' SECURITY HEADERS NATIJASI '.center(width)}║{reset}")
        print(f"{border}╠{'═' * width}╣{reset}")
        print(f"{border}║{' HEADER NAME ':<45} {' STATUS ':<12} {' IZOH ':<39}║{reset}")
        print(f"{border}╠{'═' * width}╣{reset}")

        for header, desc in self.headers_to_check.items():
            if header in self.found:
                status = f"{C_OK}Present{reset}"
            else:
                status = f"{C_ERR}Missing{reset}"

            print(f"{border}║{reset} {header:<43} {status:<12} {desc:<45}{border}║{reset}")

        print(f"{border}╚{'═' * width}╝{reset}")

        # Natija
        total = len(self.headers_to_check)
        present = len(self.found)
        score = int((present / total) * 100)
        color = C_OK if score >= 80 else C_WARN if score >= 50 else C_ERR
        print(f"\n{C_INFO}UMUMIY NATIJA: {color}{present}/{total} ta header topildi → {score}% xavfsizlik bali{C_RESET}\n")

    def show_recommendations(self):
        print(f"{C_TITLE} TAVSIYALAR (Tezda tuzatish kerak):{C_RESET}")
        print(f"{C_WARN}─────────────────────────────────────────────{C_RESET}")

        if "Strict-Transport-Security" not in self.found:
            print(f"  {C_ERR}Missing{C_RESET} HSTS → HTTPS ni majburlang!")
            print(f"     Misol: Strict-Transport-Security: max-age=31536000; includeSubDomains")

        if "Content-Security-Policy" not in self.found:
            print(f"  {C_ERR}Missing{C_RESET} CSP → XSS hujumlaridan himoya qiling!")
            print(f"     Misol: Content-Security-Policy: default-src 'self'")

        if "X-Frame-Options" not in self.found:
            print(f"  {C_ERR}Missing{C_RESET} X-Frame-Options → Clickjacking oldini oling!")
            print(f"     Misol: X-Frame-Options: DENY")

        if "X-Content-Type-Options" not in self.found:
            print(f"  {C_ERR}Missing{C_RESET} X-Content-Type-Options: nosniff")

        if len(self.missing) == 0:
            print(f"  {C_OK}Ajoyib! Barcha muhim headerlar o‘rnatilgan!{C_RESET}")

        print(f"{C_WARN}─────────────────────────────────────────────{C_RESET}")

    def save_report(self, original, final):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_domain = urlparse(original).netloc.replace(".", "_")
        filename = f"securityheaders_{safe_domain}_{timestamp}.txt"
        path = os.path.join(self.reports_dir, filename)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"SECURITY HEADERS REPORT\n")
                f.write(f"Original URL: {original}\n")
                f.write(f"Final URL: {final}\n")
                f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Score: {len(self.found)}/{len(self.headers_to_check)} ({int((len(self.found)/len(self.headers_to_check))*100)}%)\n")
                f.write("="*80 + "\n\n")
                f.write("PRESENT HEADERS:\n")
                for h, v in self.found.items():
                    f.write(f"Present {h}: {v}\n")
                f.write("\nMISSING HEADERS:\n")
                for h, desc in self.missing.items():
                    f.write(f"Missing {h} → {desc}\n")

            print(f"\n{C_OK}[+] Report saqlandi!{C_RESET}")
            print(f" → {C_INFO}{path}{C_RESET}\n")
        except Exception as e:
            print(f"{C_ERR}Saqlashda xato: {e}{C_RESET}")

    def run(self, target):
        self.check(target)
        input(f"\n{C_WARN}Press Enter to continue...{C_RESET}")


# ───────────────────────────────────────
def run_security_headers(target=""):
    if not target:
        target = input(f"{C_INFO}URL kiriting (masalan: google.com): {C_RESET}").strip()
    SecurityHeadersChecker().run(target)


if __name__ == "__main__":
    run_security_headers()