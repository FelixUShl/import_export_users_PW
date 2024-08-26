from proxway import PW
# Настройки доступа к ProxWay
login = "admin"
passwd = "admin"
serv_addr = "http://big-b.xyz:40001"
pw = PW(login=login, passwd=passwd, serv_addr=serv_addr)

# Настройки файла импорта/экспорта
path_to_data = '' # Путь до файла, можно оставить пустым, если файл лежит в корневой папке скрипта
name_csv = 'data2.csv' # Имя файла

if path_to_data:
    path_to_data += '/'
data_csv = f'{path_to_data}{name_csv}'
