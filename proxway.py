import hashlib
import requests
import base64

class PW:
    def __init__(self, login: str = "admin", passwd: str = "admin", serv_addr: str = "localhost"):
        self.passwd = passwd
        self.login = login
        self.host = serv_addr

    def __get_ssid(self) -> str:
        password_hash = hashlib.md5(f'{self.passwd}'.encode()).hexdigest().upper()
        password_hash += "F593B01C562548C6B7A31B30884BDE53"
        password_hash = hashlib.md5(password_hash.encode()).hexdigest().upper()
        password_hash = hashlib.md5(password_hash.encode()).hexdigest().upper()
        json = {
            "PasswordHash": password_hash,
            "UserName": self.login
        }
        query_str = "/json/Authenticate"
        return requests.post(f"{self.host}{query_str}", json=json).json()["UserSID"]

    def __logout(self, ssid: str):
        query_str = "/json/Logout"
        data = {
            "UserSID": ssid,
        }
        requests.post(f"{self.host}{query_str}", json=data)

    def get_users_list(self):
        ssid = self.__get_ssid()
        data = {
            "UserSID": ssid
        }
        query_str = '/json/EmployeeGetList'
        result = requests.post(f"{self.host}{query_str}", json=data).json()["Employee"]
        self.__logout(ssid)
        return result

    def get_departaments_list(self):
        ssid = self.__get_ssid()
        data = {
            "UserSID": ssid
        }
        query_str = '/json/DepartmentGetAll'
        result = requests.post(f"{self.host}{query_str}", json=data).json()["Department"]
        self.__logout(ssid)
        return result

    def get_card_list(self, user_pw_id):
        ssid = self.__get_ssid()
        data = {
            "UserSID": ssid,
            "UserToken": user_pw_id
        }
        query_str = '/json/CardGetList'
        result = requests.post(f"{self.host}{query_str}", json=data).json()["Card"]
        self.__logout(ssid)
        return result

    def get_biometric_identificator(self, user_pw_id):
        ssid = self.__get_ssid()
        data = {
            "UserSID": ssid,
            "UserToken": user_pw_id
        }
        query_str = '/json/BiometricIdentifierGetList'
        result = requests.post(f"{self.host}{query_str}", json=data).json()["BiometricIdentifier"][0]["Token"]
        query_str = '/json/BiometricIdentifierGetData'
        data = {
            "UserSID": ssid,
            "Token": result
        }
        result = requests.post(f"{self.host}{query_str}", json=data).json()["Data"]
        self.__logout(ssid)
        return base64.b64decode(result.encode("UTF-8"))
