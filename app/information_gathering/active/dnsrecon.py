# app/information_gathering/active/dnsrecon.py

import os
import sys
import subprocess
import shutil
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from app.config import C_TITLE, C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import Logger, print_header, print_footer, pause, clear_screen


def check_dnsrecon():
    """DNSRecon o'rnatilganligini tekshirish"""
    if shutil.which("dnsrecon"):
        return True
    
    Logger.error("DNSRecon topilmadi!")
    print(f"\n{C_WARN}[!] O'rnatish:{C_RESET}")
    print(f"    {C_INFO}apt install dnsrecon{C_RESET}")
    print(f"    {C_INFO}yoki: pip3 install dnsrecon{C_RESET}\n")
    return False


def get_scan_type():
    """Scan turini tanlash"""
    print(f"\n{C_TITLE}[+] DNSRecon scan turlari:{C_RESET}")
    print(f"  {C_INFO}[1]{C_RESET} Standard Enumeration    (-t std)")
    print(f"  {C_INFO}[2]{C_RESET} Zone Transfer Test      (-t axfr)")
    print(f"  {C_INFO}[3]{C_RESET} Reverse Lookup          (-t rvl)")
    print(f"  {C_INFO}[4]{C_RESET} Subdomain Bruteforce    (-t brt)")
    print(f"  {C_INFO}[5]{C_RESET} SRV Record Enumeration  (-t srv)")
    print(f"  {C_INFO}[6]{C_RESET} Google Enumeration      (-t goo)")
    print(f"  {C_INFO}[7]{C_RESET} Cache Snooping          (-t snoop)")
    print(f"  {C_INFO}[8]{C_RESET} Zone Walking            (-t zonewalk)")
    
    choice = input(f"\n{C_INFO}She11>{C_RESET} ").strip() or "1"
    
    scan_types = {
        '1': ('std', 'Standard Enumeration'),
        '2': ('axfr', 'Zone Transfer Test'),
        '3': ('rvl', 'Reverse Lookup'),
        '4': ('brt', 'Subdomain Bruteforce'),
        '5': ('srv', 'SRV Record Enumeration'),
        '6': ('goo', 'Google Enumeration'),
        '7': ('snoop', 'Cache Snooping'),
        '8': ('zonewalk', 'Zone Walking')
    }
    
    return scan_types.get(choice, ('std', 'Standard Enumeration'))


def get_scan_options(scan_type):
    """Scan parametrlarini olish"""
    options = {
        'nameserver': None,
        'threads': 10,
        'wordlist': None,
        'range': None
    }
    
    print(f"\n{C_TITLE}[+] Qo'shimcha parametrlar:{C_RESET}")
    
    # Custom nameserver
    print(f"\n{C_INFO}Custom DNS server (bo'sh qoldirish mumkin):{C_RESET}")
    print(f"    {C_WARN}Masalan: 8.8.8.8, 1.1.1.1{C_RESET}")
    ns = input(f"    {C_INFO}She11>{C_RESET} ").strip()
    if ns:
        options['nameserver'] = ns
    
    # Bruteforce uchun wordlist
    if scan_type == 'brt':
        wordlists = [
            "/usr/share/dnsrecon/namelist.txt",
            "/usr/share/wordlists/dnsmap.txt",
            "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
        ]
        
        print(f"\n{C_TITLE}[+] Wordlist tanlang:{C_RESET}")
        available = []
        for i, wl in enumerate(wordlists, 1):
            if os.path.exists(wl):
                size = os.path.getsize(wl) // 1024
                print(f"  {C_INFO}[{i}]{C_RESET} {os.path.basename(wl)} ({size} KB)")
                available.append(wl)
        
        if available:
            print(f"  {C_INFO}[0]{C_RESET} Custom wordlist")
            choice = input(f"\n{C_INFO}She11>{C_RESET} ").strip()
            
            if choice == "0":
                custom = input(f"{C_INFO}Wordlist yo'li:{C_RESET} ").strip()
                if os.path.exists(custom):
                    options['wordlist'] = custom
            else:
                try:
                    idx = int(choice) - 1
                    options['wordlist'] = available[idx] if 0 <= idx < len(available) else available[0]
                except:
                    options['wordlist'] = available[0]
    
    # Reverse lookup uchun range
    if scan_type == 'rvl':
        print(f"\n{C_INFO}IP Range (192.168.1.0/24 formatda):{C_RESET}")
        ip_range = input(f"    {C_INFO}She11>{C_RESET} ").strip()
        if ip_range:
            options['range'] = ip_range
    
    # Threads
    print(f"\n{C_INFO}Threadlar soni (default: 10):{C_RESET}")
    threads = input(f"    {C_INFO}She11>{C_RESET} ").strip()
    if threads.isdigit():
        options['threads'] = int(threads)
    
    return options


