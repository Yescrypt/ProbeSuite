# app/information_gathering/passive/wayback_urls.py

import os
import sys
import subprocess
import shutil
from datetime import datetime
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, C_TITLE, REPORTS_DIR
from app.utils import clear_screen, pause  # pause qo'shildi


# Maxsus pattern'lar
PATTERNS = {
    "1": {
        "name": "Admin Panellar",
        "keywords": ["admin", "administrator", "dashboard", "panel", "cpanel", "manage", "backend", "control"],
        "description": "Admin sahifalar va boshqaruv panellari"
    },
    "2": {
        "name": "Login/Auth Sahifalar",
        "keywords": ["login", "signin", "auth", "register", "signup", "password", "forgot", "reset"],
        "description": "Kirish va autentifikatsiya sahifalari"
    },
    "3": {
        "name": "API Endpoints",
        "keywords": ["api", "rest", "graphql", "endpoint", "v1", "v2", "v3", "json", "xml", "swagger"],
        "description": "API yo'nalishlari va versiyalari"
    },
    "4": {
        "name": "Config & Backup Files",
        "keywords": [".config", ".bak", ".backup", ".old", ".sql", ".zip", ".tar", ".gz", "backup", "dump"],
        "description": "Konfiguratsiya va zaxira fayllari"
    },
    "5": {
        "name": "Upload Directories",
        "keywords": ["upload", "uploads", "files", "media", "assets", "static", "public", "images"],
        "description": "Yuklangan fayllar kataloglari"
    },
    "6": {
        "name": "Sensitive Files",
        "keywords": [".env", ".git", ".htaccess", "wp-config", "config.php", "database", ".log", "phpinfo"],
        "description": "Maxfiy va muhim fayllar"
    },
    "7": {
        "name": "User/Profile Pages",
        "keywords": ["user", "profile", "account", "settings", "preferences", "member"],
        "description": "Foydalanuvchi profillari va sozlamalar"
    },
    "8": {
        "name": "Barcha URL'lar",
        "keywords": [],
        "description": "Hech qanday filtrsiz barcha URL'lar"
    },
    "9": {
        "name": "Custom Search",
        "keywords": [],
        "description": "O'zingiz yozadigan kalit so'z"
    }
}


