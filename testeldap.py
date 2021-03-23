from csv import DictWriter

import datetime



class WindowReport:
    def __init__(self,):
        result = [('uid=artur.santos,ou=people,dc=inova,dc=net', {'displayName': [b'Artur Santos'], 'zimbraLastLogonTimestamp': [b'20210319184426Z']})]
        address_ldap = '10.0.4.77'
        user = 'uid=zimbra,cn=admins,cn=zimbra'
        password = ''
        base = 'dc=inova,dc=net'
        path_archive = 'listateste.csv'
        domain = ''

        atributo = ['displayName', 'zimbraLastLogonTimestamp']

"""
# windowreport:
        while True:
            eventos, valores = janela.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Entrar':
                if valores['usuario'] == 'artur' and valores['senha'] == '123456':
                    print('Funfo!')
"""

"""



atributo = ['displayName', 'zimbraLastLogonTimestamp']

# result = [('uid=thais.zuppo,ou=people,dc=inova,dc=net', {'givenName': [b'Thais'], 'displayName': [b'Thais Zuppo']}), ('uid=thais.santos,ou=people,dc=inova,dc=net', {'givenName': [b'Thais'], 'displayName': [b'ThaisSantos']})]




atr_comns = ['mail', 'displayName', 'zimbraAccountStatus', 'zimbraMailAlias',
             'zimbraCOSId', 'zimbraLastLogonTimestamp', 'zimbraLastLogonTimestamp'
]




for account in result:
    dict_comprehension = {chave: str(valor).strip("'[b]'") for chave, valor in account[1].items()}
    try:
        if 'zimbraLastLogonTimestamp' in atributo:
            data = dict_comprehension['zimbraLastLogonTimestamp']
            date_br = datetime.datetime(
                int(data[:4]),
                int(data[4:6]),
                int(data[6:8]),
                int(data[8:10]),
                int(data[10:12]),
                int(data[12:14])
            ).strftime('%d/%m/%Y %H:%M')
            dict_comprehension['zimbraLastLogonTimestamp'] = str(date_br)
            print(dict_comprehension)
    except KeyError as error:
        print(f'A busca {account} não possui: {error}')



    for count in range(len(atributo)):
        get_atributo = (str(account[1].get(atributo[count])).strip("'[b]'"))
        print(get_atributo)
        print(account[1])


with open('listateste.csv', 'w') as arquivo:
    data_csv = DictWriter(arquivo, fieldnames=atributo)
    data_csv.writeheader()
    for account in result:
        dict_comprehension = {chave: str(valor).strip("'[b]'") for chave, valor in account[1].items()}
        data_csv.writerow(dict_comprehension)
"""