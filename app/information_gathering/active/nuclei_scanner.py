#!/usr/bin/env python3
# app/information_gathering/active/nuclei_scanner.py
# Nuclei → reports/nuclei/target_YYYYMMDD_HHMMSS.txt

import os
import sys
import subprocess
from datetime import datetime

# Loyiha root'ini qo'shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import clear_screen, pause


def banner():
    clear_screen()
    print(f"""
{C_OK}╔════════════════════════════════════════════════════════════════════════════════╗
║                       NUCLEI — HAQIQIY ZAIFLIKLARNI TOPADI                     ║
║               reports/information_gathering/active/nuclei/target_.txt          ║
╚════════════════════════════════════════════════════════════════════════════════╝{C_RESET}
""")


def install_nuclei():
    print(f"{C_WARN}[~] nuclei topilmadi → avtomatik o'rnatilmoqda...{C_RESET}")
    try:
        subprocess.run(
            "curl -sfL https://install.projectdiscovery.io/nuclei.sh | sh -s -- -y",
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.local/bin")
        print(f"{C_OK}[+] nuclei muvaffaqiyatli o'rnatildi!{C_RESET}")
        return True
    except Exception as e:
        print(f"{C_ERR}nuclei o'rnatib bo'lmadi: {e}{C_RESET}")
        return False


def update_templates():
    print(f"{C_WARN}[~] Nuclei template'lari yangilanmoqda...{C_RESET}")
    subprocess.run(["nuclei", "-update-templates", "-silent"], stdout=subprocess.DEVNULL)


def run_nuclei_scanner():
    banner()

    target = input(f"\n{C_INFO}URL kiriting (https:// yoki http:// bilan) → {C_RESET}").strip()
    if not target:
        print(f"{C_ERR}Target kiritilmadi!{C_RESET}")
        pause()
        return

    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    print(f"\n{C_OK}Target → {target}{C_RESET}\n")

    # nuclei bor-yo'qligini tekshirish
    if subprocess.run(["which", "nuclei"], capture_output=True).returncode != 0:
        if not install_nuclei():
            pause()
            return

    # Template'larni yangilash (faqat bir marta kerak, lekin xavfsiz)
    try:
        update_templates()
    except:
        pass

    # Fayl tayyorlash
    output_dir = "reports/information_gathering/active/nuclei"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = target.replace("://", "_").replace("/", "_").replace(":", "_")
    output_file = f"{output_dir}/{safe_name}_{timestamp}.txt"

    cmd = [
        "nuclei",
        "-u", target,
        "-severity", "info,low,medium,high,critical,unknown",
        "-c", "100",                     # concurrency
        "-rl", "150",                    # rate limit
        "-o", output_file,
        "-jsonl",                        # har bir natija alohida qatorda
        "-silent",                       # faqat natijalarni chiqaradi
        "-stats"
    ]

    print(f"{C_INFO}Skan boshlandi... (30-90 soniya){C_RESET}\n")
    print(f"{C_WARN}{'═' * 80}{C_RESET}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)

        # Ekranga chiqarish
        if result.stdout.strip():
            print(f"\n{C_OK}TOPILGAN NATIJALAR:{C_RESET}\n")
            for line in result.stdout.strip().splitlines():
                line = line.strip()
                if not line:
                    continue
                if "critical" in line.lower():
                    print(f"{C_ERR}[CRITICAL] {line}{C_RESET}")
                elif "high" in line.lower():
                    print(f"{C_WARN}[HIGH]     {line}{C_RESET}")
                elif "medium" in line.lower():
                    print(f"{C_WARN}[MEDIUM]   {line}{C_RESET}")
                elif "low" in line.lower():
                    print(f"{C_INFO}[LOW]      {line}{C_RESET}")
                else:
                    print(f"{C_INFO}[INFO]     {line}{C_RESET}")
        else:
            print(f"{C_WARN}[~] Hech qanday natija topilmadi (yoki faqat info darajasi){C_RESET}")

        # Agar fayl bo'sh bo'lsa — ma'lumot qo'shamiz
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# Nuclei Scan • {target}\n")
                f.write(f"# {datetime.now()}\n")
                f.write("# No vulnerabilities detected or scan completed with info only\n")

        print(f"\n{C_OK}SCAN TUGADI! Natija saqlandi:{C_RESET}")
        print(f" → {C_INFO}{output_file}{C_RESET}\n")

    except subprocess.TimeoutExpired:
        print(f"{C_ERR}Vaqt tugadi (15 daqiqa)!{C_RESET}")
    except Exception as e:
        print(f"{C_ERR}Xato: {e}{C_RESET}")

    pause()


if __name__ == "__main__":
    run_nuclei_scanner()