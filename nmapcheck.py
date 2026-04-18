import subprocess 
import os
import platform
import ollama



# nmap check if installed 
def nmapchk():
    try:
        subprocess.run(["nmap", "--version"], capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def work(target):
    print(f"Starting nmap scan on {target}...")
    try:
        tar_res=subprocess.run(["nmap" ,"-A" ,"-T4" ,"-oX" ,"scan.xml",target], capture_output=True, text=True, check=True)
        if tar_res.returncode ==0:
            print("Nmap scan completed successfully.")
            return True
        else:
            print("Nmap scan failed.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running nmap: {e}")
        return False
    
       