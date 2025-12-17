# app/information_gathering/active/sublist3r.py

import os
import sys
import subprocess
import shutil
import time
import re
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from app.config import C_TITLE, C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import Logger, print_header, print_footer, pause, clear_screen


def check_sublist3r():
    """Sublist3r o'rnatilganligini tekshirish"""
    # 1. Command line tool sifatida tekshirish
    if shutil.which("sublist3r"):
        return "command", "sublist3r"
    
    # 2. Python module sifatida tekshirish
    try:
        import sublist3r
        module_path = sublist3r.__file__
        return "module", module_path
    except ImportError:
        pass
    
    # 3. Mahalliy fayl sifatida tekshirish
    sublist3r_paths = [
        os.path.expanduser("~/Sublist3r/sublist3r.py"),
        "./tools/Sublist3r/sublist3r.py",
        "/opt/Sublist3r/sublist3r.py",
        "/usr/share/sublist3r/sublist3r.py"
    ]
    
    for path in sublist3r_paths:
        if os.path.exists(path):
            return "script", path
    
    Logger.error("Sublist3r topilmadi!")
    print(f"\n{C_WARN}{'='*70}{C_RESET}")
    print(f"{C_WARN}[!] O'RNATISH KO'RSATMALARI:{C_RESET}\n")
    print(f"    {C_INFO}# Git orqali yuklab olish{C_RESET}")
    print(f"    {C_OK}git clone https://github.com/aboul3la/Sublist3r.git{C_RESET}")
    print(f"    {C_OK}cd Sublist3r{C_RESET}\n")
    print(f"    {C_INFO}# Dependencies o'rnatish{C_RESET}")
    print(f"    {C_OK}pip3 install -r requirements.txt{C_RESET}\n")
    print(f"    {C_INFO}# Sistema bo'ylab o'rnatish (optional){C_RESET}")
    print(f"    {C_OK}sudo python3 setup.py install{C_RESET}\n")
    print(f"    {C_INFO}# Yoki to'g'ridan-to'g'ri ishlatish{C_RESET}")
    print(f"    {C_OK}python3 sublist3r.py -d example.com{C_RESET}")
    print(f"\n{C_WARN}{'='*70}{C_RESET}\n")
    return None, None


def get_scan_engines():
    """Search engine'larni tanlash"""
    print(f"\n{C_TITLE}[+] OSINT MANBALARINI TANLANG:{C_RESET}")
    print(f"  {C_INFO}[1]{C_RESET} Hammasi (11 ta engine - sekinroq lekin to'liqroq)")
    print(f"  {C_INFO}[2]{C_RESET} Safe Mode (6 ta - Google/Bing/Yahoo bloklangan emas) {C_OK}[RECOMMENDED]{C_RESET}")
    print(f"  {C_INFO}[3]{C_RESET} Fast (Google, Bing, Yahoo - bloklanishi mumkin)")
    print(f"  {C_INFO}[4]{C_RESET} Custom (o'zingiz tanlang)")
    
    choice = input(f"\n{C_INFO}Tanlang [1-4]{C_RESET} {C_WARN}>{C_RESET} ").strip() or "2"
    
    engines = []
    
    if choice == "1":
        engines = ['baidu', 'yahoo', 'google', 'bing', 'ask', 'netcraft', 
                   'dnsdumpster', 'virustotal', 'threatcrowd', 'ssl', 'passivedns']
        print(f"{C_OK}[✓] Barcha 11 ta engine tanlandi{C_RESET}")
    elif choice == "2":
        # Rate limit bo'lmagan engine'lar
        engines = ['netcraft', 'dnsdumpster', 'virustotal', 'threatcrowd', 'ssl', 'passivedns']
        print(f"{C_OK}[✓] Safe Mode: 6 ta bloklangan emas engine{C_RESET}")
    elif choice == "3":
        engines = ['google', 'bing', 'yahoo']
        print(f"{C_WARN}[!] Fast Mode: Bloklanishi mumkin!{C_RESET}")
    elif choice == "4":
        print(f"\n{C_INFO}MAVJUD ENGINE'LAR:{C_RESET}")
        all_engines = ['google', 'bing', 'yahoo', 'ask', 'baidu', 'netcraft', 
                       'dnsdumpster', 'virustotal', 'threatcrowd', 'ssl', 'passivedns']
        
        for i, eng in enumerate(all_engines, 1):
            print(f"    {C_INFO}[{i:2}]{C_RESET} {eng}")
        
        print(f"\n{C_INFO}Raqamlarni vergul bilan kiriting (masalan: 1,2,3):{C_RESET}")
        selected = input(f"{C_WARN}>{C_RESET} ").strip()
        
        try:
            indices = [int(x.strip())-1 for x in selected.split(',')]
            engines = [all_engines[i] for i in indices if 0 <= i < len(all_engines)]
            print(f"{C_OK}[✓] {len(engines)} ta engine tanlandi{C_RESET}")
        except:
            engines = ['netcraft', 'dnsdumpster', 'virustotal', 'threatcrowd', 'ssl', 'passivedns']
            print(f"{C_WARN}[!] Noto'g'ri format, Safe Mode engines ishlatiladi{C_RESET}")
    else:
        engines = ['netcraft', 'dnsdumpster', 'virustotal', 'threatcrowd', 'ssl', 'passivedns']
        print(f"{C_WARN}[!] Noto'g'ri tanlov, Safe Mode engines ishlatiladi{C_RESET}")
    
    time.sleep(1)
    return engines


