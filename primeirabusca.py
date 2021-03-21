import ldap
from csv import DictWriter

# Endereços para conexão

address_ldap = '10.0.4.77'
user = 'uid=zimbra,cn=admins,cn=zimbra'
password = 'e7eq_Y3pA_'
base = 'dc=inova,dc=net'

# Iniciar conexão
try:
    connection = ldap.initialize(f'ldap://{address_ldap}')
    connection.protocol_version = ldap.VERSION3
    connection.bind(user, password)

except ldap.LDAPError as E:
    print(f'Erro na conexão LDAP: {E}')

# Efetuando a busca

ldap_filter = '(mail=artur.santos*)'
atributo = ['displayName', 'zimbraLastLogonTimestamp']

result = connection.search_s(base, ldap.SCOPE_SUBTREE, ldap_filter, atributo)


with open('listateste.csv', 'w') as arquivo:
    data_csv = DictWriter(arquivo, fieldnames=atributo)
    data_csv.writeheader()
    for account in result:
        dict_comprehension = {chave: str(valor).strip("'[b]'") for chave, valor in account[1].items()}
        data_csv.writerow(dict_comprehension)
        
print('Planilha criada com sucesso')

