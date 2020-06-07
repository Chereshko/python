import os
from server import db, Vine, Producer, Sort, Comment

DBNAME = 'vines.sqlite'

if os.path.exists(DBNAME):
    os.remove(DBNAME)

db.create_all()

koblevo = Producer(name='Коблево')
massandra = Producer(name='Массандра')
vardiani = Producer(name='Вардиани')

for producer in koblevo, massandra, vardiani:
    db.session.add(producer)

red_dry = Sort(name='красное сухое')
red_semidry = Sort(name='красное полусухое')
white_dry = Sort(name='белое сухое')
red_sweet = Sort(name='красное десертное')

for sort in red_dry, red_semidry, white_dry, red_sweet:
    db.session.add(sort)

vines = [
    Vine(name='Каберне',    price=45.0, producer=koblevo,   sort=red_dry),
    Vine(name='Мерло',      price=50.0, producer=massandra, sort=red_semidry, bestseller=1),
    Vine(name='Алиготе',    price=40.0, producer=massandra, sort=white_dry),
    Vine(name='Портвейн',   price=65.0, producer=koblevo,   sort=red_sweet),
    Vine(name='Хванчкара',  price=90.0, producer=vardiani,  sort=red_semidry, bestseller=1),
    Vine(name='Кагор',      price=65.0, producer=massandra, sort=red_sweet),
    Vine(name='Саперави',   price=70.0, producer=vardiani,  sort=red_dry),
    Vine(name='Каберне',    price=50.0, producer=massandra, sort=red_dry),
    Vine(name='Шардоне',    price=55.0, producer=koblevo,   sort=white_dry, bestseller=1),
]

db.session.add_all(vines)
db.session.commit()