def get_scan_options():
    """Scan parametrlarini olish"""
    options = {
        'threads': 10,
        'ports': None,
        'bruteforce': False,
        'verbose': True,
        'timeout': 30
    }
    
    print(f"\n{C_TITLE}[+] QO'SHIMCHA PARAMETRLAR:{C_RESET}\n")
    
    # Threads
    print(f"{C_INFO}Threadlar soni [1-50] (default: 10):{C_RESET}")
    threads = input(f"{C_WARN}>{C_RESET} ").strip()
    if threads.isdigit() and 1 <= int(threads) <= 50:
        options['threads'] = int(threads)
        print(f"{C_OK}[✓] Threads: {options['threads']}{C_RESET}")
    else:
        print(f"{C_WARN}[!] Default: 10 threads{C_RESET}")
    
    # Port scanning
    print(f"\n{C_INFO}Portlarni scan qilish? [y/n] (default: n):{C_RESET}")
    if input(f"{C_WARN}>{C_RESET} ").strip().lower() == 'y':
        print(f"{C_INFO}Portlar (default: 80,443,8080,8443):{C_RESET}")
        ports = input(f"{C_WARN}>{C_RESET} ").strip()
        if ports:
            options['ports'] = ports
        else:
            options['ports'] = "80,443,8080,8443"
        print(f"{C_OK}[✓] Port scanning: {options['ports']}{C_RESET}")
    
    # Bruteforce
    print(f"\n{C_INFO}Bruteforce subdomain enumeration? [y/n]:{C_RESET}")
    print(f"    {C_WARN}⚠ Bu juda ko'p vaqt oladi (10-30 daqiqa)!{C_RESET}")
    if input(f"{C_WARN}>{C_RESET} ").strip().lower() == 'y':
        options['bruteforce'] = True
        print(f"{C_OK}[✓] Bruteforce: ENABLED{C_RESET}")
    
    time.sleep(0.5)
    return options


def is_valid_subdomain(text, domain):
    """Subdomain ekanligini tekshirish"""
    # Bo'sh yoki juda qisqa
    if not text or len(text) < 3:
        return False
    
    # Domain o'z ichiga olmasa
    if domain not in text:
        return False
    
    # Faqat domen ko'rinishida bo'lishi kerak
    # Masalan: subdomain.example.com yoki example.com
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    if not re.match(pattern, text):
        return False
    
    # Keraksiz so'zlar
    bad_words = ['searching', 'total', 'found', 'error', 'warning', 'enumerating', 
                 'starting', 'finished', 'press', 'ctrl', 'results']
    if any(word in text.lower() for word in bad_words):
        return False
    
    return True


