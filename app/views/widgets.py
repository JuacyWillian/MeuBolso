from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.list import ThreeLineListItem, OneLineListItem

from app.util import SCREENS


class ContactListItem(OneLineListItem):
    def __init__(self, uuid, **kwargs):
        super(ContactListItem, self).__init__(**kwargs)
        self.uuid = uuid
        self.app = App.get_running_app()

    def on_release(self):
        self.app.root.switch_to(SCREENS.VIEW_CONTACT, uuid=self.uuid)


class TransactionListItem(ThreeLineListItem):
    def __init__(self, **kwargs):
        super(TransactionListItem, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.uuid = kwargs.get('uuid', None)

    def on_release(self):
        self.app.root.switch_to(SCREENS.VIEW_TRANSACTION, uuid=self.uuid)


class ParcelWidget(BoxLayout):
    title = StringProperty()
    expiration = StringProperty()
    value = StringProperty()
    paid = BooleanProperty()

    def __init__(self, title, expiration, value, paid, **kwargs):
        super(ParcelWidget, self).__init__(**kwargs)
        self.title = title
        self.expiration = expiration.strftime("%y-%m-%d")
        self.value = str(value)
        self.paid = paid
