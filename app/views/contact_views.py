from datetime import datetime

from app.models import Contact
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, TwoLineAvatarIconListItem
from pony.orm import db_session, select, delete


class ContactPhoto(ILeftBody, AsyncImage):
    pass


class ContactListItem(TwoLineAvatarIconListItem):
    uuid = ObjectProperty()

    def __init__(self, uuid, **kwargs):
        super(ContactListItem, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.uuid = uuid

    def select_contact(self, ):
        app = App.get_running_app()
        with db_session:
            contato = select(c for c in Contact if c.uid == self.uuid).get()
            app.root.switch_to('viewcontact', contato=contato)


class ContactScreen(Screen):
    app = ObjectProperty()
    contact_list = ListProperty()

    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        print('opening contacts', datetime.now())
        self.app = App.get_running_app()

        print('updating toolbar', datetime.now())
        self.update_toolbar()

        print('loading contacts', datetime.now())
        self.load_contacts()

        self.populate_listview()

    def update_toolbar(self, ):
        toolbar = self.app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['account-plus',
             lambda x: self.app.root.ids.scr_mngr.switch_to(
                 NewContactScreen())]
        ]

    def load_contacts(self):
        print ('load contact list', datetime.now())
        with db_session:
            self.contact_list = select(c for c in Contact).order_by(
                Contact.name)[:]

    def populate_listview(self):
        print('loading contact listview', datetime.now())
        contact_lv = self.ids.contact_lv

        print('populating listview', datetime.now())
        for c in self.contact_list:
            item = ContactListItem(uuid=c.uid, text=c.name,
                                   secondary_text=c.status)
            item.add_widget(ContactPhoto(source=c.photo))
            contact_lv.add_widget(item)
        print('finishing of populate listview', datetime.now())

        self.remove_widget(self.ids.spinner)


class ViewContactScreen(Screen):
    contato = ObjectProperty()
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

    def on_pre_enter(self, *args):
        self.update_toolbar()
        self.load_contact()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']

        toolbar.right_action_items = [
            ['pencil', lambda x: app.root.switch_to('editcontact',
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
        content = MDLabel(text="Are you sure you want to delete this user?")

        self.dialog = MDDialog(
            title="Confirmation Dialog!",
            content=content,
            auto_dismiss=False
        )

        self.dialog.add_action_button(
            "confirm", action=lambda *x: self.confirm_delete())
        self.dialog.add_action_button(
            "Dismiss", action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    @db_session
    def confirm_delete(self):
        delete(c for c in Contact if c.uid == self.contato.uid)
        self.dialog.dismiss()

        app = App.get_running_app()
        app.root.switch_to('contacts')


class NewContactScreen(Screen):
    def __init__(self, **kwargs):
        super(NewContactScreen, self).__init__(**kwargs)

    def before_load(self, ):
        self.update_toolbar()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['check', lambda x: self.save_contact()],
            ['close',
             lambda x: app.root.switch_to('contacts')]
        ]

    def save_contact(self):
        print('saving contact')


class EditContactScreen(Screen):
    contato = ObjectProperty()

    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid', None)
        super(EditContactScreen, self).__init__(**kwargs)

    def before_load(self, ):
        self.update_toolbar()
        self.load_contact()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['check', lambda x: self.update_contact()],
            ['close', lambda x: app.root.switch_to('contacts')]
        ]

    def load_contact(self):
        with db_session:
            self.contato = select(
                c for c in Contact if c.uid == self.uuid).get()

        self.ids.contactphoto.source = self.contato.photo

    def update_contact(self):
        app = App.get_running_app()
        with db_session:
            self.contato.flush()
        app.root.switch_to('viewcontact', contato=self.contato)
