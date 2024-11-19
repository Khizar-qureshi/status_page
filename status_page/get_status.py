''''
get_status.py
Returns status of One Move Chess Components
'''

import os
import time
import requests
from status_param import Https, status_data

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

def update_status():
    home_status_info = check_http_status(status_data["home"]["url"])
    register_status_info = check_http_status(status_data["register"]["url"])
    login_status_info = check_http_status(status_data["login"]["url"])

    status_data["home"]["status"] = home_status_info
    status_data["register"]["status"] = register_status_info
    status_data["login"]["status"] = login_status_info

    return home_status_info["status"] and register_status_info["status"] and login_status_info["status"]
