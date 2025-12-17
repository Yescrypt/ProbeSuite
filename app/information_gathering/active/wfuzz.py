# app/information_gathering/active/wfuzz.py

import os
import sys
import subprocess
import shutil
import time
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from app.config import C_TITLE, C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import Logger, print_header, print_footer, pause, clear_screen


def check_wfuzz():
    """Wfuzz o'rnatilganligini tekshirish"""
    if shutil.which("wfuzz"):
        return True
    Logger.error("Wfuzz topilmadi!")
    print(f"\n{C_WARN}[!] O'rnatish:{C_RESET}")
    print(f"    {C_INFO}pip3 install wfuzz{C_RESET}")
    print(f"    {C_INFO}yoki: apt install wfuzz{C_RESET}\n")
    return False


def get_wordlist():
    """Wordlist tanlash"""
    # Subdomain uchun alohida wordlist
    subdomain_wordlists = [
        "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
        "/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt",
        "/usr/share/wordlists/dnsmap.txt",
    ]
    
    common_wordlists = [
        "/usr/share/wfuzz/wordlist/general/common.txt",
        "/usr/share/wordlists/dirb/common.txt",
        "/usr/share/seclists/Discovery/Web-Content/common.txt",
        "/usr/share/seclists/Discovery/Web-Content/big.txt",
        "/usr/share/seclists/Fuzzing/fuzz-Bo0oM.txt",
    ]
    
    print(f"\n{C_TITLE}[+] Mavjud wordlistlar:{C_RESET}")
    available = []
    for i, wl in enumerate(common_wordlists, 1):
        if os.path.exists(wl):
            size = os.path.getsize(wl) // 1024
            print(f"  {C_INFO}[{i}]{C_RESET} {os.path.basename(wl)} ({size} KB)")
            available.append(wl)
    
    if not available:
        Logger.error("Hech qanday wordlist topilmadi!")
        return None
    
    print(f"  {C_INFO}[0]{C_RESET} Custom wordlist")
    
    choice = input(f"\n{C_INFO}She11>{C_RESET} ").strip()
    
    if choice == "0":
        custom = input(f"{C_INFO}Wordlist yo'li:{C_RESET} ").strip()
        return custom if os.path.exists(custom) else None
    
    try:
        idx = int(choice) - 1
        return available[idx] if 0 <= idx < len(available) else available[0]
    except:
        return available[0]


def get_subdomain_wordlist():
    """Subdomain uchun maxsus wordlist"""
    subdomain_wordlists = [
        "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
        "/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt",
        "/usr/share/seclists/Discovery/DNS/fierce-hostlist.txt",
        "/usr/share/wordlists/dnsmap.txt",
    ]
    
    print(f"\n{C_TITLE}[+] Subdomain wordlistlari:{C_RESET}")
    available = []
    for i, wl in enumerate(subdomain_wordlists, 1):
        if os.path.exists(wl):
            size = os.path.getsize(wl) // 1024
            lines = sum(1 for _ in open(wl, 'r'))
            print(f"  {C_INFO}[{i}]{C_RESET} {os.path.basename(wl)} ({size} KB, {lines} subdomains)")
            available.append(wl)
    
    if not available:
        Logger.error("Subdomain wordlist topilmadi!")
        print(f"\n{C_WARN}[!] O'rnatish:{C_RESET}")
        print(f"    {C_INFO}git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists{C_RESET}\n")
        return None
    
    print(f"  {C_INFO}[0]{C_RESET} Custom wordlist")
    
    # Default: birinchi (eng kichik)
    print(f"\n{C_WARN}[!] Kichik wordlist tanlash tavsiya etiladi (tezroq){C_RESET}")
    choice = input(f"\n{C_INFO}She11> (default: 1){C_RESET} ").strip() or "1"
    
    if choice == "0":
        custom = input(f"{C_INFO}Wordlist yo'li:{C_RESET} ").strip()
        return custom if os.path.exists(custom) else None
    
    try:
        idx = int(choice) - 1
        return available[idx] if 0 <= idx < len(available) else available[0]
    except:
        return available[0]


