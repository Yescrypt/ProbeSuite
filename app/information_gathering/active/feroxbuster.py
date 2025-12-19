# app/information_gathering/active/feroxbuster.py
import os
import sys
import subprocess
import shutil
import time
import re  # Regex parsing uchun
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
from app.config import C_TITLE, C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import Logger, print_header, print_footer, pause, clear_screen

def check_feroxbuster():
    """Feroxbuster o'rnatilganligini tekshirish"""
    if shutil.which("feroxbuster"):
        return True
    Logger.error("Feroxbuster topilmadi!")
    print(f"\n{C_WARN}[!] O'rnatish:{C_RESET}")
    print(f" {C_INFO}curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh | bash{C_RESET}")
    print(f" {C_INFO}yoki: cargo install feroxbuster{C_RESET}\n")
    return False

def get_wordlist():
    """Wordlist tanlash"""
    common_wordlists = [
        "/usr/share/wordlists/dirb/common.txt",
        "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
        "/usr/share/seclists/Discovery/Web-Content/common.txt",
        "/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt",
    ]
    print(f"\n{C_TITLE}[+] Mavjud wordlistlar:{C_RESET}")
    available = []
    for i, wl in enumerate(common_wordlists, 1):
        if os.path.exists(wl):
            size = os.path.getsize(wl) // 1024
            print(f" {C_INFO}[{i}]{C_RESET} {os.path.basename(wl)} ({size} KB)")
            available.append(wl)
    if not available:
        Logger.error("Hech qanday wordlist topilmadi!")
        print(f"{C_WARN}[!] SecLists o'rnating:{C_RESET}")
        print(f" {C_INFO}git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists{C_RESET}\n")
        return None
    print(f" {C_INFO}[0]{C_RESET} Custom wordlist yo'li kiriting")
    choice = input(f"\n{C_INFO}She11>{C_RESET} ").strip()
    if choice == "0":
        while True:  # Qayta so'rash uchun loop
            custom = input(f"{C_INFO}Wordlist yo'li:{C_RESET} ").strip()
            if os.path.exists(custom):
                return custom
            Logger.error("Yo'l topilmadi! Qayta kiriting.")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(available):
            return available[idx]
        else:
            return available[0]
    except:
        return available[0]

def get_scan_options():
    """Scan parametrlarini olish"""
    print(f"\n{C_TITLE}[+] Feroxbuster parametrlari:{C_RESET}")
    # Threads
    print(f"\n{C_INFO}Threadlar soni (default: 50):{C_RESET}")
    threads_input = input(f" {C_INFO}She11>{C_RESET} ").strip()
    try:
        threads = int(threads_input) if threads_input else 50
        threads = min(threads, 100)  # Max limit
    except ValueError:
        threads = 50
        Logger.warning("Noto'g'ri qiymat, default 50 ishlatildi.")

    # Depth
    print(f"\n{C_INFO}Recursion depth (default: 4):{C_RESET}")
    depth_input = input(f" {C_INFO}She11>{C_RESET} ").strip()
    try:
        depth = int(depth_input) if depth_input else 4
        depth = max(1, min(depth, 10))  # Limit (1-10)
    except ValueError:
        depth = 4
        Logger.warning("Noto'g'ri qiymat, default 4 ishlatildi.")

    # Extensions
    print(f"\n{C_INFO}Fayl extensionlari (default: php,html,js,txt):{C_RESET}")
    print(f" {C_WARN}Masalan: php,html,js,asp,aspx,jsp{C_RESET}")
    extensions = input(f" {C_INFO}She11>{C_RESET} ").strip()
    if not extensions:
        extensions = "php,html,js,txt"
    extensions = extensions.replace(" ", "")  # Bo'shliqlarni tozalash

    # Status codes
    print(f"\n{C_INFO}Filter status codes (default: 200,301,302,401,403):{C_RESET}")
    status = input(f" {C_INFO}She11>{C_RESET} ").strip()
    if not status:
        status = "200,301,302,401,403"
    status = status.replace(" ", "")  # Bo'shliqlarni tozalash

    return {
        'threads': threads,
        'depth': depth,
        'extensions': extensions,
        'status': status
    }

def auto_detect_protocol(target):
    """HTTPS yoki HTTP ni avtomatik aniqlash"""
    try:
        import requests
        protocols = ['https://', 'http://']
        for proto in protocols:
            try:
                response = requests.get(proto + target, timeout=5, verify=False)
                if response.status_code < 400:  # 200 yoki redirect
                    return proto + target
            except:
                continue
    except ImportError:
        Logger.warning("Requests kutubxonasi topilmadi, HTTP default ishlatiladi.")
    return f"http://{target}"

