# app/information_gathering/active/whatweb.py

import os
import sys
import subprocess
import shutil
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from app.config import C_TITLE, C_OK, C_WARN, C_ERR, C_INFO, C_RESET
from app.utils import Logger, print_header, print_footer, pause, clear_screen


def check_whatweb():
    """WhatWeb o'rnatilganligini tekshirish"""
    if shutil.which("whatweb"):
        return True
    Logger.error("WhatWeb topilmadi!")
    print(f"\n{C_WARN}[!] O'rnatish:{C_RESET}")
    print(f"    {C_INFO}apt install whatweb{C_RESET}")
    print(f"    {C_INFO}yoki: gem install whatweb{C_RESET}\n")
    return False


def get_aggression_level():
    """Aggression darajasini tanlash"""
    print(f"\n{C_TITLE}[+] Aggression darajasi:{C_RESET}")
    print(f"  {C_INFO}[1]{C_RESET} Stealthy  - Minimal requests (passive)")
    print(f"  {C_INFO}[2]{C_RESET} Polite    - Limited requests")
    print(f"  {C_INFO}[3]{C_RESET} Aggressive - Normal scanning (default)")
    print(f"  {C_INFO}[4]{C_RESET} Heavy     - Intensive probing")
    
    choice = input(f"\n{C_INFO}She11> {C_RESET}").strip() or "3"
    
    levels = {'1': '1', '2': '2', '3': '3', '4': '4'}
    return levels.get(choice, '3')


def auto_detect_protocol(target):
    """HTTPS yoki HTTP ni avtomatik aniqlash"""
    try:
        import requests
        protocols = ['https://', 'http://']
        for proto in protocols:
            try:
                response = requests.get(proto + target, timeout=5, verify=False)
                if response.status_code < 400:
                    return proto + target
            except:
                continue
    except ImportError:
        Logger.warning("Requests kutubxonasi topilmadi, HTTP default ishlatiladi.")
    return f"http://{target}"


def parse_whatweb_output(output):
    """WhatWeb natijalarini parsing qilish"""
    results = {
        'url': '',
        'status': '',
        'title': '',
        'ip': '',
        'country': '',
        'server': '',
        'technologies': [],
        'cms': '',
        'programming': [],
        'javascript': [],
        'analytics': [],
        'cdn': '',
        'headers': {},
        'redirect': None  # Redirect uchun qo'shildi
    }
    
    try:
        data = json.loads(output)
        if isinstance(data, list) and len(data) > 0:
            # Oxirgi elementni ol (200 OK, redirectdan keyin)
            item = data[-1]
            if len(data) > 1 and data[0].get('http_status') == 301:
                results['redirect'] = data[0].get('target', '')  # Redirect URL
            results['url'] = item.get('target', '')
            results['status'] = str(item.get('http_status', ''))
            
            plugins = item.get('plugins', {})
            
            # Server
            if 'HTTPServer' in plugins:
                server_info = plugins['HTTPServer'].get('string', [''])[0]
                results['server'] = server_info
            
            # Title
            if 'Title' in plugins:
                results['title'] = plugins['Title'].get('string', [''])[0]
            
            # IP
            if 'IP' in plugins:
                results['ip'] = plugins['IP'].get('string', [''])[0]
            
            # Country
            if 'Country' in plugins:
                results['country'] = plugins['Country'].get('string', [''])[0]
            
            # CMS Detection
            cms_list = ['WordPress', 'Joomla', 'Drupal', 'Magento', 'PrestaShop', 'Shopify']
            for cms in cms_list:
                if cms in plugins:
                    version = plugins[cms].get('version', [''])[0]
                    results['cms'] = f"{cms} {version}".strip() if version else cms
                    break  # Faqat birinchisini ol
            
            # Programming Languages
            prog_langs = ['PHP', 'ASP.NET', 'Python', 'Ruby', 'Java']
            for lang in prog_langs:
                if lang in plugins:
                    version = plugins[lang].get('version', [''])[0]
                    results['programming'].append(f"{lang} {version}".strip())
            
            # JavaScript Libraries
            js_libs = ['jQuery', 'AngularJS', 'React', 'Vue.js', 'Bootstrap']
            for lib in js_libs:
                if lib in plugins:
                    version = plugins[lib].get('version', [''])[0]
                    results['javascript'].append(f"{lib} {version}".strip())
            
            # Analytics
            analytics = ['Google-Analytics', 'Yandex.Metrika']
            for tool in analytics:
                if tool in plugins:
                    results['analytics'].append(tool)
            
            # CDN
            if 'Cloudflare' in plugins:
                results['cdn'] = 'Cloudflare'
            elif 'Amazon-CloudFront' in plugins:
                results['cdn'] = 'Amazon CloudFront'
            
            # Barcha texnologiyalar
            results['technologies'] = list(plugins.keys())
            
            # Headers (UncommonHeaders dan)
            if 'UncommonHeaders' in plugins:
                results['headers'] = {'Uncommon': plugins['UncommonHeaders'].get('string', [''])[0]}
            if 'X-Frame-Options' in plugins:
                results['headers']['X-Frame-Options'] = plugins['X-Frame-Options'].get('string', [''])[0]
    
    except json.JSONDecodeError as e:
        Logger.warning(f"JSON parsing xatosi: {e}. Text rejimiga o'tildi.")
        # Fallback: Oddiy text parse
        for line in output.split('\n'):
            if '[' in line and ']' in line:
                tech = line.split('[')[1].split(']')[0]
                if tech not in results['technologies']:
                    results['technologies'].append(tech)
    
    return results