def get_fuzzing_mode():
    """Fuzzing rejimini tanlash"""
    print(f"\n{C_TITLE}[+] Fuzzing rejimi:{C_RESET}")
    print(f"  {C_INFO}[1]{C_RESET} Directory/File Discovery  (FUZZ)")
    print(f"  {C_INFO}[2]{C_RESET} Subdomain Discovery       (FUZZ.domain.com)")
    print(f"  {C_INFO}[3]{C_RESET} Parameter Fuzzing         (?param=FUZZ)")
    print(f"  {C_INFO}[4]{C_RESET} POST Data Fuzzing         (POST data)")
    print(f"  {C_INFO}[5]{C_RESET} Custom URL Pattern        (manual)")
    
    choice = input(f"\n{C_INFO}She11>{C_RESET} ").strip() or "1"
    
    # Subdomain mode uchun warning
    if choice == "2":
        print(f"\n{C_WARN}[!] DIQQAT: Subdomain enumeration DNS resolution talab qiladi{C_RESET}")
        print(f"{C_WARN}[!] Bu jarayon ancha vaqt olishi mumkin (5-10 daqiqa){C_RESET}")
        print(f"{C_INFO}[*] Tezroq natija uchun Findomain yoki Sublist3r dan foydalaning{C_RESET}")
        print(f"\n{C_INFO}Davom etish? (y/n):{C_RESET}")
        confirm = input(f"    {C_INFO}She11>{C_RESET} ").strip().lower()
        if confirm != 'y':
            return None
    
    return choice


def build_wfuzz_command(mode, target, wordlist, options):
    """Wfuzz buyrug'ini tuzish"""
    cmd = ["wfuzz"]
    
    # Threads
    cmd.extend(["-t", str(options.get('threads', 50))])
    
    # Hide responses
    if options.get('hide_codes'):
        cmd.extend(["--hc", options['hide_codes']])
    if options.get('hide_words'):
        cmd.extend(["--hw", options['hide_words']])
    if options.get('hide_lines'):
        cmd.extend(["--hl", options['hide_lines']])
    
    # Show only
    if options.get('show_codes'):
        cmd.extend(["--sc", options['show_codes']])
    
    # Wordlist
    cmd.extend(["-w", wordlist])
    
    # URL pattern bo'yicha
    if mode == "1":  # Directory/File
        if not target.endswith('/'):
            target += '/'
        url = f"{target}FUZZ"
    elif mode == "2":  # Subdomain
        base = target.replace("http://", "").replace("https://", "").split('/')[0]
        
        # Subdomain uchun qo'shimcha parametrlar
        # --hh : hide by character count (default pages ni yashirish)
        # -Z : DNS cache poisoning oldini olish
        cmd.append("-Z")  # Follow HTTP redirects
        
        # HTTP va HTTPS ikkalasini ham tekshirish
        if options.get('check_both_protocols'):
            url = f"http://FUZZ.{base}"
        else:
            url = f"http://FUZZ.{base}"
            
    elif mode == "3":  # Parameter
        param_name = options.get('param_name', 'id')
        url = f"{target}?{param_name}=FUZZ"
    elif mode == "4":  # POST Data
        post_data = options.get('post_data', 'username=FUZZ&password=test')
        cmd.extend(["-d", post_data])
        url = target
    else:  # Custom
        url = options.get('custom_url', target)
    
    cmd.append(url)
    
    return cmd, url


