from random import randint

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.list import ILeftBody, TwoLineAvatarIconListItem
from kivymd.theming import ThemeManager
from pony.orm import db_session, select

from app.models import db, Contact


class ContactPhoto(ILeftBody, AsyncImage):
    pass


class HomeScreen(Screen):
    def update_toolbar(self, ):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []


class ContactListItem(TwoLineAvatarIconListItem):
    events_callback = ObjectProperty(None)
    uuid = ObjectProperty()

    def __init__(self, uuid, **kwargs):
        super(ContactListItem, self).__init__(**kwargs)
        self.uuid = uuid
        print("printando uuid: %r"%self.uuid )

    def on_press(self):
        print(self.uuid)


class ContactScreen(Screen):
    app = ObjectProperty()

    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)

    def before_load(self):
        self.app = App.get_running_app()
        self.update_toolbar()
        self.load_contacts()

    def update_toolbar(self, ):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['account-plus',
             lambda x: app.root.ids.scr_mngr.switch_to(NewContactScreen())]
        ]

    @db_session
    def load_contacts(self):
        contact_lv = self.ids.contact_lv
        contact_list = select(c for c in Contact) \
                           .order_by(lambda: c.name)[:]

        # todo: apagar esta linha
        print (contact_list)

        for c in contact_list:
            item = ContactListItem(
                uuid=c.uid,
                text=c.name,
                secondary_text=c.status
            )
            item.add_widget(ContactPhoto(source=c.photo))
            contact_lv.add_widget(item)


class ViewContactScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['account-check', lambda x: self.save_contact()],
            ['account-off',
             lambda x: app.root.ids.scr_mngr.switch_to(ContactScreen())]
        ]


class NewContactScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['account-check', lambda x: self.save_contact()],
            ['account-off',
             lambda x: app.root.ids.scr_mngr.switch_to(ContactScreen())]
        ]

    @db_session
    def save_contact(self):
        pass


class EditContactScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['account-check', lambda x: self.save_contact()],
            ['account-off',
             lambda x: app.root.ids.scr_mngr.switch_to(ContactScreen())]
        ]

    def save_contact(self):
        pass


class IncomeScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['plus-circle',
             lambda x: app.root.ids.scr_mngr.switch_to(NewIncomeScreen())]
        ]


class NewIncomeScreen(Screen):
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
    def update_toolbar(self):
        pass


class AboutScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []


class MyScreenManager(ScreenManager):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []

    def change_screen(self, screen_name):
        self.current = screen_name


def create_contact():
    myset = 'qwertyuiopl kjhgfdsazxcvbnm '
    name = ''
    for i in xrange(0, randint(0, 20)):
        name += myset[randint(0, len(myset) - 1)]
    status = 'fail'
    photo = "screenshots.jpg"
    return Contact(name=name, status=status, photo=photo)


class MeuBolsoApp(App):
    theme_cls = ThemeManager()

    def build(self):
        self.db = db
        self.db.bind('sqlite', 'database.db', create_db=True)
        self.db.generate_mapping(create_tables=True)

        try:
            with db_session:
                contact = create_contact()
                self.db.commit()
        except Exception as ex:
            print (ex)


if __name__ == '__main__':
    app = MeuBolsoApp()
    app.run()
