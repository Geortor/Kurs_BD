from faker import Faker
from models import *
import datetime
import random

# Подключение к базе данных
db.connect()

fake = Faker('ru_RU')
Faker.seed(0)

def generate_personal_data():
     return Персональные_данные.create(
        фамилия=fake.last_name(),
        имя=fake.first_name(),
        отчество=fake.middle_name(),
        серия_паспорта=random.randint(1000, 9999),
        номер_паспорта=random.randint(100000, 999999),
        нас_пункт=fake.city(),
        улица=fake.street_name(),
        дом=fake.building_number(),
        квартира=random.randint(1, 200)
    )
def generate_employee():
    pers_data = generate_personal_data()
    return Сотрудник.create(
        персональные_данные = pers_data,
        должность=random.choice(["Менеджер", "Директор", "Агент"])
    )
def generate_client():
    pers_data = generate_personal_data()
    return Клиент.create(
        персональные_данные = pers_data
    )


def generate_tour():
    return Наименование_тура.create(
        направление=fake.country(),
        цена=random.randint(10000, 100000),
        кол_во_дней=random.randint(7, 21)
    )


def generate_deal():
     client = random.choice(Клиент.select())
     employee = random.choice(Сотрудник.select())
     tour = random.choice(Наименование_тура.select())
     status = random.choice(["Создана", "Закрыта"])

     if status == "Создана":
        return  Сделка.create(
            клиент = client,
            сотрудник = employee,
            тур = tour,
            дата_заключения=fake.date_between(start_date=datetime.date(2020, 1, 1), end_date=datetime.date.today()),
            статус = status
        )
     else:
         deal =  Сделка.create(
            клиент = client,
            сотрудник = employee,
            тур = tour,
            дата_заключения=fake.date_between(start_date=datetime.date(2020, 1, 1), end_date=datetime.date.today()),
            статус = status
         )
         Оплата.create(
            сделка = deal,
            дата_оплаты = fake.date_between(start_date=datetime.date(2020, 1, 1), end_date=datetime.date.today()),
            сумма_оплаты = random.randint(10000,100000),
            способ_оплаты = random.choice(["Наличные", "Карта"])
            )
         return deal

def generate_contract():
    deal = random.choice(Сделка.select().where(Сделка.статус == "Закрыта"))
    if deal:
        return Договор.create(
            сделка = deal,
            персональные_данные=deal.клиент.персональные_данные,
            наименование_тура = deal.тур,
            дата_составления=fake.date_between(start_date=datetime.date(2020, 1, 1), end_date=datetime.date.today())
        )

# Генерация данных
for _ in range(10):
    generate_employee()
    generate_client()
    generate_tour()

for _ in range(10):
    generate_deal()
for _ in range(5):
    generate_contract()


db.close()
print("Данные успешно сгенерированы!")