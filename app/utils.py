#!/usr/bin/env python3
# app/utils.py - ProbeSuite Utilities
import os
import subprocess
import json
import shutil
import re
from datetime import datetime
from pathlib import Path

try:
    from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET, REPORTS_DIR
except ImportError:
    # Fallback agar import ishlamasa
    from config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET, REPORTS_DIR


class Logger:
    """Logging utility"""
    
    @staticmethod
    def success(msg):
        print(f"{C_OK}[+] {msg}{C_RESET}")
    
    @staticmethod
    def error(msg):
        print(f"{C_ERR}[!] {msg}{C_RESET}")
    
    @staticmethod
    def warning(msg):
        print(f"{C_WARN}[~] {msg}{C_RESET}")
    
    @staticmethod
    def info(msg):
        print(f"{C_INFO}[*] {msg}{C_RESET}")
    
    @staticmethod
    def debug(msg):
        print(f"{C_INFO}[DEBUG] {msg}{C_RESET}")


class CommandRunner:
    """External command runner"""

    @staticmethod
    def check_tool(tool_name):
        """Tool o'rnatilganligini tekshiradi"""
        return shutil.which(tool_name) is not None
    
    @staticmethod
    def run(cmd, shell=False, timeout=300):
        """
        Komandasini ishlat
        Return: (returncode, stdout, stderr)
        """
        try:
            if isinstance(cmd, str) and not shell:
                cmd = cmd.split()
            
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            Logger.error(f"Command timeout: {cmd}")
            return -1, "", "Timeout"
        except FileNotFoundError:
            Logger.error(f"Command not found: {cmd}")
            return -1, "", "Command not found"
        except Exception as e:
            Logger.error(f"Command error: {e}")
            return -1, "", str(e)
    
    @staticmethod
    def run_live(cmd, shell=False):
        """
        Komandani live output bilan ishlat
        """
        try:
            if isinstance(cmd, str) and not shell:
                cmd = cmd.split()
            
            process = subprocess.Popen(
                cmd,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Real-time output
            for line in process.stdout:
                print(line, end='')
            
            process.wait()
            return process.returncode
        except Exception as e:
            Logger.error(f"Command error: {e}")
            return -1


class URLValidator:
    """URL validation"""
    
    @staticmethod
    def format_url(url):
        """URLni formatlash"""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            # Default https
            url = 'https://' + url
        return url
    
    @staticmethod
    def extract_domain(url):
        """URL dan domain olish"""
        url = URLValidator.format_url(url)
        # Remove protocol
        domain = url.split('//')[1] if '//' in url else url
        # Remove path
        domain = domain.split('/')[0]
        # Remove port
        domain = domain.split(':')[0]
        return domain
    
    @staticmethod
    def is_valid_url(url):
        """URL validligini tekshirish"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    @staticmethod
    def is_valid_domain(domain):
        """Domain validligini tekshirish"""
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9]'  # First character
            r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)'  # Sub domains
            r'+[a-zA-Z]{2,}$'  # TLD
        )
        return domain_pattern.match(domain) is not None
    
    @staticmethod
    def is_valid_ip(ip):
        """IP address validligini tekshirish"""
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not ip_pattern.match(ip):
            return False
        # Check octets
        octets = ip.split('.')
        return all(0 <= int(octet) <= 255 for octet in octets)


# utils.py dagi ReportWriter klasini BU KOD BILAN almashtiring:

class ReportWriter:
    """Report yazish"""
    
    @staticmethod
    def save_json(filename, data, subfolder=None):
        """JSON report"""
        if subfolder:
            report_path = os.path.join(REPORTS_DIR, subfolder)
        else:
            report_path = REPORTS_DIR
            
        Path(report_path).mkdir(parents=True, exist_ok=True)
        filepath = os.path.join(report_path, f"{filename}.json")
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        Logger.success(f"Report saved: {filepath}")
        return filepath
    
    @staticmethod
    def save_txt(filename, content, subfolder=None):
        """Text report"""
        if subfolder:
            report_path = os.path.join(REPORTS_DIR, subfolder)
        else:
            report_path = REPORTS_DIR
            
        Path(report_path).mkdir(parents=True, exist_ok=True)
        filepath = os.path.join(report_path, f"{filename}.txt")
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        Logger.success(f"Report saved: {filepath}")
        return filepath
    
    @staticmethod
    def get_timestamp():
        """Timestamp olish"""
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    @staticmethod
    def create_report_header(title, target):
        """Report header yaratish"""
        header = "=" * 80 + "\n"
        header += f"{title}\n"
        header += "=" * 80 + "\n"
        header += f"Target: {target}\n"
        header += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "=" * 80 + "\n\n"
        return header


class InputValidator:
    """Input validation"""
    
    @staticmethod
    def get_url():
        """URL so'rash"""
        while True:
            url = input(f"{C_INFO}Enter URL: {C_RESET}").strip()
            if not url:
                Logger.error("URL cannot be empty!")
                if input(f"{C_WARN}Try again? (y/n): {C_RESET}").lower() != 'y':
                    return None
                continue
            
            url = URLValidator.format_url(url)
            if URLValidator.is_valid_url(url):
                return url
            else:
                Logger.error("Invalid URL format!")
                if input(f"{C_WARN}Try again? (y/n): {C_RESET}").lower() != 'y':
                    return None
    
    @staticmethod
    def get_domain():
        """Domain so'rash"""
        while True:
            domain = input(f"{C_INFO}Enter domain: {C_RESET}").strip()
            if not domain:
                Logger.error("Domain cannot be empty!")
                if input(f"{C_WARN}Try again? (y/n): {C_RESET}").lower() != 'y':
                    return None
                continue
            
            # Remove protocol if present
            if domain.startswith(('http://', 'https://')):
                domain = URLValidator.extract_domain(domain)
            
            if URLValidator.is_valid_domain(domain) or URLValidator.is_valid_ip(domain):
                return domain
            else:
                Logger.error("Invalid domain format!")
                if input(f"{C_WARN}Try again? (y/n): {C_RESET}").lower() != 'y':
                    return None
    
    @staticmethod
    def get_ip():
        """IP so'rash"""
        while True:
            ip = input(f"{C_INFO}Enter IP address or domain: {C_RESET}").strip()
            if not ip:
                Logger.error("IP/domain cannot be empty!")
                if input(f"{C_WARN}Try again? (y/n): {C_RESET}").lower() != 'y':
                    return None
                continue
            
            # IP, domain yoki CIDR bo'lishi mumkin
            if (URLValidator.is_valid_ip(ip) or 
                URLValidator.is_valid_domain(ip) or 
                '/' in ip):  # CIDR notation
                return ip
            else:
                Logger.error("Invalid IP/domain format!")
                if input(f"{C_WARN}Try again? (y/n): {C_RESET}").lower() != 'y':
                    return None
    
    @staticmethod
    def get_choice():
        """Tanlov so'rash"""
        choice = input(f"{C_INFO}She11> {C_RESET}").strip()
        return choice
    
    @staticmethod
    def confirm(message="Continue?"):
        """Tasdiqlash"""
        response = input(f"{C_WARN}{message} (y/n): {C_RESET}").strip().lower()
        return response in ['y', 'yes']


def pause(msg="Press Enter to continue..."):
    """Pauza qilish"""
    input(f"{C_WARN}{msg}{C_RESET}")


def clear_screen():
    """Ekranni tozalash"""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(title, width=80):
    """Sarlavha chop etish"""
    print(f"\n{C_OK}{'='*width}")
    print(f"{title.center(width)}")
    print(f"{'='*width}{C_RESET}\n")


def print_footer(width=80):
    """Pastki qator chop etish"""
    print(f"\n{C_OK}{'='*width}{C_RESET}\n")


def print_separator(width=80):
    """Separator chop etish"""
    print(f"{C_WARN}{'-'*width}{C_RESET}")


def format_bytes(bytes_num):
    """Bytes ni human-readable formatga o'tkazish"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"


def get_file_size(filepath):
    """File hajmini olish"""
    try:
        return os.path.getsize(filepath)
    except:
        return 0