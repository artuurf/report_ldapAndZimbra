import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
###

from PySimpleGUI import PySimpleGUI as sg
from ldapsearch_csv import LdapSearch


class WindowReport:
    def __init__(self):
        sg.theme('Reddit')
        self.attr = []
        self.atr_zimbra = [
            'mail', 'displayName', 'zimbraAccountStatus', 'zimbraMailAlias',
            'zimbraCOSId', 'zimbraLastLogonTimestamp', 'zimbraCreateTimestamp',
            'zimbraPrefMailForwardingAddress'
        ]
        text = [
            'Selecione ou digite o atributo para adicionar uma nova coluna na planilha.\n'
            'mail: Email\ndisplayName: Nome exibição\nZimbraAccountStatus: Status da conta\nzimbraMailAlias: Alias\n'
            'zimbraCOSId: COS\nZimbraLastLogonTimestamp: Data do último acesso\nZimbraCreateTimestamp: Data da criação\n'
            'zimbraPrefMailForwardingAddres: Endereço(s) encaminhamento',
            'Digite o(s) dominio(s) para buscar separados por virgula.'
        ]

        self.layout = [
            [sg.T(' '*40), sg.Image(r'data/blue.gif', key = "image")],
            [sg.Text('Endereço LDAP:', size=(15, 1)), sg.Input(key='address', size=(20, 1)), sg.Text('Porta:'),
             sg.Input(key='port', size=(5, 1), default_text='389'), sg.Text('Tipo do relatório:', justification='center', size=(20, 1))],
            [sg.Text('Senha:', size=(15, 1)), sg.Input(key='password', password_char='*', size=(20, 1)), sg.T(' '*25),
            sg.Radio('Conta.', "typesearch", default=True, key='account')],
            [sg.Text('Domínio(s):', size=(15, 1)), sg.Input(key='domain', size=(20, 1), tooltip=text[1]), sg.T(' '*25),
            sg.Radio('Lista de distribuição.', "typesearch", key='list')],
            [sg.Text('Atributo:', size=(15, 1)), sg.Combo(self.atr_zimbra, size=(30, 1), key='attr', tooltip=text[0]),
             sg.Button('Adicionar'), sg.Button('Limpar')],
            [sg.Checkbox('Adicionar o dominio em uma coluna?', key='add_domain')],
            [sg.Text('Selecione o destino do arquivo:')],
            [sg.InputText(key='path_report'), sg.FolderBrowse()],
            [sg.Button('Buscar', key='button')],
            [sg.Output(size=(75, 10))]

        ]
        # Window
        self.janela = sg.Window('Relatórios', self.layout, icon=r'data/icon.png')

    def start(self):
        while True:
            # Search
            self.button, self.values = self.janela.Read(50)
            self.janela.FindElement("image").UpdateAnimation("data/blue.gif",time_between_frames=50)

            if self.button == 'Adicionar':
                self.attr.append(self.values['attr'])
                print(f'Coluna(s) da planilha: {self.attr}')
            elif self.button == 'Limpar':
                self.attr = []
                print('Sem colunas.')
            elif self.button == 'button':
                if self.values['domain'] == '' or self.values['domain'] == ' ':
                    print('Digite um domínio para buscar.')
                elif not self.attr:
                    print('Não há o que buscar, selecione um atributo e click em adicionar.')
                
                else:
                    print('Buscando...')
                    buscando = LdapSearch(
                        self.values['address'], self.values['port'], self.values['password'],
                        self.values['path_report'], self.values['domain'], self.attr, self.values['add_domain'],
                        self.values['account']
                    )
                    print(buscando.start())
                    print(self.values["path_report"])
            elif self.button == sg.WIN_CLOSED:
                break
        self.janela.close()


if __name__ == '__main__':
    tela = WindowReport()
    tela.start()