def run_feroxbuster_scanner(target=None):
    """Feroxbuster asosiy funksiya"""
    clear_screen()
    print_header("FEROXBUSTER - RECURSIVE DIRECTORY BRUTE-FORCER", 80)
    print(f"{C_TITLE} Fast, Parallel Web Content Discovery{C_RESET}\n")

    # Tool mavjudligini tekshirish
    if not check_feroxbuster():
        pause()
        return

    # Target olish
    if not target:
        print(f"{C_INFO}Target URL kiriting (example.com):{C_RESET}")
        target = input(f" {C_INFO}She11>{C_RESET} ").strip()
    if not target:
        Logger.error("Target kiritilmadi!")
        pause()
        return

    # Protocol aniqlash (avtomatik)
    if not target.startswith(("http://", "https://")):
        target = auto_detect_protocol(target)
        print(f"{C_INFO}[*] Protocol aniqlandi: {target}{C_RESET}")

    # Wordlist tanlash
    wordlist = get_wordlist()
    if not wordlist:
        pause()
        return

    # Parametrlarni olish
    options = get_scan_options()

    # Output faylini yaratish
    output_dir = "reports/information_gathering/active/feroxbuster"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = re.sub(r'[^a-zA-Z0-9_]', '_', target.replace("http://", "").replace("https://", ""))  # Domain tozalash
    output_file = f"{output_dir}/ferox_{domain}_{timestamp}.txt"

    # Feroxbuster buyrug'ini tuzish (-q qo'shildi: progress bar o'chirish uchun)
    cmd = [
        "feroxbuster",
        "-u", target,
        "-w", wordlist,
        "-t", str(options['threads']),
        "-d", str(options['depth']),
        "-x", options['extensions'],
        "-s", options['status'],
        "-o", output_file,
        "-k",  # SSL ignore
        "-q",  # Quiet: Progress bar va banner o'chirish (loader uchun muhim!)
    ]

    print(f"\n{C_OK}[+] Feroxbuster ishga tushirilmoqda...{C_RESET}")
    print(f"{C_INFO}[*] Target: {target}{C_RESET}")
    print(f"{C_INFO}[*] Wordlist: {os.path.basename(wordlist)}{C_RESET}")
    print(f"{C_INFO}[*] Threads: {options['threads']} | Depth: {options['depth']}{C_RESET}")
    print(f"{C_INFO}[*] Extensions: {options['extensions']}{C_RESET}")
    print(f"{C_INFO}[*] Output: {output_file}{C_RESET}\n")
    print(f"{C_WARN}{'='*80}{C_RESET}\n")

    # Loading animation
    loading_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    loading_idx = 0
    found_count = 0
    start_time = time.time()
    last_loading_time = time.time()

    try:
        # Process ishga tushirish
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        return_code = process.poll()  # Darhol tekshirish

        # Real-time output o'qish
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if not line:
                continue

            current_time = time.time()

            # Progress bar yoki banner line larini ignore qilish (agar -q ishlamasa)
            if re.match(r'^\s*[█░%\-=]+.*$', line) or 'feroxbuster' in line.lower() or '%' in line:
                continue  # Ignore progress/banner

            # Loading animation (faqat 0.2s da bir update, flicker oldini olish uchun)
            if current_time - last_loading_time > 0.2:
                sys.stdout.write(f"\r{C_INFO}{loading_chars[loading_idx]} Scanning...{C_RESET}")
                sys.stdout.flush()
                loading_idx = (loading_idx + 1) % len(loading_chars)
                last_loading_time = current_time

            # Regex bilan status code parsing (yaxshilandi: [200] [GET] ... ni to'liq olish)
            match = re.search(r'\[(\d{3})\]\s+\[(\w+)\]\s+\[Size:\s*(\d+)\]\s+(https?://.+)', line)
            if match:
                sys.stdout.write('\r' + ' ' * 50 + '\r')  # Clear loading
                status, method, size, path = match.groups()
                if status == '200':
                    print(f"{C_OK}[✓] [{status}] [{method}] [{size}B] {path}{C_RESET}")
                elif status in ['301', '302']:
                    print(f"{C_WARN}[→] [{status}] [{method}] [{size}B] {path}{C_RESET}")
                elif status in ['401', '403']:
                    print(f"{C_ERR}[!] [{status}] [{method}] [{size}B] {path}{C_RESET}")
                else:
                    print(f"{C_INFO}[*] [{status}] [{method}] [{size}B] {path}{C_RESET}")
                found_count += 1

        process.wait()
        elapsed = time.time() - start_time

        # Yakuniy natija
        sys.stdout.write('\r' + ' ' * 50 + '\r')  # Clear loading
        print(f"\n{C_WARN}{'='*80}{C_RESET}\n")
        if process.returncode != 0:
            Logger.warning(f"Feroxbuster xato kodi: {process.returncode} (oddiy holatda 0 bo'ladi)")

        if found_count > 0:
            Logger.success(f"Scan yakunlandi! {found_count} ta yo'l topildi")
            print(f"{C_INFO}[*] Vaqt: {elapsed:.2f} soniya{C_RESET}")
            print(f"{C_INFO}[*] Natijalar: {output_file}{C_RESET}\n")

            # Eng muhim natijalarni ko'rsatish
            print(f"{C_TITLE}[+] Top natijalar:{C_RESET}")
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                with open(output_file, 'r') as f:
                    lines = f.readlines()
                important = [l for l in lines if any(code in l for code in ['200', '301', '302'])][:10]
                for line in important:
                    print(f" {C_OK}{line.strip()}{C_RESET}")
            else:
                Logger.warning("Output fayl bo'sh yoki topilmadi.")
        else:
            Logger.warning("Hech narsa topilmadi!")
            print(f"{C_INFO}[*] Boshqa wordlist yoki parametrlar bilan qayta urinib ko'ring{C_RESET}\n")

    except KeyboardInterrupt:
        print(f"\n\n{C_WARN}[!] Scan to'xtatildi (Ctrl+C){C_RESET}")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        Logger.error(f"Xatolik: {str(e)}")

    print_footer()
    pause()

def run_feroxbuster(target):
    """Menu uchun wrapper funksiya"""
    run_feroxbuster_scanner(target)

if __name__ == "__main__":
    run_feroxbuster_scanner()