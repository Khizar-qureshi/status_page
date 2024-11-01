''''
get_status.py
Returns status of One Move Chess Components
'''

import os

def ping_vm_good(ip):
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        return True
    else:
        return False
    
