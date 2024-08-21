from proxway import PW

login="admin"
passwd="admin"
serv_addr="http://big-b.xyz:40001"


def export():
    pass


def main():
    pw = PW(login=login, passwd=passwd, serv_addr=serv_addr)
    users_list = pw.get_users_list()
    for user in users_list:
        card = pw.get_card_list(user["Token"])
        face = pw.get_biometric_identifier()
        print(card)
        with open(f"{user["Name"]}.png", "wb") as image:
            image.write(face)


if __name__ == "__main__":
    main()