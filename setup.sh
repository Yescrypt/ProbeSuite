#!/bin/bash
# ProbeSuite Setup Script - System Dependencies

set -e

echo "╔══════════════════════════════════════════╗"
echo "║     ProbeSuite - System Setup            ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[!] Please run as root or with sudo${NC}"
    echo "    Usage: sudo bash setup.sh"
    exit 1
fi

echo -e "${GREEN}[*] Starting system dependencies installation...${NC}"
echo ""

# Update package list
echo -e "${YELLOW}[*] Updating package list...${NC}"
apt update

# Install Python3 and pip
echo -e "${YELLOW}[*] Installing Python3 and pip...${NC}"
apt install -y python3 python3-pip python3-venv

# Install Nmap
echo -e "${YELLOW}[*] Installing Nmap...${NC}"
apt install -y nmap

# Install Masscan
echo -e "${YELLOW}[*] Installing Masscan...${NC}"
apt install -y masscan

# Install Nikto
echo -e "${YELLOW}[*] Installing Nikto...${NC}"
apt install -y nikto

# Install WPScan
echo -e "${YELLOW}[*] Installing WPScan...${NC}"
apt install -y wpscan

# Install SQLMap
echo -e "${YELLOW}[*] Installing SQLMap...${NC}"
apt install -y sqlmap

# Install Metasploit Framework
echo -e "${YELLOW}[*] Installing Metasploit Framework...${NC}"
if ! command -v msfconsole &> /dev/null; then
    apt install -y metasploit-framework
else
    echo -e "${GREEN}[✓] Metasploit already installed${NC}"
fi

# Install Exploit-DB (searchsploit)
echo -e "${YELLOW}[*] Installing Exploit-DB...${NC}"
if ! command -v searchsploit &> /dev/null; then
    apt install -y exploitdb
    echo -e "${GREEN}[✓] Updating exploit database...${NC}"
    searchsploit -u
else
    echo -e "${GREEN}[✓] Exploit-DB already installed${NC}"
    searchsploit -u
fi

# Install Hydra
echo -e "${YELLOW}[*] Installing Hydra...${NC}"
apt install -y hydra

# Install John the Ripper
echo -e "${YELLOW}[*] Installing John the Ripper...${NC}"
apt install -y john

# Install Hashcat
echo -e "${YELLOW}[*] Installing Hashcat...${NC}"
apt install -y hashcat

# Install Dirb
echo -e "${YELLOW}[*] Installing Dirb...${NC}"
apt install -y dirb

# Install Gobuster
echo -e "${YELLOW}[*] Installing Gobuster...${NC}"
apt install -y gobuster

# Install Feroxbuster (optional, newer alternative)
echo -e "${YELLOW}[*] Installing Feroxbuster...${NC}"
if ! command -v feroxbuster &> /dev/null; then
    wget https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster_amd64.deb.zip
    unzip feroxbuster_amd64.deb.zip
    apt install -y ./feroxbuster_*.deb
    rm feroxbuster_*
fi

# Install Responder
echo -e "${YELLOW}[*] Installing Responder...${NC}"
apt install -y responder

# Install Netcat
echo -e "${YELLOW}[*] Installing Netcat...${NC}"
apt install -y netcat-traditional

# Install Wireshark (optional)
echo -e "${YELLOW}[*] Installing Wireshark...${NC}"
apt install -y wireshark

# Install tcpdump
echo -e "${YELLOW}[*] Installing tcpdump...${NC}"
apt install -y tcpdump

# Install Git (if not installed)
echo -e "${YELLOW}[*] Installing Git...${NC}"
apt install -y git

# Install other useful tools
echo -e "${YELLOW}[*] Installing additional tools...${NC}"
apt install -y curl wget net-tools dnsutils whois

# Install Ruby (for some exploits)
echo -e "${YELLOW}[*] Installing Ruby...${NC}"
apt install -y ruby ruby-dev

# Install PostgreSQL (for Metasploit database)
echo -e "${YELLOW}[*] Installing PostgreSQL...${NC}"
apt install -y postgresql

# Setup Metasploit database
echo -e "${YELLOW}[*] Setting up Metasploit database...${NC}"
systemctl start postgresql
msfdb init 2>/dev/null || msfdb reinit

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation Complete!               ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}[✓] All system dependencies installed${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Install Python dependencies:"
echo "     pip3 install -r requirements.txt"
echo ""
echo "  2. Run ProbeSuite:"
echo "     python3 main.py"
echo ""
echo -e "${YELLOW}Optional:${NC}"
echo "  • Update exploit database: searchsploit -u"
echo "  • Check Metasploit: msfconsole"
echo ""