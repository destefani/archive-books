import click
from bibliothek import Library

#----------------------------------------------------------------------------

@click.command()

# Required
@click.option('--library',   help='Library name',     type=str,   required=True)
@click.option('--book-id',   help='Book identifier',  type=str,   required=True)

#----------------------------------------------------------------------------
  
def main(**kwargs):
    library = Library()
    library.load_library(kwargs['library'])
    library.download_book(kwargs['book_id'])

#----------------------------------------------------------------------------

if __name__ == "__main__":
    main()