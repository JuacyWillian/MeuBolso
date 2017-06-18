import os

from kivy.app import App
from kivy.properties import StringProperty

from kivymd.navigationdrawer import NavigationLayout
from kivymd.theming import ThemeManager

from app.models import db
from app.util import SCREENS
from app.views.about import AboutScreen
from app.views.contacts import ContactScreen, NewContactScreen, \
    ViewContactScreen, EditContactScreen
from app.views.home import HomeScreen
from app.views.incomes import IncomeScreen, NewIncomeScreen, ViewIncomeScreen
from app.views.settings import SettingsScreen

# basedir = os.path.abspath(os.path.dirname(__file__))


class MyRootLayout(NavigationLayout):
    def __init__(self, **kwargs):
        super(MyRootLayout, self).__init__(**kwargs)
        app = App.get_running_app()
        print (app)

    def switch_to(self, screen, **kwargs):
        if screen == SCREENS.HOME:
            self.ids.scr_mngr.switch_to(HomeScreen(name=screen.name))

        elif screen == SCREENS.CONTACT_LIST:
            self.ids.scr_mngr.switch_to(ContactScreen(name=screen.name))

        elif screen == SCREENS.NEW_CONTACT:
            self.ids.scr_mngr.switch_to(NewContactScreen(name=screen.name))

        elif screen == SCREENS.VIEW_CONTACT:
            uuid = kwargs.get('uuid', None)
            self.ids.scr_mngr.switch_to(
                ViewContactScreen(name=screen.name, uuid=uuid))

        elif screen == SCREENS.EDIT_CONTACT:
            uuid = kwargs.get('uuid', None)
            self.ids.scr_mngr.switch_to(
                EditContactScreen(name=screen.name, uuid=uuid))

        elif screen == SCREENS.TRANSACTION_LIST:
            self.ids.scr_mngr.switch_to(IncomeScreen(name=screen.name))

        elif screen == SCREENS.NEW_TRANSACTION:
            self.ids.scr_mngr.switch_to(NewIncomeScreen(name=screen.name))

        elif screen == SCREENS.VIEW_TRANSACTION:
            uuid = kwargs.get('uuid', None)
            self.ids.scr_mngr.switch_to(
                ViewIncomeScreen(name=screen.name, uuid=uuid))

        elif screen == SCREENS.SETTINGS:
            self.ids.scr_mngr.switch_to(SettingsScreen(name=screen.name))

        elif screen == SCREENS.ABOUT:
            self.ids.scr_mngr.switch_to(AboutScreen(name=screen.name))


class MeuBolsoApp(App):
    theme_cls = ThemeManager()
    basedir = StringProperty()

    def build(self):
        self.db = db
        self.db.bind('sqlite', 'database.db', create_db=True)
        self.db.generate_mapping(create_tables=True)
        # self.basedir = basedir

        return self.root


if __name__ == '__main__':
    MeuBolsoApp().run()
