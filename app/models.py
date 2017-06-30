from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE = 'sqlite:///storage.db'
db = create_engine(DATABASE, echo=True)
Base = declarative_base(db)


class CRUDMixim(object):
    pass


class Contato(Base):
    __tablename__ = 'contatos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, )
    telefone = Column(String, unique=True)
    email = Column(String, unique=True)
    endereco = Column(String, unique=True)
    transacoes = relationship('Transacao', back_populates='contato', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Contato(nome=%s, endereço=%s)>" % (
            self.nome, self.endereco)


class Transacao(Base):
    __tablename__ = 'transacoes'

    id = Column(Integer, primary_key=True)
    nome = Column(String, )
    descricao = Column(String, nullable=True)
    lancamento = Column(DateTime, default=datetime.now())
    parcelado = Column(Boolean, )
    parcelas = relationship('Parcela', back_populates='transacao', cascade="all, delete, delete-orphan")
    tipo_transacao = Column(String, )
    tipo_pagamento = Column(String, )
    valor = Column(Float, )
    recorrente = Column(Boolean)
    frequencia = Column(String)
    contato_id = Column(Integer, ForeignKey('contatos.id'))
    contato = relationship('Contato', back_populates='transacoes')

    def __repr__(self):
        return "<Transação(nome=%s, lançamento=%r, valor=%.2f)>" % (
            self.nome, self.lancamento, self.valor)


class Parcela(Base):
    __tablename__ = 'parcelas'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    transacao_id = Column(Integer, ForeignKey('transacoes.id'))
    transacao = relationship('Transacao', back_populates='parcelas')
    valor = Column(Float, nullable=False)
    vencimento = Column(DateTime, nullable=False)
    pago = Column(Boolean, default=False)

    def __repr__(self):
        return "<Parcela(nome=%s, valor=R$ %.2f)>" % (
            self.nome, self.valor)


Base.metadata.create_all()
Session = sessionmaker(bind=db)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()




# db = Database()
# class Contato(db.Entity):
#     nome = Required(str)
#     telefone = Optional(str)
#     endereco = Optional(str)
#     email = Optional(str)
#     transacoes = Set('Transacao')
#
#
# class Transacao(db.Entity):
#     nome = Required(str)
#     descricao = Optional(LongStr)
#     lancamento = Required(date, default=date.today())
#     parcelado = Required(bool, default=False)
#     parcelas = Set('Parcela')
#     tipo_transacao = Required(str, default=TIPO_TRANSACAO.DESPESA.name)
#     contato = Optional(Contato)
#     tipo_pagamento = Required(str, default=TIPO_PAGAMENTO.A_VISTA.name)
#     valor = Required(Decimal)
#     recorrente = Required(bool, default=False)
#     frequencia = Optional(str)
#
#
# class Parcela(db.Entity):
#     nome = Required(str)
#     transacao = Required('Transacao')
#     vencimento = Required(date)
#     valor = Required(Decimal)
#     pago = Required(bool, default=False)
