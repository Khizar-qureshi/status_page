from dataclasses import dataclass

@dataclass
class Https:
    url_home= "http://onemovechess-web.northcentralus.cloudapp.azure.com/"
    url_register= "http://onemovechess-web.northcentralus.cloudapp.azure.com/Register"
    url_login= "http://onemovechess-web.northcentralus.cloudapp.azure.com/login"
    BOT = {"botname": "testbot2", "password": "O-u+dw7e2O960Yjq=ZJ$-^4e"}

@dataclass
class IP:
    VM1_IP = '52.225.235.130'
    VM2_IP = '65.52.239.81'

status_data = {
    "home": {"status": None, "url": Https.url_home},
    "register": {"status": None, "url": Https.url_register},
    "login": {"status": None, "url": Https.url_login}
}
