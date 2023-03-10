import configparser

from mongoengine import *

DB_NAME = 'RabbitMQ_sending'

config = configparser.ConfigParser()
config.read('config_db.ini')

mongo_user = config.get('DB_DEV', 'user')
mongodb_pass = config.get('DB_DEV', 'password')
db_name = config.get('DB_DEV', 'db_name')
domain = config.get('DB_DEV', 'domain')
print(f'mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority')

connect(host=f'mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority')
