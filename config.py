from proxway import PW

login = "admin"
passwd = "admin"
serv_addr = "http://dellwin:40001"
pw = PW(login=login, passwd=passwd, serv_addr=serv_addr)

path_to_data = ''
name_csv = 'data.csv'

if path_to_data:
    path_to_data += '/'
data_csv = f'{path_to_data}{name_csv}'
