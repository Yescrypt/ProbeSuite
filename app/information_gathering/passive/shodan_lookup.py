# app/information_gathering/passive/shodan_lookup.py
import os
import sys
import socket
import requests
from datetime import datetime

# ─────── Loyiha ildizini aniqlash (ProbeSuite papkasi) ───────
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
sys.path.insert(0, BASE_DIR)

# ─────── .env yuklash ───────
from dotenv import load_dotenv
env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# ─────── Ranglar va utilitalar ───────
from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, C_TITLE, REPORTS_DIR
from app.utils import clear_screen


class ShodanLookup:
    def __init__(self):
        self.api_key = os.getenv("SHODAN_API_KEY", "").strip()

    def banner(self):
        clear_screen()
        print(f"{C_TITLE}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                              SHODAN.IO LOOKUP                                ║")
        print("║                   Internet-connected Devices Intelligence                    ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C_RESET}")

    def lookup(self, target):
        self.banner()

        target = target.strip()
        if "://" in target:
            target = target.split("//")[-1].split("/")[0].split(":")[0]

        try:
            ip = socket.gethostbyname(target)
        except:
            print(f"{C_ERR}[!] Domenni IP ga aylantirib bo‘lmadi: {target}{C_RESET}")
            input(f"\n{C_WARN}Enter bosib davom eting...{C_RESET}")
            return

        print(f"{C_INFO}[*] Shodan.io dan ma'lumot olinmoqda → {target} ({ip}){C_RESET}\n")

        if not self.api_key or len(self.api_key) < 20:
            print(f"{C_WARN}[!] SHODAN_API_KEY topilmadi → Demo rejim ishlayapti{C_RESET}")
            print(f"{C_INFO}    To‘liq natija uchun .env faylga quyidagicha yozing:")
            print(f"{C_OK}    SHODAN_API_KEY=sizning_haqiqiy_key{C_RESET}\n")
            self.demo_result(target, ip)
        else:
            self.real_shodan_lookup(target, ip)

        input(f"\n{C_WARN}Enter bosib davom eting...{C_RESET}")

    def real_shodan_lookup(self, domain, ip):
        try:
            url = f"https://api.shodan.io/shodan/host/{ip}"
            response = requests.get(url, params={"key": self.api_key}, timeout=20)

            if response.status_code == 401:
                print(f"{C_ERR}[!] API Key noto‘g‘ri yoki muddati tugagan!{C_RESET}")
                print(f"{C_WARN}    Demo rejimga o‘tildi...{C_RESET}")
                self.demo_result(domain, ip)
                return
            if response.status_code == 404:
                print(f"{C_WARN}[!] {domain} ({ip}) Shodan bazasida yo‘q{C_RESET}")
                print(f"{C_INFO}    → Ko‘pincha Cloudflare/AWS himoyasi tufayli shunday bo‘ladi.{C_RESET}")
                return
            if response.status_code != 200:
                print(f"{C_ERR}[!] Shodan xatosi: {response.status_code}{C_RESET}")
                return

            data = response.json()
            self.display_real_results(data, domain, ip)
            self.save_report(data, domain, ip)

        except requests.exceptions.RequestException:
            print(f"{C_ERR}[!] Internetga ulanishda xato!{C_RESET}")
        except Exception as e:
            print(f"{C_ERR}[!] Kutilmagan xato: {e}{C_RESET}")

    def demo_result(self, domain, ip):
        print(f"{C_TITLE}╔{'═'*98}╗{C_RESET}")
        print(f"{C_TITLE}║{C_RESET}{C_WARN} {'DEMO REJIM — HAQIQIY NATIJA EMAS':^96} {C_RESET}{C_TITLE}║{C_RESET}")
        print(f"{C_TITLE}╠{'═'*98}╣{C_RESET}")
        demo_info = [
            ("Domen", domain),
            ("IP", ip),
            ("Mamlakat", "United States"),
            ("Tashkilot", "Cloudflare / Akamai / AWS"),
            ("Ochiq portlar", "0 ta (himoyalangan)"),
            ("Holati", "Shodan bazasida ko‘rinmaydi"),
            ("Izoh", "Katta kompaniyalar odatda himoyalangan"),
        ]
        for k, v in demo_info:
            print(f"{C_TITLE}║{C_RESET} {C_INFO}{k:<18}{C_RESET}: {C_OK}{v}{C_RESET}{C_TITLE}║{C_RESET}")
        print(f"{C_TITLE}╚{'═'*98}╝{C_RESET}")
        print(f"\n{C_WARN}Haqiqiy natija uchun .env faylga SHODAN_API_KEY yozing!{C_RESET}")

    def display_real_results(self, data, domain, ip):
        w = 98
        print(f"{C_TITLE}╔{'═'*w}╗{C_RESET}")
        print(f"{C_TITLE}║{C_RESET}{C_OK} {'SHODAN.IO — HAQIQIY NATIJA':^96} {C_RESET}{C_TITLE}║{C_RESET}")
        print(f"{C_TITLE}╠{'═'*w}╣{C_RESET}")

        info = [
            ("Domen", domain),
            ("IP", ip),
            ("Mamlakat", data.get("country_name", "Nomaʼlum")),
            ("Shahar", data.get("city", "Nomaʼlum")),
            ("Tashkilot", data.get("org", "Nomaʼlum")),
            ("ISP", data.get("isp", "Nomaʼlum")),
            ("Hostname(lar)", ", ".join(data.get("hostnames", [])) or "Yoʻq"),
            ("Ochiq portlar", f"{len(data.get('ports', []))} ta"),
            ("OS", data.get("os", "Aniqlanmadi")),
            ("Zaifliklar", f"{len(data.get('vulns', {}))} ta"),
            ("Oxirgi skan", data.get("last_update", "Nomaʼlum")),
        ]

        for k, v in info:
            print(f"{C_TITLE}║{C_RESET} {C_INFO}{k:<18}{C_RESET}: {C_OK}{str(v):<76}{C_RESET}{C_TITLE}║{C_RESET}")

        print(f"{C_TITLE}╠{'═'*w}╣{C_RESET}")
        services = data.get("data", [])[:8]
        if not services:
            print(f"{C_TITLE}║{C_RESET}   → {C_WARN}Hech qanday ochiq servis topilmadi{C_RESET}{C_TITLE}║{C_RESET}")
        else:
            for s in services:
                port = s["port"]
                prod = f"{s.get('product','')} {s.get('version','')}".strip() or "Nomaʼlum"
                banner = str(s.get("data","")).replace("\n"," ").replace("\r","")[:90]
                if len(banner) >= 90: banner = banner[:87] + "..."
                print(f"{C_TITLE}║{C_RESET}   {C_OK}{port:>5}{C_RESET} │ {C_INFO}{prod}{C_RESET}")
                if banner.strip():
                    print(f"{C_TITLE}║{C_RESET}       └─ {C_WARN}{banner}{C_RESET}{C_TITLE}║{C_RESET}")

        print(f"{C_TITLE}╚{'═'*w}╝{C_RESET}")
        print(f"\n{C_OK}Shodan skani muvaffaqiyatli yakunlandi!{C_RESET}\n")

    def save_report(self, data, domain, ip):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"reports/information_gathering/shodan/shodan_{domain}_{ts}.txt"
        try:
            with open(os.path.join(REPORTS_DIR, fn), "w", encoding="utf-8") as f:
                f.write(f"SHODAN.IO - {domain} ({ip})\n")
                f.write(f"Vaqt: {datetime.now()}\n{'='*80}\n\n")
                f.write(f"Mamlakat   : {data.get('country_name','N/A')}\n")
                f.write(f"Tashkilot  : {data.get('org','N/A')}\n")
                f.write(f"Portlar    : {len(data.get('ports',[]))}\n")
                f.write(f"OS         : {data.get('os','N/A')}\n")
            print(f"{C_OK}[+] Hisobot saqlandi → {C_INFO}{fn}{C_RESET}")
        except:
            pass


def run_shodan_lookup(target=""):
    if not target:
        target = input(f"{C_INFO}Domen yoki IP kiriting (masalan: tesla.com): {C_RESET}").strip()
    ShodanLookup().lookup(target)


if __name__ == "__main__":
    run_shodan_lookup()