import part_1.connect
from part_1.models import Author, Quote


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


def read_author_by_id(id_):
    result = ''
    try:
        author = Author.objects(pk=id_)
        result = author[0].to_mongo().to_dict().get('fullname')
    except Exception as e:
        print(e)
    return result


def read_quotes_by_name(name):
    result = []
    try:
        authors_id = Author.objects(fullname__icontains=name)
        if authors_id:
            quotes = Quote.objects(author=authors_id[0].id)
            for res in quotes:
                result.append(res.to_mongo().to_dict())
    except Exception as e:
        print(e)
    return result


def read_quotes_by_tag(tag):
    result = []
    try:
        quotes = Quote.objects(tags__icontains=tag)
        for res in quotes:
            result.append(res.to_mongo().to_dict())
    except Exception as e:
        print(e)
    return result


def read_quotes_by_tags(tags):
    result = []
    tags = tags.strip().lower().split(',')
    try:
        quotes = Quote.objects(tags__in=tags)
        for res in quotes:
            result.append(res.to_mongo().to_dict())
    except Exception as e:
        print(e)
    return result


def update_author(id_, field, value):
    author = Author.objects(pk=id_)
    if field == 'fullname':
        author.update(fullname=value)
    elif field == 'fullname':
        author.update(born_date=value)
    elif field == 'fullname':
        author.update(born_location=value)
    elif field == 'fullname':
        author.update(description=value)


def delete_author(id_):
    author = Author.objects(pk=id_)
    author.delete()


if __name__ == '__main__':
    print(read_quotes_by_tags('life,live'))
