from random import choice
import json

import pika
from faker import Faker

import part_2.connect
from part_2.models import User

FAVORITE_LIST = ['SMS', 'email']
NUMBER_USERS = 10

faker = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='my_task', exchange_type='direct')
channel.queue_declare('sending', durable=True)
channel.queue_bind(exchange='my_task', queue='sending')


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
        body = json.dumps({'id': str(i.id)}).encode()
        channel.basic_publish(exchange='my_task',
                              routing_key='sending',
                              body=body,
                              properties=pika.BasicProperties(
                                  delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        print('Sent %r' % body)
    connection.close()
