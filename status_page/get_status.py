''''
get_status.py
Returns status of One Move Chess Components
'''

import os
import time
import requests
from status_param import Https, status_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from notify import send_alert_email

def ping_vm_good(ip):
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        return True
    else:
        return False
    
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
    
    home_status_info = check_http_status(status_data["home"]["url"])
    register_status_info = check_http_status(status_data["register"]["url"])
    login_status_info = check_http_status(status_data["login"]["url"])

    status_data["home"]["status"] = home_status_info
    status_data["register"]["status"] = register_status_info
    status_data["login"]["status"] = login_status_info

    # this checks which parts are failing
    failed_services = set()
    if not home_status_info["status"]:
        failed_services.add("home")
    if not register_status_info["status"]:
        failed_services.add("register")
    if not login_status_info["status"]:
        failed_services.add("login")


    if failed_services != prev_failed_services:
        if failed_services:
            subject = "ALERT: Service Failures Detected"
            details = []
            for service in failed_services:
                s = status_data[service]["status"]
                details.append(f"{service.capitalize()} page error: {s['message']}")
            body = "\n".join(details)
            send_alert_email(subject, body)
        else:
            subject = "All services recovered"
            body = "All services are now healthy."
            send_alert_email(subject, body)

        prev_failed_services = failed_services.copy()

    return len(failed_services) == 0

def signup_status():
    return


def valid_bot_password():
    return Https.BOT["botname"] != None


def check_register_status():   
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('-ignore-certificate-errors')
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
            return False
        time.sleep(2)
        driver.quit()
        return True
    except Exception as e:
        print(e)
        return False
    

def check_login_status():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('-ignore-certificate-errors')
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
