import os


def kill_api()
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-api.eastus2.cloudapp.azure.com pkill dotnet")

def kill_webui()
    os.system("ssh -i ~/.ssh/VM-Key.pem azureuser@onemovechess-web.northcentralus.cloudapp.azure.com pkill dotnet")

