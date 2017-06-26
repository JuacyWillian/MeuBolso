import json
import os

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivymd.navigationdrawer import NavigationLayout
from kivymd.theming import ThemeManager

from app.models import db
from app.util import TELAS
from app.views.configuracao import Configuracao
from app.views.contatos import ContactList, EditContact, NewContact, \
    ViewContact
from app.views.inicio import Home
from app.views.sobre import Sobre
from app.views.transacoes import NewTransaction, TransactionList, \
    ViewTransaction
from iconfonts import create_fontdict_file, register
from settings import DATABASE_CONFIG, DATABASE_ARGS, LANGUAGE, datadir, \
    ICONFONTS, FONTS

for font in ICONFONTS:
    create_fontdict_file(font['css'], font['fontd'])
    register(font['name'], font['prefix'], font['ttf'], font['fontd'])

for font in FONTS:
    LabelBase.register(**font)


class MyRootLayout(NavigationLayout):
    def __init__(self, **kwargs):
        super(MyRootLayout, self).__init__(**kwargs)
        self.pp = App.get_running_app()

    def switch_to(self, screen, **kwargs):

        if screen == TELAS.INICIO:
            self.ids.scr_mngr.switch_to(Home(name=screen.name))

        elif screen == TELAS.LISTA_CONTATO:
            self.ids.scr_mngr.switch_to(ContactList(name=screen.name))

        elif screen == TELAS.NOVO_CONTATO:
            self.ids.scr_mngr.switch_to(NewContact(name=screen.name))

        elif screen == TELAS.DETALHE_CONTATO:
            id = kwargs.get('id', None)
            self.ids.scr_mngr.switch_to(
                ViewContact(name=screen.name, id=id))

        elif screen == TELAS.EDITAR_CONTATO:
            id = kwargs.get('id', None)
            self.ids.scr_mngr.switch_to(
                EditContact(name=screen.name, id=id))

        elif screen == TELAS.LISTA_TRANSACAO:
            self.ids.scr_mngr.switch_to(TransactionList(name=screen.name))

        elif screen == TELAS.NOVA_TRANSACAO:
            self.ids.scr_mngr.switch_to(NewTransaction(name=screen.name))

        elif screen == TELAS.DETALHE_TRANSACAO:
            id = kwargs.get('id', None)
            self.ids.scr_mngr.switch_to(
                ViewTransaction(name=screen.name, id=id))

        elif screen == TELAS.CONFIGURACAO:
            self.ids.scr_mngr.switch_to(Configuracao(name=screen.name))

        elif screen == TELAS.SOBRE:
            self.ids.scr_mngr.switch_to(Sobre(name=screen.name))


class MeuBolsoApp(App):
    theme_cls = ThemeManager()
    basedir = StringProperty()

    def build(self):
        self.db = db
        self.db.bind(*DATABASE_CONFIG, **DATABASE_ARGS)
        self.db.generate_mapping(create_tables=True)
        self.load_strings()
        return self.root

    def load_strings(self):
        with open(os.path.join(datadir, 'languages', "%s.json" % LANGUAGE),
                  'r')as lang:
            self.strings = json.load(lang)


if __name__ == '__main__':
    MeuBolsoApp().run()
