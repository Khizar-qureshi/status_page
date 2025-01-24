''''
get_status.py
Returns status of One Move Chess Components
'''

import os
import time
import csv
import pandas as pd
import requests
import sys
from status_param import Https, status_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from notify import send_alert_email
from collections import deque
from status_param import IP


def ping_vm_good(ip):
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        return {"status": True,
                "message": "VM is running with No errors"
                }
    else:
        return {"status": False,
                "message": "VM is running with No errors"
                }

def check_vm1_systemd():
    systemd_running = os.system("ssh azureuser@onemovechess-api.eastus2.cloudapp.azure.com pgrep -l systemd || true")
    if systemd_running == 0:
        return {"status": True,
                "message": "VM1 System Domain Up."
            }
    else:
        return {"status": False,
                "message": "ERROR: VM1 System Domain Down."
                }
    
    
def check_vm2_systemd():
    systemd_running = os.system("ssh azureuser@onemovechess-web.northcentralus.cloudapp.azure.com pgrep -l systemd || true")
    if systemd_running == 0:
        return {"status": True,
                "message": "VM2 System Domain Up."
                }
    else:
        return {"status": True, 
                "message": "ERROR: VM2 System Domain Down."
                }

def check_vm1_dotnet_running():
    dotnet_running = os.system("ssh azureuser@onemovechess-api.eastus2.cloudapp.azure.com pgrep -l dotnet || true")
    if dotnet_running == 0:
        return {"status": True, 'message': "VM1 Dotnet running."}
    else:
        return {"status": False, 'message': "ERROR: VM1 Dotnet is not running. "}

def check_vm2_dotnet_running():
    dotnet_running = os.system("ssh azureuser@onemovechess-web.northcentralus.cloudapp.azure.com pgrep -l dotnet || true")
    if dotnet_running == 0:
        return {"status": True, 'message': "VM2 Dotnet running."}
    else:
        return {"status": True, 'message': "ERROR: VM2 Dotnet is not running."}

def check_http_status(url: str):
    try:
        session = requests.Session()
        response = session.get(url, allow_redirects=True)

        final_url = response.url
        print(f"Final URL after redirects: {final_url}")

        if final_url == Https.url_login and url != Https.url_login:
            print(f"Redirected to login page: {final_url}")
            return {
                "status": False,
                "code": response.status_code,
                "message": "Redirected to login page",
                "final_url": final_url
            }

        elif response.status_code == 200:
            print(f"Status code: {response.status_code} - Reached the correct page")
            return {
                "status": True,
                "code": response.status_code,
                "message": "Page loaded successfully",
                "final_url": final_url
            }

        else:
            print(f"Website returned status code: {response.status_code}")
            return {
                "status": False,
                "code": response.status_code,
                "message": f"Error: Unexpected status code {response.status_code}",
                "final_url": final_url
            }

    except requests.exceptions.RequestException as e:
        # for errors
        print(f"An error occurred: {e}")
        return {
            "status": False,
            "code": None,
            "message": f"Request failed with error: {e}",
            "final_url": None
        }

# created a global variable to check if a message has already been sent.
# I don't want it sending us emails constantly if something is down, just one is fine.
prev_failed_services = set() 

