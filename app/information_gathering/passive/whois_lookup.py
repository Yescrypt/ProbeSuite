# app/information_gathering/passive/whois_lookup.py
# whois_lookup.py → FIXED 2025 VERSIYA (BARCHA DOMENLAR UCHUN ISHLAYDI)

import os
import sys
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, C_TITLE
from app.utils import clear_screen

def parse_whois_object(w):
    """python-whois object-ni matn formatiga o'giradi"""
    try:
        lines = []
        
        # Domain Name
        if hasattr(w, 'name') and w.name:
            lines.append(f"Domain Name: {w.name}")
        
        # Registrar
        if hasattr(w, 'registrar') and w.registrar:
            lines.append(f"Registrar: {w.registrar}")
        
        # Creation Date
        if hasattr(w, 'creation_date'):
            dates = w.creation_date if isinstance(w.creation_date, list) else [w.creation_date]
            for d in dates:
                if d:
                    lines.append(f"Creation Date: {d}")
                    break
        
        # Expiration Date
        if hasattr(w, 'expiration_date'):
            dates = w.expiration_date if isinstance(w.expiration_date, list) else [w.expiration_date]
            for d in dates:
                if d:
                    lines.append(f"Expiration Date: {d}")
                    break
        
        # Updated Date
        if hasattr(w, 'updated_date'):
            dates = w.updated_date if isinstance(w.updated_date, list) else [w.updated_date]
            for d in dates:
                if d:
                    lines.append(f"Updated Date: {d}")
                    break
        
        # Status
        if hasattr(w, 'status'):
            statuses = w.status if isinstance(w.status, list) else [w.status]
            for s in statuses:
                if s:
                    lines.append(f"Status: {s}")
        
        # Name Servers
        if hasattr(w, 'name_servers') and w.name_servers:
            servers = w.name_servers if isinstance(w.name_servers, list) else [w.name_servers]
            for ns in servers:
                if ns:
                    lines.append(f"Name Server: {ns}")
        
        # Registrant
        if hasattr(w, 'registrant_name') and w.registrant_name:
            lines.append(f"\nRegistrant:")
            lines.append(f"  Name: {w.registrant_name}")
        
        if hasattr(w, 'registrant_organization') and w.registrant_organization:
            lines.append(f"  Organization: {w.registrant_organization}")
        
        if hasattr(w, 'registrant_country') and w.registrant_country:
            lines.append(f"  Country: {w.registrant_country}")
        
        # Emails
        if hasattr(w, 'emails') and w.emails:
            emails = w.emails if isinstance(w.emails, list) else [w.emails]
            for email in emails:
                if email and '@' in str(email):
                    lines.append(f"Email: {email}")
        
        return "\n".join(lines) if lines else None
    except Exception as e:
        print(f"{C_WARN}Parse xatosi: {e}{C_RESET}")
        return None

