from datetime import datetime, date

from pydal import DAL, Field

from app.util import TIPO_PAGAMENTO, TIPO_TRANSACAO
from settings import dbdir

db = DAL('sqlite://storage.db', folder=dbdir)

ContatoModel = db.define_table(
    'contatos',
    Field('nome'),
    Field('telefone'),
    Field('email'),
    Field('endereco')
)

TransacaoModel = db.define_table(
    'transacoes',
    Field('nome', ),
    Field('descricao'),
    Field('lancamento', 'datetime', default=datetime.now()),
    Field('tipo_transacao', default=TIPO_TRANSACAO.DESPESA.name),
    Field('valor', 'float', ),
    Field('tipo_pagamento', default=TIPO_PAGAMENTO.A_VISTA.name),
    Field('recorrente', 'boolean', default=False),
    Field('parcelado', 'boolean', default=False),
    Field('frequencia', 'string', ),
    Field('contato', 'reference contatos')
)

ParcelaModel = db.define_table(
    'parcelas',
    Field('nome'),
    Field('transacao_id', 'reference transacoes'),
    Field('valor', 'float'),
    Field('vencimento', 'date'),
    Field('pago', 'boolean'),
    Field('data_pagamento', 'date'),
)


def parcelasDefault():
    today = date.today()
    return db(
        (ParcelaModel.pago == False) & \
        (ParcelaModel.vencimento.year() <= today.year) & \
        (ParcelaModel.vencimento.month() <= today.month)) \
        .select(orderby=ParcelaModel.vencimento)
