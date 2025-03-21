#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import time
import re
import socket
import platform
import random
import signal
from datetime import datetime

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Tool:
    def __init__(self, id, name, description, command, package=None, category="General"):
        self.id = id
        self.name = name
        self.description = description
        self.command = command
        self.package = package if package else name.lower()
        self.category = category
        self.installed = self.check_installed()
    
    def check_installed(self):
        if self.package == "custom":
            return True
        return shutil.which(self.package) is not None or os.path.exists(f"/usr/bin/{self.package}")
    
    def install(self):
        if self.package == "custom":
            print(f"{Colors.YELLOW}This is a custom tool and doesn't need installation.{Colors.ENDC}")
            return True
        
        try:
            print(f"{Colors.YELLOW}Installing {self.name}...{Colors.ENDC}")
            subprocess.run(["apt-get", "update", "-q"], check=True)
            subprocess.run(["apt-get", "install", "-y", self.package], check=True)
            self.installed = self.check_installed()
            return self.installed
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}Failed to install {self.name}.{Colors.ENDC}")
            return False

    def execute(self, args=None):
        if not self.installed and self.package != "custom":
            print(f"{Colors.RED}{self.name} is not installed. Install it first.{Colors.ENDC}")
            return False
        
        try:
            cmd = self.command.split()
            if args:
                cmd.extend(args.split())
            
            subprocess.run(cmd)
            return True
        except Exception as e:
            print(f"{Colors.RED}Error executing {self.name}: {str(e)}{Colors.ENDC}")
            return False

