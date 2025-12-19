# app/information_gathering/active/gobuster_scanner.py
# ✅ DNS & VHOST TO'LIQ TUZATILDI! (2025)
# ✅ Reports yo'llari "reports/active/gobuster" ga o'zgartirildi
# ✅ Timestamp format xatosi tuzatildi (strftime ishlatildi)

import os
import subprocess
import threading
import time
import re
from datetime import datetime
from app.utils import Logger
from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET, C_TITLE

# Spinner animatsiyasi
SPINNER = "⣾⣽⣻⢿⡿⣟⣯⣷"

def live_spinner(stop_event, found_count, mode_title):
    """Spinner loader: jarayon va topilganlarni ko'rsatadi"""
    i = 0
    while not stop_event.is_set():
        print(f"\r{C_INFO}[*] {SPINNER[i % 8]} {mode_title}... ({found_count[0]} ta topildi){C_RESET}", end="", flush=True)
        i += 1
        time.sleep(0.1)
    print("\r" + " " * 100 + "\r", end="")

def locate_wordlists(patterns):
    """locate orqali kerakli wordlistlarni topadi va filtrlaydi"""
    found = []
    for pat in patterns:
        try:
            result = subprocess.run(
                ["locate", "-i", pat],
                capture_output=True, text=True, timeout=20
            )
            for path in result.stdout.splitlines():
                path = path.strip()
                if not path or not os.path.isfile(path):
                    continue
                if path.endswith(('.gz', '.zip', '.7z', '.tar', '.rar')):
                    continue
                if os.path.getsize(path) < 20_000:
                    continue
                found.append(path)
        except:
            continue
    return list(dict.fromkeys(found))

def choose_wordlist(candidates, title):
    """Foydalanuvchiga ro'yxat ko'rsatib tanlash"""
    if not candidates:
        print(f"{C_ERR}[!] {title} uchun wordlist topilmadi!{C_RESET}")
        return None
    print(f"\n{C_TITLE}{title} — Mavjud wordlistlar:{C_RESET}")
    for i, path in enumerate(candidates[:15], 1):
        size = os.path.getsize(path) / (1024*1024)
        try:
            lines = sum(1 for _ in open(path, encoding="utf-8", errors="ignore"))
        except:
            lines = "?"
        print(f" [{i}] {os.path.basename(path)} → {size:.2f} MB (~{lines} ta)")
   
    while True:
        ch = input(f"\n{C_INFO}Raqam tanlang [1-{min(len(candidates),15)}] yoki 0 = bekor: {C_RESET}").strip()
        if ch == "0":
            return None
        if ch.isdigit() and 1 <= int(ch) <= len(candidates):
            selected = candidates[int(ch)-1]
            print(f"{C_OK}[+] Tanlandi → {os.path.basename(selected)}{C_RESET}")
            return selected
        print(f"{C_ERR}Noto'g'ri tanlov!{C_RESET}")

def run_gobuster_with_loader(cmd, out_file, mode_title):
    """Gobuster ni real-time loader bilan ishga tushiradi"""
    found_count = [0]
    stop_spinner = threading.Event()
   
    spinner_thread = threading.Thread(target=live_spinner, args=(stop_spinner, found_count, mode_title), daemon=True)
    spinner_thread.start()
   
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
       
        with open(out_file, "w", encoding="utf-8") as f:
            for line in iter(process.stdout.readline, ""):
                line = line.strip()
                if not line:
                    continue
                f.write(line + "\n")
                flush = False
                
                # DIR mode uchun
                if re.search(r'Status: \d+', line) and any(s in line for s in ["200", "301", "302", "403", "401"]):
                    found_count[0] += 1
                    flush = True
                    print(f"\n{C_OK}[+] {line}{C_RESET}")
                # DNS mode uchun - Found: bilan boshlanadigan
                elif "Found:" in line:
                    found_count[0] += 1
                    flush = True
                    print(f"\n{C_OK}[+] {line}{C_RESET}")
                # VHOST mode uchun - Status: bilan keladi
                elif "Status:" in line and "200" in line:
                    found_count[0] += 1
                    flush = True
                    print(f"\n{C_OK}[+] {line}{C_RESET}")
               
                if flush:
                    stop_spinner.set()
                    time.sleep(0.01)
                    stop_spinner.clear()
                    spinner_thread = threading.Thread(target=live_spinner, args=(stop_spinner, found_count, mode_title), daemon=True)
                    spinner_thread.start()
       
        process.wait()
    except KeyboardInterrupt:
        print(f"\n{C_WARN}To'xtatildi!{C_RESET}")
        process.terminate()
    finally:
        stop_spinner.set()
        time.sleep(0.3)
   
    return found_count[0]

