from app.models import Contact
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, ObjectProperty, \
    NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, MDList, OneLineAvatarIconListItem
from pony.orm import db_session, select, delete


class ContactPhoto(ILeftBody, AsyncImage):
    pass


class ContactHeaderWidget(BoxLayout):
    photo = StringProperty()
    name = StringProperty()

    def __init__(self, **kwargs):
        super(ContactHeaderWidget, self).__init__(**kwargs)


class ContactAddressWidget(BoxLayout):
    grid_height = NumericProperty()

    def __init__(self, **kwargs):
        super(ContactAddressWidget, self).__init__(**kwargs)

    def add_address(self, address):
        self.ids.address_grid.add_widget(
            MDLabel(text=address.name, size_hint=(None, None), height=dp(44)))
        self.ids.address_grid.add_widget(
            MDLabel(text=address.address, size_hint_y=None, height=dp(44)))
        self.grid_height += dp(44)


class ContactEmailWidget(BoxLayout):
    grid_height = NumericProperty()

    def __init__(self, **kwargs):
        super(ContactEmailWidget, self).__init__(**kwargs)

    def add_email(self, email):
        self.ids.email_grid.add_widget(
            MDLabel(text=email.name, size_hint=(None, None), height=dp(24)))
        self.ids.email_grid.add_widget(
            MDLabel(text=email.email, size_hint_y=None, height=dp(24)))
        self.grid_height += dp(25)


class ContactPhoneWidget(BoxLayout):
    grid_height = NumericProperty()

    def __init__(self, **kwargs):
        super(ContactPhoneWidget, self).__init__(**kwargs)

    def add_phone(self, phone):
        self.ids.phone_grid.add_widget(
            MDLabel(text=phone.name, size_hint=(None, None), height=dp(24)))
        self.ids.phone_grid.add_widget(
            MDLabel(text=phone.phone, size_hint_y=None, height=dp(24)))
        self.grid_height += dp(25)


class ContactListItem(OneLineAvatarIconListItem):
    def __init__(self, uuid, **kwargs):
        super(ContactListItem, self).__init__(**kwargs)
        self.uuid = uuid

    def select_contact(self, ):
        app = App.get_running_app()
        with db_session:
            contact = select(c for c in Contact if c.uuid == self.uuid).get()
            app.root.switch_to('viewcontact', contact=contact)


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
        with db_session:
            self.contact_list = select(c for c in Contact).order_by(
                Contact.name)[:]

    def populate_listview(self):
        self.scrollview = ScrollView(do_scroll_x=False)
        self.contact_lv = MDList(id='contact_lv')

        for c in self.contact_list:
            item = ContactListItem(
                uuid=c.uuid, text=c.name)
            item.add_widget(ContactPhoto(source=c.photo))
            self.contact_lv.add_widget(item)

        self.scrollview.add_widget(self.contact_lv)
        self.add_widget(self.scrollview)
        self.remove_widget(self.ids.spinner)


class ViewContactScreen(Screen):
    uuid = ObjectProperty()
    cheaderwidget = ObjectProperty()

    def __init__(self, **kwargs):
        super(ViewContactScreen, self).__init__(**kwargs)
        self.uuid = kwargs.get('uuid', None)
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
                                                         contato=self.contact)],
            ['delete', lambda x: self.delete_contact()]
        ]

    @db_session
    def load_contact(self):
        contact = Contact.get(uuid=self.uuid)

        if contact is not None:

            self.ids.cheaderwidget.photo = contact.photo
            self.ids.cheaderwidget.name = contact.name

            for address in contact.addresses:
                self.ids.caddresswidget.add_address(address)

            for phone in contact.phones:
                self.ids.cphonewidget.add_phone(phone)

            for email in contact.emails:
                self.ids.cemailwidget.add_email(email)

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
        delete(c for c in Contact if c.uuid == self.contact.uuid)

        app = App.get_running_app()
        app.root.switch_to('contacts')


class NewContactScreen(Screen):
    photo = StringProperty()

    def __init__(self, **kwargs):
        super(NewContactScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.photo = 'avatar.png'

    def on_pre_enter(self, *args):
        self.update_toolbar()
        #
        # self.ids.contactphoto.source = self.photo
        # self.ids.cambutton.on_press = self.new_photo

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

    def new_photo(self, *args):
        pass

    def save_contact(self):
        print('saving contact')


class EditContactScreen(Screen):
    def __init__(self, **kwargs):
        super(EditContactScreen, self).__init__(**kwargs)
        self.contato = kwargs.get('contact', None)
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
