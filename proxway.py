import hashlib
import requests
import base64


class PW:
    def __init__(self, login: str = "admin", passwd: str = "admin", serv_addr: str = "localhost"):
        def get_hash(passwd):
            password_hash = hashlib.md5(passwd.encode()).hexdigest().upper()
            password_hash += "F593B01C562548C6B7A31B30884BDE53"
            password_hash = hashlib.md5(password_hash.encode()).hexdigest().upper()
            return hashlib.md5(password_hash.encode()).hexdigest().upper()

        self.passwd = get_hash(passwd)
        self.login = login
        self.host = serv_addr

    def __get_ssid(self) -> str:

        json = {
            "PasswordHash": self.passwd,
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
            "UserToken": user_pw_id,
            'UserTokenUsed': True
        }
        query_str = '/json/CardGetList'
        result = requests.post(f"{self.host}{query_str}", json=data).json()["Card"]
        self.__logout(ssid)
        return result

    def get_biometric_identifiers_list(self, user_pw_id):
        ssid = self.__get_ssid()
        data = {
            "UserSID": ssid,
            "UserToken": user_pw_id
        }
        query_str = '/json/BiometricIdentifierGetList'
        result = requests.post(f"{self.host}{query_str}", json=data).json()
        biometric_identifiers_list = []
        if not result["BiometricIdentifier"]:
            return biometric_identifiers_list
        else:
            for biometric_identifier in result["BiometricIdentifier"]:
                biometric_identifiers_list.append(biometric_identifier["Token"])
        return biometric_identifiers_list

    def get_biometric_identifier(self, identifier_id):
        ssid = self.__get_ssid()
        query_str = '/json/BiometricIdentifierGetData'
        data = {
            "UserSID": ssid,
            "Token": identifier_id
        }
        result = requests.post(f"{self.host}{query_str}", json=data).json()["Data"]
        self.__logout(ssid)
        return base64.b64decode(result.encode("UTF-8"))