def display_results(results):
    """Natijalarni chiroyli va tushunarli formatda ko'rsatish"""
    print(f"\n{C_TITLE}{'='*80}{C_RESET}")
    print(f"{C_TITLE}                        WHATWEB SCAN RESULTS{C_RESET}")
    print(f"{C_TITLE}{'='*80}{C_RESET}\n")
    
    # Asosiy Ma'lumotlar
    if results['redirect']:
        print(f"{C_WARN}[!] Redirect topildi: {results['redirect']} → {results['url']}{C_RESET}")
    if results['url']:
        print(f"{C_OK}[+] URL:{C_RESET} {results['url']}")
    if results['status']:
        status_color = C_OK if '200' in results['status'] else C_WARN
        print(f"{status_color}[+] Status:{C_RESET} {results['status']}")
    if results['title']:
        print(f"{C_INFO}[+] Title:{C_RESET} {results['title']}")
    if results['ip']:
        print(f"{C_INFO}[+] IP:{C_RESET} {results['ip']}")
    if results['country']:
        print(f"{C_INFO}[+] Country:{C_RESET} {results['country']}")
    
    print(f"\n{C_TITLE}[+] SERVER & SECURITY:{C_RESET}")
    if results['server']:
        print(f"    {C_OK}Server:{C_RESET} {results['server']}")
    if results['cdn']:
        print(f"    {C_OK}CDN:{C_RESET} {results['cdn']}")
    if results['headers']:
        print(f"    {C_WARN}Headers:{C_RESET} {results['headers']}")
    
    # CMS
    if results['cms']:
        print(f"\n{C_TITLE}[+] CMS:{C_RESET}")
        print(f"    {C_OK}• {results['cms']}{C_RESET}")
    
    # Programming
    if results['programming']:
        print(f"\n{C_TITLE}[+] PROGRAMMING LANGUAGES:{C_RESET}")
        for lang in results['programming']:
            print(f"    {C_OK}• {lang}{C_RESET}")
    
    # JavaScript
    if results['javascript']:
        print(f"\n{C_TITLE}[+] JAVASCRIPT LIBS:{C_RESET}")
        for lib in results['javascript']:
            print(f"    {C_INFO}• {lib}{C_RESET}")
    
    # Analytics
    if results['analytics']:
        print(f"\n{C_TITLE}[+] ANALYTICS:{C_RESET}")
        for tool in results['analytics']:
            print(f"    {C_INFO}• {tool}{C_RESET}")
    
    # Texnologiyalar (jadval shaklida, tushunarli qilish uchun)
    if results['technologies']:
        print(f"\n{C_TITLE}[+] TEXNOLOGIYALAR ({len(results['technologies'])} ta):{C_RESET}")
        # Guruhlab ko'rsatish (5 tadan)
        for i in range(0, len(results['technologies']), 5):
            batch = results['technologies'][i:i+5]
            print(f"    {C_INFO}• {', '.join(batch)}{C_RESET}")
    
    print(f"\n{C_TITLE}{'='*80}{C_RESET}\n")


