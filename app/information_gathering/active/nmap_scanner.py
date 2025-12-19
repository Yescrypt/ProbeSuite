# app/information_gathering/active/nmap_scanner.py

import os
import sys
import time
import subprocess
from datetime import datetime

# Loyiha root'ini qo'shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, BASE_DIR)

from app.utils import Logger, clear_screen, pause
from app.config import C_OK, C_WARN, C_ERR, C_INFO, C_TITLE, C_RESET


def run_command(cmd, timeout=1200):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", f"[!] Xato: {e}"


def get_nmap_report_path(target):
    """reports/information_gathering/active/nmap/domain_YYYYMMDD_HHMMSS.txt"""
    output_dir = "reports/information_gathering/active/nmap"
    os.makedirs(output_dir, exist_ok=True)
    
    safe_name = target.replace("://", "_").replace("/", "_").replace(":", "_").replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{output_dir}/{safe_name}_{timestamp}.txt"


def save_nmap_result(target, profile_name, command, output):
    report_file = get_nmap_report_path(target)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    separator = "=" * 95
    header = f"""{separator}
[ProbeSuite] NMAP SCAN • {profile_name}
Target       : {target}
Command      : {command}
Started      : {timestamp}
{separator}

"""

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(output if output.strip() else "[No open ports or output]\n")
        f.write(f"\n[{timestamp}] Nmap scan completed\n")
        f.write("-" * 95 + "\n")

    print(f"\n{C_OK}Result saved!{C_RESET}")
    print(f" {C_INFO}File → {report_file}{C_RESET}")


class NmapScanner:
    PROFILES = {
        "1": ("Basic Fast Scan", "nmap -F --open"),
        "2": ("Service Version Deep", "nmap -sV --version-all --open"),
        "3": ("Full Port Scan", "nmap -p- --open"),
        "4": ("SYN Stealth", "nmap -sS -T4 --open"),
        "5": ("UDP Top 100", "nmap -sU --top-ports 100 --open"),
        "6": ("OS + Version + Scripts", "nmap -A -T4"),
        "7": ("Aggressive + Vuln", "nmap -A -p- --script=default,vuln -T4"),
        "8": ("Vuln Scripts Only", "nmap --script vuln,safe,discovery --open"),
        "9": ("Stealth No Ping", "nmap -sS -Pn -T2"),
        "10": ("HTTP/HTTPS Enum", "nmap -p80,443 --script=http-enum,http-title,ssl-enum-ciphers,ssl-cert"),
        "11": ("Banner Grabbing", "nmap -sV --script=banner --version-intensity 9"),
        "12": ("Brute Ready", "nmap --script=brute,auth,default,vuln"),
        "13": ("FULL AGGRESSIVE", "nmap -sS -sV -O -p- -A --script=all --version-all -T4"),
        "14": ("Custom", "CUSTOM"),
    }

    @staticmethod
    def display_menu():
        clear_screen()
        print(f"{C_TITLE}╔{'═'*62}╗{C_RESET}")
        print(f"{C_TITLE}║{' NMAP SCANNER • reports/information_gathering/active/nmap ga yozadi ':^62}║{C_RESET}")
        print(f"{C_TITLE}╚{'═'*62}╝{C_RESET}\n")

        for k, (name, _) in NmapScanner.PROFILES.items():
            icon = C_WARN if k == "14" else C_INFO
            print(f" {icon}[{k.rjust(2)}]{C_RESET} {name}")
        print(f"\n {C_WARN}[ 0 ]{C_RESET} Back")

    @staticmethod
    def get_target():
        print(f"\n{C_INFO}Enter target (IP or domain):{C_RESET}")
        t = input(f" {C_INFO}nmap>{C_RESET} ").strip()
        return t if t else None

    @staticmethod
    def run_scan(target):
        while True:
            NmapScanner.display_menu()
            choice = input(f"\n{C_INFO}Select profile (1-14): {C_RESET}").strip()

            if choice == "0":
                break  # Faqat 0 bosilganda chiqamiz

            if choice not in NmapScanner.PROFILES:
                Logger.error("Invalid choice!")
                time.sleep(1)
                continue

            profile_name, base = NmapScanner.PROFILES[choice]

            if choice == "14":
                print(f"\n{C_INFO}Enter custom nmap arguments:{C_RESET}")
                opts = input(f" {C_INFO}custom>{C_RESET} ").strip()
                if not opts:
                    continue
                cmd = ["nmap"] + opts.split() + [target]
                profile_name = "Custom Scan"
            else:
                cmd = base.split() + [target]

            full_cmd = " ".join(cmd)
            print(f"\n{C_OK}Launching → {profile_name}{C_RESET}")
            print(f"{C_WARN}Command: {full_cmd}{C_RESET}\n")
            print(f"{C_WARN}{'─'*80}{C_RESET}")

            rc, out, err = run_command(cmd, timeout=1800)

            if rc == 0:
                print(out)
                save_nmap_result(target, profile_name, full_cmd, out)
            else:
                print(f"{C_ERR}Error occurred!{C_RESET}")
                if err:
                    print(f"{C_ERR}{err}{C_RESET}")

            print(f"\n{C_OK}Scan completed!{C_RESET}")
            pause()  # Enter bosishni kutamiz, keyin yana menyuga qaytamiz


def run_nmap_scanner():
    clear_screen()
    target = NmapScanner.get_target()
    if not target:
        pause()
        return

    NmapScanner.run_scan(target)

    # Nmap bo‘limidan chiqishdan oldin savol
    print(f"\n{C_INFO}Do you want to stay in the Nmap section with the same target? (y/n): {C_RESET}", end="")
    stay = input().strip().lower()
    if stay == "y" or stay == "yes":
        run_nmap_scanner()  # Rekursiv chaqiruv — yana yangi skan


if __name__ == "__main__":
    run_nmap_scanner()