def parse_dns_records(output_file):
    """DNS recordlarni parsing"""
    if not os.path.exists(output_file):
        return None
    
    try:
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        records = {
            'A': [],
            'AAAA': [],
            'MX': [],
            'NS': [],
            'TXT': [],
            'SOA': [],
            'CNAME': [],
            'SRV': [],
            'PTR': [],
            'other': []
        }
        
        for entry in data:
            record_type = entry.get('type', 'unknown')
            
            if record_type in records:
                records[record_type].append(entry)
            else:
                records['other'].append(entry)
        
        # Bo'sh ro'yxatlarni olib tashlash
        records = {k: v for k, v in records.items() if v}
        
        return records
    
    except json.JSONDecodeError:
        # Text formatda o'qish
        with open(output_file, 'r') as f:
            lines = f.readlines()
        return {'raw': lines}


def display_dns_results(records, domain, scan_type_name):
    """DNS natijalarni ko'rsatish"""
    print(f"\n{C_TITLE}{'='*80}{C_RESET}")
    print(f"{C_TITLE}                     DNSRECON RESULTS{C_RESET}")
    print(f"{C_TITLE}{'='*80}{C_RESET}\n")
    
    print(f"{C_OK}[+] Domain:{C_RESET} {domain}")
    print(f"{C_OK}[+] Scan Type:{C_RESET} {scan_type_name}\n")
    
    if 'raw' in records:
        print(f"{C_INFO}Raw Output:{C_RESET}")
        for line in records['raw']:
            print(f"    {line.strip()}")
        return
    
    # Record turlari bo'yicha
    record_icons = {
        'A': '🌐',
        'AAAA': '🌐',
        'MX': '📧',
        'NS': '🗄️',
        'TXT': '📝',
        'SOA': '⚙️',
        'CNAME': '🔗',
        'SRV': '🔌',
        'PTR': '↩️'
    }
    
    for rec_type, entries in sorted(records.items()):
        if rec_type == 'other':
            continue
        
        icon = record_icons.get(rec_type, '•')
        print(f"\n{C_TITLE}{icon} {rec_type} RECORDS ({len(entries)}):{C_RESET}")
        
        for entry in entries[:20]:
            if rec_type == 'A':
                name = entry.get('name', entry.get('hostname', 'N/A'))
                ip = entry.get('address', entry.get('ip', 'N/A'))
                print(f"    {C_OK}{name:40}{C_RESET} → {C_INFO}{ip}{C_RESET}")
            
            elif rec_type == 'MX':
                exchange = entry.get('exchange', entry.get('target', 'N/A'))
                priority = entry.get('priority', 'N/A')
                print(f"    {C_OK}[{priority:2}]{C_RESET} {C_INFO}{exchange}{C_RESET}")
            
            elif rec_type == 'NS':
                ns = entry.get('target', entry.get('nameserver', 'N/A'))
                print(f"    {C_INFO}→ {ns}{C_RESET}")
            
            elif rec_type == 'TXT':
                txt = entry.get('strings', entry.get('text', 'N/A'))
                if isinstance(txt, list):
                    txt = ' '.join(txt)
                print(f"    {C_INFO}{txt[:70]}{C_RESET}")
            
            elif rec_type == 'CNAME':
                name = entry.get('name', 'N/A')
                target = entry.get('target', 'N/A')
                print(f"    {C_OK}{name:40}{C_RESET} → {C_INFO}{target}{C_RESET}")
            
            else:
                print(f"    {C_INFO}{entry}{C_RESET}")
        
        if len(entries) > 20:
            print(f"    {C_WARN}... va yana {len(entries)-20} ta{C_RESET}")
    
    print(f"\n{C_TITLE}{'='*80}{C_RESET}\n")


