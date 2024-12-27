from peewee import *

# Подключение к базе данных MySQL (замени на свои данные)
db = MySQLDatabase('turoperator', user='root', password='00000', host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class Персональные_данные(BaseModel):
    фамилия = CharField()
    имя = CharField()
    отчество = CharField(null=True)
    серия_паспорта = IntegerField()
    номер_паспорта = IntegerField()
    нас_пункт = CharField()
    улица = CharField()
    дом = CharField()
    квартира = CharField(null=True)

class Сотрудник(BaseModel):
    персональные_данные = ForeignKeyField(Персональные_данные, backref='сотрудники')
    должность = CharField()

class Клиент(BaseModel):
    персональные_данные = ForeignKeyField(Персональные_данные, backref='клиенты')

class Наименование_тура(BaseModel):
    направление = CharField()
    цена = DecimalField()
    кол_во_дней = IntegerField()

class Сделка(BaseModel):
    клиент = ForeignKeyField(Клиент, backref='сделки')
    сотрудник = ForeignKeyField(Сотрудник, backref='сделки')
    тур = ForeignKeyField(Наименование_тура, backref='сделки')
    дата_заключения = DateField()
    статус = CharField()

class Договор(BaseModel):
    сделка = ForeignKeyField(Сделка, backref='договоры')
    персональные_данные = ForeignKeyField(Персональные_данные)
    наименование_тура = ForeignKeyField(Наименование_тура)
    дата_составления = DateField()

class Оплата(BaseModel):
    сделка = ForeignKeyField(Сделка, backref='оплаты')
    дата_оплаты = DateField()
    сумма_оплаты = DecimalField()
    способ_оплаты = CharField(max_length=25)