def run_gobuster_scanner(target_input):
    target = target_input.strip().rstrip("/")
    if not target.startswith(("http://", "https://")):
        target = "https://" + target
    domain = target.replace("https://", "").replace("http://", "").split("/")[0]
    
    # Umumiy output papkasi
    output_dir = "reports/information_gathering/active/gobuster"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{C_TITLE}╔{'═'*82}╗{C_RESET}")
    print(f"{C_TITLE}║{' GOBUSTER — ADVANCED RECON SCANNER (2025) ':^82}║{C_RESET}")
    print(f"{C_TITLE}╚{'═'*82}╝{C_RESET}\n")
    print(f" {C_INFO}[1]{C_RESET} DIR → Directory & File bruteforce")
    print(f" {C_INFO}[2]{C_RESET} DNS → Subdomain enumeration")
    print(f" {C_INFO}[3]{C_RESET} VHOST → Virtual host discovery")
    print(f" {C_INFO}[0]{C_RESET} Orqaga\n")
   
    mode = input(f"{C_INFO}Tanlov: {C_RESET}").strip()
    if mode not in ["1", "2", "3"]:
        return

    # Timestamp umumiy (har mode uchun yangi)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ==================== DIR MODE ====================
    if mode == "1":
        print(f"\n{C_INFO}locate orqali DIR wordlistlar qidirilmoqda...{C_RESET}")
        dir_patterns = ["common.txt", "raft-medium", "raft-large", "directory-list", "big.txt", "dicc.txt"]
        candidates = locate_wordlists(dir_patterns)
        wordlist = choose_wordlist(candidates, "DIRECTORY BRUTEFORCE")
        if not wordlist:
            input(); return
        
        ext = input(f"\n{C_INFO}Kengaytmalar (php,html,js,bak,zip,txt,env) → bo'sh = faqat papka: {C_RESET}").strip()
        
        out = f"{output_dir}/dir_{domain}_{timestamp}.txt"
        
        cmd = [
            "gobuster", "dir",
            "-u", target,
            "-w", wordlist,
            "-o", out,
            "-t", "200",
            "-q",
            "-k",
            "--random-agent",
            "--timeout", "5s",
            "--delay", "50ms",
            "--force",
        ]
        if ext:
            cmd += ["-x", ext]
        
        print(f"\n{C_INFO}════════════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f"{C_INFO} Target → {C_OK}{target}{C_RESET}")
        print(f"{C_INFO} Wordlist → {os.path.basename(wordlist)}")
        print(f"{C_INFO} Natija → {out}{C_RESET}")
        print(f"{C_INFO}════════════════════════════════════════════════════════════════════════════{C_RESET}\n")
        
        found = run_gobuster_with_loader(cmd, out, "DIR bruteforce")
        
        if os.path.isfile(out) and os.path.getsize(out) > 50:
            print(f"\n{C_OK}JAMI TOPILDI: {found} ta yo'l/fayl → {out}{C_RESET}")
            try:
                print(f"\n{C_TITLE}Eng muhim topilmalar:{C_RESET}")
                os.system(f"grep -E '(200|301|302|403|401)' {out} | head -15")
            except: pass
        else:
            print(f"{C_WARN}Hech narsa topilmadi{C_RESET}")
        Logger.success(f"Gobuster DIR → {target} | {found} ta")

    # ==================== DNS MODE ====================
    elif mode == "2":
        print(f"\n{C_INFO}locate orqali DNS wordlistlar qidirilmoqda...{C_RESET}")
        dns_patterns = ["subdomains-top1million", "subdomains.txt", "dns.txt", "namelist.txt", "fierce.txt"]
        candidates = locate_wordlists(dns_patterns)
        wordlist = choose_wordlist(candidates, "SUBDOMAIN ENUMERATION")
        if not wordlist:
            input(); return
        
        out = f"{output_dir}/dns_{domain}_{timestamp}.txt"
        
        cmd = [
            "gobuster", "dns",
            "-d", domain,
            "-w", wordlist,
            "-o", out,
            "-t", "50",
            "-q",
            "--resolver", "8.8.8.8",
            "--show-cname",
            "--show-ips",
        ]
        
        print(f"\n{C_INFO}════════════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f"{C_INFO} Domain → {C_OK}{domain}{C_RESET}")
        print(f"{C_INFO} Wordlist → {os.path.basename(wordlist)}")
        print(f"{C_INFO} DNS Resolver → 8.8.8.8 (Google DNS)")
        print(f"{C_INFO} Threads → 50 (DNS optimized)")
        print(f"{C_INFO} Natija → {out}{C_RESET}")
        print(f"{C_INFO}════════════════════════════════════════════════════════════════════════════{C_RESET}\n")
        print(f"{C_WARN}⚠️  ESLATMA: Katta kompaniyalar (Tesla, Google, etc) ko'pincha Wildcard DNS ishlatadi{C_RESET}")
        print(f"{C_INFO}    Bu holda natija ko'p bo'lishi mumkin (wildcard subdomains ham). ularni keyin filtrlash mumkin!{C_RESET}\n")
        
        found = run_gobuster_with_loader(cmd, out, "DNS enumeration")
        
        if os.path.isfile(out) and found > 0:
            print(f"\n{C_OK}✅ JAMI TOPILDI: {found} ta subdomain → {out}{C_RESET}")
            try:
                print(f"\n{C_TITLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C_RESET}")
                print(f"{C_TITLE}TOPILGAN SUBDOMAINLAR:{C_RESET}\n")
                with open(out, 'r') as f:
                    lines = [line.strip() for line in f if line.strip() and 'Found:' in line]
                    for idx, line in enumerate(lines[:30], 1):
                        print(f"{C_OK}{idx:3}. {line}{C_RESET}")
                if len(lines) > 30:
                    print(f"\n{C_INFO}... va yana {len(lines)-30} ta (to'liq ro'yxat: {out}){C_RESET}")
                print(f"{C_TITLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C_RESET}")
            except: pass
            Logger.success(f"Gobuster DNS → {domain} | {found} ta")
        else:
            print(f"\n{C_WARN}❌ Hech narsa topilmadi{C_RESET}\n")
            print(f"{C_INFO}Buning sabablari:{C_RESET}")
            print(f"  • Subdomain lar boshqa DNS server larda joylashgan")
            print(f"  • Wordlist da kerakli subdomain nomlar yo'q")
            print(f"  • Domain DNS himoyalangan (rate limiting, firewall)")
            print(f"\n{C_TITLE}Tavsiya qilinadigan alternativalar:{C_RESET}")
            print(f"  {C_OK}1. Sublist3r{C_RESET} - OSINT asosida subdomain topish")
            print(f"  {C_OK}2. Assetfinder{C_RESET} - Tez va samarali")
            print(f"  {C_OK}3. Amass{C_RESET} - Eng kuchli subdomain scanner")
            print(f"  {C_OK}4. crt.sh{C_RESET} - SSL sertifikat ma'lumotlari orqali")
            print(f"  {C_OK}5. DNSRecon{C_RESET} - Boshqa DNS enumeration texnikalari")
            print(f"  {C_OK}6. Findomain{C_RESET} - Rust-da yozilgan, juda tez")
            print(f"\n{C_INFO}💡 Maslahat: Yuqoridagi toollarni menyu [9], [10], [11] dan sinab ko'ring!{C_RESET}")

    # ==================== VHOST MODE ====================
    elif mode == "3":
        print(f"\n{C_INFO}locate orqali VHOST wordlist qidirilmoqda...{C_RESET}")
        candidates = locate_wordlists(["subdomains-top1million", "vhost", "hosts.txt", "namelist.txt"])
        wordlist = choose_wordlist(candidates, "VHOST DISCOVERY")
        if not wordlist:
            input(); return
        
        out = f"{output_dir}/vhost_{domain}_{timestamp}.txt"
        
        cmd = [
            "gobuster", "vhost",
            "-u", target,
            "-w", wordlist,
            "-o", out,
            "-t", "100",
            "-q",
            "-k",
            "--append-domain",
            "--random-agent",
            "--timeout", "10s"
        ]
        
        print(f"\n{C_INFO}Status kod filtri (default: hamma) → masalan 200,301,403: {C_RESET}", end="")
        status_filter = input().strip()
        if status_filter:
            cmd += ["--status-codes", status_filter]
        
        print(f"\n{C_INFO}════════════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f"{C_INFO} Target → {C_OK}{target}{C_RESET}")
        print(f"{C_INFO} Wordlist → {os.path.basename(wordlist)}")
        print(f"{C_INFO} Natija → {out}{C_RESET}")
        print(f"{C_INFO}════════════════════════════════════════════════════════════════════════════{C_RESET}\n")
        
        found = run_gobuster_with_loader(cmd, out, "VHOST discovery")
        
        if os.path.isfile(out) and found > 0:
            print(f"\n{C_OK}JAMI TOPILDI: {found} ta VHOST → {out}{C_RESET}")
            try:
                print(f"\n{C_TITLE}Topilgan VHOSTlar:{C_RESET}")
                os.system(f"cat {out} | grep -v '^#' | head -20")
            except: pass
            Logger.success(f"Gobuster VHOST → {target} | {found} ta")
        else:
            print(f"{C_WARN}Hech narsa topilmadi{C_RESET}")
            print(f"{C_INFO}Maslahat: VHOST faqat bir nechta saytlarda ishlaydi. DNS mode ko'proq natija beradi.{C_RESET}")

    print(f"\n{C_TITLE}╔{'═'*82}╗{C_RESET}")
    print(f"{C_TITLE}║{' GOBUSTER SCAN COMPLETED! 🎉 ':^82}║{C_RESET}")
    print(f"{C_TITLE}╚{'═'*82}╝{C_RESET}")
    input(f"\n{C_INFO}Davom etish uchun Enter bosing...{C_RESET}")