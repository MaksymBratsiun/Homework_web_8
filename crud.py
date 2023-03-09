import connect
from models import Author, Quote


def create_autor(fullname, born_date, born_location, description):
    try:
        Author(fullname=fullname,
               born_date=born_date,
               born_location=born_location,
               description=description).save()
    except Exception as e:
        print(e)


def create_quotes(tags, author, quote):
    try:
        author = Author.objects(fullname=author)
        Quote(tags=tags,
              author=author[0],
              quote=quote).save()
    except Exception as e:
        print(e)


def read_quotes_by_name():
    authors_id = Author.objects(fullname='Albert Einstein')
    print(authors_id[0].id)
    quotes = Quote.objects(author=authors_id[0].id)
    for i in quotes:
        print(i.to_mongo().to_dict())



def update_author():
    author = Author.objects(fullname='Albert Einstein')
    author = Author.objects(pk='64098593e26b9b455b0100f0')
    print(author[0].to_mongo().to_dict())
    author.update(description='some text')
    print(author[0].to_mongo().to_dict())


def delete_author():
    author = Author.objects(pk='64098593e26b9b455b0100f0')
    author.delete()


if __name__ == '__main__':
    read_quotes_by_name()
