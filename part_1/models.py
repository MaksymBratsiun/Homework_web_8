from mongoengine import Document
from mongoengine.fields import ListField, StringField, ReferenceField


class Author(Document):
    fullname = StringField(max_length=120, unique=True, required=True)
    born_date = StringField(max_length=30)
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Author, reverse_delete_rule='CASCADE')
    quote = StringField(unique=True)