def run_dnsrecon_scanner(target=None):
    """DNSRecon asosiy funksiya"""
    clear_screen()
    print_header("DNSRECON - DNS ENUMERATION TOOL", 80)
    print(f"{C_TITLE}         Comprehensive DNS Information Gathering{C_RESET}\n")
    
    # Tool mavjudligini tekshirish
    if not check_dnsrecon():
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
    
    # Scan turini tanlash
    scan_type, scan_type_name = get_scan_type()
    
    # Parametrlarni olish
    options = get_scan_options(scan_type)
    
    # Output fayl
    output_dir = "reports/information_gathering/active/dnsrecon"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/dnsrecon_{domain}_{scan_type}_{timestamp}"
    
    # DNSRecon buyrug'ini tuzish
    cmd = ["dnsrecon", "-d", domain, "-t", scan_type]
    
    if options['nameserver']:
        cmd.extend(["-n", options['nameserver']])
    
    if options['threads']:
        cmd.extend(["--threads", str(options['threads'])])
    
    if options['wordlist']:
        cmd.extend(["-D", options['wordlist']])
    
    if options['range']:
        cmd.extend(["-r", options['range']])
    
    # JSON output
    cmd.extend(["-j", f"{output_file}.json"])
    
    print(f"\n{C_OK}[+] DNSRecon ishga tushirilmoqda...{C_RESET}")
    print(f"{C_INFO}[*] Domain: {domain}{C_RESET}")
    print(f"{C_INFO}[*] Type: {scan_type_name}{C_RESET}")
    if options['nameserver']:
        print(f"{C_INFO}[*] DNS Server: {options['nameserver']}{C_RESET}")
    print(f"{C_INFO}[*] Output: {output_file}.json{C_RESET}\n")
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
        record_count = 0
        
        for line in process.stdout:
            line = line.strip()
            if not line or line.startswith('[*]'):
                continue
            
            # Loading animation
            sys.stdout.write(f"\r{C_INFO}{loading_chars[loading_idx]} Enumerating DNS records... ({record_count} found){C_RESET}")
            sys.stdout.flush()
            loading_idx = (loading_idx + 1) % len(loading_chars)
            
            # Record topilganda
            if any(rec in line for rec in ['A ', 'MX ', 'NS ', 'TXT ', 'CNAME ', 'SOA ']):
                record_count += 1
                sys.stdout.write('\r' + ' ' * 70 + '\r')
                
                if 'A ' in line:
                    print(f"{C_OK}[✓] {line}{C_RESET}")
                elif 'MX ' in line:
                    print(f"{C_WARN}[📧] {line}{C_RESET}")
                else:
                    print(f"{C_INFO}[•] {line}{C_RESET}")
        
        process.wait()
        elapsed = time.time() - start_time
        
        sys.stdout.write('\r' + ' ' * 70 + '\r')
        print(f"\n{C_WARN}{'='*80}{C_RESET}\n")
        
        # Natijalarni parsing
        records = parse_dns_records(f"{output_file}.json")
        
        if records:
            Logger.success(f"DNS enumeration yakunlandi!")
            print(f"{C_INFO}[*] Vaqt: {elapsed:.2f} soniya{C_RESET}\n")
            
            # Natijalarni ko'rsatish
            display_dns_results(records, domain, scan_type_name)
            
            # Text output ham saqlash
            with open(f"{output_file}.txt", 'w') as f:
                f.write(f"DNSRecon Scan Results\n")
                f.write(f"Domain: {domain}\n")
                f.write(f"Type: {scan_type_name}\n")
                f.write(f"Date: {datetime.now()}\n\n")
                
                if 'raw' in records:
                    f.write('\n'.join(records['raw']))
                else:
                    for rec_type, entries in sorted(records.items()):
                        f.write(f"\n{rec_type} Records:\n")
                        for entry in entries:
                            f.write(f"  {entry}\n")
            
            print(f"{C_INFO}[*] Natijalar saqlandi:{C_RESET}")
            print(f"    {C_OK}• {output_file}.json{C_RESET}")
            print(f"    {C_OK}• {output_file}.txt{C_RESET}\n")
        else:
            Logger.warning("Hech qanday DNS record topilmadi!")
    
    except KeyboardInterrupt:
        print(f"\n\n{C_WARN}[!] Scan to'xtatildi (Ctrl+C){C_RESET}")
        if process:
            process.terminate()
    except Exception as e:
        Logger.error(f"Xatolik: {str(e)}")
    
    print_footer()
    pause()


def run_dnsrecon(target):
    """Menu uchun wrapper"""
    run_dnsrecon_scanner(target)


if __name__ == "__main__":
    run_dnsrecon_scanner()