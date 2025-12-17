# app/information_gathering/passive/dns_lookup.py
# DNS LOOKUP v2.0 — A, AAAA, MX, NS, TXT, CNAME, SOA + DMARC + Jadval + Rang

import os
import sys
import dns.resolver
from datetime import datetime

# ProbeSuite yo‘lini qo‘shish
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, BASE_DIR)

from app.config import C_OK, C_WARN, C_ERR, C_RESET, C_INFO, C_TITLE, REPORTS_DIR
from app.utils import Logger, clear_screen


class DNSLookup:
    def __init__(self):
        self.domain = ""
        self.results = {}

    def banner(self):
        clear_screen()
        print(f"{C_TITLE}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                              DNS LOOKUP v2.0                                 ║")
        print("║                     A • MX • NS • TXT • CNAME • SOA • DMARC                  ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C_RESET}")

    def lookup(self, domain):
        self.domain = domain.strip().lower()
        if self.domain.startswith(("http://", "https://")):
            self.domain = self.domain.split("//")[-1].split("/")[0]

        self.banner()
        print(f"{C_INFO}[*] DNS so‘rovlari yuborilmoqda → {self.domain}{C_RESET}\n")

        # Har bir turdagi recordni alohida tekshirish
        self.query_records('A', "A RECORDS (IPv4)")
        self.query_records('AAAA', "AAAA RECORDS (IPv6)")
        self.query_records('MX', "MX RECORDS (Mail Servers)", sort_key=lambda x: x.preference)
        self.query_records('NS', "NS RECORDS (Nameservers)")
        self.query_records('TXT', "TXT RECORDS (SPF, DKIM, DMARC)")
        self.query_records('CNAME', "CNAME RECORDS")
        self.query_records('SOA', "SOA RECORDS")

        # DMARC alohida
        self.check_dmarc()

        self.display_results()
        self.save_report()

    def query_records(self, rtype, title, sort_key=None):
        try:
            answers = dns.resolver.resolve(self.domain, rtype)
            records = []
            for rdata in answers:
                if rtype == 'MX':
                    records.append(f"Priority: {rdata.preference} → {rdata.exchange}")
                elif rtype == 'SOA':
                    records.append({
                        'mname': str(rdata.mname),
                        'rname': str(rdata.rname),
                        'serial': rdata.serial,
                        'refresh': rdata.refresh,
                        'retry': rdata.retry,
                        'expire': rdata.expire,
                        'minimum': rdata.minimum
                    })
                else:
                    records.append(str(rdata).rstrip('.'))
            if sort_key:
                records.sort(key=sort_key)
            self.results[title] = records
        except Exception as e:
            self.results[title] = ["Not Found"]

    def check_dmarc(self):
        try:
            dmarc_records = dns.resolver.resolve(f"_dmarc.{self.domain}", 'TXT')
            for rdata in dmarc_records:
                txt = str(rdata)
                if "v=DMARC" in txt:
                    self.results["DMARC POLICY"] = [txt]
                    return
            self.results["DMARC POLICY"] = ["No DMARC record"]
        except:
            self.results["DMARC POLICY"] = ["No DMARC record"]
    def display_results(self):
        width = 98
        border = "╔═╦═╣╠╩╚╗║"  # Rang ishlatmaymiz bu yerda

        print(f"{C_TITLE}╔{'═' * width}╗{C_RESET}")
        print(f"{C_TITLE}║{C_RESET}{C_INFO} {'DNS LOOKUP NATIJALARI':^96} {C_RESET}{C_TITLE}║{C_RESET}")
        print(f"{C_TITLE}╠{'═' * width}╣{C_RESET}")

        for i, (title, records) in enumerate(self.results.items()):
            # Sarlavha — faqat ichki qism rangli
            print(f"{C_TITLE}║{C_RESET} {C_INFO}{title:<96}{C_RESET} {C_TITLE}║{C_RESET}")

            if not records or records == ["Not Found"] or ("No DMARC" in str(records[0])):
                color = C_WARN if "DMARC" in title else C_ERR
                print(f"{C_TITLE}║{C_RESET}   → {color}Not Found{C_RESET}{' ' * 82}{C_TITLE}║{C_RESET}")
            else:
                for record in records[:15]:
                    if isinstance(record, dict):
                        print(f"{C_TITLE}║{C_RESET}   Primary NS   : {C_OK}{record['mname']:<79}{C_RESET} {C_TITLE}║{C_RESET}")
                        print(f"{C_TITLE}║{C_RESET}   Admin Email  : {C_OK}{record['rname']:<79}{C_RESET} {C_TITLE}║{C_RESET}")
                        print(f"{C_TITLE}║{C_RESET}   Serial       : {C_OK}{str(record['serial']):<79}{C_RESET} {C_TITLE}║{C_RESET}")
                    else:
                        # SPF, DKIM, DMARC, MX uchun yashil rang
                        color = C_OK if any(x in record.lower() for x in ["v=spf", "v=dmarc", "priority"]) else C_INFO
                        line = record[:88]
                        if len(record) > 88:
                            line += "..."
                        print(f"{C_TITLE}║{C_RESET}   → {color}{line:<88}{C_RESET} {C_TITLE}║{C_RESET}")

                if len(records) > 15:
                    print(f"{C_TITLE}║{C_RESET}   → {C_WARN}... va yana {len(records)-15} ta record{C_RESET}{' ' * 60}{C_TITLE}║{C_RESET}")

            # Har bir bo‘limdan keyin chiziq (oxirgisidan tashqari)
            if i < len(self.results) - 1:
                print(f"{C_TITLE}╠{'═' * width}╣{C_RESET}")

        print(f"{C_TITLE}╚{'═' * width}╝{C_RESET}")
        print(f"\n{C_OK}DNS Lookup muvaffaqiyatli yakunlandi!{C_RESET}\n")

    def save_report(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"information_gathering/dns_lookup/dns_lookup_{self.domain}_{timestamp}.txt"
        path = os.path.join(REPORTS_DIR, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"DNS LOOKUP REPORT - {self.domain.upper()}\n")
            f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            for title, records in self.results.items():
                f.write(f"{title}:\n")
                if not records or records == ["Not Found"]:
                    f.write("  → Not Found\n")
                else:
                    for r in records:
                        if isinstance(r, dict):
                            f.write(f"  Primary NS: {r['mname']}\n")
                            f.write(f"  Admin: {r['rname']}\n")
                        else:
                            f.write(f"  → {r}\n")
                f.write("\n")

        print(f"\n{C_OK}[+] Report saqlandi → {C_INFO}{filename}{C_RESET}")

    def run(self, target):
        self.lookup(target)
        input(f"\n{C_WARN}Press Enter to continue...{C_RESET}")


# ───────────────────────────────────────
def run_dns_lookup(target=""):
    if not target:
        target = input(f"{C_INFO}Domen kiriting (masalan: google.com): {C_RESET}").strip()
    DNSLookup().run(target)


if __name__ == "__main__":
    run_dns_lookup()