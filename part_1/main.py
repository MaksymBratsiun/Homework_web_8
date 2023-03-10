import json

import part_1.connect
from part_1.crud import create_autor, create_quotes
from part_1.crud import read_quotes_by_name, read_quotes_by_tag, read_quotes_by_tags, read_author_by_id

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


def pretty_view(data):
    author = f'Author: {read_author_by_id(data.get("author"))}'
    tags = f'Tags: {", ".join(data.get("tags"))}'
    quote = f'Quote: {data.get("quote")}\n'
    return '\n'.join([author, tags, quote])


if __name__ == '__main__':
    while True:
        user_input = input('Create DB from file?(Y/N): ')
        if user_input.strip().lower() == 'y':
            create_from_files()
            break
        elif user_input.strip().lower() == 'n':
            break
    while True:
        user_input = input('Search quote by tag, tags, name: ')
        user_input = user_input.strip().lower()
        input_list = user_input.split(':')
        if input_list[0].strip() == 'exit':
            break
        elif input_list[0].strip() == 'name':
            seek_item = input_list[1].strip().title()
            for i in read_quotes_by_name(seek_item):
                print(pretty_view(i))
        elif input_list[0].strip() == 'tag':
            seek_item = input_list[1].strip()
            for i in read_quotes_by_tag(seek_item):
                print(pretty_view(i))
        elif input_list[0].strip() == 'tags':
            seek_item = input_list[1].strip()
            for i in read_quotes_by_tags(seek_item):
                print(pretty_view(i))
