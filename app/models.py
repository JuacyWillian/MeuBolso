from datetime import *
from decimal import Decimal
from uuid import UUID

from pony.orm import Database, PrimaryKey, Required, Optional, Set, LongStr

db = Database()


class Contact(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    name = Required(str)
    photo = Optional(str)
    phone = Optional(str)
    address = Optional(str)
    email = Optional(str)
    tickets = Set('Ticket')

    def __init__(self, name, phone=None, address=None, email=None, photo=None):
        fields = dict(name=name, phone=phone, address=address,
                      email=email, photo=photo)
        super(Contact, self).__init__(**fields)


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

    def __init__(self, title, description, tvalue, pubdate, nparcels, ttype,
                 contact):
        fields = dict(
            title=title, description=description, tvalue=tvalue,
            pubdate=pubdate, nparcels=nparcels,
            ttype=ttype, contact=contact
        )

        super(Ticket, self).__init__(**fields)


class Parcel(db.Entity):
    uuid = PrimaryKey(UUID, auto=True)
    title = Required(str)
    ticket = Required('Ticket')
    expiration = Required(date)
    value = Required(Decimal)
    paid = Required(bool, default=False)

    def __init__(self, title, value, expiration, ticket):
        fields = dict(
            title=title, value=value, expiration=expiration, ticket=ticket)

        super(Parcel, self).__init__(**fields)
