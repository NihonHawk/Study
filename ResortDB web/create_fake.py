import random
import os
import datetime
from faker import Faker
from tables import db, Clients, Orders, Tarifs, Options, Services

faker = Faker('ru_RU')

tarifs_dict = {
    "Стандарт" : 10000,
    "Стандарт+" : 15000,
    "Улучшенный стандарт" : 20000,
    "Четырехместный номер" : 25000,
    "Люкс" : 30000,
    "Президентский люкс" : 50000
}

services_dict = {
    "Завтрак в номер" : 1000,
    "Личный гид" : 5000,
    "Аренда конференц-зала" : 2000,
    "Аренда банкетного зала" : 2500,
    "Проживание с животными" : 1000,
    "Место для автомобиля на охраняемой стоянке" : 3000
}


def create_fake_clients(n):
    """Generate fake clients."""
    for i in range(n):
        clients = Clients(
            id = i+1,
            name = faker.name(),
            passport = f"{random.randint(10, 99)} {random.randint(10, 99)} {random.randint(100000, 999999)}",
            phone = faker.phone_number(),
            address = faker.address())
        db.session.add(clients)
    db.session.commit()
    print(f'Added {n} fake clients to the database.')


def create_fake_orders(n):
    """Generate fake orders."""
    for i in range(n):
        date = faker.date_between(start_date="-1y", end_date="now")
        orders = Orders(
            id = i+1,
            client_id = random.randint(1,30),
            tarif_id = random.randint(1,10),
            start_reserv = date,
            ends_reserv = date + datetime.timedelta(days=random.randint(7,21)),
            room_id = random.randint(1,500))
        db.session.add(orders)
    db.session.commit()
    print(f'Added {n} fake orders to the database.')


def create_fake_tarifs(tarifs_dict):
    """Generate fake tarifs"""
    i=0
    for key, value in tarifs_dict.items():
        tarifs = Tarifs(
            id = i+1,
            name = key,
            price = value)
        i+=1
        db.session.add(tarifs)
    db.session.commit()
    print(f'Added {len(tarifs_dict)} fake tarifs to the database.')


def create_fake_options(n):
    """Generate fake options"""
    for i in range(n):
        options = Options(
            id = i+1,
            client_id = faker.unique.random_int(1, 30),
            service_id = random.randint(1,6),
            date = faker.date_between(start_date="-1y", end_date="now"),
            status = random.choice(["Оплачено", "Ожидает"]),
            )
        db.session.add(options)
    db.session.commit()
    print(f'Added {n} fake options to the database.')


def create_fake_services(services_dict):
    """Generate fake services"""
    i=0
    for key, value in services_dict.items():
        services = Services(
            id = i+1,
            name = key,
            price = value)
        i+=1
        db.session.add(services)
    db.session.commit()
    print(f'Added {len(services_dict)} fake services to the database.')


if __name__ == '__main__':
    if os.path.exists("data.sqlite") == True:
        os.remove("data.sqlite")
    else:
        db.create_all()
    create_fake_clients(30)
    create_fake_orders(15)
    create_fake_tarifs(tarifs_dict)
    create_fake_options(10)
    create_fake_services(services_dict)