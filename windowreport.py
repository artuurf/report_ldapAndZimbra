from PySimpleGUI import PySimpleGUI as sg


class WindowReport:
    def __init__(self):
        # Layout
        sg.theme('Reddit')
        self.atr_zimbra = [
            'mail', 'displayName', 'zimbraAccountStatus', 'zimbraMailAlias',
             'zimbraCOSId', 'zimbraLastLogonTimestamp', 'zimbraLastLogonTimestamp'
        ]

        layout = [
            [sg.Text('Endereço LDAP:', size=(15, 1)), sg.Input(key='address', size=(20, 1)), sg.Text('Porta:'), sg.Input(key='port', size=(5, 1), default_text='389')],
            [sg.Text('Senha:', size=(15, 1)), sg.Input(key='password', password_char='*', size=(20, 1))],
            [sg.Text('Domínio:', size=(15, 1)), sg.Input(key='domain', size=(20, 1))],
            [sg.Text('Atributo:', size=(15, 1)), sg.Combo(self.atr_zimbra, size=(30, 1), key='attr')],
            [sg.Checkbox('Salvar o login?', key='save')],
            [sg.Text('Selecione o destino do arquivo:')],
            [sg.InputText(), sg.FolderBrowse()],
            [sg.Button('Buscar', key='button')],
            # [sg.Image(r'Loading.gif')],
            [sg.Output(size=(50, 10))]

        ]

        # Window
        self.janela = sg.Window('Gerar relatórios', layout)

    def start(self):
        print(help(self.janela))
        while True:
            # Search
            self.button, self.values = self.janela.Read()
            user = self.values['address']
            print(f'{user}')
            if self.values == sg.WIN_CLOSED:
                break
        self.janela.close()


tela = WindowReport()
tela.start()