def update_status():
    global prev_failed_services
    vm1_info = ping_vm_good(IP.VM1_IP)
    vm2_info = ping_vm_good(IP.VM2_IP)
    home_status_info = check_http_status(status_data["home"]["url"])
    register_status_info = check_register_status()
    login_status_info = check_login_status()
    vm1_sd_info = check_vm1_systemd()
    vm2_sd_info = check_vm2_systemd()
    vm1_dotnet_info = check_vm1_dotnet_running()
    vm2_dotnet_info = check_vm2_dotnet_running()


    status_data["home"]["status"] = home_status_info["status"]
    status_data["home"]["message"] = home_status_info["message"]
    status_data["home"]["code"] = home_status_info["code"]
    status_data["register"]["status"] = register_status_info["status"]
    status_data["register"]["message"] = register_status_info["message"]
    status_data["login"]["status"] = login_status_info["status"]
    status_data["login"]["message"] = login_status_info["message"]
    status_data["vm1"]["status"] = vm1_info["status"]
    status_data["vm1"]["message"] = vm1_info["message"]
    status_data["vm2"]["status"] = vm1_info["status"]
    status_data["vm2"]["message"] = vm1_info["message"]
    status_data["vm1_systemd"]["status"] = vm1_sd_info["status"]
    status_data["vm1_systemd"]["message"] = vm1_sd_info["message"]
    status_data["vm2_systemd"]["status"] = vm2_sd_info["status"]
    status_data["vm2_systemd"]["message"] = vm2_sd_info["message"]
    status_data["vm1_dotnet"]["status"] = vm1_dotnet_info["status"]
    status_data["vm1_dotnet"]["message"] = vm1_dotnet_info["message"]
    status_data["vm2_dotnet"]["status"] = vm2_dotnet_info["status"]
    status_data["vm2_dotnet"]["message"] = vm2_dotnet_info["message"]


    
    
    # this checks which parts are failing
    failed_services = set()
    if not home_status_info["status"]:
        failed_services.add("home")
    if not register_status_info["status"]:
        failed_services.add("register")
    if not login_status_info["status"]:
        failed_services.add("login")

    # Update status history (status_history.csv)
    # Updates the history CSV to reflect a failure on the status page history 
    # Also adds a new row in the history CSV when a new day starts
    df = pd.read_csv("status_history.csv")
    current_time = time.time()
    last_entry_time = df.at[0, "start_of_day"]
    if current_time >= last_entry_time + 86400:
        new_default_row = pd.DataFrame({
            "start_of_day": [last_entry_time + 86400], 
            "status": [1]
            })
        df = pd.concat([new_default_row, df], ignore_index=True)
        df.to_csv("status_history.csv", index=False)
        df = pd.read_csv("status_history.csv")
    if failed_services:
        df.at[0, "status"] = 0
        df.to_csv("status_history.csv", index=False) 
    # End of status history code

    # Emailing service
    if failed_services != prev_failed_services:
        if failed_services:
            subject = "ALERT: Service Failures Detected"
            details = []
            for service in failed_services:
                s = status_data[service]
                details.append(f"{service.capitalize()} page error: {s['message']}")
            body = "\n".join(details)
            send_alert_email(subject, body)
        else:
            subject = "All services recovered"
            body = "All services are now healthy."
            send_alert_email(subject, body)

        prev_failed_services = failed_services.copy()

    return len(failed_services) == 0


def get_status_history(days: int) -> list:
    '''
    days: number of days worth of statuses to retrieve
    '''
    return_queue = deque([])
    with open("status_history.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) # skip the header
        row_count = sum(1 for row in reader)
        if days > row_count: 
            days = row_count
        
        csvfile.seek(0) # Put reader back to start
        header = next(reader) # skip header

        for row in range(days):
            status = bool(int(next(reader)[1]))  # csv stores status as 0 or 1
            return_queue.appendleft(status)

    return list(return_queue)
    

def signup_status():
    return


def valid_bot_password():
    return Https.BOT["botname"] != None


def check_register_status():   
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://onemovechess-web.northcentralus.cloudapp.azure.com/')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(Https.url_register)

        username = driver.find_element(By.ID, 'newUserName')
        username.send_keys('BOT_TEST_REGISTER')
        time.sleep(1)
        signupcode = driver.find_element(By.ID, 'signUpCode')
        signupcode.send_keys('Carleton comps 2024-2025!')
        time.sleep(1)
        
        submit = driver.find_element(By.ID, 'registerUserButton')
        submit.click()
        time.sleep(5)
        
        password_block = driver.find_element(By.ID, 'passwordBlock')
        if password_block.is_displayed():
            generated_password = driver.find_element(By.ID, 'newPassword').get_attribute("value")
            print("Registered account successfully, PASSWORD: ",generated_password)
            Https.BOT["password"] = generated_password
        else:
            print("No password shown")
            time.sleep(2)
            driver.quit()
            return {"status": False,
                    "message": "Registration Failed. Errror: No password shown"}
        time.sleep(2)
        driver.quit()
        return {"status": True,
                "message": "Registration Successful"
            }
    except Exception as e:
        print(e)
        driver.quit()
        return {"status": False,
                "message": f'Register Bot Failed. Error: {e}'}
    

def check_login_status():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://onemovechess-web.northcentralus.cloudapp.azure.com/')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(Https.url_login)

        username = driver.find_element(By.ID, 'userName')
        username.send_keys(Https.BOT["botname"])
        time.sleep(1)
        
        signupcode = driver.find_element(By.ID, 'password')
        signupcode.send_keys(Https.BOT["password"])
        time.sleep(1)
        submit = driver.find_element(By.ID, 'loginButton')
        submit.click()
        time.sleep(2)
        login_block = driver.find_element(By.ID, 'accountLink')

        if Https.BOT["botname"] in login_block.text:
            print("Login created successfully")
        else:
            print("Invalid Login")
            return {
                "status":False,
                "message": "Login Unsuccessful",
                }
        #time.sleep(10)
        driver.quit()
        
        return {
            "status": True,
            "message": "Login Successful",
        }
    except Exception as e:
        print(e)
        return {
            "status":False,
            "message": f'Login Bot Unsuccessful Error: {e}',
        }
        

# include only if you want pop up:
#check_login_status() 
#check_register_status()
