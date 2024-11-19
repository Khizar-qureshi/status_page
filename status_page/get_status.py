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
    
def check_http_status(url: str) -> bool:
    session = requests.Session()
    response = session.get(url, allow_redirects=True)

    #check redirects        
    final_url = response.url  
    print(final_url)

    if final_url == Https.url_login and url != Https.url_login:
        print(f"Redirected to login page: {final_url}")
        return False
    elif response.status_code in [200]:
        print(f"Status code: {response.status_code} - Reached the correct page")
        return True
    else:
        print(f"Website returned status code: {response.status_code}")
        return False

def update_status():
    status_data["home"]["status"] = check_http_status(status_data["home"]["url"])
    status_data["register"]["status"] = check_http_status(status_data["register"]["url"])
    status_data["login"]["status"] = check_http_status(status_data["login"]["url"])
    return status_data["home"]["status"] and status_data["register"]["status"] and status_data["login"]["status"]



