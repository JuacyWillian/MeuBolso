from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel

from app.models import *
from app.util import TELAS
from app.views.widgets import ContactListItem

kv = """
<TelaContatos>:
    nome: 'contacts'
    ScrollView:
        do_scroll_x: False
        MDList:
            id: contact_list
            
    MDFloatingActionButton:
        icon: 'account-plus'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.1}
        on_press: app.root.switch_to(TELAS.NOVO_CONTATO)


<TelaNovoContato>:
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
                # text: root.contato.nome if root.contato is not None else ''

            MDTextField:
                id: telefone
                hint_text: 'Telefone:'
                write_tabs: False
                # text: root.contato.telefone if root.contato is not None else ''

            MDTextField:
                id: email
                hint_text: 'Email:'
                write_tabs: False
                # text: root.contato.email if root.contato is not None else ''

            MDTextField:
                id: endereco
                multiline: True
                hint_text: 'Endereço:'
                write_tabs: False
                # text: root.contato.endereco if root.contato is not None else ''
                
    MDFloatingActionButton:
        # id: float_act_btn
        icon: 'check'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.25}
        on_press: root.save_contact()

    MDFloatingActionButton:
        # id: float_act_btn
        icon: 'close'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.1}
        on_press: app.root.switch_to(TELAS.LISTA_CONTATO)


<TelaEditarContato>:
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
                text: root.contato.nome if root.contato is not None else ''

            MDTextField:
                id: telefone
                hint_text: 'Telefone:'
                text: root.contato.telefone if root.contato is not None else ''

            MDTextField:
                id: email
                hint_text: 'Email:'
                text: root.contato.email if root.contato is not None else ''

            MDTextField:
                id: endereco
                multiline: True
                hint_text: 'Endereço:'
                text: root.contato.endereco if root.contato is not None else ''
    
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
        on_press: app.root.switch_to(TELAS.DETALHE_CONTATO, contato=root.contato)


<TelaVisualizarContato>:
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
                text: root.contato.nome if root.contato is not None else ''

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height

                IconView:
                    icon: 'phone'

                MDLabel:
                    size_hint_y: None
                    height: 48
                    font_size: '16'
                    text: root.contato.telefone if root.contato is not None else ''

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height

                IconView:
                    icon: 'email'

                MDLabel:
                    size_hint_y: None
                    height: 48
                    font_size: '16'
                    text: root.contato.email if root.contato is not None else ''

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height

                IconView:
                    icon: 'home'

                MDLabel:
                    size_hint_y: None
                    height: 48
                    font_size: '16'
                    text: root.contato.endereco if root.contato is not None else ''
    
    MDFloatingActionButton:
        id: float_act_btn
        icon: 'pencil'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.1}
        on_press: app.root.switch_to(TELAS.EDITAR_CONTATO, contato=root.contato)

"""

Builder.load_string(kv)
Session = sessionmaker(bind=db)


class TelaContatos(Screen):
    def __init__(self, **kwargs):
        super(TelaContatos, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.populate_listview()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()]]
        toolbar.right_action_items = []

    def populate_listview(self):
        lista_contato = self.ids.contact_list
        session = Session()
        try:
            for c in session.query(Contato).order_by(Contato.nome).all():
                session.expunge(c)
                lista_contato.add_widget(ContactListItem(c))
                # session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


class TelaVisualizarContato(Screen):
    cheaderwidget = ObjectProperty()
    contato = ObjectProperty()

    def __init__(self, contato, **kwargs):
        self.app = App.get_running_app()
        self.contato = contato

        super(TelaVisualizarContato, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids['toolbar']
        toolbar.left_action_items = [['arrow-left', lambda x: self.app.root.switch_to(TELAS.LISTA_CONTATO)]]
        toolbar.right_action_items = []

    def delete_contact(self):
        content = MDLabel(
            text="Tem certeza que quer excluir este contato?\nEsta ação não tem retorno.",
            font_style='Caption', size_hint_y=None, valign='center')
        self.dialog = MDDialog(title="Excluir Contato.", content=content, size_hint=(0.8, None),
                               height=dp(300), auto_dismiss=True)
        self.dialog.add_action_button("Confirmar", action=lambda *x: self.confirm_delete())
        self.dialog.add_action_button("Cancelar", action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def confirm_delete(self):
        self.dialog.dismiss()
        session = Session()
        try:
            contato = session.query(Contato).filter(Contato.id == self.contato.id).first()
            session.delete(contato)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        self.app.root.switch_to(TELAS.LISTA_CONTATO)


class TelaNovoContato(Screen):
    nome = StringProperty()
    telefone = StringProperty()
    email = StringProperty()
    endereco = StringProperty()

    def __init__(self, **kwargs):
        super(TelaNovoContato, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [['menu', lambda x: self.app.root.toggle_nav_drawer()]]
        toolbar.right_action_items = []

    def save_contact(self):
        contato = None
        session = Session()
        try:
            nome = self.ids.nome.text
            telefone = self.ids.telefone.text
            email = self.ids.email.text
            endereco = self.ids.endereco.text

            contato = Contato(nome=nome, telefone=telefone, email=email, endereco=endereco)
            session.add(contato)
            session.commit()
            session.expunge(contato)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        self.app.root.switch_to(TELAS.DETALHE_CONTATO, contato=contato)


class TelaEditarContato(Screen):
    contato = ObjectProperty()

    def __init__(self, contato, **kwargs):
        self.app = App.get_running_app()
        self.contato = contato
        super(TelaEditarContato, self).__init__(**kwargs)

    # def ler_contato(self, contato_id):
    #     session = Session()
    #     try:
    #         self.contato = Contato.query.get(contato_id)
    #         print(self.contato)
    #         session.commit()
    #
    #     except:
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()
    #
    #     print(self.contato.nome)

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()], ]
        toolbar.right_action_items = []

    def save_contact(self):
        contato = None
        session = Session()
        try:
            contato = session.query(Contato).filter_by(id=self.contato.id).first()
            contato.nome = self.ids.nome.text
            contato.telefone = self.ids.telefone.text
            contato.email = self.ids.email.text
            contato.endereco = self.ids.endereco.text
            session.commit()
            session.expunge(contato)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        self.app.root.switch_to(TELAS.DETALHE_CONTATO, contato=contato)
