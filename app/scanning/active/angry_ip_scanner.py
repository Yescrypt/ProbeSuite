#!/usr/bin/env python3
"""
ProBeSuite - Angry IP Scanner Launcher
Fast and friendly network scanner
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET
from app.utils import Logger, CommandRunner, InputValidator, clear_screen, pause


class AngryIPLauncher:
    def __init__(self):
        self.installed = False
        self.command = None
        self.detect_command()
    
    def detect_command(self):
        """Detect Angry IP Scanner command"""
        possible_commands = [
            'ipscan',           # Linux package
            'angry-ip-scanner', # Alternative name
            'angryip',          # Alternative name
            'ipscan.exe',       # Windows
        ]
        
        for cmd in possible_commands:
            if CommandRunner.check_tool(cmd):
                self.command = cmd
                self.installed = True
                return
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║         😠 ANGRY IP SCANNER - NETWORK SCANNER 😠             ║
║          Fast and Friendly Network IP Scanner                ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(f"{C_INFO}{banner}{C_RESET}")
    
    def show_main_menu(self):
        menu = """
╭─ ANGRY IP SCANNER ────────────────────────────────────────────╮
│                                                               │
│  LAUNCH OPTIONS:                                              │
│    [1]  Launch Angry IP Scanner (GUI)                         │
│    [2]  Quick Scan - Local Network                            │
│    [3]  Scan Custom IP Range                                  │
│    [4]  Scan from File                                        │
│                                                               │
│  CONFIGURATION:                                               │
│    [5]  About Angry IP Scanner                                │
│    [6]  Installation Guide                                    │
│    [7]  Features Overview                                     │
│    [8]  Tips & Tricks                                         │
│                                                               │
│  ALTERNATIVES:                                                │
│    [9]  Launch Nmap GUI Alternative                           │
│    [10] Use Built-in Network Scanner                          │
│                                                               │
│  [0]  ← Back                                                  │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
        """
        print(f"{C_OK}{menu}{C_RESET}")
    
    def show_installation_guide(self):
        """Display installation instructions"""
        print(f"\n{C_INFO}╭─ ANGRY IP SCANNER INSTALLATION GUIDE ────────────────╮{C_RESET}")
        
        os_type = platform.system()
        
        print(f"\n{C_INFO}Detected OS: {os_type}{C_RESET}\n")
        
        if os_type == "Linux":
            print(f"{C_OK}For Debian/Ubuntu/Kali:{C_RESET}")
            print(f"  1. Download .deb package:")
            print(f"     wget https://github.com/angryip/ipscan/releases/download/3.9.1/ipscan_3.9.1_amd64.deb")
            print(f"  2. Install:")
            print(f"     sudo dpkg -i ipscan_3.9.1_amd64.deb")
            print(f"  3. Fix dependencies if needed:")
            print(f"     sudo apt --fix-broken install")
            
            print(f"\n{C_OK}For Fedora/RedHat/CentOS:{C_RESET}")
            print(f"  1. Download .rpm package:")
            print(f"     wget https://github.com/angryip/ipscan/releases/download/3.9.1/ipscan-3.9.1-1.x86_64.rpm")
            print(f"  2. Install:")
            print(f"     sudo rpm -i ipscan-3.9.1-1.x86_64.rpm")
            
            print(f"\n{C_OK}Universal (Java required):{C_RESET}")
            print(f"  1. Install Java:")
            print(f"     sudo apt install default-jre")
            print(f"  2. Download JAR:")
            print(f"     wget https://github.com/angryip/ipscan/releases/download/3.9.1/ipscan-3.9.1.jar")
            print(f"  3. Run:")
            print(f"     java -jar ipscan-3.9.1.jar")
        
        elif os_type == "Windows":
            print(f"{C_OK}For Windows:{C_RESET}")
            print(f"  1. Download installer:")
            print(f"     https://github.com/angryip/ipscan/releases/download/3.9.1/ipscan-3.9.1-setup.exe")
            print(f"  2. Run the installer")
            print(f"  3. Follow installation wizard")
        
        elif os_type == "Darwin":  # macOS
            print(f"{C_OK}For macOS:{C_RESET}")
            print(f"  1. Download DMG:")
            print(f"     https://github.com/angryip/ipscan/releases/download/3.9.1/ipscan-3.9.1.dmg")
            print(f"  2. Open DMG and drag to Applications")
            print(f"  3. Run from Applications")
        
        print(f"\n{C_INFO}Official Website:{C_RESET}")
        print(f"  https://angryip.org")
        
        print(f"\n{C_INFO}GitHub Repository:{C_RESET}")
        print(f"  https://github.com/angryip/ipscan")
        
        print(f"\n{C_INFO}System Requirements:{C_RESET}")
        print(f"  • Java Runtime Environment (JRE) 11 or newer")
        print(f"  • Windows 7+, Linux, or macOS 10.14+")
        
        print(f"\n{C_INFO}╰──────────────────────────────────────────────────────╯{C_RESET}")
    
    def launch_gui(self):
        """Launch Angry IP Scanner GUI"""
        Logger.info("Launching Angry IP Scanner...")
        
        if not self.installed:
            Logger.error("Angry IP Scanner not found!")
            Logger.info("Please install it first")
            return False
        
        try:
            # Launch in background
            subprocess.Popen([self.command], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            Logger.success("Angry IP Scanner launched successfully!")
            Logger.info("The application is running in the background")
            return True
            
        except Exception as e:
            Logger.error(f"Failed to launch: {e}")
            
            # Try with java -jar
            jar_paths = [
                'ipscan.jar',
                '/usr/share/ipscan/ipscan.jar',
                str(Path.home() / 'Downloads' / 'ipscan.jar')
            ]
            
            for jar_path in jar_paths:
                if os.path.exists(jar_path):
                    Logger.info(f"Trying to launch with Java: {jar_path}")
                    try:
                        subprocess.Popen(['java', '-jar', jar_path],
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL)
                        Logger.success("Launched with Java!")
                        return True
                    except:
                        continue
            
            return False
    
    def quick_scan_local(self):
        """Quick scan of local network"""
        Logger.info("Quick Local Network Scan")
        
        # Detect local network
        Logger.info("Detecting local network...")
        
        try:
            # Get local IP
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Calculate network range
            ip_parts = local_ip.split('.')
            network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
            
            Logger.info(f"Local IP: {local_ip}")
            Logger.info(f"Network Range: {network}")
            
            print(f"\n{C_INFO}This will scan: {network}{C_RESET}")
            
            if self.installed:
                Logger.info("Launching Angry IP Scanner with this range...")
                Logger.info("Please enter the range in the GUI")
                self.launch_gui()
            else:
                Logger.warning("Angry IP Scanner not installed")
                Logger.info("Using Nmap instead...")
                
                if CommandRunner.check_tool('nmap'):
                    cmd = f"nmap -sn {network}"
                    Logger.info(f"Command: {cmd}")
                    pause("Press Enter to start...")
                    os.system(cmd)
                else:
                    Logger.error("Nmap also not found!")
        
        except Exception as e:
            Logger.error(f"Failed to detect network: {e}")
    
    def scan_custom_range(self):
        """Scan custom IP range"""
        print(f"\n{C_INFO}Enter IP range to scan:{C_RESET}")
        print(f"{C_WARN}Examples:{C_RESET}")
        print(f"  • Single IP:     192.168.1.1")
        print(f"  • Range:         192.168.1.1-192.168.1.100")
        print(f"  • CIDR:          192.168.1.0/24")
        
        ip_range = input(f"\n{C_INFO}IP Range: {C_RESET}").strip()
        
        if not ip_range:
            Logger.error("No range specified!")
            return
        
        Logger.info(f"Scanning: {ip_range}")
        
        if self.installed:
            Logger.info("Please enter this range in Angry IP Scanner GUI")
            self.launch_gui()
        else:
            Logger.warning("Using Nmap instead...")
            if CommandRunner.check_tool('nmap'):
                cmd = f"nmap -sn {ip_range}"
                Logger.info(f"Command: {cmd}")
                pause("Press Enter to start...")
                os.system(cmd)
    
    def scan_from_file(self):
        """Scan IPs from file"""
        print(f"\n{C_INFO}Enter file path with IP addresses:{C_RESET}")
        print(f"{C_WARN}File format: One IP per line{C_RESET}")
        
        file_path = input(f"\n{C_INFO}File path: {C_RESET}").strip()
        
        if not file_path or not os.path.exists(file_path):
            Logger.error("File not found!")
            return
        
        # Read and display IPs
        try:
            with open(file_path, 'r') as f:
                ips = [line.strip() for line in f if line.strip()]
            
            Logger.info(f"Found {len(ips)} IP addresses")
            
            if len(ips) > 0:
                print(f"\n{C_INFO}First few IPs:{C_RESET}")
                for ip in ips[:5]:
                    print(f"{C_OK}  {ip}{C_RESET}")
                if len(ips) > 5:
                    print(f"{C_WARN}  ... and {len(ips) - 5} more{C_RESET}")
            
            if self.installed:
                Logger.info("Please load this file in Angry IP Scanner")
                Logger.info("File > Open... > Select your file")
                self.launch_gui()
            else:
                Logger.warning("Scanning with Nmap instead...")
                if CommandRunner.check_tool('nmap'):
                    cmd = f"nmap -sn -iL {file_path}"
                    Logger.info(f"Command: {cmd}")
                    pause("Press Enter to start...")
                    os.system(cmd)
        
        except Exception as e:
            Logger.error(f"Error reading file: {e}")
    
    def show_about(self):
        """Show information about Angry IP Scanner"""
        print(f"\n{C_INFO}╭─ ABOUT ANGRY IP SCANNER ─────────────────────────────╮{C_RESET}")
        print(f"{C_OK}")
        print("  Angry IP Scanner is a fast and friendly network scanner.")
        print("  It's open-source and cross-platform.")
        print()
        print("  Key Features:")
        print("    • Fast multi-threaded scanning")
        print("    • IP range, random, or file-based scanning")
        print("    • Port scanning")
        print("    • NetBIOS information")
        print("    • Hostname and MAC address detection")
        print("    • Ping functionality")
        print("    • Export results (CSV, TXT, XML)")
        print("    • Extensible with plugins")
        print()
        print("  Version: 3.9.1 (Latest)")
        print("  License: GPL-2.0")
        print("  Website: https://angryip.org")
        print("  GitHub: https://github.com/angryip/ipscan")
        print(f"{C_RESET}")
        print(f"{C_INFO}╰──────────────────────────────────────────────────────╯{C_RESET}")
    
    def show_features(self):
        """Show features overview"""
        print(f"\n{C_INFO}╭─ FEATURES OVERVIEW ──────────────────────────────────╮{C_RESET}")
        print(f"{C_OK}")
        print("  Scanning Features:")
        print("    • IP range scanning (192.168.1.1-192.168.1.254)")
        print("    • CIDR notation (192.168.1.0/24)")
        print("    • Random IP scanning")
        print("    • Import IP list from file")
        print("    • Multi-threaded (up to 512 threads)")
        print()
        print("  Detection Features:")
        print("    • Ping (ICMP echo)")
        print("    • Hostname resolution")
        print("    • MAC address detection")
        print("    • Port scanning")
        print("    • NetBIOS information")
        print("    • Web server detection")
        print()
        print("  Export Features:")
        print("    • CSV format")
        print("    • TXT format")
        print("    • XML format")
        print("    • IP:Port list")
        print()
        print("  Additional Features:")
        print("    • Save/Load scan results")
        print("    • Plugin support")
        print("    • Customizable display columns")
        print("    • OS detection")
        print(f"{C_RESET}")
        print(f"{C_INFO}╰──────────────────────────────────────────────────────╯{C_RESET}")
    
    def show_tips(self):
        """Show tips and tricks"""
        print(f"\n{C_INFO}╭─ TIPS & TRICKS ──────────────────────────────────────╮{C_RESET}")
        print(f"{C_OK}")
        print("  Performance Tips:")
        print("    • Increase thread count for faster scanning")
        print("    • Reduce timeout for dead hosts")
        print("    • Disable unnecessary features (NetBIOS, MAC)")
        print()
        print("  Scanning Tips:")
        print("    • Use CIDR notation for networks (192.168.1.0/24)")
        print("    • Save scan profiles for repeated scans")
        print("    • Use 'Skip broadcast addresses' option")
        print()
        print("  Export Tips:")
        print("    • Export to CSV for easy analysis")
        print("    • Use IP:Port list for further scanning")
        print("    • Save results before closing")
        print()
        print("  Troubleshooting:")
        print("    • Run as administrator/sudo for full features")
        print("    • Check firewall settings if results incomplete")
        print("    • Increase timeout if network is slow")
        print("    • Try different ping methods")
        print()
        print("  Keyboard Shortcuts:")
        print("    • Ctrl+R : Start scanning")
        print("    • Ctrl+X : Stop scanning")
        print("    • Ctrl+E : Export results")
        print("    • Ctrl+O : Open saved results")
        print(f"{C_RESET}")
        print(f"{C_INFO}╰──────────────────────────────────────────────────────╯{C_RESET}")
    
    def launch_nmap_alternative(self):
        """Launch Nmap GUI as alternative"""
        Logger.info("Launching Nmap GUI alternative...")
        
        if CommandRunner.check_tool('zenmap'):
            Logger.info("Found Zenmap - launching...")
            os.system('zenmap &')
        elif CommandRunner.check_tool('nmap'):
            Logger.info("Zenmap not found, using Nmap CLI")
            target = InputValidator.get_ip()
            if target:
                cmd = f"nmap -sn {target}"
                Logger.info(f"Command: {cmd}")
                pause("Press Enter to start...")
                os.system(cmd)
        else:
            Logger.error("Neither Zenmap nor Nmap found!")
    
    def built_in_scanner(self):
        """Use built-in network scanner"""
        Logger.info("Using built-in network scanner (Nmap)")
        
        if not CommandRunner.check_tool('nmap'):
            Logger.error("Nmap not installed!")
            Logger.info("Install: sudo apt install nmap")
            return
        
        print(f"\n{C_INFO}[*] Scan options:{C_RESET}")
        print(f"{C_OK}  [1]  Ping Scan (Host Discovery){C_RESET}")
        print(f"{C_OK}  [2]  Quick Port Scan{C_RESET}")
        print(f"{C_OK}  [3]  Full Port Scan{C_RESET}")
        
        choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()
        
        target = InputValidator.get_ip()
        if not target:
            return
        
        if choice == '1':
            cmd = f"nmap -sn {target}"
        elif choice == '2':
            cmd = f"nmap -F -T4 {target}"
        elif choice == '3':
            cmd = f"nmap -p- -T4 {target}"
        else:
            Logger.error("Invalid choice!")
            return
        
        Logger.info(f"Command: {cmd}")
        pause("Press Enter to start...")
        os.system(cmd)
    
    def run(self):
        """Main menu loop"""
        while True:
            clear_screen()
            self.print_banner()
            
            # Check installation status
            if self.installed:
                Logger.success(f"Angry IP Scanner found: {self.command}")
            else:
                Logger.error("Angry IP Scanner not installed!")
                Logger.info("You can still use alternatives or install it")
            
            print()
            
            self.show_main_menu()
            
            choice = InputValidator.get_choice()
            
            if choice == '0':
                break
            elif choice == '1':
                self.launch_gui()
            elif choice == '2':
                self.quick_scan_local()
            elif choice == '3':
                self.scan_custom_range()
            elif choice == '4':
                self.scan_from_file()
            elif choice == '5':
                self.show_about()
            elif choice == '6':
                self.show_installation_guide()
            elif choice == '7':
                self.show_features()
            elif choice == '8':
                self.show_tips()
            elif choice == '9':
                self.launch_nmap_alternative()
            elif choice == '10':
                self.built_in_scanner()
            else:
                Logger.error("Invalid option!")
            
            pause()


def main():
    try:
        launcher = AngryIPLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print(f"\n\n{C_ERR}[!] Interrupted by user{C_RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C_ERR}[!] Error: {e}{C_RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()