def save_results_to_files(results, output_base, target_url, mode_name, elapsed_time):
    """Natijalarni JSON va TXT formatda saqlash"""
    
    # JSON format - to'g'ri struktura
    json_data = {
        "scan_info": {
            "target": target_url,
            "mode": mode_name,
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(elapsed_time, 2),
            "total_found": len(results)
        },
        "results": results
    }
    
    json_file = f"{output_base}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # TXT format - chiroyli
    txt_file = f"{output_base}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("="*80 + "\n")
        f.write("                        WFUZZ SCAN RESULTS\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Target URL    : {target_url}\n")
        f.write(f"Scan Mode     : {mode_name}\n")
        f.write(f"Scan Date     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration      : {elapsed_time:.2f} seconds\n")
        f.write(f"Total Found   : {len(results)} results\n\n")
        
        f.write("="*80 + "\n\n")
        
        # Kategoriyalash
        categories = {
            '200': [],
            '301': [],
            '302': [],
            '401': [],
            '403': [],
            'other': []
        }
        
        for result in results:
            code = result.get('code', 'unknown')
            if code in categories:
                categories[code].append(result)
            else:
                categories['other'].append(result)
        
        # Har bir kategoriya
        status_names = {
            '200': 'SUCCESS (200 OK)',
            '301': 'MOVED PERMANENTLY (301)',
            '302': 'FOUND (302)',
            '401': 'UNAUTHORIZED (401)',
            '403': 'FORBIDDEN (403)',
            'other': 'OTHER STATUS CODES'
        }
        
        for code in ['200', '301', '302', '401', '403', 'other']:
            items = categories[code]
            if not items:
                continue
            
            f.write(f"[+] {status_names[code]} - {len(items)} results\n")
            f.write("-" * 80 + "\n\n")
            
            # Table header
            f.write(f"{'CODE':<8} {'SIZE (Ch)':<12} {'LINES':<8} {'PAYLOAD':<48}\n")
            f.write(f"{'-'*8} {'-'*12} {'-'*8} {'-'*48}\n")
            
            for item in items:
                payload = item.get('payload', 'N/A')
                if len(payload) > 45:
                    payload = payload[:42] + "..."
                
                code_val = item.get('code', '???')
                chars = item.get('chars', 'N/A')
                lines = item.get('lines', 'N/A')
                
                f.write(f"{code_val:<8} {chars:<12} {lines:<8} {payload:<48}\n")
            
            f.write("\n")
        
        # Summary
        f.write("="*80 + "\n")
        f.write("SUMMARY\n")
        f.write("="*80 + "\n\n")
        
        for code, items in categories.items():
            if items and code != 'other':
                f.write(f"  {code} responses: {len(items)}\n")
        
        if categories['other']:
            f.write(f"  Other codes: {len(categories['other'])}\n")
        
        f.write(f"\nTotal: {len(results)} results\n")
        f.write("\n" + "="*80 + "\n")
    
    return json_file, txt_file


