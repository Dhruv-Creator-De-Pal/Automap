from curses.ascii import ctrl
import subprocess
import os
import agent 
import rootcheck
import nmapcheck
import ollama

#welcome screen 
print("Welcome to the Automap")

print("Starting the pre operation check list ")

#checking the root
print("Root check.......")
if rootcheck.rootcheck() == True:
    print("Root check.......done")
else:
    print("Abort...i reapeat abort....")
    print("Sorry but looks like you need to run this script as root ")
    exit()

#nmap check
print("nmap check.......")
if nmapcheck.nmapchk() == True:
    print("nmap check.......Done")
    print("Good to go......going for ollama")
else:
    print("Abort...i reapeat abort....")
    print("nmap is not installed in your system and it is a must for this script to work")
    exit()

#ollama check 
print("Please enter the ip of the ollama server")
llm_link=input("Enter the link here in such format http://(your link):(portnumber)/: ")

print("Ollama check.......")
if agent.check_ollama(llm_link) == True:
    print("Ollama check.......done")
    
    # Get models list
    models_data = agent.llm_model(llm_link)
    if models_data and 'models' in models_data:
        models = [m['name'] for m in models_data['models']]
        print("\nAvailable models:")
        for model in models:
            print(f"  - {model}")
#The user will enter the model here         
        usr_model = input("\nPlease enter the model name: ").strip()
        target = input("\nEnter the Target IP address or range (e.g., 192.168.1.0/24): ").strip()
        
        nmapcheck.work(target)
        devices = agent.parse_xml("scan.xml")
        stats = agent.analyze_data(devices)
        insights = agent.get_ai_insights(devices, stats, usr_model, llm_link)
        report_file = agent.save_report(devices, stats, insights, target)
        print(f"✅ Report saved: {report_file}")
        nmapcheck.work(target)
    else:
        print("Abort...i reapeat abort....")
        print("Either there was a problem with ollama or there is no model installd in the ollama")
        print("Try again after checking the ollama")
        exit()
else:
    print("Abort...i reapeat abort....")
    print("Ollama is not present in the link given pls check again")
    exit()


