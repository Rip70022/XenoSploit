#!/usr/bin/env python3

import os
import sys
import time
import platform
import subprocess
import urllib.request
import re
import signal
import shutil
import socket
from datetime import datetime

# Terminal colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Tool class to store tool information
class Tool:
    def __init__(self, id, name, category, command, install_cmd, description):
        self.id = id
        self.name = name
        self.category = category
        self.command = command
        self.install_cmd = install_cmd
        self.description = description
        self.installed = self.check_installed()
    
    def check_installed(self):
        try:
            if self.command.startswith("/"):
                return os.path.exists(self.command)
            else:
                cmd_path = subprocess.check_output(["which", self.command.split()[0]], stderr=subprocess.DEVNULL).decode().strip()
                return bool(cmd_path)
        except:
            return False
    
    def install(self):
        print(f"{Colors.YELLOW}Installing {self.name}...{Colors.ENDC}")
        try:
            subprocess.run(self.install_cmd, shell=True, check=True)
            self.installed = True
            print(f"{Colors.GREEN}Successfully installed {self.name}{Colors.ENDC}")
            return True
        except:
            print(f"{Colors.RED}Failed to install {self.name}{Colors.ENDC}")
            return False
    
    def run(self, args=None):
        if not self.installed:
            print(f"{Colors.RED}{self.name} is not installed. Install it first.{Colors.ENDC}")
            return False
        
        try:
            cmd = self.command
            if args:
                cmd += " " + args
            
            print(f"{Colors.CYAN}Running: {cmd}{Colors.ENDC}")
            subprocess.run(cmd, shell=True)
            return True
        except Exception as e:
            print(f"{Colors.RED}Error executing {self.name}: {str(e)}{Colors.ENDC}")
            return False

