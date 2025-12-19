import os
import subprocess
import socket
import threading
import time
import re
from datetime import datetime
from app.utils import Logger
from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET, C_TITLE


# =================================================================
#   DEPENDENCY CHECKER & AUTO-INSTALLER
# =================================================================

def check_dirsearch_dependencies():
    """Dirsearch dependencylarini tekshiradi va avtomatik o'rnatadi"""
    
    print(f"{C_INFO}[*] Dependencies tekshirilmoqda...{C_RESET}")
    
    dirsearch_dir = "/home/kaniel/ProbeSuite/tools/dirsearch"
    requirements_file = f"{dirsearch_dir}/requirements.txt"
    
    if not os.path.isfile(requirements_file):
        print(f"{C_WARN}[!] requirements.txt topilmadi{C_RESET}")
        return
    
    try:
        # Muhim kutubxonalarni tekshirish
        critical_deps = ['defusedxml', 'jinja2', 'colorama', 'requests']
        missing = []
        
        for dep in critical_deps:
            try:
                __import__(dep.replace('-', '_'))
            except ImportError:
                missing.append(dep)
        
        if missing:
            print(f"{C_WARN}[!] Yo'q kutubxonalar: {', '.join(missing)}{C_RESET}")
            print(f"{C_INFO}[*] Avtomatik o'rnatilmoqda...{C_RESET}")
            
            # pip install
            result = subprocess.run(
                ["pip3", "install", "-q"] + missing,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"{C_OK}[+] Muvaffaqiyatli o'rnatildi!{C_RESET}\n")
            else:
                print(f"{C_ERR}[!] O'rnatishda xatolik:{C_RESET}")
                print(f"{C_INFO}    Qo'lda bajaring: pip3 install {' '.join(missing)}{C_RESET}\n")
        else:
            print(f"{C_OK}[+] Barcha dependencylar mavjud{C_RESET}\n")
            
    except Exception as e:
        print(f"{C_ERR}[!] Dependency check xatosi: {e}{C_RESET}\n")


# =================================================================
#   WORDLIST SELECTION
# =================================================================

def get_best_wordlist():
    """Eng yaxshi wordlist topadi"""
    
    print(f"{C_INFO}[*] Wordlist qidirilmoqda...{C_RESET}")
    
    wordlist_priority = [
        "/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt",
        "/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt",
        "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt",
        "/usr/share/seclists/Discovery/Web-Content/common.txt",
        "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
        "/usr/share/dirb/wordlists/common.txt",
    ]
    
    for wl_path in wordlist_priority:
        if os.path.isfile(wl_path):
            size_mb = os.path.getsize(wl_path) / (1024 * 1024)
            lines = sum(1 for _ in open(wl_path, 'rb'))
            
            print(f"{C_OK}[+] Topildi → {os.path.basename(wl_path)}{C_RESET}")
            print(f"{C_INFO}    Hajmi: {size_mb:.2f} MB | So'zlar: {lines:,}{C_RESET}")
            return wl_path
    
    print(f"{C_ERR}[!] Wordlist topilmadi!{C_RESET}")
    exit(1)


# =================================================================
#   MANUAL CONNECTIVITY TEST
# =================================================================

