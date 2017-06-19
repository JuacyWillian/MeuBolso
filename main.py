from kivy.app import App
from kivy.properties import StringProperty
from kivymd.navigationdrawer import NavigationLayout
from kivymd.theming import ThemeManager

from app.models import db
from app.util import SCREENS
from app.views.about import About
from app.views.contacts import ContactList, NewContact, \
    ViewContact, EditContact
from app.views.home import Home
from app.views.settings import Setting
from app.views.transactions import TransactionList, NewTransaction, \
    ViewTransaction


class MyRootLayout(NavigationLayout):
    def __init__(self, **kwargs):
        super(MyRootLayout, self).__init__(**kwargs)
        app = App.get_running_app()

    def switch_to(self, screen, **kwargs):

        if screen == SCREENS.HOME:
            self.ids.scr_mngr.switch_to(Home(name=screen.name))

        elif screen == SCREENS.CONTACT_LIST:
            self.ids.scr_mngr.switch_to(ContactList(name=screen.name))

        elif screen == SCREENS.NEW_CONTACT:
            self.ids.scr_mngr.switch_to(NewContact(name=screen.name))

        elif screen == SCREENS.VIEW_CONTACT:
            uuid = kwargs.get('uuid', None)
            self.ids.scr_mngr.switch_to(
                ViewContact(name=screen.name, uuid=uuid))

        elif screen == SCREENS.EDIT_CONTACT:
            uuid = kwargs.get('uuid', None)
            self.ids.scr_mngr.switch_to(
                EditContact(name=screen.name, uuid=uuid))

        elif screen == SCREENS.TRANSACTION_LIST:
            self.ids.scr_mngr.switch_to(TransactionList(name=screen.name))

        elif screen == SCREENS.NEW_TRANSACTION:
            self.ids.scr_mngr.switch_to(NewTransaction(name=screen.name))

        elif screen == SCREENS.VIEW_TRANSACTION:
            uuid = kwargs.get('uuid', None)
            self.ids.scr_mngr.switch_to(
                ViewTransaction(name=screen.name, uuid=uuid))

        elif screen == SCREENS.SETTINGS:
            self.ids.scr_mngr.switch_to(Setting(name=screen.name))

        elif screen == SCREENS.ABOUT:
            self.ids.scr_mngr.switch_to(About(name=screen.name))


class MeuBolsoApp(App):
    theme_cls = ThemeManager()
    basedir = StringProperty()

    def build(self):
        self.db = db
        self.db.bind('sqlite', 'database.db', create_db=True)
        self.db.generate_mapping(create_tables=True)
        return self.root


if __name__ == '__main__':
    MeuBolsoApp().run()
