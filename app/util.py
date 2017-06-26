from enum import Enum


class TIPO_PAGAMENTO(Enum):
    A_VISTA = 0
    A_PRAZO = 1


class TELAS(Enum):
    INICIO = 0
    LISTA_CONTATO = 1
    NOVO_CONTATO = 2
    DETALHE_CONTATO = 3
    EDITAR_CONTATO = 4
    LISTA_TRANSACAO = 5
    NOVA_TRANSACAO = 6
    DETALHE_TRANSACAO = 7
    CONFIGURACAO = 8
    SOBRE = 9
    EDITAR_TRANSACAO = 10


class TIPO_TRANSACAO(Enum):
    DESPESA = 0
    RECEITA = 1


class FREQUENCIA(Enum):
    DIARIAMENTE = 0
    SEMANALMENTE = 1
    MENSALMENTE = 2
    BIMESTRALMENTE = 3
    TRIMESTRALMENTE = 4
    SEMESTRALMENTE = 5
    ANUALMENTE = 6