def test_target_connectivity(target):
    """Targetni tekshiradi va oddiy yo'llarni sinab ko'radi"""
    
    print(f"\n{C_INFO}[*] Target tekshirilmoqda...{C_RESET}")
    
    test_paths = ['/', '/admin', '/login', '/api', '/dashboard', '/config', '/robots.txt']
    
    try:
        import requests
        requests.packages.urllib3.disable_warnings()
        
        results = []
        for path in test_paths:
            url = f"{target}{path}"
            try:
                resp = requests.get(
                    url, 
                    timeout=8, 
                    allow_redirects=False,
                    verify=False,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                
                if resp.status_code not in [404, 500]:
                    color = C_OK if resp.status_code == 200 else C_WARN
                    print(f"{color}  [+] [{resp.status_code}] {path}{C_RESET}")
                    results.append((path, resp.status_code))
                else:
                    print(f"{C_INFO}  [-] [{resp.status_code}] {path}{C_RESET}")
                    
            except Exception as e:
                print(f"{C_ERR}  [!] {path} → {str(e)[:50]}{C_RESET}")
        
        print()
        return results
        
    except ImportError:
        print(f"{C_WARN}[!] requests kutubxonasi yo'q, test o'tkazib yuborildi{C_RESET}\n")
        return []


# =================================================================
#   DIRSEARCH RUNNER - PRODUCTION MODE
# =================================================================

def run_dirsearch_scanner(target_input: str):
    """Dirsearch - to'liq ishlaydigan versiya"""
    
    # 1. Dependencylarni tekshirish
    check_dirsearch_dependencies()
    
    # 2. Target tayyorlash
    target = target_input.strip().rstrip("/")
    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    # 3. IP aniqlash
    try:
        hostname = target.replace("https://", "").replace("http://", "").split("/")[0]
        ip = socket.gethostbyname(hostname)
    except:
        ip = "unknown"

    # 4. Wordlist olish
    wordlist = get_best_wordlist()
    
    # 5. Manual connectivity test
    manual_results = test_target_connectivity(target)

    # 6. Report file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r"[^\w\-.]", "_", target.split("://")[-1])
    
    output_dir = "reports/information_gathering/active/dirsearch"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/{safe_name}_{timestamp}.txt"

    # =============================================================
    #  DIRSEARCH COMMAND - OPTIMIZED
    # =============================================================
    
    cmd = [
        "python3", "/home/kaniel/ProbeSuite/tools/dirsearch/dirsearch.py",
        "-u", target,
        "-w", wordlist,
        "-e", "php,html,htm,js,txt,zip,bak,sql,json,xml,asp,aspx,jsp",
        "--recursive",
        "--max-recursion-depth", "1",
        "--random-agent",
        "--follow-redirects",
        "-t", "30",                       # 30 threads
        "--max-rate", "200",              # 200 req/sec
        "--timeout", "20",
        "--retries", "2",
        "--header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "--exclude-status", "404,400,500,502,503",
        "--exclude-sizes", "0B",
        "--format", "plain",
        "--output", output_file
    ]

    # =============================================================
    #  BANNER
    # =============================================================
    
    print(f"{C_TITLE}╔{'═' * 82}╗{C_RESET}")
    print(f"{C_TITLE}║{'  DIRSEARCH — WEB DIRECTORY SCANNER  ':^82}║{C_RESET}")
    print(f"{C_TITLE}╚{'═' * 82}╝{C_RESET}\n")

    print(f"{C_INFO} Target      :{C_RESET} {C_OK}{target}{C_RESET}")
    print(f"{C_INFO} IP Address  :{C_RESET} {C_WARN}{ip}{C_RESET}")
    print(f"{C_INFO} Wordlist    :{C_RESET} {os.path.basename(wordlist)}")
    print(f"{C_INFO} Mode        :{C_RESET} Balanced (30 threads, 200 req/s)")
    print(f"{C_INFO} Output      :{C_RESET} {output_file}\n")

    # =============================================================
    #  PROGRESS TRACKER
    # =============================================================
    
    found_count = len(manual_results)  # Manual testdan topilganlar
    request_count = 0
    stop_spinner = threading.Event()

    def spinner():
        spins = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while not stop_spinner.is_set():
            print(
                f"\r{C_INFO}[{spins[i % len(spins)]}] Requests: {request_count:,} | "
                f"Found: {C_OK}{found_count}{C_RESET}   ",
                end="", flush=True
            )
            time.sleep(0.08)
            i += 1

    threading.Thread(target=spinner, daemon=True).start()

    # =============================================================
    #  RUN DIRSEARCH
    # =============================================================
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        with open(output_file, "w", encoding="utf-8") as f:
            # Header
            f.write(f"{'='*80}\n")
            f.write(f"DIRSEARCH SCAN REPORT\n")
            f.write(f"{'='*80}\n")
            f.write(f"Target    : {target}\n")
            f.write(f"IP        : {ip}\n")
            f.write(f"Wordlist  : {wordlist}\n")
            f.write(f"Timestamp : {datetime.now()}\n")
            f.write(f"{'='*80}\n\n")
            
            # Manual test natijalari
            if manual_results:
                f.write("MANUAL TEST RESULTS:\n")
                for path, status in manual_results:
                    f.write(f"  [{status}] {path}\n")
                f.write("\n")

            # Dirsearch natijalari
            for line in process.stdout:
                line = line.strip()
                
                # Request counter
                if any(x in line for x in ["Testing:", "Scanning:", "Target:"]):
                    request_count += 1
                
                # Status detection
                status_match = re.search(r'\[(\d{3})\]', line)
                if status_match:
                    status = status_match.group(1)
                    
                    if status not in ['404', '500']:
                        # Check if already found in manual test
                        is_duplicate = any(
                            path in line for path, _ in manual_results
                        )
                        
                        if not is_duplicate:
                            found_count += 1
                        
                        # Color coding
                        if status.startswith('2'):
                            color = C_OK
                        elif status.startswith('3'):
                            color = C_WARN
                        else:
                            color = C_INFO
                        
                        dup_mark = " (manual)" if is_duplicate else ""
                        print(f"\n{color}[+] {line}{dup_mark}{C_RESET}")
                        f.write(f"[+] {line}\n")
                        f.flush()

        process.wait()

    except KeyboardInterrupt:
        print(f"\n\n{C_WARN}[!] Scan to'xtatildi (Ctrl+C){C_RESET}")
        try:
            process.terminate()
            process.wait(timeout=3)
        except:
            process.kill()
        
    except Exception as e:
        print(f"\n{C_ERR}[!] XATOLIK: {e}{C_RESET}")

    finally:
        stop_spinner.set()
        time.sleep(0.2)
        print("\n")

    # =============================================================
    #  FINAL REPORT
    # =============================================================

    if found_count == 0:
        status_color = C_WARN
        status_msg = "⚠️  Hech narsa topilmadi"
    elif found_count < 5:
        status_color = C_INFO
        status_msg = f"ℹ️  {found_count} ta yo'l"
    else:
        status_color = C_OK
        status_msg = f"✅ {found_count} ta yo'l topildi!"

    print(f"{C_TITLE}╔{'═' * 82}╗{C_RESET}")
    print(f"{C_TITLE}║{' SCAN YAKUNLANDI ':^82}║{C_RESET}")
    print(f"{C_TITLE}╚{'═' * 82}╝{C_RESET}\n")

    print(f"{C_INFO} Target       :{C_RESET} {target}")
    print(f"{C_INFO} IP           :{C_RESET} {ip}")
    print(f"{C_INFO} Status       :{C_RESET} {status_color}{status_msg}{C_RESET}")
    print(f"{C_INFO} Scanned      :{C_RESET} {request_count:,} paths")
    print(f"{C_INFO} Wordlist     :{C_RESET} {os.path.basename(wordlist)}")
    print(f"{C_INFO} Report       :{C_RESET} {output_file}")

    print(f"\n{C_TITLE}╘{'═' * 82}╛{C_RESET}\n")

    # Tahlil
    if found_count == 0:
        print(f"{C_WARN}EHTIMOLIY SABABLAR:{C_RESET}")
        print(f"{C_INFO}  1. WAF/CDN himoyasi (CloudFlare, Akamai){C_RESET}")
        print(f"{C_INFO}  2. JavaScript SPA (React/Vue/Angular){C_RESET}")
        print(f"{C_INFO}  3. Minimal API endpoints{C_RESET}\n")
        
        print(f"{C_OK}TAVSIYALAR:{C_RESET}")
        print(f"{C_INFO}  • Boshqa toollar: Gobuster, Feroxbuster{C_RESET}")
        print(f"{C_INFO}  • API endpoints: /api/v1, /graphql{C_RESET}")
        print(f"{C_INFO}  • Sitemap: /sitemap.xml{C_RESET}\n")

    if found_count > 0:
        print(f"{C_OK}[✓] Hisobotni ko'rish:{C_RESET}")
        print(f"{C_INFO}    cat {output_file}{C_RESET}\n")

    Logger.success(f"Dirsearch → {target} | {found_count} yo'l topildi")

    input(f"{C_INFO}Davom etish uchun Enter...{C_RESET}")


if __name__ == "__main__":
    run_dirsearch_scanner("example.uz")