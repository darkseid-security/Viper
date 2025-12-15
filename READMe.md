Viper V1.2
================
Viper is a SSH Multi-Threaded Brute force Framework
 
Features
=============
- Multi Threaded using multiprocessing can use a maximum of 5 Threads
- Easy to configure 
- Adjustable Threads
- Visual UI including progress bar
- When password is cracked program will attempt to upload a file to set path
- [*New Feature] added SSH detection on port 22
- [*New Feature] added SSH version detection 
 
TODO
===========
Improve exploit detection

Note
=========
- If threads set to 5 if someone logs in to SSH while brute-forcing program will crash.
- Add own windows executable to /Files/updater.png and update variable malware.

Run
========
- Generate payloads/files and put in Files folder
- Edit config in Viper.py script to set to target