def parse_sublist3r_output(output_file, live_results=None):
    """Natijalarni parsing qilish"""
    subdomains = set()
    
    # Live results'dan olish
    if live_results:
        subdomains.update(live_results)
    
    # Fayldan o'qish
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and '.' in line:
                        # Har bir so'zni alohida tekshirish
                        for word in line.split():
                            # Faqat domain nomi bo'lishi kerak
                            if '.' in word and len(word) > 3:
                                # Qo'shimcha belgilarni olib tashlash
                                clean_word = word.strip('[](){}<>\'\",:;!?')
                                
                                # Subdomain tekshirish - domain nomi o'z ichiga olmasa tekshirmaymiz
                                # Bu yerda domain nomini bilmasligimiz muammo!
                                # Shuning uchun faqat domen formatini tekshiramiz
                                if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\-\.]*[a-zA-Z0-9]$', clean_word):
                                    subdomains.add(clean_word)
        except Exception as e:
            Logger.warning(f"Faylni o'qishda xato: {e}")
    
    if not subdomains:
        return None
    
    # Statistika
    stats = {
        'total': len(subdomains),
        'subdomains': sorted(subdomains)
    }
    
    # Kategoriyalash
    categories = {
        'admin': [],
        'api': [],
        'dev': [],
        'staging': [],
        'test': [],
        'mail': [],
        'vpn': [],
        'cdn': [],
        'database': [],
        'other': []
    }
    
    keywords = {
        'admin': ['admin', 'cpanel', 'panel', 'control', 'manage'],
        'api': ['api', 'rest', 'graphql', 'endpoint'],
        'dev': ['dev', 'development', 'devel', 'sandbox'],
        'staging': ['staging', 'stage', 'stg', 'uat'],
        'test': ['test', 'testing', 'qa', 'demo'],
        'mail': ['mail', 'smtp', 'imap', 'webmail', 'mx'],
        'vpn': ['vpn', 'remote', 'access', 'gateway'],
        'cdn': ['cdn', 'static', 'assets', 'media'],
        'database': ['db', 'mysql', 'postgres', 'mongo', 'redis']
    }
    
    for sub in stats['subdomains']:
        categorized = False
        sub_lower = sub.lower()
        
        for category, keys in keywords.items():
            if any(key in sub_lower for key in keys):
                categories[category].append(sub)
                categorized = True
                break
        
        if not categorized:
            categories['other'].append(sub)
    
    stats['categories'] = {k: v for k, v in categories.items() if v}
    
    return stats


def display_results(stats, domain, engines, elapsed_time):
    """Natijalarni chiroyli ko'rsatish"""
    print(f"\n{C_TITLE}{'='*80}{C_RESET}")
    print(f"{C_TITLE}                   SUBLIST3R SCAN NATIJALAR{C_RESET}")
    print(f"{C_TITLE}{'='*80}{C_RESET}\n")
    
    print(f"{C_OK}[+] Domain:{C_RESET}       {domain}")
    print(f"{C_OK}[+] Engines:{C_RESET}      {len(engines)} ta ({', '.join(engines[:3])}{'...' if len(engines) > 3 else ''})")
    print(f"{C_OK}[+] Topildi:{C_RESET}      {C_TITLE}{stats['total']}{C_RESET} ta subdomain")
    print(f"{C_OK}[+] Vaqt:{C_RESET}         {elapsed_time:.2f} soniya")
    print(f"{C_OK}[+] Kategoriyalar:{C_RESET} {len(stats.get('categories', {}))}\n")
    
    # Kategoriyalar bo'yicha
    if stats.get('categories'):
        print(f"{C_TITLE}{'─'*80}{C_RESET}")
        print(f"{C_TITLE}KATEGORIYALAR BO'YICHA TAQSIMLASH:{C_RESET}\n")
        
        category_info = {
            'admin': ('🔐', 'ADMIN PANEL', C_ERR),
            'api': ('🔌', 'API ENDPOINTS', C_WARN),
            'dev': ('💻', 'DEVELOPMENT', C_INFO),
            'staging': ('🚧', 'STAGING', C_WARN),
            'test': ('🧪', 'TESTING', C_INFO),
            'mail': ('📧', 'MAIL SERVICES', C_OK),
            'vpn': ('🔒', 'VPN/REMOTE', C_ERR),
            'cdn': ('🌐', 'CDN/STATIC', C_OK),
            'database': ('🗄️', 'DATABASE', C_ERR),
            'other': ('📁', 'BOSHQALAR', C_RESET)
        }
        
        for category, subs in sorted(stats['categories'].items(), key=lambda x: len(x[1]), reverse=True):
            icon, name, color = category_info.get(category, ('•', category.upper(), C_RESET))
            
            print(f"{color}{icon} {name} ({len(subs)} ta):{C_RESET}")
            
            # Birinchi 3 tani ko'rsatish
            for sub in subs[:3]:
                print(f"    {C_INFO}├─ {sub}{C_RESET}")
            
            # Qolganlarini ko'rsatish
            if len(subs) > 3:
                print(f"    {C_WARN}└─ ... va yana {len(subs)-3} ta{C_RESET}")
            
            print()
    
    # TOP 30 subdomain
    print(f"{C_TITLE}{'─'*80}{C_RESET}")
    print(f"{C_TITLE}TO'LIQ RO'YXAT (TOP 30):{C_RESET}\n")
    
    for i, sub in enumerate(stats['subdomains'][:30], 1):
        # Rangli ko'rsatish
        if 'admin' in sub.lower() or 'panel' in sub.lower():
            color = C_ERR
        elif 'api' in sub.lower() or 'dev' in sub.lower():
            color = C_WARN
        else:
            color = C_INFO
        
        print(f"    {color}[{i:2}] {sub}{C_RESET}")
    
    if len(stats['subdomains']) > 30:
        remaining = len(stats['subdomains']) - 30
        print(f"\n    {C_WARN}... va yana {remaining} ta subdomain{C_RESET}")
    
    print(f"\n{C_TITLE}{'='*80}{C_RESET}\n")


