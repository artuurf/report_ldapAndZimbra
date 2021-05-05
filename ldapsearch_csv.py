import ldap
from csv import DictWriter
import datetime


class LdapSearch:
    def __init__(self, address_ldap, port, password, path_archive, domain, atributo, typesearch=True, members=False):
        self.__address_ldap = address_ldap  #  endereço host LDAP
        self.__user = 'uid=zimbra,cn=admins,cn=zimbra'
        self.__password = password  
        self.__domain = domain
        self.typesearch = typesearch
        # self.__base = f"dc={',dc='.join(domain.split('.'))}"  # 'dc=domain,dc=com' 
        self.__path_archive = path_archive 
        self.__ldap_filter = f'(&(objectclass=zimbraAccount)(|{"".join([f"(mail=*@{d})" for d in self.__domain.split(",")]).replace(" ", "")}))' if self.typesearch else f'(&(objectClass=zimbraDistributionList)(|{"".join([f"(mail=*@{d})" for d in self.__domain.split(",")]).replace(" ", "")}))' # search domain accounts if true, if not list 
        self.__port = port
        self.__members = members

        self.today = datetime.datetime.now().date()

        self.__atributo = atributo  # ['displayName', 'zimbraLastLogonTimestamp'] 

        if self.__members and not self.typesearch:
            self.__atributo.append('zimbraMailForwardingAddress')
        self.__result = []      

    def start(self):

        # Iniciar conexão
        try:
            connection = ldap.initialize(f'ldap://{self.__address_ldap}:{self.__port}')
            connection.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)
            connection.protocol_version = ldap.VERSION3
            connection.bind_s(self.__user, self.__password)

        except ldap.INVALID_CREDENTIALS as C:
            connection.unbind()
            return f'Credenciais inválidas: \n{C}'
        except ldap.UNWILLING_TO_PERFORM as P:
            connection.unbind()
            return f'Senha inválida: \n{P}'
        except ldap.SERVER_DOWN as S:
            return f'Erro na conexão LDAP: \n{S}'

        # Efetuando a busca

        self.__result = connection.search_s('', ldap.SCOPE_SUBTREE, self.__ldap_filter, self.__atributo)
        connection.unbind()


        # Ajustando a planilha com o resultado

        with open(f'{self.__path_archive}Relatório_{self.today}.csv', 'w') as archive:
            data_csv = DictWriter(archive, fieldnames=self.__atributo)
            data_csv.writeheader()
            for account in self.__result:
                if self.typesearch:
                    dict_comprehension = {chave: valor[0].decode('utf-8') for chave, valor in account[1].items()}
                else:     
                    dict_comprehension = {chave: [v.decode('utf-8') for v in valor] for chave, valor in account[1].items()}

                if 'zimbraLastLogonTimestamp' in dict_comprehension.keys(): # Configurar data do ultimo login
                    data = dict_comprehension['zimbraLastLogonTimestamp']
                    date_br = datetime.datetime(
                    int(data[:4]),
                    int(data[4:6]),
                    int(data[6:8]),
                    int(data[8:10]),
                    int(data[10:12]),
                    int(data[12:14])
                    ).strftime('%d/%m/%Y %H:%M')

                    dict_comprehension['zimbraLastLogonTimestamp'] = date_br

                if 'zimbraCreateTimestamp' in dict_comprehension.keys(): # Configurar data de criação
                    data1 = dict_comprehension['zimbraCreateTimestamp']
                    date1_br = datetime.datetime(
                    int(data1[:4]),
                    int(data1[4:6]),
                    int(data1[6:8]),
                    int(data1[8:10]),
                    int(data1[10:12]),
                    int(data1[12:14])
                    ).strftime('%d/%m/%Y %H:%M')

                    dict_comprehension['zimbraCreateTimestamp'] = date1_br

                data_csv.writerow(dict_comprehension)

        return f'Planilha criada com SUCESSO! \nRelatório_{self.today}'


"""
        # Conectar zimbra e buscar COSNAME

        if 'zimbraCOSId' in self.__atributo:
            zmgetcos = GetZimbra()
            allcos = zmgetcos.getAllCos()


                if 'zimbraCOSId' in dict_comprehension.keys(): # Configurar nome do COS
                    cosid = dict_comprehension['zimbraCOSId']
                    cosname = [cos['name'] for cos in allcos if cosid == cos['id']]

                    dict_comprehension['zimbraCOSId'] = cosname[0]
"""
