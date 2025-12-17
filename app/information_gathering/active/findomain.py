# app/information_gathering/active/findomain.py

import os
import sys
import subprocess
import shutil
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from app.config import C_TITLE, C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import Logger, print_header, print_footer, pause, clear_screen


def check_findomain():
    """Findomain o'rnatilganligini tekshirish"""
    if shutil.which("findomain"):
        return True
    Logger.error("Findomain topilmadi!")
    print(f"\n{C_WARN}[!] O'rnatish:{C_RESET}")
    print(f"    {C_INFO}wget https://github.com/findomain/findomain/releases/latest/download/findomain-linux -O /usr/local/bin/findomain{C_RESET}")
    print(f"    {C_INFO}chmod +x /usr/local/bin/findomain{C_RESET}\n")
    return False


def get_scan_options():
    """Scan parametrlarini olish"""
    print(f"\n{C_TITLE}[+] Findomain scan turlari:{C_RESET}")
    print(f"  {C_INFO}[1]{C_RESET} Quick Scan      - Faqat API orqali (tez)")
    print(f"  {C_INFO}[2]{C_RESET} Standard Scan   - API + Passive (default)")
    print(f"  {C_INFO}[3]{C_RESET} Full Scan       - API + Passive + Active")
    print(f"  {C_INFO}[4]{C_RESET} Monitoring Mode - Doimiy monitoring")
    
    choice = input(f"\n{C_INFO}She11>{C_RESET} ").strip() or "2"
    
    options = {
        'resolve': False,
        'http_check': False,
        'monitoring': False,
        'threads': 50
    }
    
    if choice in ['2', '3']:
        print(f"\n{C_INFO}Subdomainlarni resolve qilish? (y/n):{C_RESET}")
        if input(f"    {C_INFO}She11>{C_RESET} ").strip().lower() == 'y':
            options['resolve'] = True
    
    if choice == '3':
        print(f"\n{C_INFO}HTTP/HTTPS check qilish? (y/n):{C_RESET}")
        if input(f"    {C_INFO}She11>{C_RESET} ").strip().lower() == 'y':
            options['http_check'] = True
        
        print(f"\n{C_INFO}Threadlar soni (default: 50):{C_RESET}")
        threads = input(f"    {C_INFO}She11>{C_RESET} ").strip()
        if threads.isdigit():
            options['threads'] = int(threads)
    
    if choice == '4':
        options['monitoring'] = True
        print(f"\n{C_WARN}[!] Monitoring mode - Ctrl+C bilan to'xtatish mumkin{C_RESET}")
    
    return options


def parse_findomain_output(output_file):
    """Natijalarni parsing va statistika"""
    if not os.path.exists(output_file):
        return None
    
    with open(output_file, 'r') as f:
        subdomains = [line.strip() for line in f if line.strip()]
    
    stats = {
        'total': len(subdomains),
        'unique': len(set(subdomains)),
        'subdomains': subdomains
    }
    
    # Subdomain patternlari
    patterns = {}
    for sub in subdomains:
        parts = sub.split('.')
        if len(parts) > 2:
            pattern = parts[0]
            patterns[pattern] = patterns.get(pattern, 0) + 1
    
    stats['patterns'] = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return stats


def display_results(stats, domain):
    """Natijalarni chiroyli ko'rsatish"""
    print(f"\n{C_TITLE}{'='*80}{C_RESET}")
    print(f"{C_TITLE}                    FINDOMAIN SCAN RESULTS{C_RESET}")
    print(f"{C_TITLE}{'='*80}{C_RESET}\n")
    
    print(f"{C_OK}[+] Domain:{C_RESET} {domain}")
    print(f"{C_OK}[+] Jami topilgan subdomainlar:{C_RESET} {stats['total']}")
    print(f"{C_OK}[+] Unique subdomainlar:{C_RESET} {stats['unique']}\n")
    
    # Top patterns
    if stats['patterns']:
        print(f"{C_TITLE}[+] TOP SUBDOMAIN PATTERNS:{C_RESET}")
        for pattern, count in stats['patterns'][:10]:
            bar = '█' * min(count, 50)
            print(f"    {C_INFO}{pattern:20}{C_RESET} {C_OK}{bar}{C_RESET} ({count})")
    
    # Barcha subdomainlar
    print(f"\n{C_TITLE}[+] TOPILGAN SUBDOMAINLAR:{C_RESET}")
    for i, sub in enumerate(stats['subdomains'][:30], 1):
        print(f"    {C_INFO}[{i:2}]{C_RESET} {sub}")
    
    if len(stats['subdomains']) > 30:
        remaining = len(stats['subdomains']) - 30
        print(f"\n    {C_WARN}... va yana {remaining} ta subdomain{C_RESET}")
    
    print(f"\n{C_TITLE}{'='*80}{C_RESET}\n")


