from random import choice

import pika
from faker import Faker

import part_2.connect
from part_2.models import User

FAVORITE_LIST = ['SMS', 'email']
NUMBER_USERS = 10

faker = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))



def create_users(number=NUMBER_USERS):
    for _ in range(number):
        try:
            name = faker.name()
            email = faker.email()
            phone = faker.phone_number()
            favorite = choice(FAVORITE_LIST)
            User(fullname=name,
                 email=email,
                 phone=phone,
                 favorite=favorite,
                 send=False).save()
            print(name, email, phone, favorite)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    if not User.objects():
        create_users()
    for i in User.objects():
        print(i.to_mongo().to_dict())
