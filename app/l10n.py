from datetime import date

from babel import Locale
from babel.dates import format_date
from decimal import Decimal

from babel.numbers import format_decimal, format_currency

locale = Locale('pt_BR')
print(format_date(date.today(), locale=locale))

preco = Decimal('132.23')
print(format_currency(preco, 'BRL', locale=locale))
print(format_decimal(preco))