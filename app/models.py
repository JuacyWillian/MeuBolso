from datetime import *
from uuid import UUID

from pony.orm import *

db = Database()


class Contact(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    name = Required(str)
    photo = Optional(str)
    emails = Set('Email')
    phones = Set('Phone')
    addresses = Set('Address')
    incomes = Set('Income')
    status = Optional(str)


class Email(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    name = Required(str)
    email = Required(str)
    contact = Required(Contact)


class Phone(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    name = Required(str)
    phone = Required(str)
    contact = Required(Contact)


class Address(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    name = Required(str)
    address = Required(str)
    contact = Required(Contact)


class Income(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    title = Required(str)
    description = Optional(LongStr)
    pubdate = Required(datetime, default=datetime.now())
    total_value = Required(float)
    contact = Required(Contact)
    nparcels = Required(int, default=1)
    parcels = Set('IncomeParcel')
    type = Required('IncomeType')


class IncomeParcel(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    income = Required(Income)
    description = Required(str)
    validate = Required(date)
    value = Required(float)


class IncomeType(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    title = Required(str)
    description = Optional(LongStr)
    income = Set(Income)
