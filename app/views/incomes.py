from datetime import date
from decimal import Decimal, ROUND_DOWN

from app.models import *
from dateutil.relativedelta import relativedelta
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty, \
    NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import MDList, IRightBody, \
    OneLineListItem, ThreeLineListItem
from kivymd.selectioncontrols import MDCheckbox
from pony.orm import db_session, select, rollback, delete


class IncomeListItem(ThreeLineListItem):
    def __init__(self, **kwargs):
        super(IncomeListItem, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.uuid = kwargs.get('uuid', None)

    def on_release(self):
        self.app.root.switch_to('viewincome', uuid=self.uuid)


class IncomeListItemRight(IRightBody, MDCheckbox):
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
            ['cash-usd', lambda x: self.app.root.switch_to('newincome')], ]

    @db_session
    def populate_listview(self):
        self.scrollview = ScrollView(do_scroll_x=False)
        income_lv = MDList(id='income_lv')

        today = date.today()
        for p in select(p for p in Parcel if (
                p.expiration.year == today.year \
                and p.expiration.month == today.month)\
                or (p.paid == False and p.expiration < today))\
                           .order_by(Parcel.expiration)[:]:
            text = p.title
            secontary_text = "%s\nR$ %.2f" % (
                p.expiration.strftime("%Y-%m-%d"), p.value)

            item = IncomeListItem(
                text=text, secondary_text=secontary_text, uuid=p.uuid)
            # item.add_widget(IncomeListItemRight())
            income_lv.add_widget(item)

        self.scrollview.add_widget(income_lv)
        self.add_widget(self.scrollview)


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


class ViewIncomeScreen(Screen):
    uuid = ObjectProperty()
    ttitle = StringProperty()
    tdescription = StringProperty()
    tvalue = NumericProperty()
    tcontact = ObjectProperty()
    tcontactuuid = ObjectProperty()
    tpubdate = StringProperty()
    tnparcels = NumericProperty()
    ttype = StringProperty()
    parcels = ListProperty()

    def __init__(self, **kwargs):
        super(ViewIncomeScreen, self).__init__(**kwargs)
        self.uuid = kwargs.get('uuid', None)
        self.app = App.get_running_app()
        self.load_ticket()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids['toolbar']
        toolbar.left_action_items = [
            ['arrow-left', lambda x: self.app.root.switch_to('incomes')]]

        toolbar.right_action_items = [
            ['pencil',
             lambda x: self.app.root.switch_to('editincome', uuid=self.uuid)],
            ['delete', lambda x: self.remove()]]

    @db_session
    def load_ticket(self):
        ticket = Parcel.get(uuid=self.uuid).ticket

        if ticket:
            self.uuid = ticket.uuid
            self.ttitle = ticket.title
            self.tdescription = ticket.description
            self.tvalue = ticket.tvalue
            self.tcontact = ticket.contact
            self.tpubdate = ticket.pubdate.strftime("%Y-%m-%d")
            self.tnparcels = ticket.nparcels
            self.ttype = ticket.ttype
            self.parcels = select(p for p in Parcel if p.ticket == ticket) \
                               .order_by(Parcel.expiration)[:]

            parcel_list = self.ids.parcel_list
            for p in self.parcels:

                item = ParcelWidget(p.title, p.expiration, p.value, False)
                parcel_list.add_widget(item)

    def remove(self):
        content = StackLayout()
        content.add_widget(
            MDLabel(
                text="Are you sure you want to delete this ticket?",
                font_style='Caption', size_hint_y=None, valign='center'))

        self.dialog = MDDialog(
            title="Confirmation Dialog!", content=content,
            size_hint=(.8, .9), auto_dismiss=False)

        self.dialog.add_action_button(
            "confirm", action=lambda *x: self.confirm_delete())

        self.dialog.add_action_button(
            "Dismiss", action=lambda *x: self.dialog.dismiss())

        self.dialog.open()

    def confirm_delete(self):
        self.dialog.dismiss()
        with db_session:
            delete(t for t in Ticket if t.uuid == self.uuid)

        app = App.get_running_app()
        app.root.switch_to('incomes')


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

        self.listbox = MDList(id='userList')

        self.content = self.listbox

        self.load_contacts()
        self.add_action_button(text="Dismiss",
                               action=lambda *x: self.dismiss())

    def load_contacts(self, ):
        with db_session:
            contacts = select(c for c in Contact).order_by(Contact.name)[:]

            for c in contacts:
                self.listbox.add_widget(
                    ChooseContactItem(uuid=c.uuid, icon=c.photo, name=c.name))


