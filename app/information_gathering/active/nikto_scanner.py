# app/information_gathering/active/nikto_scanner.py

import os
import subprocess
import socket
import time
import threading
from datetime import datetime
from app.utils import Logger
from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET, C_TITLE

def run_nikto_scanner(target_input: str):
    target = target_input.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    
    try:
        ip = socket.gethostbyname(target)
    except:
        ip = "noma'lum"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = target.replace(".", "_")
    output_file = f"reports/information_gathering/nikto/{ip}_{safe_name}_{timestamp}.txt"
    os.makedirs("reports/information_gathering/nikto", exist_ok=True)

    print(f"\n{C_TITLE}╔{'═'*74}╗{C_RESET}")
    print(f"{C_TITLE}║{'  NIKTO — ULTRA LIGHTNING RECON + REPORT  ':^74}║{C_RESET}")
    print(f"{C_TITLE}╚{'═'*74}╝{C_RESET}\n")
    print(f"{C_INFO} Target  :{C_RESET} {target}")
    print(f"{C_INFO} IP      :{C_RESET} {ip}")
    print(f"{C_INFO} Hisobot :{C_RESET} {output_file}\n")

    # ── Chiroyli loader ─────────────────────────────────────
    stop_loader = threading.Event()
    def loader():
        spinner = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        i = 0
        while not stop_loader.is_set():
            print(f"\r{C_INFO}[*] {spinner[i%8]} Nikto lightning recon ishlamoqda...{C_RESET}", end="", flush=True)
            i += 1
            time.sleep(0.1)
        print("\r" + " " * 80 + "\r", end="")

    threading.Thread(target=loader, daemon=True).start()

    cmd = [
        "nikto", "-h", target, "-port", "80,443",
        "-Tuning", "19", "-no404", "-evasion", "0",
        "-maxtime", "15", "-ask", "no", "-Display", "1234"
    ]

    recon = []

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"NIKTO LIGHTNING RECON — {target}\n")
            f.write(f"IP: {ip} | {datetime.now()}\n")
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write("="*80 + "\n\n")

            for line in result.stdout.splitlines():
                line = line.strip()
                if not line.startswith("+ "):
                    continue

                clean = line[2:].strip()
                f.write(line + "\n")  # Faylga yoziladi

                lower = clean.lower()
                if any(kw in lower for kw in ["server:", "x-frame-options", "x-content-type-options",
                                            "strict-transport-security", "hsts", "content-security-policy",
                                            "x-xss-protection", "cookie", "allowed methods", "robots.txt",
                                            "sitemap.xml", "directory listing"]):
                    recon.append(clean)

    except Exception as e:
        recon = []
    finally:
        stop_loader.set()
        time.sleep(0.2)

    # ── Natija ekranga ─────────────────────────────────────
    print(f"{C_OK}Nikto lightning recon yakunlandi!{C_RESET}\n")

    if recon:
        print(f"{C_TITLE}PENTESTER RECON NATIJALARI:{C_RESET}\n")
        for item in recon:
            lower = item.lower()
            if "server:" in lower:
                print(f"{C_OK}  Server     → {item}{C_RESET}")
            elif any(x in lower for x in ["missing", "not present", "not set", "no hsts"]):
                print(f"{C_ERR}  Header     → {item}{C_RESET}")
            elif "cookie" in lower:
                print(f"{C_WARN}  Cookie     → {item}{C_RESET}")
            elif "allowed methods" in lower:
                print(f"{C_OK}  Methods    → {item}{C_RESET}")
            else:
                print(f"{C_WARN}  Info       → {item}{C_RESET}")
    else:
        print(f"{C_WARN}Hech qanday ma'lumot topilmadi (HTTPS yoki firewall bo'lishi mumkin){C_RESET}")

    print(f"\n{C_TITLE}{'═'*74}{C_RESET}")
    print(f"{C_TITLE}{' '*20}NIKTO — LIGHTNING RECON HISOBOTI{' '*20}{C_RESET}")
    print(f"{C_TITLE}{'═'*74}{C_RESET}")
    print(f"{C_INFO} Target      :{C_RESET} {target}")
    print(f"{C_INFO} Vaqt        :{C_RESET} 8–12 sekund")
    print(f"{C_INFO} Natijalar   :{C_RESET} {C_OK}{len(recon)} ta{C_RESET}")
    print(f"{C_INFO} Hisobot     :{C_RESET} {output_file}{C_RESET}")
    print(f"{C_TITLE}{'═'*74}{C_RESET}\n")

    Logger.success(f"Nikto LIGHTNING → {target} | {len(recon)} ta ma'lumot | {output_file}")

    input(f"{C_INFO}Enter bosing...{C_RESET}")