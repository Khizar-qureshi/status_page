from dataclasses import dataclass
import random

@dataclass
class Login:
    username = "testbot2"
    password = "nL12^Cj3P=rcMq1Sw4Dq%!p2"
    cookies_file_path = "automation/utils/cookies.json"
    link = "http://onemovechess-web.northcentralus.cloudapp.azure.com/Login"

class Time:
    def sleep():
        return random.uniform(2, 4)
