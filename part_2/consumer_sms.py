import sys
import json

import pika

import part_2.connect
from part_2.models import User

TEXT = ' You win $1000. Call 8-900-*******'


def message_sending(id_, text):
    print(f'Dear {update_user(id_)}, {text}')


def update_user(id_):
    user = User.objects(pk=id_)
    user.update(send=True)
    return user[0].to_mongo().to_dict().get('fullname')


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='sending_sms', durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f'Received {message}')
        message_sending(message.get('id'), TEXT)
        print(f'Done: {method.delivery_tag}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sending_sms', on_message_callback=callback)
    print('Waiting for message. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
