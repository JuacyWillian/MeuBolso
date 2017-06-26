from decimal import ROUND_DOWN

from dateutil.relativedelta import relativedelta
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty, \
    NumericProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from pony.orm import db_session, select, rollback, delete

from app.models import *
from app.util import TELAS
from app.views.dialogos import FrequenciaDialog, ContactDialog, \
    ExcluirTransacaoDialogo
from app.views.widgets import TransactionListItem, ItemParcela

kv = """
<TransactionList>:
    ScrollView:
        do_scroll_x: False
        MDList:
            id: transaction_list
            
    MDFloatingActionButton:
        id: float_act_btn
        icon: 'plus'
        opposite_colors: True
        elevation_normal: 8
        pos_hint: {'center_x': 0.85, 'center_y': 0.1}
        on_press: app.root.switch_to(TELAS.NOVA_TRANSACAO)


<NewTransaction>:
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
                hint_text: "Nome: "
                required: True

            MDTextField:
                id: descricao
                multiline: True
                hint_text: 'Descrição: '

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                MDTextField:
                    id: lancamento
                    hint_text: 'Data: '
                    required: True

                MDIconButton:
                    size_hint: None, None
                    icon: 'calendar'
                    on_press: root.show_datepicker('lancamento')

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                MDTextField:
                    id: vencimento
                    hint_text: 'Validade: '
                    required: True

                MDIconButton:
                    size_hint: None, None
                    icon: 'calendar'
                    on_press: root.show_datepicker('vencimento')

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                spacing: '10dp'

                MDTextField:
                    id: valor
                    hint_text: "Valor: "
                    input_filter: 'float'
                    input_type: 'number'
                    required: True
                    text: '0'

                MDCheckbox:
                    id: parcelamento
                    size_hint_x: None #, None
                    size: '24dp', '24dp'
                    active: False

                MDTextField:
                    id: nparcelas
                    hint_text: "Parcelas:"
                    size_hint_x: None
                    width: '100dp'
                    required: True
                    input_filter: 'int'
                    text: '1'
                    disabled: False if parcelamento.active else True

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                spacing: '10dp'

                MDCheckbox:
                    id: recorrente
                    size_hint_x: None #, None
                    size: '24dp', '24dp'
                    active: False

                MDTextField:
                    id: frequencia
                    hint_text: "Frequência:"
                    required: True
                    text: '1'
                    disabled: False if recorrente.active else True
                    on_focus: root.show_frequency_dialog()

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)

                MDLabel:
                    # id: type_ticket
                    font_style: 'Caption'
                    font_size: '16dp'
                    text: 'Receita'
                    disabled: False if switch.active else True
                    size_hint_x: .4
                    size_hint_y: None
                    halign: 'center'
                    height: '24dp'

                MDSwitch:
                    id: switch
                    size_hint: None, None
                    size: '48dp', '24dp'
                    height: '24dp'

                MDLabel:
                    # id: type_ticket
                    font_style: 'Caption'
                    font_size: '16dp'
                    text: 'Despesa'
                    disabled: True if switch.active else False
                    size_hint_x: .4
                    size_hint_y: None
                    halign: 'center'
                    height: '24dp'

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                MDTextField:
                    id: contato
                    hint_text: 'Contato:'
                    disabled: True

                MDIconButton:
                    size_hint: None, None
                    icon: 'close'
                    on_press: root.contato = []
                    disabled: True if contato.text == '' else False

                MDIconButton:
                    size_hint: None, None
                    icon: 'account-box-outline'
                    on_press: root.show_choose_contact_dialog()


<ViewTransaction>:
    ScrollView:
        do_scroll_x: False

        StackLayout:
            size_hint_y: None
            height: self.minimum_height
            padding: '10dp'
            spacing: '5dp'

            MDLabel:
                id: nome
                font_style: 'Title'
                size_hint_y: None
                height: dp(60)

            MDLabel:
                id: descricao
                font_style: 'Body1'
                size_hint_y: None

            GridLayout:
                cols: 2
                size_hint_y: None
                height: dp(160)
                spacing: dp(5)
                row_force_default: True
                row_default_height: '20dp'
                padding: [0,15,0,5]

                MDLabel:
                    id: lancamento
                    size_hint_x: None
                    font_style: 'Caption'

                MDLabel:
                    id: valor
                    size_hint_x: None
                    font_style: 'Caption'

                MDLabel:
                    id: parcelado
                    font_style: 'Caption'

                MDLabel:
                    id: tipo_pagamento
                    font_style: 'Caption'

                MDLabel:
                    id: tipo_transacao
                    size_hint_x: None
                    font_style: 'Caption'

                MDLabel:
                    id: frequencia
                    font_style: 'Caption'

                MDLabel:
                    id: recorrente
                    size_hint_x: None
                    text: 'Tipo: '
                    font_style: 'Caption'

                MDLabel:
                    id: contato
                    font_style: 'Caption'


            BoxLayout:
                size_hint_y: None
                orientation: 'vertical'
                height: self.minimum_height
                spacing: dp(5)
                id: parcel_list
"""

