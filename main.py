from random import randint

from kivy.uix.screenmanager import ScreenManager
from kivymd.navigationdrawer import NavigationLayout
from kivymd.theming import ThemeManager

from app.models import db, Contact
from app.views.contact_views import *


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def before_load(self, ):
        self.update_toolbar()

    def update_toolbar(self, ):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []


class IncomeScreen(Screen):
    def __init__(self, **kwargs):
        super(IncomeScreen, self).__init__(**kwargs)

    def before_load(self, ): self.update_toolbar()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['plus-circle',
             lambda x: app.root.ids.scr_mngr.switch_to(NewIncomeScreen())]
        ]


class NewIncomeScreen(Screen):
    def __init__(self, **kwargs):
        super(NewIncomeScreen, self).__init__(**kwargs)

    def before_load(self, ): self.update_toolbar()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['content-save', lambda x: self.save_income()],
            ['close',
             lambda x: app.root.ids.scr_mngr.switch_to(IncomeScreen())]
        ]

    def save_income(self):
        pass


class EditIncomeScreen(Screen):
    def __init__(self, **kwargs):
        super(EditIncomeScreen, self).__init__(**kwargs)

    def before_load(self, ): self.update_toolbar()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['content-save', lambda x: self.save_income()],
            ['close',
             lambda x: app.root.ids.scr_mngr.switch_to(IncomeScreen())]
        ]

    def save_income(self):
        pass


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    def before_load(self, ): self.update_toolbar()

    def update_toolbar(self):
        pass


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

    def before_load(self, ): self.update_toolbar()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []


class MyRootLayout(NavigationLayout):
    def __init__(self, **kwargs):
        super(MyRootLayout, self).__init__(**kwargs)

    def switch_to(self, screen_name, **kwargs):
        if screen_name == 'home':
            self.ids.scr_mngr.switch_to(HomeScreen(name=screen_name))

        elif screen_name == 'contacts':
            self.ids.scr_mngr.switch_to(ContactScreen(name=screen_name))

        elif screen_name == 'newcontact':
            self.ids.scr_mngr.switch_to(NewContactScreen(name=screen_name))

        elif screen_name == 'viewcontact':
            contato = kwargs.get('contato', None)
            self.ids.scr_mngr.switch_to(
                ViewContactScreen(name=screen_name, contato=contato))

        elif screen_name == 'editcontact':
            contato = kwargs.get('contato', None)
            self.ids.scr_mngr.switch_to(
                EditContactScreen(name=screen_name, contato=contato))

        elif screen_name == 'incomes':
            self.ids.scr_mngr.switch_to(IncomeScreen(name=screen_name))

        elif screen_name == 'settings':
            self.ids.scr_mngr.switch_to(SettingsScreen(name=screen_name))

        elif screen_name == 'about':
            self.ids.scr_mngr.switch_to(AboutScreen(name=screen_name))


class MyScreenManager(ScreenManager):
    def before_load(self, ): pass

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []

    def change_screen(self, screen_name):
        self.current = screen_name


def create_contact(qtde):
    contact_list = []
    for i in range(qtde):
        try:
            with db_session:
                myset = 'qwertyuiopl kjhgfdsazxcvbnm '
                name = ''
                for i in xrange(0, randint(0, 20)):
                    name += myset[randint(0, len(myset) - 1)]
                status = 'fail'
                photo = "avatar.png"
                contact_list.append(
                    Contact(name=name, status=status, photo=photo))
        except:
            pass


class MeuBolsoApp(App):
    theme_cls = ThemeManager()

    def build(self):
        self.db = db
        self.db.bind('sqlite', 'database.db', create_db=True)
        self.db.generate_mapping(create_tables=True)

        # create_contact(50)

        return self.root


if __name__ == '__main__':
    app = MeuBolsoApp()
    app.run()