class XenoSploit:
    def __init__(self):
        self.version = "1.0.0"
        self.tools = self.load_tools()
        self.categories = sorted(list(set(tool.category for tool in self.tools)))
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        print(f"\n{Colors.YELLOW}Exiting XenoSploit...{Colors.ENDC}")
        self.running = False
        sys.exit(0)
    
    def load_tools(self):
        tools = [
            # Reconnaissance Tools
            Tool(1, "Nmap", "Network mapper for port scanning and service detection", "nmap", category="Reconnaissance"),
            Tool(2, "Recon-ng", "Web-based reconnaissance framework", "recon-ng", category="Reconnaissance"),
            Tool(3, "Maltego", "Open source intelligence and forensics application", "maltego", category="Reconnaissance"),
            Tool(4, "theHarvester", "Email, subdomain and people names harvester", "theharvester", category="Reconnaissance"),
            Tool(5, "Shodan", "Search engine for Internet-connected devices", "shodan", category="Reconnaissance"),
            
            # Vulnerability Analysis
            Tool(6, "OpenVAS", "Open vulnerability assessment scanner", "openvas", category="Vulnerability Analysis"),
            Tool(7, "Nikto", "Web server scanner", "nikto", category="Vulnerability Analysis"),
            Tool(8, "SQLmap", "Automatic SQL injection tool", "sqlmap", category="Vulnerability Analysis"),
            Tool(9, "WPScan", "WordPress vulnerability scanner", "wpscan", category="Vulnerability Analysis"),
            Tool(10, "Nessus", "Vulnerability scanner", "nessus", category="Vulnerability Analysis"),
            
            # Web Application Analysis
            Tool(11, "Burp Suite", "Web vulnerability scanner and proxy", "burpsuite", category="Web Application"),
            Tool(12, "OWASP ZAP", "Web application vulnerability scanner", "zaproxy", "zap", category="Web Application"),
            Tool(13, "Dirb", "Web content scanner", "dirb", category="Web Application"),
            Tool(14, "Skipfish", "Web application security reconnaissance tool", "skipfish", category="Web Application"),
            Tool(15, "w3af", "Web application attack and audit framework", "w3af", category="Web Application"),
            
            # Database Assessment
            Tool(16, "SQLmap", "SQL injection and database takeover tool", "sqlmap", category="Database Assessment"),
            Tool(17, "NoSQLMap", "Automated NoSQL database enumeration and injection tool", "nosqlmap", category="Database Assessment"),
            Tool(18, "BBQSQL", "Blind SQL injection exploitation tool", "bbqsql", category="Database Assessment"),
            
            # Password Attacks
            Tool(19, "Hydra", "Parallelized login cracker", "hydra", category="Password Attacks"),
            Tool(20, "John the Ripper", "Password cracker", "john", category="Password Attacks"),
            Tool(21, "Hashcat", "Advanced password recovery utility", "hashcat", category="Password Attacks"),
            Tool(22, "CeWL", "Custom wordlist generator", "cewl", category="Password Attacks"),
            Tool(23, "Medusa", "Parallel network login auditor", "medusa", category="Password Attacks"),
            
            # Wireless Attacks
            Tool(24, "Aircrack-ng", "WiFi security auditing tools suite", "aircrack-ng", category="Wireless Attacks"),
            Tool(25, "Wifite", "Automated wireless attack tool", "wifite", category="Wireless Attacks"),
            Tool(26, "Kismet", "Wireless network detector and sniffer", "kismet", category="Wireless Attacks"),
            Tool(27, "Fern WiFi Cracker", "Wireless attack and auditing tool", "fern-wifi-cracker", category="Wireless Attacks"),
            
            # Exploitation Tools
            Tool(28, "Metasploit", "Penetration testing framework", "msfconsole", category="Exploitation"),
            Tool(29, "BeEF", "Browser exploitation framework", "beef-xss", category="Exploitation"),
            Tool(30, "Armitage", "Graphical cyber attack management tool", "armitage", category="Exploitation"),
            Tool(31, "Searchsploit", "SearchSploit - the offline exploit finder", "searchsploit", category="Exploitation"),
            Tool(32, "MSFPC", "MSFvenom Payload Creator", "msfpc", category="Exploitation"),
            
            # Sniffing & Spoofing
            Tool(33, "Wireshark", "Network protocol analyzer", "wireshark", category="Sniffing & Spoofing"),
            Tool(34, "Ettercap", "Man-in-the-middle attack suite", "ettercap", category="Sniffing & Spoofing"),
            Tool(35, "Bettercap", "Network attack and monitoring tool", "bettercap", category="Sniffing & Spoofing"),
            Tool(36, "Responder", "LLMNR, NBT-NS and MDNS poisoner", "responder", category="Sniffing & Spoofing"),
            Tool(37, "MITMproxy", "Interactive TLS-capable intercepting HTTP proxy", "mitmproxy", category="Sniffing & Spoofing"),
            
            # Post Exploitation
            Tool(38, "PowerSploit", "PowerShell post-exploitation framework", "powersploit", category="Post Exploitation"),
            Tool(39, "Empire", "PowerShell and Python post-exploitation framework", "empire", category="Post Exploitation"),
            Tool(40, "Mimikatz", "Windows password extractor", "mimikatz", category="Post Exploitation"),
            Tool(41, "Privilege Escalation Scripts", "Linux and Windows PE scripts", "pe-scripts", "custom", category="Post Exploitation"),
            
            # Forensics
            Tool(42, "Volatility", "Memory forensics framework", "volatility", category="Forensics"),
            Tool(43, "Autopsy", "Digital forensics platform", "autopsy", category="Forensics"),
            Tool(44, "Foremost", "File recovery tool", "foremost", category="Forensics"),
            Tool(45, "Binwalk", "Firmware analysis tool", "binwalk", category="Forensics"),
            
            # Reverse Engineering
            Tool(46, "Ghidra", "Software reverse engineering framework", "ghidra", category="Reverse Engineering"),
            Tool(47, "Radare2", "Reverse engineering framework", "radare2", category="Reverse Engineering"),
            Tool(48, "apktool", "Android APK reverse engineering tool", "apktool", category="Reverse Engineering"),
            
            # Social Engineering
            Tool(49, "Social-Engineer Toolkit (SET)", "Social engineering framework", "setoolkit", category="Social Engineering"),
            Tool(50, "King Phisher", "Phishing campaign toolkit", "king-phisher", category="Social Engineering")
        ]
        
        return tools

    def print_banner(self):
        banner = f"""
{Colors.CYAN}██╗  ██╗███████╗███╗   ██╗ ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
╚██╗██╔╝██╔════╝████╗  ██║██╔═══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
 ╚███╔╝ █████╗  ██╔██╗ ██║██║   ██║███████╗██████╔╝██║     ██║   ██║██║   ██║   
 ██╔██╗ ██╔══╝  ██║╚██╗██║██║   ██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
██╔╝ ██╗███████╗██║ ╚████║╚██████╔╝███████║██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   {Colors.ENDC}
{Colors.YELLOW}Advanced Penetration Testing Framework - v{self.version}{Colors.ENDC}
{Colors.RED}Author: https://www.github.com/Rip70022{Colors.ENDC}

{Colors.GREEN}[*] System: {platform.system()} {platform.release()}
[*] Hostname: {socket.gethostname()}
[*] Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}
"""
        print(banner)
    
    def print_menu(self, category=None):
        if category:
            tools = [tool for tool in self.tools if tool.category == category]
            category_title = f"Category: {category}"
            print(f"\n{Colors.BOLD}{Colors.BLUE}{category_title}{Colors.ENDC}")
            print(f"{Colors.BLUE}{'=' * len(category_title)}{Colors.ENDC}\n")
        else:
            tools = self.tools
        
        table_width = 100
        header = f"{Colors.BOLD}{'ID':^5} | {'Tool Name':^20} | {'Status':^12} | {'Description':^50}{Colors.ENDC}"
        print(header)
        print(f"{Colors.BLUE}{'-' * table_width}{Colors.ENDC}")
        
        for tool in tools:
            status = f"{Colors.GREEN}Installed{Colors.ENDC}" if tool.installed else f"{Colors.RED}Not Installed{Colors.ENDC}"
            print(f"{tool.id:^5} | {tool.name:^20} | {status:^25} | {tool.description[:50]:^50}")
        
        print(f"{Colors.BLUE}{'-' * table_width}{Colors.ENDC}")
    
    def print_categories(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}Available Categories:{Colors.ENDC}")
        for i, category in enumerate(self.categories, start=1):
            print(f"{Colors.CYAN}{i}.{Colors.ENDC} {category}")
    
    def print_help(self):
        help_text = f"""
{Colors.BOLD}{Colors.YELLOW}XenoSploit Help Menu{Colors.ENDC}

{Colors.GREEN}Available Commands:{Colors.ENDC}
  {Colors.CYAN}help{Colors.ENDC}                 - Display this help menu
  {Colors.CYAN}list{Colors.ENDC}                 - List all available tools
  {Colors.CYAN}categories{Colors.ENDC}           - List all tool categories
  {Colors.CYAN}category <name>{Colors.ENDC}      - List tools in a specific category
  {Colors.CYAN}search <keyword>{Colors.ENDC}     - Search for tools by keyword
  {Colors.CYAN}info <id>{Colors.ENDC}            - Show detailed information about a tool
  {Colors.CYAN}install <id>{Colors.ENDC}         - Install a specific tool
  {Colors.CYAN}run <id> [args]{Colors.ENDC}      - Run a specific tool with optional arguments
  {Colors.CYAN}update{Colors.ENDC}               - Update XenoSploit framework
  {Colors.CYAN}check{Colors.ENDC}                - Check for missing dependencies
  {Colors.CYAN}clear{Colors.ENDC}                - Clear the screen
  {Colors.CYAN}exit/quit{Colors.ENDC}            - Exit XenoSploit

{Colors.YELLOW}Examples:{Colors.ENDC}
  {Colors.CYAN}run 1 -sV 192.168.1.1{Colors.ENDC}    - Run Nmap with specific arguments
  {Colors.CYAN}category "Web Application"{Colors.ENDC} - List tools in Web Application category
  {Colors.CYAN}search sql{Colors.ENDC}                - Search for tools related to SQL
"""
        print(help_text)
    
    def install_tool(self, tool_id):
        try:
            tool_id = int(tool_id)
            for tool in self.tools:
                if tool.id == tool_id:
                    if tool.installed:
                        print(f"{Colors.GREEN}{tool.name} is already installed.{Colors.ENDC}")
                        return True
                    
                    if os.geteuid() != 0:
                        print(f"{Colors.RED}This operation requires root privileges. Please run as root.{Colors.ENDC}")
                        return False
                    
                    success = tool.install()
                    if success:
                        print(f"{Colors.GREEN}{tool.name} installed successfully.{Colors.ENDC}")
                    return success
            
            print(f"{Colors.RED}Tool with ID {tool_id} not found.{Colors.ENDC}")
            return False
        except ValueError:
            print(f"{Colors.RED}Invalid tool ID. Please provide a number.{Colors.ENDC}")
            return False
    
    def run_tool(self, tool_id, args=None):
        try:
            tool_id = int(tool_id)
            for tool in self.tools:
                if tool.id == tool_id:
                    return tool.execute(args)
            
            print(f"{Colors.RED}Tool with ID {tool_id} not found.{Colors.ENDC}")
            return False
        except ValueError:
            print(f"{Colors.RED}Invalid tool ID. Please provide a number.{Colors.ENDC}")
            return False
    
    def search_tools(self, keyword):
        keyword = keyword.lower()
        results = [tool for tool in self.tools if keyword in tool.name.lower() or keyword in tool.description.lower()]
        
        if results:
            print(f"\n{Colors.BOLD}{Colors.YELLOW}Search Results for '{keyword}':{Colors.ENDC}")
            table_width = 100
            header = f"{Colors.BOLD}{'ID':^5} | {'Tool Name':^20} | {'Status':^12} | {'Description':^50}{Colors.ENDC}"
            print(header)
            print(f"{Colors.BLUE}{'-' * table_width}{Colors.ENDC}")
            
            for tool in results:
                status = f"{Colors.GREEN}Installed{Colors.ENDC}" if tool.installed else f"{Colors.RED}Not Installed{Colors.ENDC}"
                print(f"{tool.id:^5} | {tool.name:^20} | {status:^25} | {tool.description[:50]:^50}")
            
            print(f"{Colors.BLUE}{'-' * table_width}{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}No tools found matching '{keyword}'.{Colors.ENDC}")
    
    def show_tool_info(self, tool_id):
        try:
            tool_id = int(tool_id)
            for tool in self.tools:
                if tool.id == tool_id:
                    status = f"{Colors.GREEN}Installed{Colors.ENDC}" if tool.installed else f"{Colors.RED}Not Installed{Colors.ENDC}"
                    info = f"""
{Colors.BOLD}{Colors.BLUE}Tool Information:{Colors.ENDC}
{Colors.CYAN}ID:{Colors.ENDC}           {tool.id}
{Colors.CYAN}Name:{Colors.ENDC}         {tool.name}
{Colors.CYAN}Category:{Colors.ENDC}     {tool.category}
{Colors.CYAN}Status:{Colors.ENDC}       {status}
{Colors.CYAN}Description:{Colors.ENDC}  {tool.description}
{Colors.CYAN}Command:{Colors.ENDC}      {tool.command}
{Colors.CYAN}Package:{Colors.ENDC}      {tool.package}
"""
                    print(info)
                    return True
            
            print(f"{Colors.RED}Tool with ID {tool_id} not found.{Colors.ENDC}")
            return False
        except ValueError:
            print(f"{Colors.RED}Invalid tool ID. Please provide a number.{Colors.ENDC}")
            return False
    
    def check_dependencies(self):
        print(f"{Colors.YELLOW}Checking system dependencies...{Colors.ENDC}")
        
        essential_packages = [
            "python3", "python3-pip", "git", "curl", "wget", "nmap"
        ]
        
        missing = []
        for package in essential_packages:
            if not shutil.which(package):
                missing.append(package)
        
        if missing:
            print(f"{Colors.RED}Missing dependencies: {', '.join(missing)}{Colors.ENDC}")
            if os.geteuid() == 0:
                response = input(f"{Colors.YELLOW}Do you want to install missing dependencies? (y/n): {Colors.ENDC}")
                if response.lower() == 'y':
                    try:
                        subprocess.run(["apt-get", "update", "-q"], check=True)
                        subprocess.run(["apt-get", "install", "-y"] + missing, check=True)
                        print(f"{Colors.GREEN}Dependencies installed successfully.{Colors.ENDC}")
                    except subprocess.CalledProcessError:
                        print(f"{Colors.RED}Failed to install dependencies.{Colors.ENDC}")
            else:
                print(f"{Colors.RED}Please run as root to install dependencies.{Colors.ENDC}")
        else:
            print(f"{Colors.GREEN}All essential dependencies are installed.{Colors.ENDC}")
    
    def update_framework(self):
        print(f"{Colors.YELLOW}Checking for updates...{Colors.ENDC}")
        print(f"{Colors.GREEN}XenoSploit is up to date (version {self.version}).{Colors.ENDC}")
    
    def run(self):
        if os.name == 'nt':
            print(f"{Colors.RED}XenoSploit is designed for Kali Linux and may not work correctly on Windows.{Colors.ENDC}")
        
        self.print_banner()
        
        while self.running:
            try:
                user_input = input(f"{Colors.BOLD}{Colors.RED}XenoSploit{Colors.ENDC}{Colors.BOLD}({Colors.BLUE}~{Colors.ENDC}{Colors.BOLD})> {Colors.ENDC}").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit']:
                    print(f"{Colors.YELLOW}Exiting XenoSploit...{Colors.ENDC}")
                    self.running = False
                    break
                
                if user_input.lower() == 'clear':
                    os.system('clear')
                    self.print_banner()
                    continue
                
                if user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                if user_input.lower() == 'list':
                    self.print_menu()
                    continue
                
                if user_input.lower() == 'categories':
                    self.print_categories()
                    continue
                
                if user_input.lower() == 'check':
                    self.check_dependencies()
                    continue
                
                if user_input.lower() == 'update':
                    self.update_framework()
                    continue
                
                if user_input.lower().startswith('category '):
                    category_name = user_input[9:].strip()
                    if category_name in self.categories:
                        self.print_menu(category_name)
                    else:
                        print(f"{Colors.RED}Category '{category_name}' not found.{Colors.ENDC}")
                        self.print_categories()
                    continue
                
                if user_input.lower().startswith('search '):
                    keyword = user_input[7:].strip()
                    self.search_tools(keyword)
                    continue
                
                if user_input.lower().startswith('info '):
                    tool_id = user_input[5:].strip()
                    self.show_tool_info(tool_id)
                    continue
                
                if user_input.lower().startswith('install '):
                    tool_id = user_input[8:].strip()
                    self.install_tool(tool_id)
                    continue
                
                if user_input.lower().startswith('run '):
                    parts = user_input[4:].strip().split(' ', 1)
                    tool_id = parts[0]
                    args = parts[1] if len(parts) > 1 else None
                    self.run_tool(tool_id, args)
                    continue
                
                print(f"{Colors.RED}Unknown command: {user_input}{Colors.ENDC}")
                print(f"{Colors.YELLOW}Type 'help' to see available commands.{Colors.ENDC}")
                
            except Exception as e:
                print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")

if __name__ == "__main__":
    try:
        xenosploit = XenoSploit()
        xenosploit.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Exiting XenoSploit...{Colors.ENDC}")
        sys.exit(0)