def run_sublist3r_command(cmd, output_file, domain):
    """Sublist3r buyrug'ini ishga tushirish - YANGILANGAN"""
    live_results = set()
    
    print(f"{C_INFO}[DEBUG] Buyruq: {' '.join(cmd)}{C_RESET}\n")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        loading_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        loading_idx = 0
        current_engine = ""
        subdomain_count = 0
        
        # Stdout va stderr ni birga o'qish
        import select
        
        while True:
            # Process tugaganini tekshirish
            if process.poll() is not None:
                break
            
            # Stdout'dan o'qish
            try:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    
                    # DEBUG: Har bir qatorni ko'rsatish
                    if line:
                        print(f"{C_WARN}[RAW]{C_RESET} {line}")
                    
                    # Engine ismini aniqlash
                    engine_keywords = {
                        'baidu': 'Baidu',
                        'yahoo': 'Yahoo', 
                        'google': 'Google',
                        'bing': 'Bing',
                        'ask': 'Ask',
                        'netcraft': 'Netcraft',
                        'dnsdumpster': 'DNSdumpster',
                        'virustotal': 'VirusTotal',
                        'threatcrowd': 'ThreatCrowd',
                        'ssl': 'SSL Certificates',
                        'passivedns': 'PassiveDNS'
                    }
                    
                    line_lower = line.lower()
                    
                    # Engine o'zgarishini aniqlash
                    if 'searching now in' in line_lower or 'enumerating' in line_lower:
                        for key, name in engine_keywords.items():
                            if key in line_lower:
                                current_engine = name
                                print(f"\n{C_TITLE}[+] Searching: {current_engine}{C_RESET}")
                                break
                        continue
                    
                    # Total found qatorini aniqlash
                    if 'total unique subdomains found' in line_lower:
                        # Masalan: "Total Unique Subdomains Found: 45"
                        match = re.search(r'(\d+)', line)
                        if match:
                            total = int(match.group(1))
                            print(f"\n{C_OK}[✓] Jami: {total} ta subdomain topildi!{C_RESET}\n")
                        continue
                    
                    # Subdomain topilganda - HAR XIL FORMATDA
                    # Format 1: "subdomain.example.com"
                    # Format 2: "[+] subdomain.example.com"
                    # Format 3: "subdomain.example.com" (qo'shtirnoq ichida)
                    
                    # Qatordan barcha so'zlarni ajratib olish
                    words = line.split()
                    for word in words:
                        # Qo'shimcha belgilarni olib tashlash
                        clean_word = word.strip('[](){}\'\"<>:,;!?')
                        
                        # Subdomain ekanligini tekshirish
                        if is_valid_subdomain(clean_word, domain):
                            if clean_word not in live_results:
                                live_results.add(clean_word)
                                subdomain_count += 1
                                print(f"{C_OK}[✓] {clean_word}{C_RESET}")
                    
                    # Loading animation
                    sys.stdout.write(f"\r{C_INFO}{loading_chars[loading_idx]} Scanning... "
                                   f"({subdomain_count} found){C_RESET}")
                    sys.stdout.flush()
                    loading_idx = (loading_idx + 1) % len(loading_chars)
            
            except:
                time.sleep(0.1)
        
        # Qolgan outputni o'qish
        remaining_output = process.stdout.read()
        if remaining_output:
            for line in remaining_output.split('\n'):
                line = line.strip()
                if line:
                    print(f"{C_WARN}[RAW]{C_RESET} {line}")
                    words = line.split()
                    for word in words:
                        clean_word = word.strip('[](){}\'\"<>:,;!?')
                        if is_valid_subdomain(clean_word, domain):
                            if clean_word not in live_results:
                                live_results.add(clean_word)
                                print(f"{C_OK}[✓] {clean_word}{C_RESET}")
        
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        process.wait()
        
        return live_results, process.returncode
        
    except Exception as e:
        Logger.error(f"Jarayon xatosi: {e}")
        import traceback
        traceback.print_exc()
        return live_results, -1


