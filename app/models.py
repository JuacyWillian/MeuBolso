from datetime import *
from decimal import Decimal
from uuid import UUID

from pony.orm import Database, PrimaryKey, Required, Optional, Set, LongStr

db = Database()


class Contact(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    name = Required(str)
    phone = Optional(str)
    address = Optional(str)
    email = Optional(str)
    tickets = Set('Ticket')


class Ticket(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    title = Required(str)
    description = Optional(LongStr)
    pubdate = Required(date, default=datetime.now())
    tvalue = Required(float)
    nparcels = Required(int, default=1)
    parcels = Set('Parcel')
    ttype = Required(str)
    contact = Optional(Contact)


class Parcel(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    title = Required(str)
    ticket = Required('Ticket')
    expiration = Required(date)
    value = Required(Decimal)
    paid = Required(bool, default=False)
