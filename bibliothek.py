import json
import os
from pathlib import Path # implement paths!
import sqlite3
import tarfile
import tempfile
import zipfile
import cv2
import pandas as pd
from tqdm import tqdm
from internetarchive import get_item, download


## Plan
# - input: id and list of ids of the books
# - Download images of the books ✅
# - Classify each page (image) of the books
# - Save the results sqlite3

# Goal: RPG like library for managing collections of books images

## 1. Download images of the books

# The librarian is in charge of processing the books
# For a book to be added to the library:
# - Make a request to add the book to the library

# The books are in the library

# ----------------------------------------------------------------------------


class Library:
    "Stores books and books catalog"
    # db location
    # methods
    def __init__(self, name: str, library_location=None):
        self.name = name
        if library_location is None:
            self.library_location = Path.resolve(self) / name 
        self.library_location = library_location

    def open_library(self):
        "Creates a database and directory to store books" 
        # Create directory structure
        if not os.path.exists(self.library_location):
            os.makedirs(self.library_location / "books")
        # Create database and catalog table
        create_library(self.name, self.library_location)



def check_if_library_exists(library_name: str) -> bool:
    "Checks if the library exists"
    return os.path.exists(library_name)

def create_library(name: str, directory='.'):
    "Creates a .csv file with the books catalog"
    # Check if the library exists
    print(f'- - - Creating library - - -')
    print('Name:', name)
    library_path = Path(directory) / name
    print('Location:', library_path)
    if check_if_library_exists(library_path):
        raise Exception(f"The library {name} already exists")

    # Create directories
    os.makedirs(library_path / "books")
    
    # Create the library catalog
    library_df =  pd.DataFrame(columns=['identifier', 'date', 'subject', 'title', 'year', 'language'])
    library_df.to_csv(library_path / 'catalog.csv', index=False)
    print('Done')

    
    def add_book(self, book):
        "Adds a book to the library"
        # Check if the book is already in the library

        # Download the book
        # Add the book to the catalog
        conn = sqlite3.connect(self.library_location / "catalog.db")
        cursor = conn.cursor()
        sql = ''' INSERT INTO catalog (identifier, date, subject, title, year, language)
                  VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(sql, (book.identifier, book.date, book.subject, book.title, book.year, book.language))
        conn.commit()
        cursor.lastrowid

    def remove_book():
        pass

    def get_book():
        pass

    def check_id():
        pass

    def request_catalog(self):
        conn = sqlite3.connect(self.library_location / "catalog.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM catalog
            """
        )
        catalog = cursor.fetchall()
        conn.close()
        return catalog


# ----------------------------------------------------------------------------


class Librarian:
    "Manages the library, gets the data"

    def __init__(self, library_name):
        self.library_name = library_name

    def book_data(self, book_identifier):
        item = get_item(book_identifier)
        return item.item_metadata["metadata"]

    def add_book(self, book, library, download=True):
        library.add_book(book)
        # Check if the book is already in the library
        # Download the book
        # Add the book to the catalog
        pass
        

    def remove_book():
        pass

    def get_book(self, book):
        book_identifier = book['identifier']
        book_directory = Path(self.library_name) / "books" / book_identifier
        book_directory.mkdir(parents=True, exist_ok=True)
        # Download the bookdef create_library(name, directory):
    "Creates a .csv file with the books catalog"
    # Check if the library exists
    if check_if_library_exists(name):
        raise Exception(f"The library {name} already exists")
            downloaded_file = os.listdir(temp_dir / book_identifier)[0]
            downloaded_file_path = temp_dir / book_identifier / downloaded_file
            # check how to get downloaded file from
            extract(downloaded_file_path, temp_dir)
            # Convert jp2 to png
            convert_jp2_to_png(temp_dir, book_directory)
        return book
            


def download_book(book_identifier, dest_directory, verbose=True):
    print(f'Downloading {book_identifier}')
    download(
        book_identifier,
        destdir=dest_directory,
        formats="Single Page Processed JP2 ZIP",
        verbose=verbose,
    )


def extract(file, dest):
    print(f'Extracting {file} to {dest}')
    if file.suffix == ".zip":
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(dest)
    if file.suffix == ".tar":
        tar = tarfile.open(file)
        tar.extractall(dest)
        tar.close()
    print('Done')


def convert_jp2_to_png(jp2_directory, png_directory):
    print('Converting images to png')
    image_files_list = list(jp2_directory.rglob('*.jp2'))
    for file in tqdm(image_files_list):
        image = cv2.imread(str(file))
        filename = str((png_directory / file.stem).with_suffix('.png'))
        cv2.imwrite(filename, image)
    print('Done')


# ----------------------------------------------------------------------------


class Historian:
    "Classifies books"
    # model
    # methods
    pass


# ----------------------------------------------------------------------------


class Book:
    "Pure magic in paper"

    def __init__(self, book_data, library):
        # Books metadata
        self.library = library
        self.book_data = book_data
        self.book_id = book_data['identifier']
        self.book_directory = Path(self.library) / "books" / self.book_id
        
        # Book images directory
    # def images(self):
    #     book_directory / 

    # def __len__(self):
    # return len()


# ----------------------------------------------------------------------------


class Collection:
    "Personal collection of library books"
    pass


# ----------------------------------------------------------------------------
