import socket
import sys
from colorama import Fore


host = "10.1.1.41"  # Replace with the target IP or hostname
port = 22


def check_ssh(ip,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        print("[" + Fore.RED + "Checking SSH Service" + Fore.RESET + "] " + Fore.WHITE +  f"Port {port} is open" + Fore.RESET)
        banner = s.recv(1024).decode().strip()
        print("[" + Fore.RED + "SSH Version" + Fore.RESET + "] " + banner)
        s.close()
    except socket.error:
        print("[" + Fore.RED + "Checking SSH Service" + Fore.RESET + "] " + Fore.WHITE +  f"Port {port} is closed" + Fore.RESET)
        print("[" + Fore.RED + "Initiating Program Shutdown" + Fore.RESET + "] " + "Goodbye")
        sys.exit()
