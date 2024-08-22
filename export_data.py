import os
from proxway import PW

login = "admin"
passwd = "admin"
serv_addr = "http://big-b.xyz:40001"
pw = PW(login=login, passwd=passwd, serv_addr=serv_addr)


def get_departament_list():
    row_list = pw.get_departaments_list()
    result = []
    for row in row_list:
        result.append({'Token': row['Token'],
                       'Name': row['Name'],
                       'ParentToken': row['ParentToken'],
                       })
    return result


def get_user_identifiers(user_id):
    cards = pw.get_card_list(user_id)
    biometric_identifiers_id = pw.get_biometric_identifiers_list(user_id)
    result = {'cards': [], 'biometric_identifiers': []}
    if cards:
        for card in cards:
            if card['IdentifierType'] == 0:
                code = card['Code'].lstrip('0')
                while code[0:2] == 'FF':
                    code = code[2:]
                result['cards'].append({'Code': code,
                                        'Name': card['Name'],
                                        'AntipassbackDisabled': card['AntipassbackDisabled'],
                                        'Disalarm': card['Disalarm'],
                                        'PIN': card['PIN'],
                                        'Security': card['Security'],
                                        'Status': card['Status'],
                                        'VIP': card['VIP'],
                                        'ValidTo': card['ValidTo'],
                                        'ValidFrom': card['ValidFrom']
                                        })
    if biometric_identifiers_id:
        if not os.path.isdir('biometric'):
            os.mkdir('biometric')
        for biometric_identifier_id in biometric_identifiers_id:
            biometric_identifier = pw.get_biometric_identifier(biometric_identifier_id)
            file_path = f"biometric/{biometric_identifier_id}.png"
            with open(file_path, "wb") as image:
                image.write(biometric_identifier)
            result['biometric_identifiers'].append(file_path)
    return result


def get_user_properties(user):
    identifiers = get_user_identifiers(user['Token'])
    result = [{'Имя Сотрудника': user['Name'],
               'Отдел': user['DepartmentName'],
               'Вышестоящий отдел': '',
               'Имя карты': '',
               'Код карты': '',
               'Статус': '',
               'Antipassback': '',
               'Disalarm': '',
               'Security': '',
               'VIP': '',
               'PIN': '',
               'Действителен с': '',
               'Действителен по': '',
               'Фото сотрудника': '',
               }]

    if identifiers['cards']:
        for card_n in range(len(identifiers['cards'])):
            card = identifiers['cards'][card_n]
            if card_n == 0:
                result = list()
            for key in card.keys():
                if card[key] is False:
                    card[key] = 0
                elif card[key] is True:
                    card[key] = 1

            result.append({'Имя Сотрудника': user['Name'],
                           'Отдел': user['DepartmentName'],
                           'Имя карты': card['Name'],
                           'Код карты': card['Code'],
                           'Статус': card['Status'],
                           'Antipassback': card['AntipassbackDisabled'],
                           'Disalarm': card['Disalarm'],
                           'Security': card['Security'],
                           'VIP': card['VIP'],
                           'PIN': card['PIN'],
                           'Действителен с': card['ValidFrom'],
                           'Действителен по': card['ValidTo'],
                           'Фото сотрудника': ''
                           })
    if identifiers['biometric_identifiers']:
        result[0]['Фото сотрудника'] = identifiers['biometric_identifiers'][0]
    return result


def get_parent_dept(dept_name, depts_list):
    for dept in depts_list:
        if dept_name == dept['Name']:
            for parent in depts_list:
                if dept['ParentToken'] == parent['Token']:
                    return parent['Name']
    return ""


def export():
    deps = get_departament_list()
    users = pw.get_users_list()
    export_data = ('Имя Сотрудника;Отдел;Вышестоящий отдел;Имя карты;Код карты;Статус;Antipassback;Disalarm;Security;'
                   'VIP;PIN;Фото сотрудника\n')
    for user in users:
        data = get_user_properties(user)

        export_data += (f"{data[0]['Имя Сотрудника']};"
                        f"{data[0]['Отдел']};"
                        f"{get_parent_dept(data[0]['Отдел'], deps)};"
                        f"{data[0]['Имя карты']};"
                        f'{data[0]['Код карты']};'
                        f'{data[0]['Статус']};'
                        f'{data[0]['Antipassback']};'
                        f'{data[0]['Disalarm']};'
                        f'{data[0]['Security']};'
                        f'{data[0]['VIP']};'
                        f'{data[0]['PIN']};'
                        # f'{data[0]['Действителен с']};'
                        # f'{data[0]['Действителен по']};'
                        f'{data[0]['Фото сотрудника']}'
                        f"\n")

        if len(data) > 1:
            for row in data[1:]:
                export_data += (f";;;"
                                f"{row['Имя карты']};"
                                f'{row['Код карты']};'
                                f'{row['Статус']};'
                                f'{row['Antipassback']};'
                                f'{row['Disalarm']};'
                                f'{row['Security']};'
                                f'{row['VIP']};'
                                f'{row['PIN']};'
                                # f'{row['Действителен с']};'
                                # f'{row['Действителен по']};'
                                f"\n")
    with open("data.csv", "w") as f:
        f.write(export_data[:-1])