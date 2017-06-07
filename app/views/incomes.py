from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, OptionProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.date_picker import MDDatePicker
from kivymd.label import MDLabel
from kivymd.list import MDList, TwoLineListItem, ThreeLineListItem, IRightBody
from kivymd.selectioncontrols import MDCheckbox
from pony.orm import db_session, select

from app.models import *
from app.views.widgets import ContactPhoto, ContactListItem


class IncomeListItem(ThreeLineListItem):
    def __init__(self, **kwargs):
        super(IncomeListItem, self).__init__(**kwargs)
        self.app = App.get_running_app()

class IncomeListItemLeft(MDLabel, IRightBody):
    pass


class IncomeScreen(Screen):
    def __init__(self, **kwargs):
        super(IncomeScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.populate_listview()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()], ]

        toolbar.right_action_items = [
            ['cash-usd', lambda x: self.app.root.switch_to('newincome')],]

    @db_session
    def populate_listview(self):
        self.scrollview = ScrollView(do_scroll_x=False)
        income_lv = MDList(id='income_lv')

        for t in select(t for t in Ticket if t.type == 'income').order_by(
                Ticket.pubdate)[:]:
            item = IncomeListItem(title=t.title, secondary_text=t.description)
            item.add_widget(IncomeListItemLeft(text=str(t.tvalue)))
            income_lv.add_widget(item)

        self.scrollview.add_widget(income_lv)
        self.add_widget(self.scrollview)

    def show_datepicker(self, value):
        print(value)

# class ViewIncomeScreen(Screen):
#     uuid = ObjectProperty()
#     phone = StringProperty()
#     c_name = StringProperty()
#     phone = StringProperty()
#     email = StringProperty()
#     address = StringProperty()
#
#     def __init__(self, **kwargs):
#         super(ViewIncomeScreen, self).__init__(**kwargs)
#         self.uuid = kwargs.get('uuid', None)
#         self.app = App.get_running_app()
#         self.load_contact()
#
#     def on_pre_enter(self, *args):
#         toolbar = self.app.root.ids['toolbar']
#         toolbar.left_action_items = [
#             ['arrow-left', lambda x: self.app.root.switch_to('contacts')]]
#
#         toolbar.right_action_items = [
#             ['pencil', lambda x: self.app.root.switch_to('editcontact', uuid=self.uuid)],
#             ['delete', lambda x: self.delete_contact()]]
#
#     @db_session
#     def load_contact(self):
#         contact = Contact.get(uuid=self.uuid)
#
#         if contact is not None:
#             self.ids.cheaderwidget.photo = contact.photo
#             self.ids.cheaderwidget.name = contact.name
#
#             self.c_name = contact.name
#             self.phone = contact.phone
#             self.email = contact.email
#             self.address = contact.address
#
#     def delete_contact(self):
#         content = MDLabel(
#             text="Are you sure you want to delete this user?",
#             font_style='Caption', size_hint_y=None, valign='center')
#
#         self.dialog = MDDialog(
#             title="Confirmation Dialog!", content=content,
#             size_hint=(0.8, None), height=dp(300), auto_dismiss=False)
#
#         self.dialog.add_action_button(
#             "confirm", action=lambda *x: self.confirm_delete())
#
#         self.dialog.add_action_button(
#             "Dismiss", action=lambda *x: self.dialog.dismiss())
#
#         self.dialog.open()
#
#     def confirm_delete(self):
#         self.dialog.dismiss()
#         with db_session:
#             delete(c for c in Contact if c.uuid == self.uuid)
#
#         app = App.get_running_app()
#         app.root.switch_to('contacts')


class MyCheckBox(MDCheckbox):
    def __init__(self, **kwargs):
        super(MyCheckBox, self).__init__(**kwargs)

    def on_active(self, instance, value):
        super(MyCheckBox, self).on_active(instance, value)

class NewIncomeScreen(Screen):



    def __init__(self, **kwargs):
        super(NewIncomeScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()],]
        toolbar.right_action_items = [
            ['check', lambda x: self.save_contact()],
            ['close', lambda x: self.app.root.switch_to('incomes')],]

    def change_check(self, name):
        if name == 'chk_despesa':
            print(self.ids[name].active, 'despesa')
        elif name == 'chk_receita':
            print(self.ids[name].active, 'receita')


    def show_datepicker(self, value):
        self.mywidget = self.ids[value]
        MDDatePicker(self.set_date).open()

    def set_date(self, data_obj):
        self.mywidget.text = str(data_obj)

    def save_contact(self):
        try:
            with db_session:

                validate=self.ids.validate.text,

                ticket = Ticket(
                    title=self.ids.title.text,
                    description=self.ids.description.text,
                    pubdate=self.ids.pubdate.text,
                )

            self.app.root.switch_to('incomes')
        except Exception as err:
            print err


# class EditContactScreen(Screen):
#     uuid = ObjectProperty()
#
#     photo = StringProperty()
#     c_name = StringProperty()
#     phone = StringProperty()
#     email = StringProperty()
#     address = StringProperty()
#
#     def __init__(self, **kwargs):
#         super(EditContactScreen, self).__init__(**kwargs)
#         self.app = App.get_running_app()
#         self.uuid = kwargs.get('uuid', None)
#         self.load_contact()
#
#     def on_pre_enter(self, *args):
#         toolbar = self.app.root.ids.toolbar
#         toolbar.left_action_items = [
#             ['menu', lambda x: self.app.root.toggle_nav_drawer()],]
#
#         toolbar.right_action_items = [
#             ['check', lambda x: self.save_contact()],
#             ['close',lambda x: self.app.root.switch_to('viewcontact', uuid=self.uuid)],]
#
#     def load_contact(self):
#         with db_session:
#             contact = Contact.get(uuid=self.uuid)
#
#             self.photo = contact.photo if contact.photo is not None else ''
#             self.c_name = contact.name
#             self.phone = contact.phone
#             self.email = contact.email
#             self.address = contact.address
#
#     def add_photo(self, *args):
#         content = BoxLayout()
#         content.add_widget(MDIconButton(icon='camera'))
#         content.add_widget(MDIconButton(icon='image-multiple'))
#
#         self.dialog = MDDialog(title='Choose font of image!', content=content)
#         self.dialog.add_action_button('Cancel', action=lambda *x: self.dialog.dismiss())
#         self.dialog.open()
#
#     def save_contact(self):
#         try:
#             with db_session:
#                 contact = Contact.get(uuid=self.uuid)
#
#                 photo = self.ids.photo.source or os.path.join(
#                     self.app.basedir, 'assets', 'images', 'avatar.jpg')
#
#                 contact.photo = photo
#                 contact.c_name = self.ids.name.text
#                 contact.phone = self.ids.phone.text
#                 contact.email = self.ids.email.text
#                 contact.address = self.ids.address.text
#
#             self.app.root.switch_to('viewcontact', uuid=self.uuid)
#
#         except Exception as err:
#             print (err)