Builder.load_string(kv)


class TransactionList(Screen):
    lista_transacao = ListProperty()

    def __init__(self, **kwargs):
        super(TransactionList, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.populate_listview()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['menu', lambda x: self.app.root.toggle_nav_drawer()],
        ]
        toolbar.right_action_items = []

    @db_session
    def populate_listview(self):
        lista_transacao = self.ids.transaction_list
        today = date.today()
        for p in select(p for p in db.Parcela if (
                        p.vencimento.year == today.year and p.vencimento.month == today.month) or (
                        p.pago == False and p.vencimento < today)).order_by(
            db.Parcela.vencimento)[:]:
            lista_transacao.add_widget(TransactionListItem(p))


class ViewTransaction(Screen):
    transacao = ObjectProperty()

    def __init__(self, id, **kwargs):
        super(ViewTransaction, self).__init__(**kwargs)
        self.app = App.get_running_app()
        with db_session:
            self.transacao = Transacao.get(id=id)

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids['toolbar']
        toolbar.left_action_items = [
            ['arrow-left',
             lambda x: self.app.root.switch_to(TELAS.LISTA_TRANSACAO)]]

        toolbar.right_action_items = [
            ['pencil',lambda x: self.app.root.switch_to(TELAS.EDITAR_TRANSACAO, id=self.transacao.id)],
            ['delete', lambda x: self.remove()]]

    @db_session
    def on_transacao(self, instance, value):
        lista_parcelas = self.ids.parcel_list
        lista_parcelas.clear_widgets()
        # transacao_fields = [
        #     'nome', 'descricao', 'valor', 'lancamento', 'parcelado',
        #     'tipo_transacao', 'contato', 'tipo_pagamento',
        #     'recorrente', 'frequencia',
        # ]
        #
        # for field in transacao_fields:
        #     self.ids[field].text = str(getattr(self.transacao, field, None))

        self.ids.nome.text = self.transacao.nome
        self.ids.descricao.text = self.transacao.descricao
        self.ids.valor.text = "Valor:\n%.2f" % self.transacao.valor
        self.ids.lancamento.text = "Lançamento:\n%s" % self.transacao.lancamento.strftime("%Y/%m/%d")
        self.ids.parcelado.text = "Parcelado:\n%s" % 'Sim' if self.transacao.parcelado else 'Não'
        self.ids.tipo_transacao.text = "Transação:\n%s" % self.transacao.tipo_transacao
        self.ids.tipo_pagamento.text = "Pagamento:\n%s" % self.transacao.tipo_pagamento.replace('_', ' ')
        self.ids.recorrente.text = "Recorrente:\n%s" % 'Sim' if self.transacao.recorrente else 'Não'
        self.ids.frequencia.text = "Frequencia:\n%s" % self.transacao.frequencia
        self.ids.contato.text = "Contato:\n%s" % self.transacao.contato.nome if self.transacao.contato else ''

        for parcela in self.transacao.parcelas.order_by(db.Parcela.vencimento):
            lista_parcelas.add_widget(ItemParcela(parcela))

    def remove(self):
        self.excluirdialog = ExcluirTransacaoDialogo(self, action=self.confirm_delete)
        self.excluirdialog.open()

    def confirm_delete(self, *args):
        self.excluirdialog.dismiss()
        with db_session:
            delete(t for t in db.Transacao if t.id == self.transacao.id)

        self.app.root.switch_to(TELAS.LISTA_TRANSACAO)


