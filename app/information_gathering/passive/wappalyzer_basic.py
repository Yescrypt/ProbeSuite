# app/information_gathering/passive/wappalyzer_basic.py
# Oddiy regex asosidagi Wappalyzer — kutubxona ishlamasa ishlaydi
# Reports → reports/passive/wappalyzer/wappalyzer_basic_domain_YYYYMMDD_HHMMSS.txt

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, USER_AGENT
from app.utils import Logger
import requests
import re
import os
from datetime import datetime
from urllib.parse import urlparse


def run_wappalyzer_basic(url: str):
    """Oddiy regex asosidagi Wappalyzer — kutubxona ishlamasa ishlaydi"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"\n{C_WARN}[~] Kutubxona ishlamadi → Oddiy regex skaner ishga tushdi{C_RESET}\n")

    # <<< YANGI >>> Reports papkasi
    reports_dir = "reports/information_gathering/passive/wappalyzer"
    os.makedirs(reports_dir, exist_ok=True)

    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, timeout=15, headers=headers, verify=False)
        content = response.text.lower()
        headers_str = str(response.headers).lower()

        techs = []

        patterns = {
            "Nginx": [r"nginx[/\s]?([\d\.]+)?", r"server: nginx"],
            "Apache": [r"apache[/\s]?([\d\.]+)?"],
            "Cloudflare": [r"cloudflare", r"cf-ray"],
            "Bootstrap": [r"bootstrap.*\.(css|js)", r"bootstrap"],
            "jQuery": [r"jquery.*\.js", r"jquery"],
            "WordPress": [r"wp-content", r"wp-includes", r"wp-json"],
            "Django": [r"django", r"csrftoken", r"sessionid"],
            "Python": [r"python[\s]?([\d\.]+)", r"powered by python"],
            "Ubuntu": [r"ubuntu", r"linux", r"x-powered-by.*ubuntu"],
            "Google Font API": [r"fonts\.googleapis\.com", r"fonts\.gstatic\.com"],
            "Font Awesome": [r"font.?awesome", r"fa-"],
            "React": [r"react.*\.js", r"react-dom"],
            "Vue.js": [r"vue.*\.js"],
        }

        for name, pats in patterns.items():
            for p in pats:
                if re.search(p, content) or re.search(p, headers_str):
                    version = None
                    m = re.search(r"([\d]+\.[\d\.]+)", p if "version" in p else content + headers_str)
                    if m:
                        version = m.group(1)
                    techs.append(f"{name}{' ' + version if version else ''}")
                    break

        print(f"{C_OK}Topildi → {len(techs)} ta texnologiya (oddiy usul):{C_RESET}")
        for t in techs:
            print(f"   • {t}")

        # Report saqlash → reports/passive/wappalyzer
        domain = urlparse(url).netloc
        safe_domain = re.sub(r'[^\w\-]', '_', domain)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wappalyzer_basic_{safe_domain}_{timestamp}.txt"
        path = os.path.join(reports_dir, filename)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Basic Wappalyzer Report\n")
            f.write(f"URL: {url}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            for t in techs:
                f.write(f"• {t}\n")

        print(f"\n{C_INFO}Saqlandi → {path}{C_RESET}")

    except Exception as e:
        print(f"{C_ERR}Hatto oddiy skaner ham ishlamadi: {e}{C_RESET}")