from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, TwoLineAvatarIconListItem, MDList
from pony.orm import db_session, select, delete

from app.models import Contact


class ContactPhoto(ILeftBody, AsyncImage):
    pass


class ContactListItem(TwoLineAvatarIconListItem):
    def __init__(self, uuid, **kwargs):
        super(ContactListItem, self).__init__(**kwargs)
        self.uuid = uuid

    def select_contact(self, ):
        app = App.get_running_app()
        with db_session:
            contato = select(c for c in Contact if c.uid == self.uuid).get()
            app.root.switch_to('viewcontact', contato=contato)


class ContactScreen(Screen):
    contact_list = ListProperty()

    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_enter(self, *args):
        self.update_toolbar()
        self.load_contacts()
        self.populate_listview()

    def update_toolbar(self, ):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()],
        ]

        toolbar.right_action_items = [
            ['account-plus', lambda x: self.app.root.switch_to('newcontact')]
        ]

    def load_contacts(self):
        print ('load contact list', datetime.now())
        with db_session:
            self.contact_list = select(c for c in Contact).order_by(
                Contact.name)[:]

    def populate_listview(self):
        self.scrollview = ScrollView(do_scroll_x=False)
        self.contact_lv = MDList(id='contact_lv')

        print('loading contact listview', datetime.now())
        # contact_lv = self.ids.contact_lv

        print('populating listview', datetime.now())
        for c in self.contact_list:
            item = ContactListItem(
                uuid=c.uid, text=c.name, secondary_text=c.status)
            item.add_widget(ContactPhoto(source=c.photo))
            self.contact_lv.add_widget(item)
        print('finishing of populate listview', datetime.now())

        self.scrollview.add_widget(self.contact_lv)
        self.add_widget(self.scrollview)
        self.remove_widget(self.ids.spinner)


class ViewContactScreen(Screen):
    nome = StringProperty()
    photo = ObjectProperty()
    status = StringProperty()
    addresses = ObjectProperty()
    phones = ObjectProperty()
    emails = ObjectProperty()
    incomes = ObjectProperty()

    def __init__(self, **kwargs):
        super(ViewContactScreen, self).__init__(**kwargs)
        self.contato = kwargs.get('contato', None)
        self.app = App.get_running_app()

    def on_pre_enter(self, *args):
        self.update_toolbar()
        self.load_contact()

    def update_toolbar(self):
        toolbar = self.app.root.ids['toolbar']
        toolbar.left_action_items = [
            ['arrow-left', lambda x: self.app.root.switch_to('contacts')]
        ]

        toolbar.right_action_items = [
            ['pencil', lambda x: self.app.root.switch_to('editcontact',
                                                    contato=self.contato)],
            ['delete', lambda x: self.delete_contact()]
        ]

    def load_contact(self):
        self.name = self.contato.name
        self.photo = self.contato.photo
        self.status = self.contato.status
        self.addresses = self.contato.addresses
        self.phones = self.contato.phones
        self.emails = self.contato.emails
        self.incomes = self.contato.incomes

    def delete_contact(self):
        content = MDLabel(
            text="Are you sure you want to delete this user?",
            font_style='Body2', theme_text_color='Secondary',
            size_hint_y=None,
            valign='center')

        self.dialog = MDDialog(
            title="Confirmation Dialog!",
            content=content,
            size_hint=(0.8, None),
            height=dp(200),
            auto_dismiss=False
        )

        self.dialog.add_action_button(
            "confirm", action=lambda *x: self.confirm_delete())
        self.dialog.add_action_button(
            "Dismiss", action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    @db_session
    def confirm_delete(self):
        self.dialog.dismiss()
        delete(c for c in Contact if c.uid == self.contato.uid)

        app = App.get_running_app()
        app.root.switch_to('contacts')


class NewContactScreen(Screen):
    def __init__(self, **kwargs):
        super(NewContactScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def before_load(self, ):
        self.update_toolbar()

    def update_toolbar(self):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()],
        ]
        toolbar.right_action_items = [
            ['check', lambda x: self.save_contact()],
            ['close',
             lambda x: self.app.root.switch_to('contacts')]
        ]

    def save_contact(self):
        print('saving contact')


class EditContactScreen(Screen):
    def __init__(self, **kwargs):
        super(EditContactScreen, self).__init__(**kwargs)
        self.contato = kwargs.get('contato', None)
        self.app = App.get_running_app()

    def before_load(self, ):
        self.update_toolbar()
        self.load_contact()

    def update_toolbar(self):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()],
        ]
        toolbar.right_action_items = [
            ['check', lambda x: self.update_contact()],
            ['close', lambda x: self.app.root.switch_to('contacts')]
        ]

    def load_contact(self):
        pass

    def update_contact(self):
        with db_session:
            self.contato.flush()
        self.app.root.switch_to('viewcontact', contato=self.contato)
