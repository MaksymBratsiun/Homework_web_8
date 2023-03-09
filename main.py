import json

import connect
from models import Author, Quote
from crud import read_authors, create_autor, create_quotes


AUTHORS_JSON = 'authors.json'
QUOTES_JSON = 'quotes.json'


def read_from_file(json_name):
    with open(json_name, 'r', encoding='utf-8') as fh:
        read_data = json.load(fh)
    return read_data


def create_from_files():
    authors = read_from_file(AUTHORS_JSON)
    for author in authors:
        create_autor(fullname=author.get('fullname'),
                     born_date=author.get('born_date'),
                     born_location=author.get('born_location'),
                     description=author.get('description'))

    quotes = read_from_file(QUOTES_JSON)
    for quote in quotes:
        create_quotes(tags=quote.get('tags'),
                      author=quote.get('author'),
                      quote=quote.get('quote'))


if __name__ == '__main__':
    pass
