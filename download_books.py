import yaml
import click
from bibliothek import Library

# ----------------------------------------------------------------------------


@click.command()

# Required
@click.option("--library", help="Library name", type=str, required=True)

# Optional
@click.option("--book-id", help="Book identifier", type=str, default=None)
@click.option("--book-list", help="Book list file location", type=str, default=None)
def main(**kwargs):
    print(kwargs)
    library = Library()
    library.load_library(kwargs["library"])

    if kwargs["book_list"] is not None:
        print("Loading ")
        books_list = read_yaml(kwargs["book_list"])
        print(f"Downloading {kwargs['book_list']}")
        print("Books to download: ", len(books_list))
        library.add_books(books_list)
    else:
        library.add_book(kwargs["book_id"])


def read_yaml(books_list_file):
    with open(books_list_file, "r") as f:
        yaml_file = yaml.load(f, Loader=yaml.FullLoader)
        books_list = yaml_file["books_list"]
        print(books_list)

    return books_list


# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
