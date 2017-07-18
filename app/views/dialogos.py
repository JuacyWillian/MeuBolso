from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.stacklayout import StackLayout
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import OneLineListItem, MDList

from app.models import *
from app.util import FREQUENCIA

kv = """

<BaseDialog@Dialog>:
    size_hint: 0.8, 0.8


<ChooseUserDialog@BaseDialog>:
    size_hint: .85, .95

"""

Builder.load_string(kv)


class ChooseContactItem(OneLineListItem):
    contato = ObjectProperty()

    def __init__(self, dialog, contato, **kwargs):
        super(ChooseContactItem, self).__init__(**kwargs)
        self.contato = contato
        self.dialog = dialog
        self.text = self.contato.nome

    def on_release(self):
        app = App.get_running_app()
        cur_screen = app.root.ids.scr_mngr.current_screen
        cur_screen.contato = self.contato
        self.dialog.dismiss()


class ContactDialog(MDDialog):
    def __init__(self, screen, **kwargs):
        super(ContactDialog, self).__init__(**kwargs)
        self.screen = screen
        self.content = MDList()
        self.load_contacts()
        self.add_action_button(text="Cancelar",
                               action=lambda *x: self.dismiss())

    def load_contacts(self, ):
        for c in db(ContatoModel).select(orderby=ContatoModel.nome):
            self.content.add_widget(ChooseContactItem(self, c))

        # with session_scope() as session:
        #     for c in session.query(Contato).order_by(Contato.nome).all():
        #         self.content.add_widget(ChooseContactItem(self, c))
        #         session.expunge(c)


class FrequenciaItem(OneLineListItem):
    item = ObjectProperty()

    def __init__(self, dialog, item, **kwargs):
        super(FrequenciaItem, self).__init__(**kwargs)
        self.dialog = dialog
        self.item = item
        self.text = self.item.name

    def on_press(self):
        app = App.get_running_app()
        cur_screen = app.root.ids.scr_mngr.current_screen
        cur_screen.frequencia = self.item
        self.dialog.dismiss()


class FrequenciaDialog(MDDialog):
    def __init__(self, screen, **kwargs):
        super(FrequenciaDialog, self).__init__(**kwargs)
        self.screen = screen

        self.content = MDList()
        self.load_options()
        self.add_action_button(text="Cancelar", action=lambda *x: self.dismiss())

    def load_options(self, ):
        for item in FREQUENCIA:
            self.content.add_widget(FrequenciaItem(self, item))



class ExcluirTransacaoDialogo(MDDialog):
    def __init__(self, screen, action, **kwargs):
        super(ExcluirTransacaoDialogo, self).__init__(**kwargs)
        self.title = 'Excluir Transação'

        self.content = StackLayout()
        self.content.add_widget(MDLabel(
                text="Tem certeza que deseja excluir esta transação?\nEsta ação não tem retorno.",
                font_style='Caption', size_hint_y=None,
                valign='center')
        )
        self.add_action_button("Excluir", action=action)
        self.add_action_button("Cancelar", action=self.dismiss)

#
# class ItemFrequencia(OneLineListItem):
#     enum = ObjectProperty()
#
#     def __init__(self, dialog, enum):
#         super(ItemFrequencia, self).__init__()
#         self.enum = enum
#         self.dialog = dialog
#         self.text = self.enum.name
#
#     def on_press(self):
#         self.dialog.item = self.enum
#         self.dialog.dismiss()
#
#
# class FrequenciaDialog(MDDialog):
#     items = ObjectProperty()
#     screen = None
#     item = ObjectProperty()
#
#     def __init__(self, **kwargs):
#         super(FrequenciaDialog, self).__init__()
#         self.items = kwargs.get('items')
#         self.screen = kwargs.get('screen')
#         self.content = MDList()
#
#         for i in self.items:
#             item = ItemFrequencia(self, i)
#             self.content.add_widget(item)
#         self.add_action_button('Cancelar', self.dismiss)
#
#     def on_item(self, instance, value):
#         self.screen.frequencia = value
