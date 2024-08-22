import os
from proxway import PW

login = "admin"
passwd = "admin"
serv_addr = "http://big-b.xyz:40001"
pw = PW(login=login, passwd=passwd, serv_addr=serv_addr)


def departament_list():
    row_list = pw.get_departaments_list()
    result = []
    for row in row_list:
        result.append({'Token':row['Token'],
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
                result['cards'].append({'Code': card['Code'],
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
            result['biometric_identifiers'].append({'FilePath': file_path})
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
            'PIN':'',
            'Действителен с': '',
            'Действителен по': '',
            'Фото сотрудника': '',
            }]
    if len(identifiers['cards']):
        result[0]['Имя карты'] = identifiers['cards'][0]['Name'],
        result[0]['Код карты'] = identifiers['cards'][0]['Code'],
        result[0]['Статус'] = identifiers['cards'][0]['Status'],
        result[0]['Antipassback'] = identifiers['cards'][0]['AntipassbackDisabled'],
        result[0]['Disalarm'] = identifiers['cards'][0]['Disalarm'],
        result[0]['Security'] = identifiers['cards'][0]['Security'],
        result[0]['VIP'] = identifiers['cards'][0]['VIP'],
        result[0]['PIN'] = identifiers['cards'][0]['PIN'],
        result[0]['Действителен с'] = identifiers['cards'][0]['ValidFrom'],
        result[0]['Действителен по'] = identifiers['cards'][0]['ValidTo']
    if len(identifiers['cards']) > 1:
        for card in identifiers['cards'][1:]:
            result.append({'Имя Сотрудника': user['Name'],
                            'Отдел': user['DepartmentName'],
                            'Имя карты': card['Name'],
                            'Код карты': card['Code'],
                            'Статус': card['Status'],
                            'Antipassback': card['AntipassbackDisabled'],
                            'Disalarm': card['Disalarm'],
                            'Security': card['Security'],
                            'VIP': card['VIP'],
                            'PIN':card['PIN'],
                            'Действителен с': card['ValidFrom'],
                            'Действителен по': card['ValidTo']
                            })
    if identifiers['biometric_identifiers']:
        for biometric_identifier in identifiers['biometric_identifiers']:
            result[0]['Фото сотрудника'] = identifiers['biometric_identifiers'][0]
    return result



def export():
    deps = departament_list()
    users = pw.get_users_list()
    export_data = ('Имя Сотрудника;Отдел;Вышестоящий отдел;Имя карты;Код карты;Статус;Antipassback;Disalarm;Security;'
                   'VIP;PIN;Действителен с;Действителен по;Фото сотрудника\n')
    for user in users:
        data = get_user_properties(user)
        for row in data:
            export_data += (f''
                            Имя Сотрудника': user['Name'],
                            'Отдел': user['DepartmentName'],
                            'Имя карты': card['Name'],
                            'Код карты': card['Code'],
                            'Статус': card['Status'],
                            'Antipassback': card['AntipassbackDisabled'],
                            'Disalarm': card['Disalarm'],
                            'Security': card['Security'],
                            'VIP': card['VIP'],
                            'PIN':card['PIN'],
                            'Действителен с': card['ValidFrom'],
                            'Действителен по': card['ValidTo']')




def main():
    users_list = pw.get_users_list()
    for user in users_list:
        print(user['Name'], pw.get_card_list(user['Token']))


if __name__ == "__main__":
    main()
