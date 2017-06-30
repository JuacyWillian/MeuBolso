from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.list import ThreeLineListItem, OneLineListItem

from app.models import Transacao, Session
from app.util import TELAS

kv = """
<ItemParcela>:
    orientation: 'vertical'
    size_hint_y: None
    height: '50dp'
    
    MDLabel:
        contato: parcel_title
        font_style: 'Caption'
        text: root.parcela.nome
        bold: True
        
    BoxLayout:
        padding: [0,0,0,15]
        MDLabel:
            contato: parcel_expiration
            font_style: 'Caption'
            text: "Validade: %s"%root.parcela.vencimento
            size_hint: .4, None
            height: '25dp'

        MDLabel:
            contato: parcel_value
            font_style: 'Caption'
            # text: "R$ %s" % root.valor
            size_hint: .3, None
            height: '25dp'

        MDCheckbox:
            contato: parcel_paid
            size_hint: .05, None
            height: self.width

        MDLabel:
            contato: parcel_paid
            font_style: 'Caption'
            halign: 'center'
            text: 'Pago' if parcel_paid else 'Não Pago'
            size_hint: .15, None
            height: '25dp'


<IconView@MDLabel>:
    font_style: 'Icon'
    size_hint: None, None
    font_size: '24'
    size: 48, 48
    halign: 'center'
    valign: 'center'
    icon: ''
    text: u'{}'.format(md_icons.get(root.icon, ''))
"""

Builder.load_string(kv)


class ContactListItem(OneLineListItem):
    def __init__(self, contato, **kwargs):
        super(ContactListItem, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.contato = contato
        self.text = self.contato.nome

    def on_release(self):
        self.app.root.switch_to(TELAS.DETALHE_CONTATO, contato=self.contato)


class TransactionListItem(ThreeLineListItem):
    # parcela = ObjectProperty()
    transacao_id = ObjectProperty()
    def __init__(self, parcela, **kwargs):
        self.app = App.get_running_app()

        # self.parcela = parcela
        self.transacao_id = parcela.transacao.id
        super(TransactionListItem, self).__init__(**kwargs)

        self.text = parcela.nome
        self.secondary_text = "Vencimento: %s\nR$ %.2f" % (
            parcela.vencimento.strftime("%Y/%m/%d"), parcela.valor)

    def on_release(self):
        self.app.root.switch_to(TELAS.DETALHE_TRANSACAO, transacao_id=self.transacao_id)

class ItemParcela(BoxLayout):
    parcela = ObjectProperty()

    def __init__(self, parcela, **kwargs):
        self.parcela = parcela
        super(ItemParcela, self).__init__(**kwargs)
