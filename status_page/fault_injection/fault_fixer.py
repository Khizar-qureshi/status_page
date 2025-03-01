import os
import time

def restart_api():
    print("Starting to restart API...")
    os.system('ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com "sudo killall dotnet; cd /opt/OneMoveChess; nohup dotnet OneMoveChess.Api.dll 1> /var/log/onemovechess.log 2> /var/log/onemovechess.log &"')
    time.sleep(3)
    print("API has been restarted on VM1.")
    time.sleep(10)

def restart_webui():
    print("Starting to restart webui...")
    os.system('ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-web.northcentralus.cloudapp.azure.com "sudo killall dotnet; cd /opt/OneMoveChess; nohup dotnet OneMoveChess.WebUI.dll 1> /var/log/onemovechess.log 2> /var/log/onemovechess.log &"')
    time.sleep(3)
    print("Web UI has been restarted on VM2.")
    time.sleep(10)

''' 
def rename_db():
    os.system('ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com mv /home/azureuser/.config/*.db /home/azureuser/.config/OneMoveChess.db')
    restart_api()
'''


