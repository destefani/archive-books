import yaml
import click
from bibliothek import Library

#----------------------------------------------------------------------------

@click.command()

# Required
@click.option('--library',   help='Library name',              type=str,   required=True)
@click.option('--book-id',   help='Book identifier',           type=str,   default=None)

# Optional
@click.option('--book-list', help='Book list file location',   type=str,   default=None)

def read_yaml(books_list_file):
    with open(books_list_file, 'r') as f:
        books_list = yaml.load(f)
    return books_list

def main(**kwargs):
    print(kwargs)
    library = Library()
    library.load_library(kwargs['library'])

    if kwargs['book_list'] is not None:
        print('Loading ')
        books_list = read_yaml(kwargs['book_list'])
        print(f"Downloading {kwargs['book_list']}")
        print("Books to download: ", len(books_list))
        library.add_books(books_list)
    else:
        library.add_book(kwargs['book_id'])

#----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
