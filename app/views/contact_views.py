from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivymd.list import ILeftBody, TwoLineAvatarIconListItem
from pony.orm import db_session, select

from app.models import Contact


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
        app.root.switch_to('viewcontact', uuid=self.uuid)


class ContactScreen(Screen):
    app = ObjectProperty()

    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)

    def before_load(self):
        self.app = App.get_running_app()
        self.update_toolbar()
        self.load_contacts()

    def update_toolbar(self, ):
        toolbar = self.app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['account-plus',
             lambda x: self.app.root.ids.scr_mngr.switch_to(
                 NewContactScreen())]
        ]

    @db_session
    def load_contacts(self):
        contact_lv = self.ids.contact_lv
        contact_list = select(c for c in Contact) \
                           .order_by(lambda: c.name)[:]

        for c in contact_list:
            item = ContactListItem(
                uuid=c.uid,
                text=c.name,
                secondary_text=c.status
            )
            item.add_widget(ContactPhoto(source=c.photo))
            contact_lv.add_widget(item)

    def select_contact(self):
        pass


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
        self.uuid = kwargs.get('uuid', None)
        super(ViewContactScreen, self).__init__(**kwargs)

    def before_load(self, ):
        self.update_toolbar()
        self.load_contact()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.left_action_items = [
            ['arrow-left', lambda x: app.root.switch_to('contacts')],
        ]

        toolbar.right_action_items = [
            ['account-edit', lambda x: self.save_contact()],
            ['account-remove', lambda x: self.delete_contact()]
        ]

    def load_contact(self):
        with db_session:
            contato = select(c for c in Contact if c.uid == self.uuid).get()
        self.name = contato.name
        self.photo = contato.photo
        self.status = contato.status
        self.addresses = contato.addresses
        self.phones = contato.phones
        self.emails = contato.emails
        self.incomes = contato.incomes


class NewContactScreen(Screen):
    def __init__(self, **kwargs):
        super(NewContactScreen, self).__init__(**kwargs)

    def before_load(self, ):
        self.update_toolbar()

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
    def __init__(self, **kwargs):
        super(EditContactScreen, self).__init__(**kwargs)

    def before_load(self, ): self.update_toolbar()

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
