#!/usr/bin/env python3
"""
ProBeSuite - Zenmap GUI Launcher
Graphical interface for Nmap
"""

import os
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import C_OK, C_ERR, C_WARN, C_INFO, C_RESET
from app.utils import Logger, CommandRunner, InputValidator, clear_screen, pause


class ZenmapLauncher:
    def __init__(self):
        self.zenmap_installed = False
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║              🗺️  ZENMAP - NMAP GUI INTERFACE 🗺️              ║
║                Graphical Network Mapping Tool                ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(f"{C_INFO}{banner}{C_RESET}")
    
    def show_main_menu(self):
        menu = """
╭─ ZENMAP LAUNCHER ─────────────────────────────────────────────╮
│                                                               │
│  LAUNCH OPTIONS:                                              │
│    [1]  Launch Zenmap (Empty)                                 │
│    [2]  Launch with Target                                    │
│    [3]  Launch with Quick Scan Profile                        │
│    [4]  Launch with Intense Scan Profile                      │
│    [5]  Launch with Comprehensive Scan                        │
│                                                               │
│  QUICK ACTIONS:                                               │
│    [6]  Open Recent Scan                                      │
│    [7]  Compare Scan Results                                  │
│                                                               │
│  INFORMATION:                                                 │
│    [8]  About Zenmap                                          │
│    [9]  Installation Guide                                    │
│    [10] Scan Profiles Info                                    │
│                                                               │
│  [0]  ← Back                                                  │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
        """
        print(f"{C_OK}{menu}{C_RESET}")
    
    def check_zenmap(self):
        """Check if Zenmap is installed"""
        # Try multiple possible commands
        commands = ['zenmap', 'zenmap-kbx', 'nmap']
        
        for cmd in commands:
            if CommandRunner.check_tool(cmd):
                if cmd == 'zenmap' or cmd == 'zenmap-kbx':
                    self.zenmap_installed = True
                    return True
        
        return False
    
    def show_installation_guide(self):
        """Display installation instructions"""
        print(f"\n{C_INFO}╭─ ZENMAP INSTALLATION GUIDE ──────────────────────────╮{C_RESET}")
        print(f"{C_WARN}")
        print("⚠️  Note: Zenmap is deprecated and no longer maintained.")
        print("    Consider using Nmap directly or other alternatives.")
        print(f"{C_RESET}")
        print(f"\n{C_INFO}For Kali Linux / Debian / Ubuntu:{C_RESET}")
        print(f"{C_OK}  sudo apt update{C_RESET}")
        print(f"{C_OK}  sudo apt install zenmap{C_RESET}")
        
        print(f"\n{C_INFO}Alternative (Zenmap KBX - Python 3 version):{C_RESET}")
        print(f"{C_OK}  git clone https://github.com/nmap/nmap.git{C_RESET}")
        print(f"{C_OK}  cd nmap/zenmap{C_RESET}")
        print(f"{C_OK}  sudo python3 setup.py install{C_RESET}")
        
        print(f"\n{C_INFO}For other distributions:{C_RESET}")
        print(f"{C_OK}  Visit: https://nmap.org/zenmap/{C_RESET}")
        
        print(f"\n{C_WARN}Alternatives to Zenmap:{C_RESET}")
        print(f"{C_INFO}  • Nmap GUI (Web-based): https://nmap-gui.com{C_RESET}")
        print(f"{C_INFO}  • Angry IP Scanner: GUI network scanner{C_RESET}")
        print(f"{C_INFO}  • Netdiscover: Active/passive ARP reconnaissance{C_RESET}")
        
        print(f"\n{C_INFO}╰──────────────────────────────────────────────────────╯{C_RESET}")
    
    def launch_empty(self):
        """Launch Zenmap without parameters"""
        Logger.info("Launching Zenmap...")
        
        try:
            # Try different commands
            if CommandRunner.check_tool('zenmap'):
                subprocess.Popen(['zenmap'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            elif CommandRunner.check_tool('zenmap-kbx'):
                subprocess.Popen(['zenmap-kbx'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            else:
                Logger.error("Zenmap not found!")
                return False
            
            Logger.success("Zenmap launched successfully!")
            Logger.info("The application is running in the background")
            return True
            
        except Exception as e:
            Logger.error(f"Failed to launch Zenmap: {e}")
            return False
    
    def launch_with_target(self):
        """Launch Zenmap with a target"""
        target = InputValidator.get_ip()
        if not target:
            return
        
        Logger.info(f"Launching Zenmap with target: {target}")
        
        try:
            if CommandRunner.check_tool('zenmap'):
                subprocess.Popen(['zenmap', '-t', target], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            elif CommandRunner.check_tool('zenmap-kbx'):
                subprocess.Popen(['zenmap-kbx', '-t', target], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            else:
                Logger.error("Zenmap not found!")
                return
            
            Logger.success("Zenmap launched with target!")
            
        except Exception as e:
            Logger.error(f"Failed to launch: {e}")
    
    def launch_with_profile(self, profile_name, profile_cmd):
        """Launch Zenmap with specific scan profile"""
        target = InputValidator.get_ip()
        if not target:
            return
        
        Logger.info(f"Launching Zenmap - {profile_name}")
        Logger.info(f"Target: {target}")
        Logger.info(f"Profile: {profile_cmd}")
        
        try:
            if CommandRunner.check_tool('zenmap'):
                subprocess.Popen(['zenmap', '-t', target, '-p', profile_name], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            elif CommandRunner.check_tool('zenmap-kbx'):
                subprocess.Popen(['zenmap-kbx', '-t', target, '-p', profile_name], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            else:
                # Fallback to direct nmap command
                Logger.warning("Zenmap not found, running Nmap directly...")
                cmd = f"nmap {profile_cmd} {target}"
                Logger.info(f"Command: {cmd}")
                pause("Press Enter to start...")
                os.system(cmd)
                return
            
            Logger.success("Zenmap launched!")
            
        except Exception as e:
            Logger.error(f"Failed to launch: {e}")
    
    def quick_scan(self):
        """Quick scan profile"""
        self.launch_with_profile(
            "Quick scan",
            "-T4 -F"
        )
    
    def intense_scan(self):
        """Intense scan profile"""
        self.launch_with_profile(
            "Intense scan",
            "-T4 -A -v"
        )
    
    def comprehensive_scan(self):
        """Comprehensive scan profile"""
        self.launch_with_profile(
            "Comprehensive scan",
            "-sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script=default"
        )
    
    def open_recent_scan(self):
        """Open recent scan results"""
        Logger.info("Opening Zenmap to view recent scans...")
        
        # Zenmap saves scans in ~/.zenmap/
        scan_dir = Path.home() / ".zenmap"
        
        if scan_dir.exists():
            Logger.info(f"Recent scans location: {scan_dir}")
            
            # List recent scans
            scan_files = list(scan_dir.glob("*.xml"))
            if scan_files:
                print(f"\n{C_INFO}Recent scans found:{C_RESET}")
                for i, scan_file in enumerate(scan_files[:5], 1):
                    print(f"{C_OK}  [{i}] {scan_file.name}{C_RESET}")
            else:
                Logger.warning("No recent scans found")
        
        # Launch Zenmap
        self.launch_empty()
    
    def compare_results(self):
        """Compare scan results"""
        Logger.info("Launching Zenmap for result comparison...")
        Logger.info("Use Tools > Compare Results in Zenmap menu")
        self.launch_empty()
    
    def show_about(self):
        """Show information about Zenmap"""
        print(f"\n{C_INFO}╭─ ABOUT ZENMAP ───────────────────────────────────────╮{C_RESET}")
        print(f"{C_OK}")
        print("  Zenmap is the official Nmap Security Scanner GUI.")
        print("  It provides a user-friendly interface for Nmap.")
        print()
        print("  Features:")
        print("    • Visual network topology mapping")
        print("    • Scan result comparison")
        print("    • Profile editor for custom scans")
        print("    • Search and filter scan results")
        print("    • Save and load scan results")
        print()
        print("  Status: Deprecated (No longer actively maintained)")
        print("  Last stable version: 7.94")
        print()
        print("  Website: https://nmap.org/zenmap/")
        print("  GitHub: https://github.com/nmap/nmap/tree/master/zenmap")
        print(f"{C_RESET}")
        print(f"{C_INFO}╰──────────────────────────────────────────────────────╯{C_RESET}")
    
    def show_profiles_info(self):
        """Show information about scan profiles"""
        print(f"\n{C_INFO}╭─ ZENMAP SCAN PROFILES ───────────────────────────────╮{C_RESET}")
        print(f"{C_OK}")
        
        profiles = [
            ("Intense scan", "-T4 -A -v", "Comprehensive scan with OS detection, version detection, script scanning, and traceroute"),
            ("Intense scan plus UDP", "-sS -sU -T4 -A -v", "Same as Intense scan but also scans UDP ports"),
            ("Intense scan, all TCP ports", "-p 1-65535 -T4 -A -v", "Scans all TCP ports"),
            ("Intense scan, no ping", "-T4 -A -v -Pn", "For hosts that don't respond to ping"),
            ("Ping scan", "-sn", "Only determines which hosts are online"),
            ("Quick scan", "-T4 -F", "Fast scan of the most common ports"),
            ("Quick scan plus", "-sV -T4 -O -F --version-light", "Quick scan with version detection"),
            ("Quick traceroute", "-sn --traceroute", "Quick traceroute to target"),
            ("Regular scan", "", "Standard scan with default options"),
            ("Slow comprehensive scan", "-sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script default", "Very thorough scan")
        ]
        
        for name, flags, desc in profiles:
            print(f"  {name}")
            print(f"    Flags: {flags if flags else 'default'}")
            print(f"    {desc}")
            print()
        
        print(f"{C_RESET}")
        print(f"{C_INFO}╰──────────────────────────────────────────────────────╯{C_RESET}")
    
    def run(self):
        """Main menu loop"""
        while True:
            clear_screen()
            self.print_banner()
            
            # Check if Zenmap is installed
            if not self.check_zenmap():
                Logger.error("Zenmap is not installed!")
                print()
                self.show_installation_guide()
                print()
                
                if not InputValidator.confirm("Continue anyway? (will use Nmap CLI)"):
                    break
            else:
                Logger.success("Zenmap is installed and ready")
                print()
            
            self.show_main_menu()
            
            choice = InputValidator.get_choice()
            
            if choice == '0':
                break
            elif choice == '1':
                self.launch_empty()
            elif choice == '2':
                self.launch_with_target()
            elif choice == '3':
                self.quick_scan()
            elif choice == '4':
                self.intense_scan()
            elif choice == '5':
                self.comprehensive_scan()
            elif choice == '6':
                self.open_recent_scan()
            elif choice == '7':
                self.compare_results()
            elif choice == '8':
                self.show_about()
            elif choice == '9':
                self.show_installation_guide()
            elif choice == '10':
                self.show_profiles_info()
            else:
                Logger.error("Invalid option!")
            
            pause()


def main():
    try:
        launcher = ZenmapLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print(f"\n\n{C_ERR}[!] Interrupted by user{C_RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C_ERR}[!] Error: {e}{C_RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()