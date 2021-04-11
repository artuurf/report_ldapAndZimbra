import pythonzimbra.communication
from pythonzimbra.communication import Communication
import pythonzimbra.tools
from pythonzimbra.tools import auth



class GetZimbra():
    def __init__(self):
        hostname = 'webmail.inova.com.br'
        self.url = f'https://{hostname}:7071/service/admin/soap'
        self.usr = 'artur.santos@inova.net'
        self.__password = 'Art.854796'
        self.domain = 'inova.net'

        self.comm = Communication(self.url)

        self.__token = auth.authenticate(self.url, self.usr, self.__password, admin_auth=True)
        self.request = self.comm.gen_request(token=self.__token, set_batch=True)

    def getLdapZimbra(self):
        pass

    def getAllCos(self):
        """Retorna todos os COS do ambiente"""
        self.request.add_request(
            "GetAllCosRequest",
            {
            },
            "urn:zimbraAdmin"
        )
        response = self.comm.send_request(self.request)
        if not response.is_fault():
            allcos = response.get_response(1)['GetAllCosResponse']['cos']
            return [{k: v for k, v in cos.items() if k == 'name' or k == 'id'} for cos in allcos] # Retornar somente name e ID do COS
        else:
            return f'Error getAllCos: {response.get_fault_message()}'
    
    def getAllDomains(self):
        """Retornar todos os dominios do ambiente"""
        pass

    def countAccount(self):
        """Limite de COS por dominio"""
        self.request.add_request(
           'CountAccountRequest',
           {
                "domain": {
                    "_content": self.domain,
                    "by": "name"
                }
            },
            'urn:zimbraAdmin'
        )
        response = self.comm.send_request(self.request)
        if not response.is_fault():
            countcos = response.get_response(1)
            return countcos 
        else:
            return f'Error CountAccount: {response.get_fault_message()}'


if __name__ == '__main__':
    zmteste = GetZimbra()
    print(zmteste.getAllCos())  

"""       
    def getQuota(self):
        self.request.add_request(
            "GetQuotaUsageRequest",
            {   
                "domain": self.domain,
                "allServers": "1"
            },
            "urn:zimbraAdmin"
        )
        response = self.comm.send_request(self.request)
        if not response.is_fault():
            return response.get_response()['GetQuotaUsageResponse']['account']
        else:
            return f'Error getQuota: {response.get_fault_message()}'



[{cos['pudim'], cos['goiaba']} for cos in listcos]
result = [{'seila', 'seilaoq'}, {'seilaoto', 'seioto'}]
"""