class XenoSploit:
    def __init__(self):
        self.version = "1.0.0"
        self.author = "https://www.github.com/Rip70022"
        self.update_url = "https://www.github.com/Rip70022/XenoSploit"
        self.tools = self.load_tools()
        self.categories = sorted(list(set([tool.category for tool in self.tools])))
        
    def load_tools(self):
        tools = [
            Tool(1, "Nmap", "Reconnaissance", "nmap", "apt-get install nmap -y", "Network discovery and security auditing"),
            Tool(2, "Metasploit Framework", "Exploitation", "msfconsole", "apt-get install metasploit-framework -y", "Penetration testing framework"),
            Tool(3, "Aircrack-ng", "Wireless", "aircrack-ng", "apt-get install aircrack-ng -y", "WiFi network security tools"),
            Tool(4, "Hydra", "Password Attacks", "hydra", "apt-get install hydra -y", "Parallelized login cracker"),
            Tool(5, "John the Ripper", "Password Attacks", "john", "apt-get install john -y", "Password cracker"),
            Tool(6, "Wireshark", "Sniffing & Spoofing", "wireshark", "apt-get install wireshark -y", "Network protocol analyzer"),
            Tool(7, "Burp Suite", "Web Application Analysis", "burpsuite", "apt-get install burpsuite -y", "Web vulnerability scanner"),
            Tool(8, "OWASP ZAP", "Web Application Analysis", "zaproxy", "apt-get install zaproxy -y", "Web app vulnerability scanner"),
            Tool(9, "sqlmap", "Web Application Analysis", "sqlmap", "apt-get install sqlmap -y", "Automatic SQL injection tool"),
            Tool(10, "Nikto", "Web Application Analysis", "nikto", "apt-get install nikto -y", "Web server scanner"),
            Tool(11, "Hashcat", "Password Attacks", "hashcat", "apt-get install hashcat -y", "Advanced password recovery"),
            Tool(12, "Dirb", "Web Application Analysis", "dirb", "apt-get install dirb -y", "Web content scanner"),
            Tool(13, "Wifite", "Wireless", "wifite", "apt-get install wifite -y", "Automated wireless attack tool"),
            Tool(14, "Kismet", "Wireless", "kismet", "apt-get install kismet -y", "Wireless network detector"),
            Tool(15, "Reaver", "Wireless", "reaver", "apt-get install reaver -y", "WPS attack tool"),
            Tool(16, "Ettercap", "Sniffing & Spoofing", "ettercap", "apt-get install ettercap-graphical -y", "MITM attacks suite"),
            Tool(17, "Scapy", "Sniffing & Spoofing", "scapy", "apt-get install python3-scapy -y", "Packet manipulation program"),
            Tool(18, "Beef XSS Framework", "Web Application Analysis", "beef-xss", "apt-get install beef-xss -y", "Browser exploitation framework"),
            Tool(19, "Setoolkit", "Social Engineering", "setoolkit", "apt-get install set -y", "Social Engineering Toolkit"),
            Tool(20, "Maltego", "Reconnaissance", "maltego", "apt-get install maltego -y", "Open source intelligence tool"),
            Tool(21, "Autopsy", "Forensics", "autopsy", "apt-get install autopsy -y", "Digital forensics platform"),
            Tool(22, "Volatility", "Forensics", "volatility", "apt-get install volatility -y", "Memory forensics framework"),
            Tool(23, "Armitage", "Exploitation", "armitage", "apt-get install armitage -y", "Graphical cyber attack management tool"),
            Tool(24, "Lynis", "Vulnerability Analysis", "lynis", "apt-get install lynis -y", "Security auditing tool"),
            Tool(25, "Shellter", "Exploitation", "shellter", "apt-get install shellter -y", "Dynamic shellcode injection tool"),
            Tool(26, "Responder", "Sniffing & Spoofing", "responder", "apt-get install responder -y", "LLMNR/NBT-NS/mDNS poisoner"),
            Tool(27, "Empire", "Post Exploitation", "empire", "apt-get install powershell-empire -y", "Post-exploitation framework"),
            Tool(28, "Searchsploit", "Exploitation", "searchsploit", "apt-get install exploitdb -y", "Exploit database search tool"),
            Tool(29, "WPScan", "Web Application Analysis", "wpscan", "apt-get install wpscan -y", "WordPress vulnerability scanner"),
            Tool(30, "Masscan", "Reconnaissance", "masscan", "apt-get install masscan -y", "TCP port scanner"),
        ]
        return tools
    
    def clear_screen(self):
        os.system('clear')
    
    def print_banner(self):
        banner = f"""
{Colors.BLUE}██╗  ██╗███████╗███╗   ██╗ ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
╚██╗██╔╝██╔════╝████╗  ██║██╔═══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
 ╚███╔╝ █████╗  ██╔██╗ ██║██║   ██║███████╗██████╔╝██║     ██║   ██║██║   ██║   
 ██╔██╗ ██╔══╝  ██║╚██╗██║██║   ██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
██╔╝ ██╗███████╗██║ ╚████║╚██████╔╝███████║██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   {Colors.ENDC}
                                                                            
{Colors.GREEN}[*] {Colors.BOLD}XenoSploit Framework {self.version}{Colors.ENDC}
{Colors.GREEN}[*] {Colors.BOLD}Author: {self.author}{Colors.ENDC}
{Colors.GREEN}[*] {Colors.BOLD}Update URL: {self.update_url}{Colors.ENDC}
{Colors.YELLOW}[*] {Colors.BOLD}Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}
{Colors.YELLOW}[*] {Colors.BOLD}System: {platform.system()} {platform.release()}{Colors.ENDC}
{Colors.YELLOW}[*] {Colors.BOLD}Hostname: {socket.gethostname()}{Colors.ENDC}
"""
        print(banner)
    
    def print_menu(self):
        self.print_banner()
        print(f"\n{Colors.CYAN}[*] Available Categories:{Colors.ENDC}")
        
        for i, category in enumerate(self.categories, 1):
            print(f"{Colors.YELLOW}[{i}]{Colors.ENDC} {category}")
        
        print(f"\n{Colors.CYAN}[*] Available Commands:{Colors.ENDC}")
        print(f"{Colors.YELLOW}help{Colors.ENDC} - Display help information")
        print(f"{Colors.YELLOW}list{Colors.ENDC} - List all available tools")
        print(f"{Colors.YELLOW}list <category>{Colors.ENDC} - List tools in category")
        print(f"{Colors.YELLOW}search <keyword>{Colors.ENDC} - Search for tools")
        print(f"{Colors.YELLOW}info <tool_id>{Colors.ENDC} - Show tool information")
        print(f"{Colors.YELLOW}install <tool_id>{Colors.ENDC} - Install a tool")
        print(f"{Colors.YELLOW}run <tool_id> [args]{Colors.ENDC} - Run a tool with optional arguments")
        print(f"{Colors.YELLOW}update{Colors.ENDC} - Update XenoSploit Framework")
        print(f"{Colors.YELLOW}installed{Colors.ENDC} - Show installed tools")
        print(f"{Colors.YELLOW}check{Colors.ENDC} - Check tool installation status")
        print(f"{Colors.YELLOW}clear{Colors.ENDC} - Clear the screen")
        print(f"{Colors.YELLOW}exit{Colors.ENDC} - Exit XenoSploit Framework")
        print()
    
    def list_tools(self, category=None):
        table_width = 100
        header = f"{Colors.BOLD}{'ID':<4} {'NAME':<25} {'CATEGORY':<25} {'STATUS':<12} {'DESCRIPTION':<50}{Colors.ENDC}"
        separator = "-" * table_width
        
        print(f"\n{Colors.CYAN}[*] Available Tools:{Colors.ENDC}")
        print(separator)
        print(header)
        print(separator)
        
        for tool in self.tools:
            if category and tool.category != category:
                continue
            
            status = f"{Colors.GREEN}[INSTALLED]" if tool.installed else f"{Colors.RED}[NOT INSTALLED]"
            print(f"{tool.id:<4} {tool.name:<25} {tool.category:<25} {status:<30} {tool.description[:50]}{Colors.ENDC}")
        
        print(separator)
        print()
    
    def search_tools(self, keyword):
        if not keyword:
            print(f"{Colors.RED}[!] Please provide a search keyword{Colors.ENDC}")
            return
        
        results = []
        for tool in self.tools:
            if (
                keyword.lower() in tool.name.lower() or
                keyword.lower() in tool.category.lower() or
                keyword.lower() in tool.description.lower()
            ):
                results.append(tool)
        
        if not results:
            print(f"{Colors.RED}[!] No tools found matching '{keyword}'{Colors.ENDC}")
            return
        
        table_width = 100
        header = f"{Colors.BOLD}{'ID':<4} {'NAME':<25} {'CATEGORY':<25} {'STATUS':<12} {'DESCRIPTION':<50}{Colors.ENDC}"
        separator = "-" * table_width
        
        print(f"\n{Colors.CYAN}[*] Search Results for '{keyword}':{Colors.ENDC}")
        print(separator)
        print(header)
        print(separator)
        
        for tool in results:
            status = f"{Colors.GREEN}[INSTALLED]" if tool.installed else f"{Colors.RED}[NOT INSTALLED]"
            print(f"{tool.id:<4} {tool.name:<25} {tool.category:<25} {status:<30} {tool.description[:50]}{Colors.ENDC}")
        
        print(separator)
        print()
    
    def show_tool_info(self, tool_id):
        try:
            tool_id = int(tool_id)
            tool = next((t for t in self.tools if t.id == tool_id), None)
            
            if not tool:
                print(f"{Colors.RED}[!] Tool with ID {tool_id} not found{Colors.ENDC}")
                return
            
            status = f"{Colors.GREEN}INSTALLED" if tool.installed else f"{Colors.RED}NOT INSTALLED"
            
            print(f"\n{Colors.CYAN}[*] Tool Information:{Colors.ENDC}")
            print(f"{Colors.YELLOW}ID:{Colors.ENDC} {tool.id}")
            print(f"{Colors.YELLOW}Name:{Colors.ENDC} {tool.name}")
            print(f"{Colors.YELLOW}Category:{Colors.ENDC} {tool.category}")
            print(f"{Colors.YELLOW}Status:{Colors.ENDC} {status}{Colors.ENDC}")
            print(f"{Colors.YELLOW}Command:{Colors.ENDC} {tool.command}")
            print(f"{Colors.YELLOW}Description:{Colors.ENDC} {tool.description}")
            print(f"{Colors.YELLOW}Install Command:{Colors.ENDC} {tool.install_cmd}")
            print()
            
        except ValueError:
            print(f"{Colors.RED}[!] Invalid tool ID{Colors.ENDC}")
    
    def install_tool(self, tool_id):
        try:
            tool_id = int(tool_id)
            tool = next((t for t in self.tools if t.id == tool_id), None)
            
            if not tool:
                print(f"{Colors.RED}[!] Tool with ID {tool_id} not found{Colors.ENDC}")
                return
            
            if tool.installed:
                print(f"{Colors.YELLOW}[!] Tool '{tool.name}' is already installed{Colors.ENDC}")
                return
            
            # Check if running as root
            if os.geteuid() != 0:
                print(f"{Colors.RED}[!] This operation requires root privileges. Please run as root.{Colors.ENDC}")
                return
            
            tool.install()
            
        except ValueError:
            print(f"{Colors.RED}[!] Invalid tool ID{Colors.ENDC}")
    
    def run_tool(self, tool_id, args=None):
        try:
            tool_id = int(tool_id)
            tool = next((t for t in self.tools if t.id == tool_id), None)
            
            if not tool:
                print(f"{Colors.RED}[!] Tool with ID {tool_id} not found{Colors.ENDC}")
                return
            
            tool.run(args)
            
        except ValueError:
            print(f"{Colors.RED}[!] Invalid tool ID{Colors.ENDC}")
    
    def show_installed_tools(self):
        installed_tools = [tool for tool in self.tools if tool.installed]
        
        if not installed_tools:
            print(f"{Colors.YELLOW}[!] No tools are currently installed{Colors.ENDC}")
            return
        
        table_width = 80
        header = f"{Colors.BOLD}{'ID':<4} {'NAME':<25} {'CATEGORY':<25} {'DESCRIPTION':<50}{Colors.ENDC}"
        separator = "-" * table_width
        
        print(f"\n{Colors.CYAN}[*] Installed Tools:{Colors.ENDC}")
        print(separator)
        print(header)
        print(separator)
        
        for tool in installed_tools:
            print(f"{tool.id:<4} {tool.name:<25} {tool.category:<25} {tool.description[:50]}")
        
        print(separator)
        print()
    
    def check_installation_status(self):
        print(f"\n{Colors.CYAN}[*] Checking tool installation status...{Colors.ENDC}")
        
        for tool in self.tools:
            tool.installed = tool.check_installed()
            status = f"{Colors.GREEN}[INSTALLED]" if tool.installed else f"{Colors.RED}[NOT INSTALLED]"
            print(f"{Colors.YELLOW}[*]{Colors.ENDC} {tool.name:<25} {status}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}[*] Check completed{Colors.ENDC}")
    
    def update_framework(self):
        print(f"{Colors.YELLOW}[*] Checking for updates...{Colors.ENDC}")
        print(f"{Colors.GREEN}[*] Current version: {self.version}{Colors.ENDC}")
        
        try:
            print(f"{Colors.GREEN}[*] XenoSploit will be updated from: {self.update_url}{Colors.ENDC}")
            print(f"{Colors.YELLOW}[*] This feature is not fully implemented yet. Please check the repository for updates:{Colors.ENDC}")
            print(f"{Colors.BLUE}{self.update_url}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}[!] Update failed: {str(e)}{Colors.ENDC}")
    
    def parse_command(self, command):
        if not command:
            return
        
        args = command.split()
        cmd = args[0].lower()
        
        if cmd == "help":
            self.print_menu()
        
        elif cmd == "list":
            if len(args) > 1:
                try:
                    category_index = int(args[1]) - 1
                    if 0 <= category_index < len(self.categories):
                        self.list_tools(self.categories[category_index])
                    else:
                        print(f"{Colors.RED}[!] Invalid category index{Colors.ENDC}")
                except ValueError:
                    category_name = " ".join(args[1:])
                    if category_name in self.categories:
                        self.list_tools(category_name)
                    else:
                        print(f"{Colors.RED}[!] Category '{category_name}' not found{Colors.ENDC}")
            else:
                self.list_tools()
        
        elif cmd == "search":
            if len(args) > 1:
                self.search_tools(" ".join(args[1:]))
            else:
                print(f"{Colors.RED}[!] Please provide a search keyword{Colors.ENDC}")
        
        elif cmd == "info":
            if len(args) > 1:
                self.show_tool_info(args[1])
            else:
                print(f"{Colors.RED}[!] Please provide a tool ID{Colors.ENDC}")
        
        elif cmd == "install":
            if len(args) > 1:
                self.install_tool(args[1])
            else:
                print(f"{Colors.RED}[!] Please provide a tool ID{Colors.ENDC}")
        
        elif cmd == "run":
            if len(args) > 1:
                tool_id = args[1]
                tool_args = " ".join(args[2:]) if len(args) > 2 else None
                self.run_tool(tool_id, tool_args)
            else:
                print(f"{Colors.RED}[!] Please provide a tool ID{Colors.ENDC}")
        
        elif cmd == "update":
            self.update_framework()
        
        elif cmd == "installed":
            self.show_installed_tools()
        
        elif cmd == "check":
            self.check_installation_status()
        
        elif cmd == "clear":
            self.clear_screen()
            self.print_banner()
        
        elif cmd == "exit":
            print(f"{Colors.GREEN}[*] Exiting XenoSploit Framework. Goodbye!{Colors.ENDC}")
            sys.exit(0)
        
        else:
            print(f"{Colors.RED}[!] Unknown command: {cmd}{Colors.ENDC}")
            print(f"{Colors.YELLOW}[*] Type 'help' to see available commands{Colors.ENDC}")
    
    def run(self):
        signal.signal(signal.SIGINT, self.handle_exit)
        
        # Check if running as root
        if os.geteuid() != 0:
            print(f"{Colors.YELLOW}[!] Warning: Some features require root privileges{Colors.ENDC}")
        
        self.clear_screen()
        self.print_menu()
        
        while True:
            try:
                user_input = input(f"{Colors.GREEN}XenoSploit{Colors.BLUE} ➤ {Colors.ENDC}")
                self.parse_command(user_input)
            except Exception as e:
                print(f"{Colors.RED}[!] Error: {str(e)}{Colors.ENDC}")
    
    def handle_exit(self, sig, frame):
        print(f"\n{Colors.GREEN}[*] Exiting XenoSploit Framework. Goodbye!{Colors.ENDC}")
        sys.exit(0)

if __name__ == "__main__":
    framework = XenoSploit()
    framework.run()