def run_sublist3r_scanner(target=None):
    """Sublist3r asosiy funksiya"""
    clear_screen()
    print_header("SUBLIST3R - OSINT SUBDOMAIN DISCOVERY", 80)
    print(f"{C_TITLE}         Fast Subdomains Enumeration Using OSINT{C_RESET}")
    print(f"{C_INFO}         https://github.com/aboul3la/Sublist3r{C_RESET}\n")
    
    # Tool mavjudligini tekshirish
    sublist3r_type, sublist3r_path = check_sublist3r()
    if not sublist3r_type:
        pause()
        return
    
    print(f"{C_OK}[✓] Sublist3r topildi: {sublist3r_type}{C_RESET}")
    if sublist3r_path:
        print(f"{C_INFO}[*] Path: {sublist3r_path}{C_RESET}\n")
    else:
        print()
    time.sleep(1)
    
    # Domain olish
    if not target:
        print(f"{C_INFO}Target domain kiriting:{C_RESET}")
        print(f"    {C_WARN}Masalan: example.com, google.com, tesla.com{C_RESET}")
        target = input(f"\n{C_INFO}Domain{C_RESET} {C_WARN}>{C_RESET} ").strip()
    
    if not target:
        Logger.error("Domain kiritilmadi!")
        pause()
        return
    
    # URL'ni tozalash
    domain = target.replace("http://", "").replace("https://", "")
    domain = domain.replace("www.", "").split('/')[0].split(':')[0]
    
    print(f"\n{C_OK}[✓] Target: {domain}{C_RESET}")
    time.sleep(0.5)
    
    # Engine'larni tanlash
    engines = get_scan_engines()
    
    # Parametrlarni olish
    options = get_scan_options()
    
    # Output faylini yaratish
    output_dir = "reports/information_gathering/sublist3r"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.abspath(f"{output_dir}/{domain}_{timestamp}.txt")
    
    # Buyruqni tuzish
    if sublist3r_type == "command":
        cmd = ["sublist3r"]
    elif sublist3r_type == "module":
        cmd = [sys.executable, "-m", "sublist3r"]
    else:  # script
        cmd = [sys.executable, sublist3r_path]
    
    cmd.extend(["-d", domain, "-o", output_file])
    
    if engines:
        cmd.extend(["-e", ",".join(engines)])
    
    if options['threads']:
        cmd.extend(["-t", str(options['threads'])])
    
    if options['ports']:
        cmd.extend(["-p", options['ports']])
    
    if options['bruteforce']:
        cmd.append("-b")
    
    # Verbose mode - bu juda muhim!
    cmd.append("-v")
    
    # Scan boshlash
    print(f"\n{C_TITLE}{'='*80}{C_RESET}")
    print(f"{C_TITLE}                         SCAN BOSHLANDI{C_RESET}")
    print(f"{C_TITLE}{'='*80}{C_RESET}\n")
    print(f"{C_OK}[+] Domain:{C_RESET}      {domain}")
    print(f"{C_OK}[+] Engines:{C_RESET}     {len(engines)} ta")
    print(f"{C_OK}[+] Threads:{C_RESET}     {options['threads']}")
    if options['ports']:
        print(f"{C_OK}[+] Ports:{C_RESET}       {options['ports']}")
    if options['bruteforce']:
        print(f"{C_WARN}[+] Bruteforce:{C_RESET}  ENABLED ⚠")
    print(f"{C_OK}[+] Output:{C_RESET}      {output_file}")
    print(f"\n{C_WARN}{'='*80}{C_RESET}\n")
    
    start_time = time.time()
    
    try:
        # Sublist3r ishga tushirish
        live_results, return_code = run_sublist3r_command(cmd, output_file, domain)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{C_WARN}{'='*80}{C_RESET}\n")
        
        # Natijalarni parsing
        stats = parse_sublist3r_output(output_file, live_results)
        
        if stats and stats['total'] > 0:
            Logger.success(f"Scan muvaffaqiyatli tugadi!")
            display_results(stats, domain, engines, elapsed_time)
            print(f"{C_INFO}[💾] Natijalar saqlandi: {output_file}{C_RESET}\n")
        else:
            Logger.warning("Hech qanday subdomain topilmadi!")
            print(f"\n{C_ERR}{'='*80}{C_RESET}")
            print(f"{C_ERR}              RATE LIMIT / BLOKLASH MUAMMOSI{C_RESET}")
            print(f"{C_ERR}{'='*80}{C_RESET}\n")
            
            print(f"{C_WARN}Sabablari:{C_RESET}")
            print(f"  {C_ERR}✗ Google/Bing/Yahoo sizni bloklagan (rate limit){C_RESET}")
            print(f"  {C_WARN}• Domain mavjud emas yoki noto'g'ri{C_RESET}")
            print(f"  {C_WARN}• Internet aloqasi muammosi{C_RESET}\n")
            
            print(f"{C_OK}Yechimlar:{C_RESET}\n")
            print(f"  {C_INFO}1. Safe Mode ishlatish:{C_RESET}")
            print(f"     {C_OK}Qayta scan qiling va [2] Safe Mode tanlang{C_RESET}\n")
            
            print(f"  {C_INFO}2. VPN/Proxy ishlatish:{C_RESET}")
            print(f"     {C_OK}export HTTP_PROXY=http://proxy:8080{C_RESET}")
            print(f"     {C_OK}export HTTPS_PROXY=http://proxy:8080{C_RESET}\n")
            
            print(f"  {C_INFO}3. Kutib turish:{C_RESET}")
            print(f"     {C_OK}10-15 daqiqa kutib qayta urinib ko'ring{C_RESET}\n")
            
            print(f"  {C_INFO}4. Alternative tools:{C_RESET}")
            print(f"     {C_OK}• Amass (ko'proq engine, rate limit kam){C_RESET}")
            print(f"     {C_OK}• Subfinder (juda tez, passive){C_RESET}")
            print(f"     {C_OK}• Assetfinder (yengil va tez){C_RESET}\n")
            
            # Output faylni tekshirish
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"{C_INFO}[*] Output fayl: {output_file} ({file_size} bytes){C_RESET}")
                if file_size > 0:
                    print(f"{C_INFO}[*] Fayl ichidagi ma'lumotlar:{C_RESET}")
                    with open(output_file, 'r') as f:
                        content = f.read()
                        print(content[:500])
            print()
    
    except KeyboardInterrupt:
        print(f"\n\n{C_ERR}[!] Scan to'xtatildi (Ctrl+C){C_RESET}\n")
    except Exception as e:
        Logger.error(f"Kritik xatolik: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"\n{C_INFO}Debug ma'lumotlari:{C_RESET}")
        print(f"  Command: {' '.join(cmd)}")
        print(f"  Output: {output_file}\n")
    
    print_footer()
    pause()


def run_sublist3r(target):
    """Menu uchun wrapper funksiya"""
    run_sublist3r_scanner(target)


if __name__ == "__main__":
    # Test rejimi
    if len(sys.argv) > 1:
        run_sublist3r_scanner(sys.argv[1])
    else:
        run_sublist3r_scanner()