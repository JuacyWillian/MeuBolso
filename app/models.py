from datetime import *
from uuid import UUID

from pony.orm import *

db = Database()


class Contact(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    name = Required(str)
    photo = Optional(str)
    phone = Optional(str)
    address = Optional(str)
    email = Optional(str)
    incomes = Set('Income')
    status = Optional(str)


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
