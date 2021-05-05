from csv import DictWriter
import datetime
import pythonzimbra.communication
from pythonzimbra.communication import Communication
import pythonzimbra.tools
from pythonzimbra.tools import auth
import urllib


class GetZimbra():
    def __init__(self, hostname, user, password, domain, pathzm, atributo, add_domain, quota, path_archive):
        self.url = f'https://{hostname}:7071/service/admin/soap'
        self.usr = user
        self.__password = password
        self.domain = domain.split(',')
        self.__atributo = atributo
        self.quota = quota
        self.__add_domain = add_domain
        self.__path_archive = path_archive

        self.today = datetime.datetime.now().date()
        self.colum = ['name']
        
    def connect(self):
        try:
            self.comm = Communication(self.url)

            self.__token = auth.authenticate(self.url, self.usr, self.__password, admin_auth=True)
            self.request = self.comm.gen_request(token=self.__token, set_batch=True)

            return 'Conectado'

        except urllib.error.URLError as E:
        # catastrophic error. bail.
            return f'Erro na conexão: {E}'


    def getAllDomains(self):
        """Retornar todos os dominios do ambiente"""
        self.request.add_request(
        'GetAllDomainsRequest',
        {
        },
            'urn:zimbraAdmin'
        )
        response = self.comm.send_request(self.request)
        if not response.is_fault():
            alldomains = response.get_response(1)['GetAllDomainsResponse']['domain']
            return [{k: v for k, v in cos.items() if k == 'name'} for cos in alldomains] # Retornar somente name do dominio

        else:
            return f'Error CountAccount: {response.get_fault_message()}'


    def countAccount(self):
        """Limite de COS por dominio"""
        for dom in self.domain:
            self.request.add_request(
            'CountAccountRequest',
            {
                    "domain": {
                        "_content": dom,
                        "by": "name"
                    }
                },
                'urn:zimbraAdmin'
            )
        response = self.comm.send_request(self.request)
        if not response.is_fault():
            allcount = response.get_response(1)['CountAccountResponse']
            l_domains = []
            d = 0

            if len(self.domain) > 1:
                for a in allcount:
                    cos = {}
                    cos.update({'name': self.domain[d]})
                    d =+ 1
                    for v in a['cos']:
                        cos.update({v['name']: v['_content']})
                        if v['name'] not in self.colum:
                            self.colum.append(v['name'])
                    l_domains.append(cos)
            else: 
                cos = {}
                cos.update({'name': self.domain[d]})
                for a in allcount['cos']:
                    cos.update({a['name']: a['_content']})
                    if a['name'] not in self.colum:
                        self.colum.append(a['name'])
                l_domains.append(cos)

            return l_domains

        else:
            return f'Error CountAccount: {response.get_fault_message()}'


    def getAllAccounts(self):
        """Consulta todas as contas por dominio"""

        if self.__add_domain:
            if 'name' in self.__atributo:
                self.__atributo.insert(1, 'domain')
            else:
                return "Só é possivel adicionar o dominio se adicionar o atributo 'name'"

        self.request.add_request(
            "GetAllAccountsRequest",
            {   
                "domain": {
                    "_content": self.domain[0],
                    "by": "name"
                }
            },
            "urn:zimbraAdmin"
        )
        self.request.add_request(
            "GetAllCosRequest",
            {
            },
            "urn:zimbraAdmin"
        )
        if self.quota:
            self.request.add_request(
                "GetQuotaUsageRequest",
                {   
                    "domain": self.domain[0],
                    "allServers": "1"
                },
                "urn:zimbraAdmin"
                )
        response = self.comm.send_request(self.request)
        
        if not response.is_fault():
            allAccounts = [response.get_response(1)['GetAllAccountsResponse']['account'],response.get_response(2)['GetAllCosResponse']['cos']]
            if self.quota:
                allAccounts.append(response.get_response(3)['GetQuotaUsageResponse']['account'])
            return allAccounts

        else:
            return f'Error getAllAccounts: {response.get_fault_message()}'


    def getFormatted(self, func=None):
        quota = ''
        lista_dict = []
        for account in func[0]:
            a_atr = {}
            a_atr['name'] = account['name']
            for atr in account['a']:
                if atr['n'] in self.__atributo:
                    a_atr[atr['n']] = atr['_content']
            lista_dict.append(a_atr)

        if 'zimbraCOSId' in self.__atributo:
            allcos = [{k: v for k, v in cos.items() if k == 'name' or k == 'id'} for cos in func[1]] 

        if self.quota:
            quota = func[2]
            for account in quota:
                account['used'] = f"{int(account['used'] / 1024 / 1024)} MB"
                account['limit'] = f"{int(account['limit'] / 1024 / 1024)} MB"
            [self.__atributo.append(i) for i in ['used', 'limit']]
            
        with open(f'{self.__path_archive}Relatório_{self.domain[0]}.csv', 'w') as archive:
            data_csv = DictWriter(archive, fieldnames=self.__atributo)
            data_csv.writeheader()
            for account in lista_dict:
                dict_comprehension = {chave: valor for chave, valor in account.items()}

                if self.__add_domain:
                    dict_comprehension['domain'] = dict_comprehension['name'].split('@')[1]

                if self.quota: # Configurar quota com as contas
                    for i in quota:
                        if i['name'] == account['name']:
                            dict_comprehension['used'] = i['used']
                            dict_comprehension['limit'] = i['limit']
                

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
                
                if 'zimbraCOSId' in dict_comprehension.keys(): # Configurar nome do COS
                    cosid = dict_comprehension['zimbraCOSId']
                    cosname = [cos['name'] for cos in allcos if cosid == cos['id']]

                    dict_comprehension['zimbraCOSId'] = cosname[0]

                data_csv.writerow(dict_comprehension)

        return f'Planilha criada com SUCESSO! \nRelatório_{self.today}'


    def formatedPlan(self, func):
        list_domains = func

        with open(f'{self.__path_archive}Relatório_{self.today}.csv', 'w') as archive:
            data_csv = DictWriter(archive, fieldnames=self.colum)
            data_csv.writeheader()
            for domain_count in list_domains:
                list_domains = {chave: valor for chave, valor in domain_count.items()}
                data_csv.writerow(list_domains)
        
        return f'Planilha criada com SUCESSO! \nRelatório_{self.today}'

"""

if __name__ == '__main__':
    zmteste = GetZimbra()
    #print(zmteste.geta())
    print(zmteste.connect())
    print(zmteste.getFormatted(zmteste.getAllAccounts()))


"""