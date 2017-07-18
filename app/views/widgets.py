from datetime import datetime

from babel.dates import format_date
from babel.numbers import format_currency
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.card import MDCard
from kivymd.list import ThreeLineListItem, OneLineListItem
from kivymd.menu import MDDropdownMenu, MDMenuItem

from app.lang import gettext as _
from app.models import ParcelaModel, db, ContatoModel
from app.util import TELAS

kv = """
<ItemParcela>:
    orientation: 'vertical'
    padding: '10dp'
    # height: self.minimum_height

    MDLabel:
        id: parcel_title
        font_style: 'Caption'
        font_size: '16sp'
        text: root.parcela.nome
        size_hint_y: None
        height: '40dp'
        bold:True
        
    BoxLayout:
        size_hint_y: None
        height: self.minimum_height
        MDLabel:
            id: parcel_expiration
            font_style: 'Caption'
            markup: True
            halign: 'center'
            text: "[b]Vencimento[/b]\\n %s"%format_date(root.parcela.vencimento,'short', locale=app.locale)
            size_hint_y: None
            height: '40dp'
    
        MDLabel:
            id: parcel_value
            font_style: 'Caption'
            markup: True
            halign: 'center'
            text: "[b]Pagamento[/b]\\n %s"%format_date(root.parcela.vencimento,'short', locale=app.locale)
            size_hint_y: None
            height: '40dp'
    
        MDLabel:
            id: parcel_value
            font_style: 'Caption'
            markup: True
            halign: 'center'
            text: "[b]Valor[/b]\\n %s"%format_currency(root.parcela.valor, 'BRL', locale=app.locale)
            size_hint_y: None
            height: '40dp'


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
        self.app.root.switch_to(TELAS.DETALHE_CONTATO, contato_id=self.contato.id)


class TransactionListItem(ThreeLineListItem):
    transacao_id = ObjectProperty()

    def __init__(self, parcela=None, **kwargs):
        self.app = App.get_running_app()

        self.menu_items = [
            {'viewclass': 'MDMenuItem', 'text': 'Marcar como Paga!', 'on_press': lambda *x: self.marcar_como_paga()},
        ]

        self.transacao_id = parcela.transacao_id
        self.parcela_id = parcela.id
        super(TransactionListItem, self).__init__(**kwargs)

        self.text = parcela.nome
        self.secondary_text = "Vencimento: {dataVenc}\nValor: {valor}".format(
            dataVenc=format_date(parcela.vencimento),
            valor=format_currency(parcela.valor, 'BRL', locale=self.app.locale))

    def on_press(self):
        self.start_press = datetime.now()

    def on_release(self):
        self.end_press = datetime.now()
        self.time_pressed = (self.end_press - self.start_press).total_seconds()
        self.start_press = None
        self.end_press = None

        if self.time_pressed <= 1:
            self.app.root.switch_to(TELAS.DETALHE_TRANSACAO, transacao_id=self.transacao_id)
        else:
            self.show_options()

    def show_options(self):
        MDDropdownMenu(items=self.menu_items, width_mult=4).open(self)

    def marcar_como_paga(self, *args):
        parcela = db(ParcelaModel.id==self.parcela_id).update(pago=True)
        db.commit()
        # parcela = session.query(Parcela).filter_by(id=self.parcela_id).first()
        # parcela.pago = True
        self.app.root.switch_to(TELAS.LISTA_TRANSACAO)


class ItemParcela(MDCard):
    parcela = ObjectProperty()

    def __init__(self, parcela, **kwargs):
        self.parcela = parcela
        super(ItemParcela, self).__init__(**kwargs)

    def on_release(self, *args):
        print(self.parcela)
