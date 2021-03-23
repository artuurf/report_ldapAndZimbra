from PySimpleGUI import PySimpleGUI as sg


class WindowReport:
    def __init__(self):
        # Layout
        sg.theme('Reddit')
        self.attr = []
        self.addd = ''
        self.atr_zimbra = [
            'mail', 'displayName', 'zimbraAccountStatus', 'zimbraMailAlias',
            'zimbraCOSId', 'zimbraLastLogonTimestamp', 'zimbraLastLogonTimestamp'
        ]
        text = [
            'Selecione ou digite o atributo para adicionar uma nova coluna na planilha.',
            'Digite o dominio para buscar'
        ]

        self.layout = [
            [sg.Text('Endereço LDAP:', size=(15, 1)), sg.Input(key='address', size=(20, 1)), sg.Text('Porta:'),
             sg.Input(key='port', size=(5, 1), default_text='389')],
            [sg.Text('Senha:', size=(15, 1)), sg.Input(key='password', password_char='*', size=(20, 1))],
            [sg.Text('Domínio:', size=(15, 1)), sg.Input(key='domain', size=(20, 1), tooltip=text[1])],
            [sg.Text('Atributo:', size=(15, 1)), sg.Combo(self.atr_zimbra, size=(30, 1), key='attr', tooltip=text[0]),
             sg.Button('Adicionar'), sg.Button('Limpar')],
            [sg.Checkbox('Adicionar o dominio em uma coluna?', key='add_domain')],
            [sg.Text('Selecione o destino do arquivo:')],
            [sg.InputText(key='path_report'), sg.FolderBrowse()],
            [sg.Button('Buscar', key='button')],
            [sg.Output(size=(70, 10))]

        ]
        # Window
        self.janela = sg.Window('Gerar relatórios', self.layout, icon=r'icon.png')

    def start(self):
        while True:
            # Search
            self.button, self.values = self.janela.Read(100)

            if self.button == 'Adicionar':
                self.attr.append(self.values['attr'])
                print(f'Coluna(s) da planilha: {self.attr}')
            elif self.button == 'Limpar':
                self.attr = []
                print('Colunas vazias.')
            elif self.button == 'button':
                if not self.attr:
                    print('Não há o que buscar, selecione um atributo e click em adicionar.')
                else:
                    print('Buscando e gerando relatório...\n'
                          f'Relatório gerado com SUCESSO em:\n{self.values["path_report"]}')
                    if self.values['add_domain']:
                        print('domain add')
            elif self.button == sg.WIN_CLOSED:
                break
        self.janela.close()



tela = WindowReport()
tela.start()
