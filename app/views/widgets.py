from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.list import ThreeLineListItem, OneLineListItem

from app.util import TELAS

kv = """

<ItemParcela>:
    orientation: 'vertical'
    size_hint_y: None
    height: '50dp'
    
    MDLabel:
        id: parcel_title
        font_style: 'Caption'
        text: root.parcela.nome
        bold: True
        
    BoxLayout:
        padding: [0,0,0,15]
        MDLabel:
            id: parcel_expiration
            font_style: 'Caption'
            text: "Validade: %s"%root.parcela.vencimento
            size_hint: .4, None
            height: '25dp'

        MDLabel:
            id: parcel_value
            font_style: 'Caption'
            # text: "R$ %s" % root.valor
            size_hint: .3, None
            height: '25dp'

        MDCheckbox:
            id: parcel_paid
            size_hint: .05, None
            height: self.width

        MDLabel:
            id: parcel_paid
            font_style: 'Caption'
            halign: 'center'
            text: 'Pago' if parcel_paid else 'Não Pago'
            size_hint: .15, None
            height: '25dp'

"""

Builder.load_string(kv)


class ContactListItem(OneLineListItem):
    def __init__(self, id, **kwargs):
        super(ContactListItem, self).__init__(**kwargs)
        self.id = id
        self.app = App.get_running_app()

    def on_release(self):
        self.app.root.switch_to(TELAS.DETALHE_CONTATO, id=self.id)


class TransactionListItem(ThreeLineListItem):
    parcela = ObjectProperty()

    def __init__(self, parcela, **kwargs):
        super(TransactionListItem, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.parcela = parcela
        self.text = parcela.nome
        self.secondary_text = "%s\t%.2f" % (
            self.parcela.vencimento.strftime("%Y/%m/%d"), self.parcela.valor)

    def on_release(self):
        self.app.root.switch_to(
            TELAS.DETALHE_TRANSACAO, id=self.parcela.transacao.id)


class ItemParcela(BoxLayout):
    parcela = ObjectProperty()

    def __init__(self, parcela, **kwargs):
        self.parcela = parcela

        super(ItemParcela, self).__init__(**kwargs)
