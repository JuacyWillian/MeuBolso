from datetime import *
from decimal import Decimal

from pony.orm import Database, Required, Optional, Set, LongStr

from app.util import TIPO_TRANSACAO, TIPO_PAGAMENTO

db = Database()


class Contato(db.Entity):
    nome = Required(str)
    telefone = Optional(str)
    endereco = Optional(str)
    email = Optional(str)
    transacoes = Set('Transacao')


class Transacao(db.Entity):
    nome = Required(str)
    descricao = Optional(LongStr)
    lancamento = Required(date, default=date.today())
    parcelado = Required(bool, default=False)
    parcelas = Set('Parcela')
    tipo_transacao = Required(str, default=TIPO_TRANSACAO.DESPESA.name)
    contato = Optional(Contato)
    tipo_pagamento = Required(str, default=TIPO_PAGAMENTO.A_VISTA.name)
    valor = Required(Decimal)
    recorrente = Required(bool, default=False)
    frequencia = Optional(str)


class Parcela(db.Entity):
    nome = Required(str)
    transacao = Required('Transacao')
    vencimento = Required(date)
    valor = Required(Decimal)
    pago = Required(bool, default=False)
