import os
import time


def kill_api():
    print("Starting to kill api...")
    os.system('ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com "sudo killall dotnet"')
    time.sleep(3)
    print("API on VM1 has been killed.")
    time.sleep(10)
    
def kill_webui():
    print("Starting to kill web ui...")
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-web.northcentralus.cloudapp.azure.com sudo killall dotnet")
    time.sleep(3)
    print("Web UI on VM2 has been killed.")
    time.sleep(10)


'''
#note: don't use this until we back up the db
def drop_games_from_db():
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com sqlite3 /home/azureuser/.config/OneMoveChess.db 'DROP TABLE games'")
def rename_db():
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com mv /home/azureuser/.config/OneMoveChess.db /home/azureuser/.config/OneMoveChess-Moved.db")
'''