def show_search_menu():
    """Qidiruv menyusini ko'rsatish"""
    print(f"\n{C_TITLE}╔══════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_TITLE}║{C_RESET}                        {C_INFO}QIDIRUV REJIMINI TANLANG{C_RESET}                              {C_TITLE}║{C_RESET}")
    print(f"{C_TITLE}╠══════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
    
    for key, value in PATTERNS.items():
        print(f"{C_TITLE}║{C_RESET} {C_OK}[{key:>2}]{C_RESET} {value['name']:<24} {C_INFO}{value['description']:<46}{C_RESET} {C_TITLE}║{C_RESET}")
    
    print(f"{C_TITLE}║{C_RESET} {C_WARN}[ 0]{C_RESET} Orqaga{' '*66}{C_TITLE}║{C_RESET}")
    print(f"{C_TITLE}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}")


def check_waybackurls():
    """waybackurls toolining o'rnatilganligini tekshirish"""
    
    # PATH ni kengaytirish
    go_paths = [
        os.path.expanduser("~/go/bin"),
        os.path.expanduser("~/.local/bin"),
        "/usr/local/go/bin",
        "/usr/local/bin"
    ]
    
    # PATH ga qo'shish
    current_path = os.environ.get('PATH', '')
    for gp in go_paths:
        if os.path.exists(gp) and gp not in current_path:
            os.environ['PATH'] = f"{gp}:{current_path}"
            current_path = os.environ['PATH']
    
    has_cli = shutil.which("waybackurls") is not None
    has_python = False
    
    try:
        import waybackpy
        has_python = True
    except ImportError:
        pass
    
    if has_cli:
        print(f"{C_OK}[✓] waybackurls CLI tool topildi (Go versiyasi - tezroq){C_RESET}")
        return "cli"
    elif has_python:
        print(f"{C_WARN}[!] waybackurls CLI topilmadi, Python versiyasi ishlatiladi (SEKIN!){C_RESET}")
        print(f"{C_INFO}[*] CLI versiyasini o'rnatish (tavsiya etiladi):{C_RESET}")
        print(f"    {C_WARN}go install github.com/tomnomnom/waybackurls@latest{C_RESET}")
        print(f"    {C_WARN}export PATH=$PATH:~/go/bin{C_RESET}")
        
        # Foydalanuvchidan tasdiqlash
        choice = input(f"\n{C_INFO}Python versiyasi bilan davom etasizmi? (y/n): {C_RESET}").strip().lower()
        if choice != 'y':
            return None
        return "python"
    else:
        print(f"\n{C_ERR}[!] Wayback tool topilmadi!{C_RESET}")
        print(f"{C_INFO}[*] Quyidagilardan birini o'rnating:{C_RESET}\n")
        print(f"    {C_OK}1. Go versiyasi (tavsiya etiladi - tezroq):{C_RESET}")
        print(f"       {C_WARN}go install github.com/tomnomnom/waybackurls@latest{C_RESET}")
        print(f"       {C_WARN}export PATH=$PATH:~/go/bin{C_RESET}\n")
        print(f"    {C_OK}2. Python versiyasi:{C_RESET}")
        print(f"       {C_WARN}pip install waybackpy{C_RESET}\n")
        return None


def run_waybackurls_tool(domain, method="cli"):
    """waybackurls toolini ishga tushirish (CLI yoki Python)"""
    
    if method == "cli":
        # Go CLI versiyasi (tezroq)
        try:
            print(f"{C_INFO}[*] waybackurls CLI ishga tushirilmoqda...{C_RESET}")
            
            # Environment PATH ni to'g'ri o'rnatish
            env = os.environ.copy()
            if 'HOME' in env:
                go_bin = os.path.join(env['HOME'], 'go', 'bin')
                if os.path.exists(go_bin):
                    env['PATH'] = f"{go_bin}:{env.get('PATH', '')}"
            
            result = subprocess.run(
                ["waybackurls", domain],
                capture_output=True,
                text=True,
                timeout=180,  # 3 daqiqa
                env=env
            )
            
            if result.returncode == 0:
                # Stdout ni tekshirish
                output = result.stdout.strip()
                if not output:
                    print(f"{C_WARN}[!] waybackurls hech narsa qaytarmadi{C_RESET}")
                    return []
                
                # URL'larni ajratish
                urls = [url.strip() for url in output.split('\n') if url.strip()]
                
                # URL'lar sonini tekshirish
                if len(urls) < 10:
                    print(f"{C_WARN}[!] Juda kam URL topildi ({len(urls)} ta){C_RESET}")
                    print(f"{C_INFO}[*] Terminal'da sinab ko'ring: waybackurls {domain}{C_RESET}")
                
                return urls
            else:
                error_msg = result.stderr.strip() if result.stderr else "Noma'lum xato"
                print(f"{C_ERR}[!] Xato: {error_msg}{C_RESET}")
                return []
                
        except subprocess.TimeoutExpired:
            print(f"{C_WARN}[!] Timeout: 3 daqiqadan oshdi{C_RESET}")
            return []
        except FileNotFoundError:
            print(f"{C_ERR}[!] waybackurls command topilmadi{C_RESET}")
            print(f"{C_INFO}[*] PATH: {os.environ.get('PATH', 'NOT SET')}{C_RESET}")
            return []
        except Exception as e:
            print(f"{C_ERR}[!] Xato: {str(e)}{C_RESET}")
            import traceback
            traceback.print_exc()
            return []
    
    elif method == "python":
        # Python versiyasi (sekinroq lekin ishlaydi)
        try:
            from waybackpy import WaybackMachineCDXServerAPI
            
            print(f"{C_INFO}[*] Python waybackpy ishlatilmoqda...{C_RESET}")
            print(f"{C_WARN}[*] Katta saytlar uchun bu juda sekin bo'lishi mumkin!{C_RESET}")
            
            # Limit qo'yish (katta saytlar uchun)
            MAX_URLS = 50000
            print(f"{C_INFO}[*] Maksimal limit: {MAX_URLS} ta URL{C_RESET}")
            
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            cdx_api = WaybackMachineCDXServerAPI(domain, user_agent)
            
            urls = []
            count = 0
            print(f"{C_INFO}[*] URL'lar yuklanmoqda", end="", flush=True)
            
            try:
                for item in cdx_api.snapshots():
                    if item.archive_url:
                        urls.append(item.original)
                        count += 1
                        
                        # Har 500 ta URL'da progress ko'rsatish (tezroq)
                        if count % 500 == 0:
                            print(".", end="", flush=True)
                        
                        # Har 5000 ta URL'da raqam ko'rsatish
                        if count % 5000 == 0:
                            print(f" {count}", end="", flush=True)
                        
                        # Limitga yetganda to'xtatish
                        if count >= MAX_URLS:
                            print(f"\n{C_WARN}[!] Limit ({MAX_URLS}) ga yetdi, to'xtatilmoqda...{C_RESET}")
                            break
            except KeyboardInterrupt:
                print(f"\n{C_WARN}[!] Foydalanuvchi tomonidan to'xtatildi{C_RESET}")
            
            print(f" {C_OK}✓{C_RESET}\n")  # Tugadi belgisi
            
            return list(set(urls))  # Dublikatlarni olib tashlash
            
        except ImportError:
            print(f"{C_ERR}[!] waybackpy kutubxonasi topilmadi{C_RESET}")
            print(f"{C_INFO}[*] O'rnatish: pip install waybackpy{C_RESET}")
            return []
        except Exception as e:
            print(f"\n{C_ERR}[!] Xato: {str(e)}{C_RESET}")
            return []
    
    return []


def filter_urls(urls, keywords):
    """URL'larni kalit so'zlar bo'yicha filtrlash (grep kabi)"""
    if not keywords:
        return urls
    
    filtered = []
    for url in urls:
        url_lower = url.lower()
        
        # Har bir keyword uchun tekshirish
        for keyword in keywords:
            kw_lower = keyword.lower()
            
            # Agar keyword fayl kengaytmasi bo'lsa (.txt, .php, .config)
            if kw_lower.startswith('.') and len(kw_lower) > 1:
                # URL oxirida bo'lishi kerak
                if url_lower.endswith(kw_lower):
                    filtered.append(url)
                    break
            # Agar keyword robots.txt, sitemap.xml kabi to'liq fayl nomi bo'lsa
            elif '.' in kw_lower and not kw_lower.startswith('http'):
                # Fayl nomi URL'da biron joyda bo'lishi mumkin
                # Masalan: /robots.txt, /path/robots.txt, /username/robots.txt
                # Split qilib oxirgi qismini olish
                parts = url_lower.split('/')
                if kw_lower in parts:  # Aniq fayl nomi
                    filtered.append(url)
                    break
                # Yoki URL'da umuman mavjudmi
                elif kw_lower in url_lower:
                    filtered.append(url)
                    break
            # Oddiy so'z qidiruvi (admin, login, api)
            else:
                if kw_lower in url_lower:
                    filtered.append(url)
                    break
    
    return filtered


def get_file_extensions(urls):
    """URL'lardan fayl kengaytmalarini ajratib olish"""
    extensions = {}
    for url in urls:
        match = re.search(r'\.(php|html|js|css|jpg|png|pdf|txt|xml|json|asp|jsp|config|bak|sql|env|log|zip|tar|gz)$', url.lower())
        if match:
            ext = match.group(1)
            extensions[ext] = extensions.get(ext, 0) + 1
    return extensions


def categorize_urls(urls):
    """URL'larni kategoriyalarga ajratish"""
    categories = {
        "Admin": 0,
        "Login": 0,
        "API": 0,
        "Upload": 0,
        "Config": 0,
        "Sensitive": 0
    }
    
    for url in urls:
        url_lower = url.lower()
        if any(word in url_lower for word in ["admin", "panel", "dashboard"]):
            categories["Admin"] += 1
        if any(word in url_lower for word in ["login", "signin", "auth"]):
            categories["Login"] += 1
        if any(word in url_lower for word in ["api", "rest", "endpoint"]):
            categories["API"] += 1
        if any(word in url_lower for word in ["upload", "files", "media"]):
            categories["Upload"] += 1
        if any(word in url_lower for word in [".config", ".bak", ".sql", "backup"]):
            categories["Config"] += 1
        if any(word in url_lower for word in [".env", ".git", ".log"]):
            categories["Sensitive"] += 1
    
    return categories


def run_wayback_urls(target=""):
    clear_screen()
    
    if not target:
        target = input(f"{C_INFO}Domen kiriting (masalan: example.com): {C_RESET}").strip()

    domain = target.replace("https://", "").replace("http://", "").split("/")[0].lower()

    print(f"{C_TITLE}")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                       WAYBACK MACHINE (archive.org)                          ║")
    print("║                  Saytning eski sahifalari va arxivlari                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{C_RESET}")

    # waybackurls toolini tekshirish
    method = check_waybackurls()
    if not method:
        pause()
        return
    
    print()  # Bo'sh qator

    # Asosiy tsikl – bir domen bilan bir necha marta turli rejimda skan qilish mumkin
    while True:
        show_search_menu()
        choice = input(f"\n{C_INFO}Rejimni tanlang [1-9]: {C_RESET}").strip()

        if choice == "0":
            break  # Orqaga chiqish

        if choice not in PATTERNS:
            print(f"{C_ERR}[!] Noto'g'ri tanlov!{C_RESET}")
            pause()
            continue

        selected_pattern = PATTERNS[choice]
        keywords = selected_pattern["keywords"].copy()

        # Custom search uchun
        if choice == "9":
            custom = input(f"{C_INFO}Kalit so'zlarni kiriting (vergul bilan ajrating): {C_RESET}").strip()
            keywords = [k.strip() for k in custom.split(",") if k.strip()]
            if not keywords:
                print(f"{C_ERR}[!] Kalit so'z kiritilmadi!{C_RESET}")
                pause()
                continue

        print(f"\n{C_INFO}[*] waybackurls ishga tushirilmoqda → {domain}{C_RESET}")
        if keywords:
            print(f"{C_INFO}[*] Filtrlash: {C_OK}{', '.join(keywords[:5])}{C_RESET}")
            if len(keywords) > 5:
                print(f"{C_INFO}    va yana {len(keywords)-5} ta...{C_RESET}")
        
        print(f"{C_WARN}[*] Bu jarayon biroz vaqt olishi mumkin...{C_RESET}\n")

        try:
            # waybackurls toolini ishga tushirish
            all_urls = run_waybackurls_tool(domain, method)
            
            if not all_urls:
                print(f"{C_WARN}[!] {domain} uchun arxiv topilmadi{C_RESET}")
                print(f"\n{C_INFO}[*] Mumkin bo'lgan sabablar:{C_RESET}")
                print(f"    {C_INFO}→ Sayt Wayback Machine'da arxivlanmagan{C_RESET}")
                print(f"    {C_INFO}→ Sayt robots.txt orqali bloklangan{C_RESET}")
                print(f"    {C_INFO}→ Sayt yaqinda yaratilgan{C_RESET}\n")
                pause()
                continue

            total = len(all_urls)
            print(f"{C_OK}[+] {total} ta URL topildi!{C_RESET}\n")

            # Filtrlash (grep kabi)
            if choice == "8":  # Barcha URL'lar
                urls = all_urls
                filtered_count = total
            else:
                print(f"{C_INFO}[*] Filtrlash jarayoni...{C_RESET}")
                urls = filter_urls(all_urls, keywords)
                filtered_count = len(urls)
                print(f"{C_OK}[✓] {filtered_count} ta mos URL topildi{C_RESET}\n")

            if filtered_count == 0:
                print(f"{C_WARN}[!] Bu kalit so'zlar bo'yicha hech narsa topilmadi{C_RESET}")
                print(f"\n{C_INFO}[*] Tavsiyalar:{C_RESET}")
                print(f"    {C_INFO}→ [8] Barcha URL'lar rejimini sinab ko'ring{C_RESET}")
                print(f"    {C_INFO}→ [9] Custom Search orqali boshqa so'zlarni kiriting{C_RESET}\n")
                
                # Umumiy statistika
                categories = categorize_urls(all_urls)
                if any(categories.values()):
                    print(f"{C_INFO}[*] Mavjud kategoriyalar:{C_RESET}")
                    for cat, count in categories.items():
                        if count > 0:
                            print(f"    {C_OK}→ {cat}: {count} ta{C_RESET}")
                    print()
                
                pause()
                continue

            # Fayl kengaytmalari
            extensions = get_file_extensions(urls)
            if extensions:
                print(f"{C_INFO}[*] Topilgan fayl turlari:{C_RESET}")
                for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:
                    print(f"    {C_OK}→ .{ext}: {count} ta{C_RESET}")
                print()

            # Natijalarni ko'rsatish
            w = 100
            print(f"{C_TITLE}╔{'═'*w}╗{C_RESET}")
            print(f"{C_TITLE}║{C_RESET}{C_OK} {selected_pattern['name'].upper() + ' → ' + domain.upper():^99}{C_RESET}{C_TITLE}║{C_RESET}")
            print(f"{C_TITLE}╠{'═'*w}╣{C_RESET}")
            
            if choice == "8":
                print(f"{C_TITLE}║{C_RESET} {C_INFO}Jami URL'lar:{C_RESET} {C_OK}{total} ta{C_RESET}{' '*62}{C_TITLE}║{C_RESET}")
            else:
                print(f"{C_TITLE}║{C_RESET} {C_INFO}Jami:{C_RESET} {C_OK}{total} ta{C_RESET}  |  {C_INFO}Filtrlangan:{C_RESET} {C_OK}{filtered_count} ta{C_RESET}{' '*61}{C_TITLE}║{C_RESET}")
            
            print(f"{C_TITLE}╠{'═'*w}╣{C_RESET}")

            # Birinchi 50 ta natija
            display_limit = min(50, len(urls))
            for i, url in enumerate(urls[:display_limit], 1):
                short = url.replace("https://", "").replace("http://", "")
                if len(short) > 85:
                    short = short[:82] + "..."
                
                # Kalit so'zlarni highlight qilish
                display_url = short
                if keywords and choice != "8":
                    for kw in keywords:
                        if kw.lower() in short.lower():
                            pattern = re.compile(re.escape(kw), re.IGNORECASE)
                            display_url = pattern.sub(f"{C_WARN}{kw}{C_INFO}", short)
                            break
                
                print(f"{C_TITLE}║{C_RESET} {C_OK}{i:>3}.{C_RESET} {C_INFO}{display_url:<112}{C_RESET}{C_TITLE}║{C_RESET}")

            if filtered_count > display_limit:
                remaining = filtered_count - display_limit
                print(f"{C_TITLE}║{C_RESET}      {C_WARN}... yana {remaining} ta URL (to'liq ro'yxat hisobotda){C_RESET}{' '*48}{C_TITLE}║{C_RESET}")
            
            print(f"{C_TITLE}╚{'═'*w}╝{C_RESET}")

            # Hisobotni saqlash
            save_report(domain, urls, total, filtered_count, selected_pattern, keywords)

        except KeyboardInterrupt:
            print(f"\n\n{C_WARN}[!] Jarayon to'xtatildi{C_RESET}")
        except Exception as e:
            print(f"\n{C_ERR}[!] Xato: {str(e)}{C_RESET}")

        pause()  # Har bir skandan keyin Enter kutamiz, keyin menyuga qaytamiz


def save_report(domain, urls, total, filtered_count, pattern, keywords):
    """Hisobotni saqlash"""
    # <<< YANGI USUL >>> Papka va fayl yo'lini to'g'ridan-to'g'ri yaratamiz
    reports_dir = "reports/information_gathering/passive/waybackurls"
    os.makedirs(reports_dir, exist_ok=True)  # Agar yo'q bo'lsa — avto yaratiladi
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pattern_name = pattern['name'].replace(" ", "_").lower()
    filename = f"wayback_{domain}_{pattern_name}_{ts}.txt"
    full_path = os.path.join(reports_dir, filename)
    
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("="*100 + "\n")
            f.write("WAYBACK MACHINE - URL DISCOVERY (waybackurls tool)\n")
            f.write("="*100 + "\n\n")
            f.write(f"Domen:          {domain}\n")
            f.write(f"Qidiruv turi:   {pattern['name']}\n")
            f.write(f"Kalit so'zlar:  {', '.join(keywords) if keywords else 'Hammasi (filtrsiz)'}\n")
            f.write(f"Jami URL'lar:   {total}\n")
            f.write(f"Filtrlangan:    {filtered_count}\n")
            f.write(f"Sana/Vaqt:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + "="*100 + "\n\n")
            
            # Fayl statistikasi
            extensions = get_file_extensions(urls)
            if extensions:
                f.write("FAYL TURLARI STATISTIKASI:\n")
                f.write("-" * 50 + "\n")
                for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(urls)) * 100
                    f.write(f"  .{ext:<10} → {count:>5} ta ({percentage:>5.1f}%)\n")
                f.write("\n" + "="*100 + "\n\n")
            
            # URL kategoriyalari
            categories = categorize_urls(urls)
            if any(categories.values()):
                f.write("URL KATEGORIYALARI:\n")
                f.write("-" * 50 + "\n")
                for cat, count in categories.items():
                    if count > 0:
                        f.write(f"  {cat:<15} → {count} ta\n")
                f.write("\n" + "="*100 + "\n\n")
            
            # To'liq URL ro'yxati
            f.write("TO'LIQ URL RO'YXATI:\n")
            f.write("-" * 100 + "\n\n")
            for i, url in enumerate(urls, 1):
                f.write(f"{i:>5}. {url}\n")
        
         # Ekranga chiqadigan yo'l ham yangi papkaga moslashtirildi
        relative_path = f"reports/information_gathering/passive/waybackurls/{filename}"
        print(f"\n{C_OK}[+] Hisobot saqlandi → {C_INFO}{relative_path}{C_RESET}")
        print(f"{C_INFO}[*] Hisobotda {filtered_count} ta URL mavjud{C_RESET}")
        
    except Exception as e:
        print(f"{C_ERR}[!] Hisobotni saqlashda xato: {str(e)}{C_RESET}")


if __name__ == "__main__":
    run_wayback_urls()