from datetime import date
from decimal import ROUND_DOWN, Decimal

from dateutil.relativedelta import relativedelta
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import (NumericProperty, ObjectProperty, ListProperty, )
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel

from app.lang import s
from app.models import parcelasDefault, db, TransacaoModel, ParcelaModel, ContatoModel
from app.util import TELAS, TIPO_TRANSACAO, TIPO_PAGAMENTO, FREQUENCIA
from app.views.dialogos import ExcluirTransacaoDialogo, ContactDialog, FrequenciaDialog
from app.views.widgets import TransactionListItem, ItemParcela

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

                MDTextField:
                    id: freq_qtd
                    hint_text: "Quantidade:"
                    size_hint_x: None
                    width: '100dp'
                    input_filter: 'int'
                    required: True if recorrente.active else False
                    disabled: False if recorrente.active else True

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
                    
    # MDFloatingActionButton:
    #     id: float_act_btn
    #     icon: 'content-save'
    #     opposite_colors: True
    #     elevation_normal: 8
    #     pos_hint: {'center_x': 0.85, 'center_y': 0.1}
    #     on_press: root.salvar_transacao()


<TelaEditarTransacao>:
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
                text: root.transacao.nome
                required: True

            MDTextField:
                id: descricao
                multiline: True
                text: root.transacao.descricao
                hint_text: 'Descrição: '

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                MDTextField:
                    id: lancamento
                    hint_text: 'Data: '
                    text: format_date(root.transacao.lancamento, locale=app.locale)
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
                    # text: format_date(root.transacao.vencimento, locale=app.locale)
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
                    text: str(root.transacao.valor)

                MDCheckbox:
                    id: parcelamento
                    size_hint_x: None #, None
                    size: '24dp', '24dp'
                    active: True if root.transacao.parcelado else False

                MDTextField:
                    id: nparcelas
                    hint_text: "Parcelas:"
                    size_hint_x: None
                    width: '100dp'
                    required: True
                    input_filter: 'int'
                    text: str(len(root.parcelas))
                    disabled: False if parcelamento.active else True

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                spacing: '10dp'

                MDCheckbox:
                    id: recorrente
                    size_hint_x: None #, None
                    size: '24dp', '24dp'
                    active: True if root.transacao.recorrente else False

                MDTextField:
                    id: frequencia
                    hint_text: "Frequência:"
                    required: True
                    text: root.transacao.frequencia if root.transacao.recorrente else ''
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
                    text: root.transacao.nome if root.contato else ''
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
                text: root.transacao.descricao

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
                    text: root.transacao.frequencia if root.transacao.frequencia else ''

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

            MDList:
                id: lista_parcelas
                
    # MDFloatingActionButton:
    #     id: float_act_btn
    #     icon: 'content-save'
    #     opposite_colors: True
    #     elevation_normal: 8
    #     pos_hint: {'center_x': 0.85, 'center_y': 0.3}
    #     on_press: self.salvar_transacao()
