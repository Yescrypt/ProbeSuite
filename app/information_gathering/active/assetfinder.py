#!/usr/bin/env python3
# app/information_gathering/active/assetfinder.py
# Assetfinder → reports/assetfinder/domain_YYYYMMDD_HHMMSS.txt ga yozadi

import os
import sys
import subprocess
from datetime import datetime

# Loyiha root'ini qo'shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import Logger, clear_screen, pause


def banner():
    clear_screen()
    print(f"""
{C_OK}
    ╔════════════════════════════════════════════════════════════════════════════════════╗
    ║                                 ASSETFINDER SCANNER                                ║
    ║         Natija → reports/information_gathering/assetfinder/domain_*.txt            ║
    ╚════════════════════════════════════════════════════════════════════════════════════╝
{C_RESET}
""")


def run_assetfinder_scanner():
    banner()

    domain = input(f"{C_INFO}Domen kiriting (masalan: tesla.com) → {C_RESET}").strip().lower()
    if not domain or "." not in domain:
        Logger.error("Noto'g'ri domen!")
        pause()
        return

    print(f"\n{C_INFO}Target → {domain}{C_RESET}\n")

    # assetfinder avto-o'rnatish
    if subprocess.run(["which", "assetfinder"], capture_output=True).returncode != 0:
        print(f"{C_WARN}assetfinder topilmadi → o'rnatilmoqda...{C_RESET}")
        subprocess.run(["go", "install", "github.com/tomnomnom/assetfinder@latest"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.environ["PATH"] += os.pathsep + os.path.expanduser("~/go/bin")

    print(f"{C_OK}Subdomain qidirilmoqda...{C_RESET}\n")

    try:
        result = subprocess.run(
            ["assetfinder", "--subs-only", domain],
            capture_output=True, text=True, timeout=180
        )

        if result.returncode != 0:
            print(f"{C_ERR}Xato: {result.stderr.strip()}{C_RESET}")
            pause()
            return

        subs = sorted({line.strip() for line in result.stdout.splitlines() if line.strip() and "." in line})

        print(f"{C_OK}Topildi: {len(subs)} ta subdomain!{C_RESET}\n")
        for i, sub in enumerate(subs[:30], 1):
            print(f"   {C_INFO}{i:2}. {sub}{C_RESET}")
        if len(subs) > 30:
            print(f"   {C_WARN}... +{len(subs)-30} ta → faylda{C_RESET}\n")

        # reports/assetfinder papkasiga saqlash
        os.makedirs("reports/information_gathering/assetfinder", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_domain = domain.replace(".", "_")
        txt_file = f"reports/information_gathering/assetfinder/{safe_domain}_{timestamp}.txt"

        header = f"""# Assetfinder Results
# Target: {domain}
# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Total: {len(subs)} subdomains

"""
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(header + "\n".join(subs))

        print(f"{C_OK}Natija saqlandi!{C_RESET}")
        print(f" → {txt_file}{C_RESET}")

    except Exception as e:
        print(f"{C_ERR}Xato: {e}{C_RESET}")

    pause()


# active_menu.py dan chaqiriladigan funksiya
run_assetfinder_scanner = run_assetfinder_scanner


if __name__ == "__main__":
    run_assetfinder_scanner()