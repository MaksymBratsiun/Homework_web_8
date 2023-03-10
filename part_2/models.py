from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class User(Document):
    fullname = StringField(max_length=120, required=True)
    email = StringField(max_length=30, unique=True, required=True)
    phone = StringField(max_length=30, unique=True, required=True)
    favorite = StringField(max_length=10)
    send = BooleanField()