class NewIncomeScreen(Screen):
    contact = ListProperty()

    def __init__(self, **kwargs):
        super(NewIncomeScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()], ]
        toolbar.right_action_items = [
            ['check', lambda x: self.save_contact()],
            ['close', lambda x: self.app.root.switch_to('incomes')], ]

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

    def show_choose_contact_dialog(self):

        # sv = ScrollView()
        ml = MDList()
        # sv.add_widget(ml)

        with db_session:
            for c in select(c for c in Contact).order_by(Contact.name)[:]:
                ml.add_widget(
                    ChooseContactItem(
                        uuid=c.uuid, name=c.name
                    )
                )

        self.dialog = MDDialog(title="Choose a Contact.", content=ml)
        self.dialog.add_action_button(text="Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def on_contact(self, instance, value):
        contact_name = self.ids.contact_name
        if value:
            contact_name.text = self.contact[1]
        else:
            contact_name.text = ''

    @db_session
    def save_contact(self):

        # List of errors
        errors = []

        # Getting data of fields
        title = self.ids.title.text
        description = self.ids.description.text
        pubdate = self.ids.pubdate.text
        expiration = self.ids.expiration.text
        value = Decimal(self.ids.value.text).quantize(Decimal('1.00'),
                                                      rounding=ROUND_DOWN)
        parcels = int(self.ids.parcels.text)
        ttype = 'receita' if self.ids.switch.active else 'despesa'
        contact = self.contact[0] if self.contact else None

        # Validating fields
        if title == '':
            errors.append("Field 'Title' is required!")

        if pubdate == '':
            errors.append("Field 'Pubdate' is required!")

        else:
            try:
                pubdate = date(
                    *[int(f) for f in self.ids.pubdate.text.split('-')])

            except:
                errors.append(
                    "Invalid format for 'Pubdate' field! must be 'yyyy-mm-dd'.")

        if expiration == '':
            errors.append("Field 'Validate' is required!")

        else:
            try:
                expiration = date(
                    *[int(f) for f in self.ids.expiration.text.split('-')])

            except:
                errors.append(
                    "Invalid format for 'Expiration' field! must be 'yyyy-mm-dd'.")

        try:
            diferenca = expiration - pubdate
            if diferenca.days < 0:
                errors.append(
                    "Expiration can not be less than the date of Pubdate.")

        except:
            pass

        if value < 0:
            errors.append("Field 'Value' can not be less than 0.")

        if parcels < 1:
            errors.append("Field 'Parcels' can not be less than 1!")

        if contact:
            contact = Contact.get(uuid=contact)

        # Showing dialog with errors found
        if errors:
            dialog = MDDialog(title='Errors', size_hint=(.9, .8))
            box = StackLayout(size_hint_y=None)
            for e in errors:
                box.add_widget(MDLabel(
                    text=e, size_hint_y=None, height='48dp',
                    font_size='18dp', theme_text_color='Error'))

            dialog.content = box
            dialog.add_action_button(
                'Close', action=lambda *x: dialog.dismiss())
            dialog.open()

        else:
            try:
                # Creating a Ticket
                parcels = parcels
                value = value

                parcel_value = (value / parcels).quantize(Decimal('1.00'),
                                                          rounding=ROUND_DOWN)
                excedent = (value - (parcel_value * parcels)).quantize(
                    Decimal('1.00'), rounding=ROUND_DOWN)

                ticket = Ticket(
                    title=title, description=description, tvalue=value,
                    pubdate=pubdate, nparcels=parcels, ttype=ttype,
                    contact=contact)

                # Creating Parcels of the Ticket
                if parcels == 1:
                    ticket.parcels.create(
                        title="%s %d/%d" % (title, 1, parcels),
                        value=value, expiration=expiration)

                else:
                    for p in range(parcels):
                        if p == parcels - 1:
                            parcel_value += excedent
                        nExpiration = expiration + relativedelta(months=p)
                        ticket.parcels.create(
                            title="%s %d/%d" % (title, p + 1, parcels),
                            value=parcel_value, expiration=nExpiration)

                # Changing to IncomeList
                self.app.root.switch_to('incomes')
            except Exception as err:
                rollback()
                print str(err)

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
