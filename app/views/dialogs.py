from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivymd.dialog import MDDialog
from kivymd.list import OneLineListItem
from pony.orm import db_session, select

from app.models import Contact


class ChooseContactItem(OneLineListItem):
    uuid = ObjectProperty()
    icon = StringProperty()
    name = StringProperty()

    def __init__(self, **kwargs):
        super(ChooseContactItem, self).__init__(**kwargs)
        self.uuid = kwargs.get('uuid')
        self.name = kwargs.get('name')

        self.text = self.name

    def on_release(self):
        app = App.get_running_app()
        cur_screen = app.root.ids.scr_mngr.current_screen
        cur_screen.contact = self.uuid, self.name
        cur_screen.dialog.dismiss()


class ChooseUserDialog(MDDialog):
    def __init__(self, **kwargs):
        super(ChooseUserDialog, self).__init__(**kwargs)

        self.load_contacts()
        self.add_action_button(text="Dismiss",
                               action=lambda *x: self.dismiss())

    def load_contacts(self, ):
        with db_session:
            contacts = select(c for c in Contact).order_by(Contact.name)[:]
            for c in contacts:
                self.listbox.add_widget(
                    ChooseContactItem(uuid=c.uuid, icon=c.photo, name=c.name))


class ChoosePhotoDialog(MDDialog):
    def __init__(self, **kwargs):
        super(ChoosePhotoDialog, self).__init__(**kwargs)
        self.load_dialog()

    def load_dialog(self):
        pass
