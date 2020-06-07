from server import db, Vine, Producer, Sort, Comment

def show():
    for vine in Vine.query.all():
        name = vine.name
        sort = vine.sort.name
        price = vine.price
        producer = vine.producer.name
        print(f"|{vine.id:^5}|{name:^15}|{sort:^20}|{price:^10.2f}|{producer:^15}|")

if __name__ == '__main__':
    show()
    vine_id = int(input('введите id: '))
    # vine = Vine.query.filter(Vine.id == vine_id).first()
    vine = Vine.query.get(vine_id)
    print(f'ваш выбор: {vine.name} \"{vine.producer.name}\"')
    option = int(input('введите вариант: 1 - менять название, 2 - cорт: '))
    if option == 1:
        newname = input('введите новое название: ')
        vine.name = newname
    if option == 2:
        for sort in Sort.query.all():
            print(f"{sort.id} - {sort.name}")
        sort_id = int(input('введите новый id сорта: '))
        vine.sort = Sort.query.get(sort_id)
    db.session.commit()
    show()


