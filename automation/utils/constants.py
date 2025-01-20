from dataclasses import dataclass
import random

@dataclass
class Login:
    username = "testbot2"
    password = "O-u+dw7e2O960Yjq=ZJ$-^4e"
    cookies_file_path = "automation/utils/cookies.json"
    link = "http://onemovechess-web.northcentralus.cloudapp.azure.com/Login"

class Time:
    def sleep():
        return random.uniform(2, 4)
