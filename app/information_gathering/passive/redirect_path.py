# app/information_gathering/passive/redirect_path.py

import os
import sys
import requests
import warnings
from urllib.parse import urlparse, urljoin
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

# InsecureRequestWarning ni yo‘q qilish
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# ProbeSuite yo‘lini qo‘shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, C_TITLE, USER_AGENT
from app.utils import Logger, clear_screen


class RedirectPathTracker:
    def __init__(self):
        self.redirect_chain = []
        self.final_url = ""
        self.start_time = datetime.now()
        # <<< YANGI >>> Umumiy reports papkasi
        self.reports_dir = "reports/information_gathering/passive/redirectpath"
        os.makedirs(self.reports_dir, exist_ok=True)

    def banner(self):
        clear_screen()
        print(f"{C_TITLE}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                           REDIRECT PATH TRACKER v2.0                         ║")
        print("║                     HTTPS downgrade • Open Redirect • Chain                  ║")
        print("║         Natija → reports/passive/redirectpath/redirectpath_*.txt            ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C_RESET}")

    def track(self, url):
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        self.banner()
        print(f"{C_INFO}[*] Boshlang‘ich URL → {url}{C_RESET}\n")

        headers = {"User-Agent": USER_AGENT}
        current_url = url
        seen = set()
        step = 1
        max_steps = 15

        while step <= max_steps:
            if current_url in seen:
                print(f"{C_ERR}Loop aniqlandi! {current_url}{C_RESET}")
                break
            seen.add(current_url)

            try:
                # HEAD so‘rov — tezroq va kamroq trafik
                response = requests.head(
                    current_url,
                    headers=headers,
                    timeout=15,
                    allow_redirects=False,
                    verify=False
                )
                status = response.status_code
                location = response.headers.get("Location", "")

            except requests.exceptions.RequestException as e:
                print(f"{C_ERR}Xato: {e}{C_RESET}")
                break

            # Ma'lumotlarni saqlash
            entry = {
                "step": step,
                "url": current_url,
                "status": status,
                "location": location
            }
            self.redirect_chain.append(entry)

            # Chiqarish
            arrow = "Final" if status < 300 or status >= 400 else "Redirect"
            color = C_OK if status < 300 else C_WARN if status in [301, 302] else C_ERR
            print(f"  {color}{step:>2} → {status} {arrow}{C_RESET} {current_url}")

            if location:
                next_url = urljoin(current_url, location)
                print(f"       ↓")
                print(f"     {C_INFO}{next_url}{C_RESET}\n")
            else:
                print(f"       {C_OK}Final URL{C_RESET}\n")
                self.final_url = current_url
                break

            # Redirect bo‘lsa davom etamiz
            if status in [301, 302, 303, 307, 308] and location:
                current_url = urljoin(current_url, location)
                step += 1
            else:
                self.final_url = current_url
                break
        else:
            print(f"{C_WARN}Maksimal redirectlar soni (15) ga yetdi!{C_RESET}")

        self.show_analysis()
        self.save_report(url)

    def show_analysis(self):
        print(f"{C_TITLE}══════════════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f"{C_OK}        REDIRECT ZANJIRI TUGALLANDI!{C_RESET}")
        print(f"{C_TITLE}══════════════════════════════════════════════════════════════════════════════{C_RESET}\n")

        start = self.redirect_chain[0]["url"]
        final = self.final_url

        print(f"{C_INFO}Boshlang‘ich URL :{C_RESET} {start}")
        print(f"{C_INFO}Yakuniy URL      :{C_RESET} {final}")
        print(f"{C_INFO}Redirectlar soni :{C_RESET} {len(self.redirect_chain) - 1}")
        print(f"{C_INFO}Vaqt             :{C_RESET} {(datetime.now() - self.start_time).seconds} sekund\n")

        # XAVFSIZLIK OGOHLANTIRISHLARI
        warnings_found = False

        # HTTPS → HTTP downgrade
        if start.startswith("https://") and final.startswith("http://"):
            print(f"{C_ERR}HTTPS dan HTTP ga tushish aniqlandi! (Open Redirect xavfi){C_RESET}")
            warnings_found = True

        # Tashqi domen ga redirect
        start_domain = urlparse(start).netloc
        final_domain = urlparse(final).netloc
        if start_domain != final_domain:
            print(f"{C_WARN}Domen o‘zgardi: {start_domain} → {final_domain} (Open Redirect){C_RESET}")
            warnings_found = True

        # Uzun zanjir
        if len(self.redirect_chain) > 5:
            print(f"{C_WARN}Juda uzun redirect zanjiri ({len(self.redirect_chain)}) — SEO va xavfsizlik muammosi{C_RESET}")
            warnings_found = True

        if not warnings_found:
            print(f"{C_OK}Xavfsizlik muammosi topilmadi. Redirectlar toza!{C_RESET}")

        print(f"{C_TITLE}══════════════════════════════════════════════════════════════════════════════{C_RESET}")

    def save_report(self, original_url):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_domain = urlparse(original_url).netloc.replace(".", "_")
        filename = f"redirectpath_{safe_domain}_{timestamp}.txt"
        path = os.path.join(self.reports_dir, filename)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"REDIRECT PATH TRACKER REPORT\n")
                f.write(f"Original URL: {original_url}\n")
                f.write(f"Final URL: {self.final_url}\n")
                f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Redirects: {len(self.redirect_chain) - 1}\n")
                f.write("="*80 + "\n\n")
                for r in self.redirect_chain:
                    f.write(f"[{r['step']}] {r['status']} → {r['url']}\n")
                    if r['location']:
                        f.write(f"     ↓ Location: {r['location']}\n")
                f.write("\nFINAL URL: " + self.final_url + "\n")

            print(f"\n{C_OK}[+] Report saqlandi!{C_RESET}")
            print(f" → {C_INFO}{path}{C_RESET}\n")
        except Exception as e:
            print(f"{C_ERR}Saqlashda xato: {e}{C_RESET}")

    def run(self, target):
        self.track(target)
        input(f"\n{C_WARN}Press Enter to continue...{C_RESET}")


# ───────────────────────────────────────
def run_redirect_path(target=""):
    if not target:
        target = input(f"{C_INFO}Enter URL (masalan: google.com): {C_RESET}").strip()
    RedirectPathTracker().run(target)


if __name__ == "__main__":
    run_redirect_path()