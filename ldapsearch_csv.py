import ldap
from csv import DictWriter
import datetime


class LdapSearch:
    def __init__(self, address_ldap, port, password, path_archive, domain, atributo, add_domain=False, typesearch=True):
        self.__address_ldap = address_ldap  #  endereço host LDAP
        self.__user = 'uid=zimbra,cn=admins,cn=zimbra'
        self.__password = password  
        self.__domain = domain
        # self.__base = f"dc={',dc='.join(domain.split('.'))}"  # 'dc=domain,dc=com' 
        self.__path_archive = path_archive 
        self.__ldap_filter = f'(&(objectclass=zimbraAccount)(|{"".join([f"(mail=*@{d})" for d in domain.split(",")]).replace(" ", "")})' if typesearch else f'(&(objectClass=zimbraDistributionList)(|{"".join([f"(mail=*@{d})" for d in domain.split(",")]).replace(" ", "")}))' # search domain accounts if true, if not list 
        self.__port = port
        self.__add_domain = add_domain

        self.today = datetime.datetime.now().date()

        self.__atributo = atributo  # ['displayName', 'zimbraLastLogonTimestamp'] 

        self.__result = []      

    def start(self):
        if self.__add_domain:
            if 'mail' in self.__atributo:
                self.__atributo.insert(1, 'domain')
            else:
                return "Só é possivel adicionar o dominio se adicionar atributo 'mail'"

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
                dict_comprehension = {chave: valor[0].decode('utf-8') for chave, valor in account[1].items()}
                if self.__add_domain:
                    dict_comprehension['domain'] = dict_comprehension['mail'].split('@')[1]
                if 'zimbraLastLogonTimestamp' in dict_comprehension.keys():
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

                if 'zimbraCreateTimestamp' in dict_comprehension.keys():
                    data = dict_comprehension['zimbraCreateTimestamp']
                    date_br = datetime.datetime(
                    int(data[:4]),
                    int(data[4:6]),
                    int(data[6:8]),
                    int(data[8:10]),
                    int(data[10:12]),
                    int(data[12:14])
                    ).strftime('%d/%m/%Y %H:%M')

                    dict_comprehension['zimbraCreateTimestamp'] = date_br

                data_csv.writerow(dict_comprehension)

        return f'Planilha criada com SUCESSO! \nRelatório_ {self.today}'
        