def check_http_status(subdomain_list, threads=50):
    """HTTP/HTTPS statuslarini tekshirish"""
    print(f"\n{C_INFO}[*] HTTP/HTTPS statuslarini tekshirish...{C_RESET}")
    
    alive_hosts = []
    loading_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    loading_idx = 0
    
    for i, subdomain in enumerate(subdomain_list):
        sys.stdout.write(f"\r{C_INFO}{loading_chars[loading_idx]} Checking {i+1}/{len(subdomain_list)}{C_RESET}")
        sys.stdout.flush()
        loading_idx = (loading_idx + 1) % len(loading_chars)
        
        try:
            # HTTP check
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                 f"http://{subdomain}", "--max-time", "3"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout and result.stdout.startswith('2'):
                alive_hosts.append(('http', subdomain, result.stdout))
                sys.stdout.write('\r' + ' ' * 60 + '\r')
                print(f"{C_OK}[✓] http://{subdomain} → {result.stdout}{C_RESET}")
            
            # HTTPS check
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                 f"https://{subdomain}", "--max-time", "3", "-k"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout and result.stdout.startswith('2'):
                alive_hosts.append(('https', subdomain, result.stdout))
                sys.stdout.write('\r' + ' ' * 60 + '\r')
                print(f"{C_OK}[✓] https://{subdomain} → {result.stdout}{C_RESET}")
        
        except:
            pass
    
    sys.stdout.write('\r' + ' ' * 60 + '\r')
    return alive_hosts


def run_findomain_scanner(target=None):
    """Findomain asosiy funksiya"""
    clear_screen()
    print_header("FINDOMAIN - FAST SUBDOMAIN ENUMERATOR", 80)
    print(f"{C_TITLE}         The Fastest Subdomain Discovery Tool{C_RESET}\n")
    
    # Tool mavjudligini tekshirish
    if not check_findomain():
        pause()
        return
    
    # Domain olish
    if not target:
        print(f"{C_INFO}Domain kiriting (example.com):{C_RESET}")
        target = input(f"    {C_INFO}She11>{C_RESET} ").strip()
    
    if not target:
        Logger.error("Domain kiritilmadi!")
        pause()
        return
    
    # http/https ni olib tashlash
    domain = target.replace("http://", "").replace("https://", "").split('/')[0]
    
    # Options olish
    options = get_scan_options()
    
    # Output fayl
    output_dir = "reports/information_gathering/findomain"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/findomain_{domain}_{timestamp}.txt"
    
    # Findomain buyrug'ini tuzish
    cmd = ["findomain", "-t", domain, "-u", output_file]
    
    if options['resolve']:
        cmd.append("-r")
    
    if options['monitoring']:
        cmd.extend(["-m", "--monitoring-flag", "subdomain-changes"])
    
    print(f"\n{C_OK}[+] Findomain ishga tushirilmoqda...{C_RESET}")
    print(f"{C_INFO}[*] Domain: {domain}{C_RESET}")
    print(f"{C_INFO}[*] Resolve: {'Yes' if options['resolve'] else 'No'}{C_RESET}")
    print(f"{C_INFO}[*] Output: {output_file}{C_RESET}\n")
    print(f"{C_WARN}{'='*80}{C_RESET}\n")
    
    # Loading animation
    loading_chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    loading_idx = 0
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        start_time = time.time()
        subdomain_count = 0
        
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            
            # Loading animation
            sys.stdout.write(f"\r{C_INFO}{loading_chars[loading_idx]} Enumerating subdomains... ({subdomain_count} found){C_RESET}")
            sys.stdout.flush()
            loading_idx = (loading_idx + 1) % len(loading_chars)
            
            # Subdomain topilganda
            if domain in line and not line.startswith('['):
                subdomain_count += 1
                if subdomain_count % 10 == 0:  # Har 10 tadan biri
                    sys.stdout.write('\r' + ' ' * 70 + '\r')
                    print(f"{C_OK}[+] {line}{C_RESET}")
        
        process.wait()
        elapsed = time.time() - start_time
        
        sys.stdout.write('\r' + ' ' * 70 + '\r')
        print(f"\n{C_WARN}{'='*80}{C_RESET}\n")
        
        # Natijalarni parsing
        stats = parse_findomain_output(output_file)
        
        if stats and stats['total'] > 0:
            Logger.success(f"Scan yakunlandi! {stats['total']} ta subdomain topildi")
            print(f"{C_INFO}[*] Vaqt: {elapsed:.2f} soniya{C_RESET}\n")
            
            # Natijalarni ko'rsatish
            display_results(stats, domain)
            
            # HTTP check
            if options['http_check'] and stats['subdomains']:
                alive = check_http_status(stats['subdomains'][:50], options['threads'])
                
                if alive:
                    print(f"\n{C_TITLE}[+] ACTIVE HOSTS:{C_RESET}")
                    for proto, host, code in alive:
                        print(f"    {C_OK}[✓] {proto}://{host} → {code}{C_RESET}")
                    
                    # Alive hosts ni alohida saqlash
                    alive_file = output_file.replace('.txt', '_alive.txt')
                    with open(alive_file, 'w') as f:
                        for proto, host, code in alive:
                            f.write(f"{proto}://{host}\n")
                    print(f"\n{C_INFO}[*] Active hosts: {alive_file}{C_RESET}")
            
            print(f"\n{C_INFO}[*] To'liq natijalar: {output_file}{C_RESET}\n")
        else:
            Logger.warning("Hech qanday subdomain topilmadi!")
    
    except KeyboardInterrupt:
        print(f"\n\n{C_WARN}[!] Scan to'xtatildi (Ctrl+C){C_RESET}")
        if process:
            process.terminate()
    except Exception as e:
        Logger.error(f"Xatolik: {str(e)}")
    
    print_footer()
    pause()


def run_findomain(target):
    """Menu uchun wrapper"""
    run_findomain_scanner(target)


if __name__ == "__main__":
    run_findomain_scanner()