"""

Builder.load_string(kv)


class TelaTransacoes(Screen):
    lista_transacao = ListProperty()

    def __init__(self, **kwargs):
        super(TelaTransacoes, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.populate_listview(self.load_items())

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.title = s.transacoes.capitalize()
        toolbar.left_action_items = [['menu', lambda x: self.app.root.toggle_nav_drawer()]]
        toolbar.right_action_items = []

    def load_items(self):
        return parcelasDefault()

    def populate_listview(self, items):
        lista_transacao = self.ids.transaction_list
        lista_transacao.clear_widgets()
        for p in items:
            lista_transacao.add_widget(TransactionListItem(p))


class TelaVisualizarTransacao(Screen):
    transacao_id = NumericProperty()
    transacao = ObjectProperty()
    contato = ObjectProperty()

    def __init__(self, transacao_id, **kwargs):
        self.app = App.get_running_app()
        self.transacao = TransacaoModel[transacao_id]
        super(TelaVisualizarTransacao, self).__init__(**kwargs)
        self.carregar_parcelas(self.load_items())

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids['toolbar']
        toolbar.left_action_items = [
            ['arrow-left', lambda x: self.app.root.switch_to(TELAS.LISTA_TRANSACAO)]]

        toolbar.right_action_items = [
            ['pencil', lambda x: self.app.root.switch_to(TELAS.EDITAR_TRANSACAO,
                                                         transacao_id=self.transacao.id)],
            ['delete', lambda x: self.remover_transacao()]]

    def load_items(self):
        return db(ParcelaModel.transacao_id == self.transacao_id).select(
            orderby=ParcelaModel.vencimento)

    def carregar_parcelas(self, items):
        lista_parcelas = self.ids.lista_parcelas
        for p in items:
            lista_parcelas.add_widget(ItemParcela(p))

    def remover_transacao(self):
        self.excluirdialog = ExcluirTransacaoDialogo(self, action=self.confirmar_remocao)
        self.excluirdialog.open()

    def confirmar_remocao(self, *args):
        self.excluirdialog.dismiss()

        db(TransacaoModel.id == self.transacao.id).delete()
        db.commit()

        self.app.root.switch_to(TELAS.LISTA_TRANSACAO)


class TelaNovaTransacao(Screen):
    def __init__(self, **kwargs):
        super(TelaNovaTransacao, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_pre_enter(self, *args):
        toolbar = self.app.root.ids.toolbar
        toolbar.left_action_items = [
            ['arrow-left', lambda x: self.app.root.switch_to(TELAS.LISTA_TRANSACAO)]]
        toolbar.right_action_items = [['content-save', lambda x: self.salvar_transacao()]]

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
        valor = Decimal(self.ids.valor.text).quantize(Decimal('1.00'), rounding=ROUND_DOWN)
        parcelado = self.ids.parcelamento.active
        num_parcelas = int(self.ids.nparcelas.text)
        recorrente = self.ids.recorrente.active
        frequencia = self.ids.frequencia.text
        freq_qtd = self.ids.freq_qtd.text
        tipo_transacao = TIPO_TRANSACAO.RECEITA if self.ids.switch.active else TIPO_TRANSACAO.DESPESA
        tipo_pagamento = TIPO_PAGAMENTO.A_PRAZO if parcelado else TIPO_PAGAMENTO.A_VISTA
        contato = self.contato

        # Validating fields
        if nome in ['', ' ', None]: erros.append("O Campo 'nome' é obrigatório!")
        if lancamento in ['', ' ', None]:
            erros.append("O Campo 'data' é obrigatório!")
        else:
            try:
                lancamento = date(*[int(f) for f in self.ids.lancamento.text.split('-')])
            except:
                erros.append("formato de data inválido para 'data'. \nClique no icone ao lado >>")

        if vencimento in ['', ' ', None]:
            erros.append("O Campo 'validade' é obrigatório!")
        else:
            try:
                vencimento = date(*[int(f) for f in self.ids.vencimento.text.split('-')])
            except:
                erros.append(
                    "Formato de data inválido para 'validade'.\nClique no icone ao lado >>")

        try:
            diferenca = vencimento - lancamento
            if diferenca.days < 0: erros.append("A 'validade' não pode ser menor que a 'data'")
        except:
            pass

        if valor < 0: erros.append("O Campo 'valor' não pode ter valor negativo!")

        if recorrente and parcelado:
            erros.append("A transação não pode ser parcelada e recorrente ao mesmo tempo.\n"
                         "Marque apenas uma das opções.")

        if parcelado:
            if num_parcelas < 1: erros.append("O Campo 'parcela' não pode ser menor que 1!")
        else:
            num_parcelas = 1

        if not recorrente:
            frequencia = None
            freq_qtd = None
        else:
            if freq_qtd in ('', None) or int(freq_qtd) < 2:
                erros.append("O Campo 'nome' é obrigatório!\n"
                             "E não pode ser inferior a 2.")
        try:
            contato = ContatoModel[self.contato.id]
        except:
            pass

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
            transacao_id = None

            parcel_value = (valor / num_parcelas).quantize(Decimal('1.00'), rounding=ROUND_DOWN)
            excedent = (valor - (parcel_value * num_parcelas)).quantize(
                Decimal('1.00'), rounding=ROUND_DOWN)

            transacao_id = TransacaoModel.insert(
                nome=nome, descricao=descricao, valor=valor,
                lancamento=lancamento, tipo_transacao=tipo_transacao.name,
                parcelado=parcelado, tipo_pagamento=tipo_pagamento.name,
                recorrente=recorrente, frequencia=frequencia
            )
            db.commit()

            # Creating Parcels of the Ticket
            if not parcelado and not recorrente:
                ParcelaModel.insert(
                    nome=nome, valor=valor, vencimento=vencimento, pago=False,
                    transacao_id=transacao_id
                )
                db.commit()
            elif parcelado:
                for p in range(num_parcelas):
                    if p == num_parcelas - 1: parcel_value += excedent
                    nExpiration = vencimento + relativedelta(months=p)
                    ParcelaModel.insert(
                        nome="{nome} {parcela}/{total}".format(
                            nome=nome, parcela=p + 1, total=num_parcelas),
                        valor=parcel_value, vencimento=nExpiration, pago=False,
                        transacao_id=transacao_id
                    )
                    db.commit()
            elif recorrente:
                for req in range(int(freq_qtd)):
                    periodo = self.calcula_periodo(frequencia, req)
                    nExpiration = vencimento + periodo
                    ParcelaModel.insert(
                        nome="{nome} {mes}/{ano}".format(
                            nome=nome, mes=nExpiration.month, ano=nExpiration.year),
                        valor=valor, vencimento=nExpiration, pago=False,
                        transacao_id=transacao_id
                    )
                    db.commit()
            self.app.root.switch_to(TELAS.DETALHE_TRANSACAO, transacao_id=transacao_id)

    def calcula_periodo(self, frequencia, passo):
        if frequencia == FREQUENCIA.DIARIAMENTE.name:
            return relativedelta(days=1 * passo)
        elif frequencia == FREQUENCIA.SEMANALMENTE.name:
            return relativedelta(weeks=1 * passo)
        elif frequencia == FREQUENCIA.MENSALMENTE.name:
            return relativedelta(months=1 * passo)
        elif frequencia == FREQUENCIA.BIMESTRALMENTE.name:
            return relativedelta(months=2 * passo)
        elif frequencia == FREQUENCIA.TRIMESTRALMENTE.name:
            return relativedelta(months=3 * passo)
        elif frequencia == FREQUENCIA.SEMESTRALMENTE.name:
            return relativedelta(months=6 * passo)
        elif frequencia == FREQUENCIA.ANUALMENTE.name:
            return relativedelta(years=1 * passo)


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
        self.transacao = db(TransacaoModel.id == self.transacao_id).select().first()
        self.contato = self.transacao.contato
        self.parcelas = self.transacao.parcelas.select()