class NewTransaction(Screen):
    nome = StringProperty()
    descricao = StringProperty()
    valor = NumericProperty()

    lancamento = ObjectProperty()
    vencimento = ObjectProperty()

    tipo_transacao = ObjectProperty()
    tipo_pagamento = ObjectProperty()
    frequencia = ObjectProperty()

    parcelado = BooleanProperty()
    recorrente = BooleanProperty()

    contato = ObjectProperty()

    dialog = None
    frequencia_dialog = None

    def __init__(self, **kwargs):
        super(NewTransaction, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [['arrow-left',
                                      lambda x: self.app.root.switch_to(
                                          TELAS.LISTA_TRANSACAO)]]
        toolbar.right_action_items = [
            ['check', lambda x: self.salvar_transacao()]]

    def show_datepicker(self, value):
        self.mywidget = self.ids[value]
        MDDatePicker(self.set_date).open()

    def set_date(self, data_obj):
        self.mywidget.text = str(data_obj)

    def show_choose_contact_dialog(self):
        self.contato_dialog = ContactDialog(self)
        self.contato_dialog.open()

    def show_frequency_dialog(self):
        self.frequencia_dialog = FrequenciaDialog(self)
        self.frequencia_dialog.open()

    def on_contato(self, instance, value):
        contato = self.ids.contato
        if value:
            contato.text = self.contato.nome
        else:
            contato.text = ''

    def on_frequencia(self, instance, value):
        frequencia = self.ids.frequencia
        if value:
            frequencia.text = self.frequencia.name
        else:
            frequencia.text = ''

    @db_session
    def salvar_transacao(self):  # todo

        # List of errors
        erros = []

        # Getting data of fields
        nome = self.ids.nome.text
        descricao = self.ids.descricao.text

        lancamento = self.ids.lancamento.text
        vencimento = self.ids.vencimento.text

        valor = Decimal(self.ids.valor.text).quantize(
            Decimal('1.00'), rounding=ROUND_DOWN)

        parcelado = self.ids.parcelamento.active
        num_parcelas = int(self.ids.nparcelas.text)

        recorrente = self.ids.recorrente.active
        frequencia = self.ids.frequencia.text

        tipo_transacao = TIPO_TRANSACAO.RECEITA if self.ids.switch.active else TIPO_TRANSACAO.DESPESA
        tipo_pagamento = TIPO_PAGAMENTO.A_PRAZO if parcelado else TIPO_PAGAMENTO.A_VISTA

        contato = self.contato

        # Validating fields
        if nome in ['', ' ', None]:
            erros.append("O Campo 'nome' é obrigatório!")

        if lancamento in ['', ' ', None]:
            erros.append("O Campo 'data' é obrigatório!")

        else:
            try:
                lancamento = date(
                    *[int(f) for f in self.ids.lancamento.text.split('-')])

            except:
                erros.append(
                    "formato de data inválido para 'data'. \nClique no icone ao lado >>")

        if vencimento in ['', ' ', None]:
            erros.append("O Campo 'validade' é obrigatório!")

        else:
            try:
                vencimento = date(
                    *[int(f) for f in self.ids.vencimento.text.split('-')])

            except:
                erros.append(
                    "Formato de data inválido para 'validade'. \nClique no icone ao lado >>")

        try:
            diferenca = vencimento - lancamento
            if diferenca.days < 0:
                erros.append(
                    "A 'validade' não pode ser menor que a 'data'")

        except:
            pass

        if valor < 0:
            erros.append("O Campo 'valor' não pode ser 0 ou menos!")

        if num_parcelas < 1:
            erros.append("O Campo 'parcela' não pode ser menor que 1!")

        if contato:
            contato = Contato.get(id=contato.id)

        # Showing dialog with errors found
        if erros:
            dialog = MDDialog(title='Errors', size_hint=(.9, .8))
            box = StackLayout(size_hint_y=None)
            for e in erros:
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
                # num_parcelas = num_parcelas
                # valor = valor

                parcel_value = (valor / num_parcelas).quantize(Decimal('1.00'),
                                                               rounding=ROUND_DOWN)
                excedent = (valor - (parcel_value * num_parcelas)).quantize(
                    Decimal('1.00'), rounding=ROUND_DOWN)

                transacao = Transacao(
                    nome=nome, descricao=descricao, valor=valor,
                    lancamento=lancamento, tipo_transacao=tipo_transacao.name,
                    parcelado=parcelado, tipo_pagamento=tipo_pagamento.name,
                    recorrente=recorrente, frequencia=frequencia
                )

                # Creating Parcels of the Ticket
                if num_parcelas == 1:
                    transacao.parcelas.create(
                        nome="%s %d/%d" % (nome, 1, num_parcelas),
                        valor=valor, vencimento=vencimento, pago=False)

                else:
                    for p in range(num_parcelas):
                        if p == num_parcelas - 1:
                            parcel_value += excedent
                        nExpiration = vencimento + relativedelta(months=p)
                        transacao.parcelas.create(
                            nome="%s %d/%d" % (nome, p + 1, num_parcelas),
                            valor=parcel_value, vencimento=nExpiration,
                            pago=False)

                        # Changing to IncomeList
            except Exception as err:
                rollback()
                raise err
            finally:
                self.app.root.switch_to(TELAS.LISTA_TRANSACAO)


class EditTransaction(Screen):
    def __init__(self, **kwargs):
        super(EditTransaction, self).__init__(**kwargs)
        # todo
