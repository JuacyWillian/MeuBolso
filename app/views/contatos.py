from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from pony.orm import db_session, select, delete

from app.models import db
from app.util import TELAS
from app.views.widgets import ContactListItem

kv = """
<ContactList>:
    nome: 'contacts'
    ScrollView:
        do_scroll_x: False
        MDList:
            id: contact_list
            
    MDFloatingActionButton:
        id: float_act_btn
        icon: 'account-plus'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.1}
        on_press: app.root.switch_to(TELAS.NOVO_CONTATO)


<NewContact>:
    ScrollView:
        do_scroll_x: False
        BoxLayout:
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            padding: dp(10), dp(10)
            spacing: dp(10)

            MDTextField:
                id: nome
                hint_text: 'Nome:'
                write_tabs: False
                text: root.nome if root.nome is not None else ''

            MDTextField:
                id: telefone
                hint_text: 'Telefone:'
                write_tabs: False
                text: root.telefone if root.telefone is not None else ''

            MDTextField:
                id: email
                hint_text: 'Email:'
                write_tabs: False
                text: root.email if root.email is not None else ''

            MDTextField:
                id: endereco
                multiline: True
                hint_text: 'Endereço:'
                write_tabs: False
                text: root.endereco if root.endereco is not None else ''
                
    MDFloatingActionButton:
        id: float_act_btn
        icon: 'check'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.25}
        on_press: root.save_contact()

    MDFloatingActionButton:
        id: float_act_btn
        icon: 'close'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.1}
        on_press: app.root.switch_to(TELAS.LISTA_CONTATO)


<EditContact>:
    ScrollView:
        do_scroll_x: False
        BoxLayout:
            id: box
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            padding: dp(10), dp(10)
            spacing: dp(10)

            MDTextField:
                id: nome
                hint_text: 'Nome:'
                text: root.nome if root.nome is not None else ''

            MDTextField:
                id: telefone
                hint_text: 'Telefone:'
                text: root.telefone if root.telefone is not None else ''

            MDTextField:
                id: email
                hint_text: 'Email:'
                text: root.email if root.email is not None else ''

            MDTextField:
                id: endereco
                multiline: True
                hint_text: 'Endereço:'
                text: root.endereco if root.endereco is not None else ''
    
    MDFloatingActionButton:
        id: float_act_btn
        icon: 'check'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.25}
        on_press: root.save_contact()

    MDFloatingActionButton:
        id: float_act_btn
        icon: 'close'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.1}
        on_press: app.root.switch_to(TELAS.DETALHE_CONTATO, id=root.id)


<ViewContact>:
    ScrollView:
        do_scroll_x: False

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            padding: dp(10), dp(10)
            spacing: dp(10)
            height: self.minimum_height

            MDLabel:
                size_hint_y: None
                font_style: 'Display1'
                height: dp(50)
                text: root.nome if root.nome is not None else ''

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height

                IconView:
                    icon: 'phone'

                MDLabel:
                    size_hint_y: None
                    height: 48
                    font_size: '16'
                    text: root.telefone if root.telefone is not None else ''

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height

                IconView:
                    icon: 'email'

                MDLabel:
                    size_hint_y: None
                    height: 48
                    font_size: '16'
                    text: root.email if root.email is not None else ''

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height

                IconView:
                    icon: 'home'

                MDLabel:
                    size_hint_y: None
                    height: 48
                    font_size: '16'
                    text: root.endereco if root.endereco is not None else ''
    
    MDFloatingActionButton:
        id: float_act_btn
        icon: 'pencil'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.1}
        on_press: app.root.switch_to(TELAS.EDITAR_CONTATO, id=root.id)

"""

Builder.load_string(kv)


class ContactList(Screen):
    def __init__(self, **kwargs):
        super(ContactList, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.populate_listview()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()]]
        toolbar.right_action_items = []

    @db_session
    def populate_listview(self):
        lista_contato = self.ids.contact_list

        for c in select(c for c in db.Contato).order_by(
                db.Contato.nome)[:]:
            item = ContactListItem(id=str(c.id), text=c.nome)
            lista_contato.add_widget(item)


class ViewContact(Screen):
    cheaderwidget = ObjectProperty()
    id = ObjectProperty()
    telefone = StringProperty()
    nome = StringProperty()
    email = StringProperty()
    endereco = StringProperty()

    def __init__(self, **kwargs):
        super(ViewContact, self).__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.app = App.get_running_app()
        self.load_contact()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids['toolbar']
        toolbar.left_action_items = [
            ['arrow-left',
             lambda x: self.app.root.switch_to(TELAS.LISTA_CONTATO)]]
        toolbar.right_action_items = []

    @db_session
    def load_contact(self):
        contato = db.Contato.get(id=self.id)

        if contato is not None:
            self.nome = contato.nome
            self.telefone = contato.telefone
            self.email = contato.email
            self.endereco = contato.endereco

    def delete_contact(self):
        content = MDLabel(
            text="Tem certeza que quer excluir este contato?\nEsta ação não tem retorno.",
            font_style='Caption', size_hint_y=None, valign='center')

        self.dialog = MDDialog(
            title="Excluir Contato.", content=content,
            size_hint=(0.8, None), height=dp(300), auto_dismiss=False)

        self.dialog.add_action_button(
            "Confirmar", action=lambda *x: self.confirm_delete())

        self.dialog.add_action_button(
            "Cancelar", action=lambda *x: self.dialog.dismiss())

        self.dialog.open()

    def confirm_delete(self):
        self.dialog.dismiss()
        with db_session:
            delete(c for c in db.Contato if c.id == self.id)

        app = App.get_running_app()
        app.root.switch_to(TELAS.LISTA_CONTATO)


class NewContact(Screen):
    nome = StringProperty()
    telefone = StringProperty()
    email = StringProperty()
    endereco = StringProperty()

    def __init__(self, **kwargs):
        super(NewContact, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()]]
        toolbar.right_action_items = []

    def save_contact(self):
        try:
            with db_session:
                self.nome = self.ids.nome.text
                self.telefone = self.ids.telefone.text
                self.email = self.ids.email.text
                self.endereco = self.ids.endereco.text

                contato = db.Contato(
                    nome=self.nome, telefone=self.telefone,
                    email=self.email, endereco=self.endereco)

            self.app.root.switch_to(TELAS.LISTA_CONTATO)
        except Exception as err:
            raise err


class EditContact(Screen):
    id = ObjectProperty()

    nome = StringProperty()
    telefone = StringProperty()
    email = StringProperty()
    endereco = StringProperty()

    def __init__(self, **kwargs):
        super(EditContact, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.id = kwargs.get('id', None)
        self.load_contact()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()], ]
        toolbar.right_action_items = []

    def load_contact(self):
        with db_session:
            contact = db.Contato.get(id=self.id)

            self.nome = contact.nome
            self.telefone = contact.telefone
            self.email = contact.email
            self.endereco = contact.endereco

    def save_contact(self):
        try:
            with db_session:
                contato = db.Contato.get(id=int(self.id))

                contato.nome = self.ids.nome.text
                contato.telefone = self.ids.telefone.text
                contato.email = self.ids.email.text
                contato.endereco = self.ids.endereco.text

            self.app.root.switch_to(TELAS.DETALHE_CONTATO, id=self.id)

        except Exception as err:
            print(err)
