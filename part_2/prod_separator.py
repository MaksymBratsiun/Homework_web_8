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

channel_with_email = connection.channel()
channel_with_email.exchange_declare(exchange='my_task', exchange_type='direct')
channel_with_email.queue_declare('sending_email', durable=True)
channel_with_email.queue_bind(exchange='my_task', queue='sending_email')

channel_with_sms = connection.channel()
channel_with_sms.exchange_declare(exchange='my_task', exchange_type='direct')
channel_with_sms.queue_declare('sending_sms', durable=True)
channel_with_sms.queue_bind(exchange='my_task', queue='sending_sms')

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


def channel_sms(payload):

    channel_with_sms.basic_publish(exchange='my_task',
                                   routing_key='sending_sms',
                                   body=payload,
                                   properties=pika.BasicProperties(
                                       delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    return 'Sent %r' % body


def channel_email(payload):
    channel_with_email.basic_publish(exchange='my_task',
                                     routing_key='sending_email',
                                     body=payload,
                                     properties=pika.BasicProperties(
                                         delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    return 'Sent %r' % body


if __name__ == '__main__':

    if not User.objects():
        create_users()

    for i in User.objects():
        body = json.dumps({'id': str(i.id)}).encode()
        if i.favorite == 'SMS':
            print(channel_sms(body))
        elif i.favorite == 'email':
            print(channel_email(body))
    connection.close()
