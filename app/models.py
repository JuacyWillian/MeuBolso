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
    tickets = Set('Ticket')


class Ticket(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    title = Required(str)
    description = Optional(LongStr)
    pubdate = Required(datetime, default=datetime.now())
    tvalue = Required(float)
    nparcels = Required(int, default=1)
    parcels = Set('Parcel')
    type = Required(str)
    contact = Optional(Contact)


class Parcel(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    ticket = Required('Ticket')
    validate = Required(datetime)