def run_whatweb_scanner(target=None):
    """WhatWeb asosiy funksiya"""
    clear_screen()
    print_header("WHATWEB - WEB TECHNOLOGY IDENTIFIER", 80)
    print(f"{C_TITLE}           Identify Technologies Used by Websites{C_RESET}\n")
    
    # Tool tekshirish
    if not check_whatweb():
        pause()
        return
    
    # Target olish
    if not target:
        print(f"{C_INFO}Target URL kiriting (example.com):{C_RESET}")
        target = input(f"    {C_INFO}She11>{C_RESET} ").strip()
    
    if not target:
        Logger.error("Target kiritilmadi!")
        pause()
        return
    
    # Protocol aniqlash
    if not target.startswith(("http://", "https://")):
        target = auto_detect_protocol(target)
        print(f"{C_INFO}[*] Protocol: {target}{C_RESET}")
    
    # Aggression tanlash
    aggression = get_aggression_level()
    
    # Output fayllari
    output_dir = "reports/information_gathering/whatweb"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = target.replace("http://", "").replace("https://", "").replace("/", "_").replace(":", "_")
    output_file = f"{output_dir}/whatweb_{domain}_{timestamp}"
    
    # WhatWeb cmd
    cmd = [
        "whatweb",
        "-a", aggression,
        "--log-json", f"{output_file}.json",
        "--color=never",
        "--follow-redirect=always",  # Redirectlarni follow qilish
        target
    ]
    
    print(f"\n{C_OK}[+] WhatWeb ishga tushmoqda...{C_RESET}")
    print(f"{C_INFO}[*] Target: {target}{C_RESET}")
    print(f"{C_INFO}[*] Aggression: {aggression}{C_RESET}")
    print(f"{C_INFO}[*] Output: {output_file}.json{C_RESET}\n")
    
    # Loading
    loading_chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    loading_idx = 0
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Loading loop
        while process.poll() is None:
            sys.stdout.write(f"\r{C_INFO}{loading_chars[loading_idx]} Analyzing...{C_RESET}")
            sys.stdout.flush()
            loading_idx = (loading_idx + 1) % len(loading_chars)
            time.sleep(0.1)
        
        sys.stdout.write('\r' + ' ' * 60 + '\r')  # Clear
        
        stdout, stderr = process.communicate()
        
        # JSON o'qish va parse
        json_path = f"{output_file}.json"
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                json_output = f.read()
            reports = parse_whatweb_output(json_output)
            display_results(reports)
            
            # TXT saqlash
            txt_path = f"{output_file}.txt"
            with open(txt_path, 'w') as f:
                f.write(stdout)
            
            Logger.success("Scan yakunlandi!")
            print(f"{C_INFO}[*] Fayllar:{C_RESET} {json_path}, {txt_path}\n")
        else:
            Logger.error("JSON fayl yaratilmadi!")
            if stdout:
                print(f"\n{C_INFO}Raw:{C_RESET}\n{stdout}")
        
        if stderr:
            Logger.warning(f"Stderr: {stderr.strip()}")
    
    except KeyboardInterrupt:
        print(f"\n\n{C_WARN}[!] To'xtatildi (Ctrl+C){C_RESET}")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        Logger.error(f"Xato: {str(e)}")
    
    print_footer()
    pause()


def run_whatweb(target):
    """Wrapper"""
    run_whatweb_scanner(target)


if __name__ == "__main__":
    run_whatweb_scanner()