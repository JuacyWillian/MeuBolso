from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivymd.list import ILeftBody, OneLineAvatarIconListItem
from pony.orm import db_session


class ContactPhoto(ILeftBody, AsyncImage):
    pass


class ContactHeaderWidget(BoxLayout):
    photo = StringProperty()
    name = StringProperty()

    def __init__(self, **kwargs):
        super(ContactHeaderWidget, self).__init__(**kwargs)


class ContactListItem(OneLineAvatarIconListItem):
    def __init__(self, uuid, **kwargs):
        super(ContactListItem, self).__init__(**kwargs)
        self.uuid = uuid

    def select_contact(self, ):
        app = App.get_running_app()

        with db_session:
            app.root.switch_to('viewcontact', uuid=self.uuid)
