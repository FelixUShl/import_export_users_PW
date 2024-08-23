from config import pw

from pprint import pprint


def get_data_from_csv(path_to_csv):
    row_data = ''
    data = list()
    with open(path_to_csv, 'r') as f:
        row_data = f.read().split('\n')
    if row_data[0] != ('Имя Сотрудника;Отдел;Вышестоящий отдел;Имя карты;Код карты;Статус;Antipassback;Disalarm;'
                       'Security;VIP;PIN;Фото сотрудника'):
        return False
    for row in row_data[1:]:
        if row == '': break
        row = row.split(';')
        card = None
        if row[4]:
            card = {'Имя карты': row[3],
                    'Код карты': row[4],
                    'Статус': int(row[5]),
                    'Antipassback': int(row[6]),
                    'Disalarm': int(row[7]),
                    'Security': int(row[8]),
                    'VIP': int(row[9]),
                    'PIN': row[10]
                    }
        if not (row[0] and row[1]):
            data[-1]['Карты'].append(card)
        else:
            data.append({
                'Имя Сотрудника': row[0],
                'Отдел': row[1],
                'Вышестоящий отдел': row[2],
                'Карты': [card],
                'Фото сотрудника': row[11]
                        })

    return data


def create_depts(data_from_csv):
    dept_list = list()
    depts_in_pw = pw.get_departaments_list()
    for row in data_from_csv:
        if [row['Отдел'], row['Вышестоящий отдел']] not in dept_list:
            dept_list.append([row['Отдел'], row['Вышестоящий отдел']])
    for dept_elem in range(len(dept_list)):
        dept_id =int()
        for dept_in_pw in depts_in_pw:
            if dept_list[dept_elem][0] == dept_in_pw['Name']:
                dept_id = dept_in_pw['Token']
                in_pw = False
                break
        if not dept_id:
            dept_id = pw.set_departament(dept_list[dept_elem][0])
        dept_list[dept_elem] = {'Отдел': dept_list[dept_elem][0],
                                'Вышестоящий отдел': dept_list[dept_elem][1],
                                'dept_id': dept_id}
    print (dept_list)
    for dept in dept_list:
        if dept['Вышестоящий отдел']:
            for parent_dept in dept_list:
                if dept['Вышестоящий отдел'] == parent_dept['Отдел']:
                    pw.set_departament(name=dept['Отдел'], self_id=dept['dept_id'], parent_id=parent_dept['dept_id'])
        else:
            pw.set_departament(name=dept['Отдел'], self_id=dept['dept_id'])
    return dept_list


def create_users(data_from_csv):
    depts_list = create_depts(data_from_csv)
    users_list = pw.get_users_list()
    for emploee in data_from_csv:
        pass




def import_data():
    data = get_data_from_csv('data.csv')
    create_depts(data)


import_data()
