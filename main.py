from babel import Locale
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivymd.navigationdrawer import NavigationLayout
from kivymd.theming import ThemeManager

from app.models import db
from app.util import TELAS
from app.views.configuracao import Configuracao
from app.views.contatos import (TelaContatos, TelaEditarContato, TelaNovoContato,
                                TelaVisualizarContato)
from app.views.inicio import Home
from app.views.sobre import Sobre
from app.views.transacoes import (TelaNovaTransacao, TelaTransacoes, TelaVisualizarTransacao,
                                  TelaEditarTransacao)
from iconfonts import create_fontdict_file, register
from settings import ICONFONTS, FONTS, LOCALE

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
            self.ids.scr_mngr.switch_to(TelaContatos(name=screen.name))

        elif screen == TELAS.NOVO_CONTATO:
            self.ids.scr_mngr.switch_to(TelaNovoContato(name=screen.name))

        elif screen == TELAS.DETALHE_CONTATO:
            contato_id = kwargs.get('contato_id', None)
            self.ids.scr_mngr.switch_to(
                TelaVisualizarContato(name=screen.name, contato_id=contato_id))

        elif screen == TELAS.EDITAR_CONTATO:
            contato_id = kwargs.get('contato_id', None)
            self.ids.scr_mngr.switch_to(TelaEditarContato(name=screen.name, contato_id=contato_id))

        elif screen == TELAS.LISTA_TRANSACAO:
            self.ids.scr_mngr.switch_to(TelaTransacoes(name=screen.name))

        elif screen == TELAS.NOVA_TRANSACAO:
            self.ids.scr_mngr.switch_to(TelaNovaTransacao(name=screen.name))

        elif screen == TELAS.DETALHE_TRANSACAO:
            transacao_id = kwargs.get('transacao_id', None)
            self.ids.scr_mngr.switch_to(
                TelaVisualizarTransacao(name=screen.name, transacao_id=transacao_id))

        elif screen == TELAS.EDITAR_TRANSACAO:
            transacao_id = kwargs.get('transacao_id', None)
            self.ids.scr_mngr.switch_to(
                TelaEditarTransacao(name=screen.name, transacao_id=transacao_id))

        elif screen == TELAS.CONFIGURACAO:
            self.ids.scr_mngr.switch_to(Configuracao(name=screen.name))

        elif screen == TELAS.SOBRE:
            self.ids.scr_mngr.switch_to(Sobre(name=screen.name))


class MeuBolsoApp(App):
    theme_cls = ThemeManager()
    locale = ObjectProperty()

    def build(self):
        self.db = db
        self.locale = Locale(LOCALE)
        return self.root


if __name__ == '__main__':
    MeuBolsoApp().run()