def run_wfuzz_scanner(target=None):
    """Wfuzz asosiy funksiya"""
    clear_screen()
    print_header("WFUZZ - WEB APPLICATION FUZZER", 80)
    print(f"{C_TITLE}           Advanced Web Content & Parameter Discovery{C_RESET}\n")
    
    # Tool mavjudligini tekshirish
    if not check_wfuzz():
        pause()
        return
    
    # Target olish
    if not target:
        print(f"{C_INFO}Target URL kiriting:{C_RESET}")
        target = input(f"    {C_INFO}She11>{C_RESET} ").strip()
    
    if not target:
        Logger.error("Target kiritilmadi!")
        pause()
        return
    
    # http/https qo'shish
    if not target.startswith(("http://", "https://")):
        target = f"http://{target}"
    
    # Fuzzing rejimini tanlash
    mode = get_fuzzing_mode()
    if mode is None:  # Agar subdomain da cancel qilsa
        pause()
        return
        
    mode_names = {
        '1': 'Directory/File Discovery',
        '2': 'Subdomain Discovery',
        '3': 'Parameter Fuzzing',
        '4': 'POST Data Fuzzing',
        '5': 'Custom URL Pattern'
    }
    mode_name = mode_names.get(mode, 'Unknown')
    
    # Wordlist tanlash - subdomain uchun alohida
    if mode == "2":
        wordlist = get_subdomain_wordlist()
    else:
        wordlist = get_wordlist()
    
    if not wordlist:
        pause()
        return
    
    # Options
    print(f"\n{C_TITLE}[+] Wfuzz parametrlari:{C_RESET}")
    
    # Subdomain mode uchun maxsus parametrlar
    if mode == "2":
        print(f"\n{C_INFO}Threadlar (subdomain uchun tavsiya: 10-20):{C_RESET}")
        threads = input(f"    {C_INFO}She11>{C_RESET} ").strip() or "10"
        
        print(f"\n{C_INFO}Hide status codes (default: 404,000):{C_RESET}")
        print(f"    {C_WARN}000 = DNS resolution failed{C_RESET}")
        hide_codes = input(f"    {C_INFO}She11>{C_RESET} ").strip() or "404,000"
        
        print(f"\n{C_INFO}Show only codes (default: 200,301,302,403):{C_RESET}")
        show_codes = input(f"    {C_INFO}She11>{C_RESET} ").strip() or "200,301,302,403"
    else:
        print(f"\n{C_INFO}Threadlar (default: 50):{C_RESET}")
        threads = input(f"    {C_INFO}She11>{C_RESET} ").strip() or "50"
        
        print(f"\n{C_INFO}Hide status codes (404,403 yoki bo'sh):{C_RESET}")
        hide_codes = input(f"    {C_INFO}She11>{C_RESET} ").strip() or "404"
        
        print(f"\n{C_INFO}Show only codes (200,301,302 yoki bo'sh):{C_RESET}")
        show_codes = input(f"    {C_INFO}She11>{C_RESET} ").strip()
    
    # Output fayl
    output_dir = "reports/information_gathering/wfuzz"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = target.replace("http://", "").replace("https://", "").replace("/", "_").replace(":", "_")
    output_base = f"{output_dir}/wfuzz_{domain}_{timestamp}"
    
    options = {
        'threads': threads,
        'hide_codes': hide_codes,
        'show_codes': show_codes
    }
    
    # POST mode uchun qo'shimcha
    if mode == "4":
        print(f"\n{C_INFO}POST data pattern (default: username=FUZZ&password=test):{C_RESET}")
        post_data = input(f"    {C_INFO}She11>{C_RESET} ").strip()
        if post_data:
            options['post_data'] = post_data
    
    # Parameter mode uchun
    if mode == "3":
        print(f"\n{C_INFO}Parameter nomi (default: id):{C_RESET}")
        param = input(f"    {C_INFO}She11>{C_RESET} ").strip() or "id"
        options['param_name'] = param
    
    # Custom URL
    if mode == "5":
        print(f"\n{C_INFO}Custom URL pattern (FUZZ ni ishlating):{C_RESET}")
        print(f"    {C_WARN}Masalan: http://example.com/api/FUZZ/data{C_RESET}")
        custom = input(f"    {C_INFO}She11>{C_RESET} ").strip()
        if custom:
            options['custom_url'] = custom
    
    # Command tuzish
    cmd, target_url = build_wfuzz_command(mode, target, wordlist, options)
    
    print(f"\n{C_OK}[+] Wfuzz ishga tushirilmoqda...{C_RESET}")
    print(f"{C_INFO}[*] Target: {target_url}{C_RESET}")
    print(f"{C_INFO}[*] Mode: {mode_name}{C_RESET}")
    print(f"{C_INFO}[*] Wordlist: {os.path.basename(wordlist)}{C_RESET}")
    print(f"{C_INFO}[*] Threads: {threads}{C_RESET}")
    
    # Subdomain mode uchun qo'shimcha ma'lumot
    if mode == "2":
        print(f"{C_WARN}[*] DNS resolution aktiv - bu vaqt oladi{C_RESET}")
        print(f"{C_INFO}[*] Progress: Real-time ko'rsatilmaydi, sabr qiling...{C_RESET}")
    
    print(f"{C_INFO}[*] Command: {' '.join(cmd)}{C_RESET}\n")
    print(f"{C_WARN}{'='*80}{C_RESET}\n")
    
    # Loading
    loading_chars = ['|', '/', '-', '\\']
    loading_idx = 0
    
    results = []
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        found_count = 0
        start_time = time.time()
        
        for line in process.stdout:
            line = line.strip()
            if not line or "Warning" in line:
                continue
            
            # Loading animation - subdomain mode da kamroq
            if mode == "2":
                # Subdomain da har 5 soniyada yangilansin
                if int(time.time() - start_time) % 5 == 0:
                    sys.stdout.write(f"\r{C_INFO}{loading_chars[loading_idx]} DNS Resolution in progress... ({found_count} found) - {int(time.time() - start_time)}s{C_RESET}")
                    sys.stdout.flush()
                    loading_idx = (loading_idx + 1) % len(loading_chars)
            else:
                sys.stdout.write(f"\r{C_INFO}{loading_chars[loading_idx]} Fuzzing... ({found_count} found){C_RESET}")
                sys.stdout.flush()
                loading_idx = (loading_idx + 1) % len(loading_chars)
            
            # Natijalarni ko'rsatish - status code bor bo'lsa
            # Subdomain mode da 000 (DNS failed) ni skip qilish
            if mode == "2" and " C=000 " in line:
                continue
                
            if any(code in line for code in ['200', '301', '302', '401', '403', '500', '503']):
                sys.stdout.write('\r' + ' ' * 80 + '\r')
                
                # Line dan ma'lumotlarni parse qilish (oddiy usul)
                parts = line.split()
                result_data = {
                    'raw_line': line,
                    'code': '',
                    'chars': '',
                    'lines': '',
                    'payload': ''
                }
                
                # Status code ni topish
                for part in parts:
                    if part.startswith('C='):
                        result_data['code'] = part.replace('C=', '')
                    elif part.endswith('Ch'):
                        result_data['chars'] = part.replace('Ch', '')
                    elif part.endswith('L'):
                        result_data['lines'] = part.replace('L', '')
                
                # Payload (oxirgi qo'shtirnoq ichidagi)
                if '"' in line:
                    start_idx = line.rfind('"')
                    if start_idx != -1:
                        # Oxirdan birinchi " dan oldingi " ni topish
                        temp = line[:start_idx]
                        if '"' in temp:
                            payload_start = temp.rfind('"') + 1
                            result_data['payload'] = line[payload_start:start_idx]
                
                results.append(result_data)
                found_count += 1
                
                # Rang kodlari
                code = result_data['code']
                
                if '200' in line:
                    print(f"{C_OK}[✓] {line}{C_RESET}")
                elif '301' in line or '302' in line:
                    print(f"{C_WARN}[→] {line}{C_RESET}")
                elif '401' in line or '403' in line:
                    print(f"{C_ERR}[!] {line}{C_RESET}")
                else:
                    print(f"{C_INFO}[*] {line}{C_RESET}")
        
        process.wait()
        elapsed = time.time() - start_time
        
        sys.stdout.write('\r' + ' ' * 60 + '\r')
        print(f"\n{C_WARN}{'='*80}{C_RESET}\n")
        
        if results:
            Logger.success(f"Fuzzing yakunlandi! {len(results)} ta natija topildi")
            print(f"{C_INFO}[*] Vaqt: {elapsed:.2f} soniya{C_RESET}\n")
            
            # Natijalarni saqlash
            json_file, txt_file = save_results_to_files(
                results, output_base, target_url, mode_name, elapsed
            )
            
            print(f"{C_INFO}[*] Natijalar saqlandi:{C_RESET}")
            print(f"    {C_OK}• JSON: {json_file}{C_RESET}")
            print(f"    {C_OK}• TXT:  {txt_file}{C_RESET}\n")
            
            # Quick summary
            print(f"{C_TITLE}[+] QUICK SUMMARY:{C_RESET}")
            status_counts = {}
            for r in results:
                code = r.get('code', 'unknown')
                if code:
                    status_counts[code] = status_counts.get(code, 0) + 1
            
            for code, count in sorted(status_counts.items()):
                print(f"    {C_INFO}{code}: {count} results{C_RESET}")
            
        else:
            Logger.warning("Hech narsa topilmadi!")
            print(f"{C_INFO}[*] Boshqa parametrlar bilan qayta urinib ko'ring{C_RESET}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{C_WARN}[!] Fuzzing to'xtatildi (Ctrl+C){C_RESET}")
        if process:
            process.terminate()
        
        # To'xtatilgan holatda ham natijalarni saqlash
        if results:
            elapsed = time.time() - start_time
            json_file, txt_file = save_results_to_files(
                results, output_base, target_url, mode_name, elapsed
            )
            print(f"\n{C_INFO}[*] Qisman natijalar saqlandi:{C_RESET}")
            print(f"    {C_OK}• {json_file}{C_RESET}")
            print(f"    {C_OK}• {txt_file}{C_RESET}\n")
    
    except Exception as e:
        Logger.error(f"Xatolik: {str(e)}")
    
    print_footer()
    pause()


def run_wfuzz(target):
    """Menu uchun wrapper"""
    run_wfuzz_scanner(target)


if __name__ == "__main__":
    run_wfuzz_scanner()