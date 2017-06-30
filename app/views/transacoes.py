from datetime import date
from decimal import ROUND_DOWN, Decimal

from dateutil.relativedelta import relativedelta
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivymd.date_picker import MDDatePicker
# from pony.orm import rollback, delete
from sqlalchemy import or_, and_, extract, cast, Date

from app.util import *
from app.views.dialogos import *
from app.views.widgets import *

kv = """
<TelaTransacoes>:
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


<TelaNovaTransacao>:
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


<TelaVisualizarTransacao>:
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
                text: root.transacao.nome
                size_hint_y: None
                height: dp(60)

            MDLabel:
                id: descricao
                font_style: 'Body1'
                size_hint_y: None
                # text: root.transacao.descricao

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
                    text: root.transacao.lancamento.strftime("%Y/%m/%d")

                MDLabel:
                    id: valor
                    size_hint_x: None
                    font_style: 'Caption'
                    text: "R$ %.2f"%root.transacao.valor

                MDLabel:
                    id: parcelado
                    font_style: 'Caption'
                    text: "%s"%root.transacao.parcelado

                MDLabel:
                    id: tipo_pagamento
                    font_style: 'Caption'
                    text: "%s"%root.transacao.tipo_pagamento.replace('_', ' ')

                MDLabel:
                    id: tipo_transacao
                    size_hint_x: None
                    font_style: 'Caption'
                    text: "%s"%root.transacao.tipo_transacao.replace('_', ' ')

                MDLabel:
                    id: frequencia
                    font_style: 'Caption'
                    text: root.transacao.frequencia

                MDLabel:
                    id: recorrente
                    size_hint_x: None
                    text: 'Tipo: '
                    font_style: 'Caption'
                    text: "%s"%root.transacao.recorrente

                MDLabel:
                    id: contato
                    font_style: 'Caption'
                    text: root.contato.nome if root.contato else ''


            BoxLayout:
                size_hint_y: None
                orientation: 'vertical'
                height: self.minimum_height
                spacing: dp(5)
                id: parcel_list
"""

Builder.load_string(kv)


class TelaTransacoes(Screen):
    lista_transacao = ListProperty()

    def __init__(self, **kwargs):
        super(TelaTransacoes, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.populate_listview()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [['menu', lambda x: self.app.root.toggle_nav_drawer()]]
        toolbar.right_action_items = []

    def populate_listview(self):
        lista_transacao = self.ids.transaction_list
        today = date.today()
        with session_scope() as session:
            for p in session.query(Parcela).filter(or_(
                    and_(extract('year', Parcela.vencimento) == today.year, extract('month', Parcela.vencimento) == today.month),
                    and_(Parcela.pago == False, cast(Parcela.vencimento, Date) < cast(today, Date)))).order_by(Parcela.vencimento).all():
                lista_transacao.add_widget(TransactionListItem(p))
                session.expunge(p)


class TelaVisualizarTransacao(Screen):
    transacao_id = NumericProperty()
    transacao = ObjectProperty()
    contato = ObjectProperty()

    def __init__(self, transacao_id, **kwargs):
        self.app = App.get_running_app()
        self.transacao_id = transacao_id
        self.load_data()
        super(TelaVisualizarTransacao, self).__init__(**kwargs)

    def load_data(self, ):
        with session_scope() as session:
            self.transacao = session.query(Transacao).filter_by(id=self.transacao_id).first()
            self.contato = self.transacao.contato
            session.expunge_all()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids['toolbar']
        toolbar.left_action_items = [
            ['arrow-left', lambda x: self.app.root.switch_to(TELAS.LISTA_TRANSACAO)]]

        toolbar.right_action_items = [
            ['pencil', lambda x: self.app.root.switch_to(
                TELAS.EDITAR_TRANSACAO, transacao_id=self.transacao.id)],
            ['delete', lambda x: self.remove()]]

    def remove(self):
        self.excluirdialog = ExcluirTransacaoDialogo(self, action=self.confirm_delete)
        self.excluirdialog.open()

    def confirm_delete(self, *args):
        self.excluirdialog.dismiss()

        with session_scope() as session:
            transacao = session.query(Transacao).filter_by(id=self.transacao_id).first()
            session.delete(transacao)
            session.commit()
        self.app.root.switch_to(TELAS.LISTA_TRANSACAO)


class TelaNovaTransacao(Screen):
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
        super(TelaNovaTransacao, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [['arrow-left', lambda x: self.app.root.switch_to(TELAS.LISTA_TRANSACAO)]]
        toolbar.right_action_items = [['check', lambda x: self.salvar_transacao()]]

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

        with session_scope() as session:
            if contato:
                contato = session.query(Contato).filter_by(id=self.contato.id).first()
                session.commit()
                session.expunge(contato)

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
            transacao = None
            with session_scope() as session:

                parcel_value = (valor / num_parcelas).quantize(Decimal('1.00'), rounding=ROUND_DOWN)
                excedent = (valor - (parcel_value * num_parcelas)).quantize(
                    Decimal('1.00'), rounding=ROUND_DOWN)

                transacao = Transacao(
                    nome=nome, descricao=descricao, valor=valor,
                    lancamento=lancamento, tipo_transacao=tipo_transacao.name,
                    parcelado=parcelado, tipo_pagamento=tipo_pagamento.name,
                    recorrente=recorrente, frequencia=frequencia
                )
                session.add(transacao)
                session.commit()

                # Creating Parcels of the Ticket
                if num_parcelas == 1:
                    parcela = Parcela(
                        nome="%s %d/%d" % (nome, 1, num_parcelas),
                        valor=valor, vencimento=vencimento, pago=False)
                    session.add(parcela)
                    transacao.parcelas.append(parcela)
                    session.commit()

                else:
                    for p in range(num_parcelas):
                        if p == num_parcelas - 1: parcel_value += excedent
                        nExpiration = vencimento + relativedelta(months=p)
                        parcela = Parcela(
                            nome="%s %d/%d" % (nome, p + 1, num_parcelas),
                            valor=parcel_value, vencimento=nExpiration,
                            pago=False)
                        session.add(parcela)
                        transacao.parcelas.append(parcela)
                        session.commit()
                self.app.root.switch_to(TELAS.DETALHE_TRANSACAO, transacao_id=transacao.id)


class TelaEditarTransacao(Screen):  # todo
    transacao_id = NumericProperty()
    transacao = ObjectProperty()
    contato = ObjectProperty()

    def __init__(self, transacao_id, **kwargs):
        self.app = App.get_running_app()
        self.transacao_id = transacao_id
        self.load_data()
        super(TelaEditarTransacao, self).__init__(**kwargs)

    def load_data(self):
        with session_scope() as session:
            self.transacao = session.query(Transacao).filter_by(id=self.transacao_id).first()
            self.contato = self.transacao.contato
            session.expunge_all()
