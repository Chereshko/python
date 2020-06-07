from faker import Faker
import random

fake=Faker()

for i in range(30):
    name=fake.first_name()
    age = random.randint(10,15)
    koef = random.randint(110,130)/10
    height = round(age*koef, 1)
    print(f'{name},{age},{height}')