def run_whois(target=""):
    clear_screen()
    if not target:
        target = input(f"{C_INFO}Domen kiriting: {C_RESET}").strip()

    domain = re.sub(r"^https?://", "", target).split("/")[0].split(":")[0].lower()

    print(f"{C_TITLE}")
    print("╔" + "═" * 78 + "╗")
    print("║" + " UNIVERSAL WHOIS LOOKUP – 2025 YIL UCHUN YANGILANDI ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    print(f"{C_RESET}")
    print(f"{C_INFO}[*] WHOIS izlanmoqda → {domain}{C_RESET}\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    raw_text = ""
    source_name = ""

    # 1. whois.com → hali ham ishlaydi
    try:
        print(f"{C_INFO}[1/6] whois.com → sinov...{C_RESET}")
        r = requests.get(f"https://www.whois.com/whois/{domain}", headers=headers, timeout=12)
        if "df-raw" in r.text:
            soup = BeautifulSoup(r.text, "html.parser")
            block = soup.find("pre", {"class": "df-raw"})
            if block:
                raw_text = block.get_text(separator="\n")
                source_name = "whois.com"
                print(f"{C_OK}[+] whois.com → muvaffaqiyat!{C_RESET}\n")
    except Exception as e:
        print(f"{C_WARN}    whois.com xato: {str(e)[:40]}{C_RESET}")

    # 2. whois.net
    if not raw_text:
        try:
            print(f"{C_INFO}[2/6] whois.net → sinov...{C_RESET}")
            r = requests.get(f"https://whois.net/{domain}", headers=headers, timeout=12)
            if "Registrar" in r.text and len(r.text) > 2000:
                soup = BeautifulSoup(r.text, "html.parser")
                pre = soup.find("pre")
                if pre:
                    raw_text = pre.get_text(separator="\n")
                    source_name = "whois.net"
                    print(f"{C_OK}[+] whois.net → muvaffaqiyat!{C_RESET}\n")
        except Exception as e:
            print(f"{C_WARN}    whois.net xato: {str(e)[:40]}{C_RESET}")

    # 3. whoisjson.com API
    if not raw_text:
        try:
            print(f"{C_INFO}[3/6] whoisjson.com API → sinov...{C_RESET}")
            r = requests.get(f"https://whoisjson.com/api/v1/{domain}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                lines = []
                for k, v in data.items():
                    if isinstance(v, dict):
                        for kk, vv in v.items():
                            lines.append(f"{kk}: {vv}")
                    elif isinstance(v, list):
                        for item in v:
                            lines.append(f"{k}: {item}")
                    else:
                        lines.append(f"{k}: {v}")
                
                if lines:
                    raw_text = "\n".join(lines)
                    source_name = "whoisjson.com (API)"
                    print(f"{C_OK}[+] API orqali olindi!{C_RESET}\n")
        except Exception as e:
            print(f"{C_WARN}    API xato: {str(e)[:40]}{C_RESET}")

    # 4. python-whois → TO'G'RILANGAN!
    if not raw_text:
        try:
            print(f"{C_INFO}[4/6] python-whois → sinov...{C_RESET}")
            import whois
            w = whois.query(domain)
            if w:
                parsed = parse_whois_object(w)
                if parsed and len(parsed) > 50:
                    raw_text = parsed
                    source_name = "python-whois"
                    print(f"{C_OK}[+] python-whois → muvaffaqiyat!{C_RESET}\n")
                else:
                    print(f"{C_WARN}    python-whois ma'lumot qaytarmadi{C_RESET}")
        except Exception as e:
            print(f"{C_WARN}    python-whois xato: {str(e)[:50]}{C_RESET}")

    # 5. whois.pw
    if not raw_text:
        try:
            print(f"{C_INFO}[5/6] whois.pw → sinov...{C_RESET}")
            r = requests.get(f"https://whois.pw/{domain}", headers=headers, timeout=10)
            if "Domain Name" in r.text:
                soup = BeautifulSoup(r.text, "html.parser")
                pre = soup.find("pre")
                if pre:
                    raw_text = pre.get_text(separator="\n")
                    source_name = "whois.pw"
                    print(f"{C_OK}[+] whois.pw → muvaffaqiyat!{C_RESET}\n")
        except Exception as e:
            print(f"{C_WARN}    whois.pw xato: {str(e)[:40]}{C_RESET}")

    # 6. who.is
    if not raw_text:
        try:
            print(f"{C_INFO}[6/6] who.is → sinov...{C_RESET}")
            r = requests.get(f"https://who.is/whois/{domain}", headers=headers, timeout=10)
            if "domain" in r.text.lower():
                soup = BeautifulSoup(r.text, "html.parser")
                pre = soup.find("pre", {"class": "df-raw"})
                if not pre:
                    pre = soup.find("pre")
                if pre:
                    raw_text = pre.get_text(separator="\n")
                    source_name = "who.is"
                    print(f"{C_OK}[+] who.is → muvaffaqiyat!{C_RESET}\n")
        except Exception as e:
            print(f"{C_WARN}    who.is xato: {str(e)[:40]}{C_RESET}")

    if not raw_text:
        print(f"{C_ERR}[!] Barcha manbalar ishlamadi!{C_RESET}")
        print(f"{C_WARN}Ehtimol domen mavjud emas yoki internet muammosi.{C_RESET}")
        input(f"\n{C_WARN}Enter bosib chiqing...{C_RESET}")
        return

    # SPAM FILTR
    cleaned = []
    spam_block = False
    
    for line in raw_text.split("\n"):
        s = line.rstrip()
        l = s.lower()
        
        # Uzun legal spam
        if s.startswith("%") and len(s) > 60:
            if not spam_block:
                cleaned.append("% [Legal notice shortened]")
                spam_block = True
            continue
        
        # Spam kalit so'zlar
        if any(x in l for x in [
            ">>> last update", "terms of use", "uzinfocom", 
            "prohibited without", "rights reserved", "abuse contact"
        ]):
            continue
        
        # Bo'sh qatorlarni o'tkazib yuborish
        if not s.strip():
            continue
        
        cleaned.append(s)

    lines = cleaned if cleaned else raw_text.split("\n")

    # NATIJANI CHOP ETISH
    print(f"{C_TITLE}╔{'═'*100}╗{C_RESET}")
    print(f"{C_TITLE}║{(' WHOIS → ' + domain.upper()):^100}║{C_RESET}")
    print(f"{C_TITLE}╠{'═'*100}╣{C_RESET}")

    registrant_started = False
    ns_count = 0

    for line in lines:
        s = line.rstrip()
        l = s.lower()

        # Name Server (maksimal 6 ta)
        if any(x in l for x in ["name server", "nserver", "dns"]) and "not.defined" not in l:
            if ns_count < 6:
                print(f"{C_TITLE}║{C_RESET} {C_INFO}{s:<98}{C_RESET}{C_TITLE}║{C_RESET}")
                ns_count += 1
            continue

        # Registrant bo'limi
        if any(x in l for x in ["registrant", "owner", "admin", "tech", "billing", "ega"]):
            if not registrant_started:
                print(f"{C_TITLE}╠{'═'*100}╣{C_RESET}")
                print(f"{C_TITLE}║{C_WARN}{' REGISTRANT / OWNER INFO (Privacy Protected) ':^100}{C_RESET}{C_TITLE}║{C_RESET}")
                registrant_started = True
            print(f"{C_TITLE}║{C_RESET}   {s:<96}{C_RESET}{C_TITLE}║{C_RESET}")
            continue

        # Asosiy ma'lumotlar
        if any(k in l for k in [
            "domain name", "registrar", "creation", "expiration", 
            "updated", "status", "whois", "referral"
        ]):
            print(f"{C_TITLE}║{C_RESET} {C_INFO}{s:<98}{C_RESET}{C_TITLE}║{C_RESET}")
        else:
            # Oddiy satrlar
            if s.strip() and not s.startswith("%"):
                print(f"{C_TITLE}║{C_RESET} {s:<98}{C_RESET}{C_TITLE}║{C_RESET}")

    print(f"{C_TITLE}╚{'═'*100}╝{C_RESET}")
    print(f"\n{C_OK}✓ WHOIS muvaffaqiyatli olindi → {C_INFO}{domain.upper()}{C_RESET}")

    # <<< YANGI >>> FAYLGA SAQLASH – reports/papka ichiga
    reports_dir = "reports/information_gathering/passive/whois"
    os.makedirs(reports_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"whois_{domain}_{ts}.txt"
    filepath = os.path.join(reports_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"WHOIS LOOKUP REPORT\n")
            f.write(f"Domain: {domain.upper()}\n")
            f.write(f"Source: {source_name}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")
            f.write("\n".join(lines))
        
        relative_path = f"reports/information_gathering/passive/whois/{filename}"
        print(f"{C_OK}[+] Hisobot saqlandi → {C_INFO}{relative_path}{C_RESET}\n")
    except Exception as e:
        print(f"{C_WARN}Faylga saqlashda xato: {e}{C_RESET}\n")

    input(f"{C_WARN}Enter bosib davom eting...{C_RESET}")

if __name__ == "__main__":
    run_whois()