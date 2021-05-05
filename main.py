import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
###

from PySimpleGUI import PySimpleGUI as sg
from ldapsearch_csv import LdapSearch
from comm_zimbra import GetZimbra


class WindowReport:
    def __init__(self):
        sg.theme('Reddit')
        self.attr_l = []
        self.attr_z = []
        self.atr_ldap = [
            'mail', 'displayName', 'zimbraAccountStatus', 'zimbraMailAlias',
            'zimbraLastLogonTimestamp', 'zimbraCreateTimestamp',
            'zimbraPrefMailForwardingAddress'
        ]
        self.atr_zimbra = [
            'name', 'displayName','zimbraCOSId', 'zimbraAccountStatus', 'zimbraMailAlias',
            'zimbraLastLogonTimestamp', 'zimbraCreateTimestamp',
            'zimbraPrefMailForwardingAddress'
        ]
        text = [
            'Selecione ou digite o atributo para adicionar uma nova coluna na planilha.\n'
            'mail: Email\ndisplayName: Nome exibição\nZimbraAccountStatus: Status da conta\nzimbraMailAlias: Alias\n'
            'zimbraCOSId: COS\nZimbraLastLogonTimestamp: Data do último acesso\nZimbraCreateTimestamp: Data da criação\n'
            'zimbraPrefMailForwardingAddres: Endereço(s) encaminhamento',
            'Digite o(s) dominio(s) para buscar separados por virgula.'
        ]

        self.l_tabldap = [
            [sg.Text('Endereço LDAP:', size=(15, 1)), sg.Input(key='address', size=(30, 1)), sg.Text('Porta:'),
             sg.Input(key='port', size=(5, 1), default_text='389'), sg.Text('Tipo do relatório:', justification='center', size=(17, 1))],
            [sg.Text('Senha:', size=(15, 1)), sg.Input(key='password', password_char='*', size=(30, 1)), sg.T(' '*15),
            sg.Radio('Conta.', "typesearch", default=True, key='account')],
            [sg.Text('Domínio(s):', size=(15, 1)), sg.Input(key='domain', size=(30, 1), tooltip=text[1]), sg.T(' '*15),
            sg.Radio('Lista de distribuição.', "typesearch", key='list')],
            [sg.T(' '*102), sg.Checkbox('Membros', key='add_members')],
            [sg.Text('Atributo:', size=(15, 1)), sg.Combo(self.atr_ldap, size=(30, 1), key='attr', tooltip=text[0]),
             sg.Button('Adicionar', key='add_atrldap'), sg.Button('Limpar', key='clearldap')],
            [sg.Text('Selecione o destino do arquivo:')],
            [sg.InputText(key='path_report'), sg.FolderBrowse()],
            [sg.Button('Buscar', key='buttonldap')]     
        ]

        self.l_tabzimbra = [
            [sg.Text('Host Zimbra:', size=(15, 1)), sg.Input(key='hostzm', size=(30, 1)), sg.T(' '*7), sg.Text('Tipo do relatório:', justification='center')],
            [sg.Text('Conta admin:', size=(15, 1)), sg.Input(key='accountzm', size=(30, 1) ), sg.T(' '*5),
            sg.Radio('Conta.', "tsearch_zm", default=True, key='typeaccount')],
            [sg.Text('Senha:', size=(15, 1)), sg.Input(key='passwordzm', password_char='*', size=(30, 1)), sg.T(' '*5),
            sg.Radio('Licenças por dominio.', "tsearch_zm", key='typelicense_d')],
            [sg.Text('Domínio(s):', size=(15, 1)), sg.Input(key='domainzm', size=(30, 1), tooltip=text[1]), sg.T(' '*5),
            sg.Radio('Lista de distribuição.', "tsearch_zm", key='typelist', disabled=True)],
            [sg.T(' '*91), sg.Radio('Dominios do ambiente', "tsearch_zm", key='typedomain')],
            [sg.Text('Atributo:', size=(15, 1)), sg.Combo(self.atr_zimbra, size=(30, 1), key='attrzm', tooltip=text[0]),
             sg.Button('Adicionar', key='add_atrzm'), sg.Button('Limpar', key='clearzm')],
            [sg.Checkbox('Adicionar o dominio em uma coluna', key='add_domainzm')],
            [sg.Checkbox('Adicionar quota', key='add_quota')],
            [sg.Text('Salvar o arquivo em:')],
            [sg.InputText(key='path_reportzm'), sg.FolderBrowse()],
            [sg.Button('Buscar', key='buttonzm')]
        ]

        self.layout = [
            [sg.T(' '*40), sg.Image(r'data/blue.gif', key = "image")],
            [sg.TabGroup([[sg.Tab('Ldapsearch', self.l_tabldap), sg.Tab('Zimbra',self.l_tabzimbra)]], tab_location='center')],
            [sg.Output(size=(75, 10))] 
        ]

        # Window
        self.janela = sg.Window('Relatórios', self.layout, icon=r'data/icon.png')
        

    def start(self):

        while True:
            # Search
            self.button, self.values = self.janela.Read(50)
            self.janela.FindElement("image").UpdateAnimation("data/blue.gif",time_between_frames=50)

            # LDAP

            if self.values['list']:
                self.janela['add_members'].update(disabled=False)
            else:
                self.janela['add_members'].update(disabled=True)
                self.janela['add_members'].update('')

            if self.button == 'add_atrldap':
                self.attr_l.append(self.values['attr'])
                print(f'Coluna(s) da planilha: {self.attr_l}')
            elif self.button == 'clearldap':
                self.attr_l = []
                print('Sem colunas.')
            elif self.button == 'buttonldap':
                if self.values['domain'] == '' or self.values['domain'] == ' ':
                    print('Digite um domínio para buscar.')
                elif not self.attr_l:
                    print('Não há o que buscar, selecione um atributo e click em adicionar.')
                
                else:
                    print('Buscando...')
                    buscando_ldap = LdapSearch(
                        self.values['address'], self.values['port'], self.values['password'],
                        self.values['path_report'], self.values['domain'], self.attr_l,
                        self.values['account']
                    )
                    print(buscando_ldap.start())
                    print(self.values["path_report"])

            # Zimbra 

            if self.values['typedomain']:
                self.janela['domainzm'].update(disabled=True)
                self.janela['add_quota'].update(disabled=True)
                self.janela['domainzm'].update('')
            else: 
                self.janela['domainzm'].update(disabled=False)
                self.janela['add_quota'].update(disabled=False)

            if self.values['typelicense_d'] or self.values['typelist'] or self.values['typedomain']:
                self.janela['attrzm'].update(disabled=True)
                self.janela['attrzm'].update('')
                self.attr_z = []
                self.janela['add_domainzm'].update(False)
                self.janela['add_quota'].update(False)
                self.janela['add_atrzm'].update(disabled=True)
                self.janela['clearzm'].update(disabled=True)
                self.janela['add_quota'].update(disabled=True)
                self.janela['add_domainzm'].update(disabled=True)
                
            else: 
                self.janela['attrzm'].update(disabled=False)
                self.janela['add_atrzm'].update(disabled=False)
                self.janela['clearzm'].update(disabled=False)
                self.janela['add_quota'].update(disabled=False)
                self.janela['add_domainzm'].update(disabled=False)
            

            if self.button == 'add_atrzm':
                self.attr_z.append(self.values['attrzm'])
                print(f'Coluna(s) da planilha: {self.attr_z}')
            elif self.button == 'clearzm':
                self.attr_z = []
                print('Sem colunas.')
            elif self.button == 'buttonzm':

                if self.values['domainzm'] == '' and not self.values['typedomain']:
                    
                    print('Digite um domínio para buscar.')
                
                
                else:
                    print('Conectando...')
                    # chamar objeto zimbra
                    c_zimbra = GetZimbra(
                        self.values['hostzm'], self.values['accountzm'], self.values['passwordzm'],
                        self.values['domainzm'], self.values['path_reportzm'], self.attr_z, self.values['add_domainzm'], self.values['add_quota'],
                        self.values['path_reportzm']
                    )
                    if c_zimbra.connect() == 'Conectado':
                        # conta
                        if self.values['typeaccount']:
                            if not self.attr_z:
                                print('Não há o que buscar, selecione um atributo e click em adicionar.')
                            else:    
                                print(c_zimbra.getFormatted(c_zimbra.getAllAccounts()))

                        # licença por dominio
                        elif self.values['typelicense_d']:
                            print(c_zimbra.formatedPlan(c_zimbra.countAccount()))

                        # lista de distribuição

                        # dominios por ambiente
                        elif self.values['typedomain']:
                            print(c_zimbra.formatedPlan(c_zimbra.getAllDomains()))

                        print(self.values['path_reportzm'])
                    
                    else: 
                        print(c_zimbra.connect())


            if self.button == sg.WIN_CLOSED:
                break
        self.janela.close()


if __name__ == '__main__':
    tela = WindowReport()
    tela.start()
