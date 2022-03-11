import json
import os
from pathlib import Path # implement paths!
import sqlite3
import tarfile
import tempfile
import zipfile
# os.environ['OPENCV_IO_ENABLE_JASPER']='TRUE' # enable jasper
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

    def load_library(self, library_location):
        "Loads the library"
        self.library_location = Path(library_location)
        self.name = self.library_location.stem

        self.catalog_df = pd.read_csv(self.library_location / "catalog.csv")
        print(f'Library {self.name} loaded')
        print(f'Books: {len(self.catalog_df)}')

    def open_library(self, name):
        self.name = name
        "Creates a database and directory to store books" 
        # Create database and catalog table
        create_library(self.name)

    def add_book(self, book_id: str):
        "Adds a book to the library"
        book_directory = self.library_location / 'books' / book_id 
       
        # Check if book is already in the catalog
        if os.path.exists(book_directory):
            raise Exception("Book already in the library")
        if book_id in self.catalog_df.identifier:
            raise Exception("Book already in the catalog") 
        
        # Get book metadata
        book_metadata = get_item(book_id).item_metadata
        book_date = book_metadata['metadata']['date']
        book_subject = book_metadata['metadata']['subject']
        book_title = book_metadata['metadata']['title']
        book_year = book_metadata['metadata']['year']
        book_language = book_metadata['metadata']['language']

        # Download book
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            download_book(book_id, temp_dir)
            for file in os.listdir(temp_dir/ book_id):
                extract(temp_dir/ book_id / file, temp_dir / 'extracted')
                for directory in os.listdir(temp_dir / 'extracted'):
                    convert_jp2_to_png(temp_dir / 'extracted' / directory, book_directory)
        
        # Add book to the catalog
        book_df = pd.DataFrame(
            {'identifier': book_id,
             'title': book_title,
             'subject': book_subject,
             'date': book_date,
             'year': book_year,
             'language': book_language}
        )
        self.catalog_df = pd.concat([self.catalog_df, book_df])
        self.catalog_df.to_csv(self.library_location / "catalog.csv", index=False)
        print('Book added to the catalog')

# Library utility functions
def check_if_library_exists(library_name: str) -> bool:
    "Checks if the library exists"
    return os.path.exists(library_name)

def create_library(name: str, directory='.'):
    "Creates a .csv file with the books catalog"
    # Check if the library exists
    print('- - - Creating library - - -')
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

# Download and process book
def download_book(book_id, dest_path, verbose=True):
    print(f'Downloading {book_id}')
    download(
        book_id,
        destdir=dest_path,
        formats="Single Page Processed JP2 ZIP",
        verbose=verbose,
    )

def extract(file, dest_path):
    print(f'Extracting {file} to {dest_path}')
    if file.suffix == ".zip":
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(dest_path)
    if file.suffix == ".tar":
        tar = tarfile.open(file)
        tar.extractall(dest_path)
        tar.close()
    print('Done')


def convert_jp2_to_png(jp2_directory, png_directory):
    print('Converting images to png')
    if not os.path.exists(png_directory):
        os.mkdir(png_directory)
    image_files_list = list(jp2_directory.rglob('*.jp2'))
    for file in tqdm(image_files_list):
        image = cv2.imread(str(file))
        filename = str((png_directory / file.stem).with_suffix('.png'))
        cv2.imwrite(filename, image)
    print('Done')

    def remove_book():
        pass

    def get_book():
        pass

    def check_id():
        pass

    def request_catalog(self):
        pass

# ----------------------------------------------------------------------------


# class Librarian:
#     "Manages the library, gets the data"

#     def __init__(self, library_name):
#         self.library_name = library_name

#     def book_data(self, book_identifier):
#         item = get_item(book_identifier)
#         return item.item_metadata["metadata"]

#     def add_book(self, book, library, download=True):
#         library.add_book(book)
#         # Check if the book is already in the library
#         # Download the book
#         # Add the book to the catalog
#         pass
        

#     def remove_book():
#         pass

#     def get_book(self, book):
#         book_identifier = book['identifier']
#         book_directory = Path(self.library_name) / "books" / book_identifier
#         book_directory.mkdir(parents=True, exist_ok=True)
#         # Download the bookdef create_library(name, directory):
#     "Creates a .csv file with the books catalog"
#     # Check if the library exists
#     if check_if_library_exists(name):
#         raise Exception(f"The library {name} already exists")
#             downloaded_file = os.listdir(temp_dir / book_identifier)[0]
#             downloaded_file_path = temp_dir / book_identifier / downloaded_file
#             # check how to get downloaded file from
#             extract(downloaded_file_path, temp_dir)
#             # Convert jp2 to png
#             convert_jp2_to_png(temp_dir, book_directory)
#         return book
            


# def download_book(book_id, dest_path, verbose=True):
#     print(f'Downloading {book_id}')
#     download(
#         book_id,
#         destdir=dest_path,
#         formats="Single Page Processed JP2 ZIP",
#         verbose=verbose,
#     )


# def extract(file, dest):
#     print(f'Extracting {file} to {dest}')
#     if file.suffix == ".zip":
#         with zipfile.ZipFile(file, "r") as zip_ref:
#             zip_ref.extractall(dest)
#     if file.suffix == ".tar":
#         tar = tarfile.open(file)
#         tar.extractall(dest)
#         tar.close()
#     print('Done')


# def convert_jp2_to_png(jp2_directory, png_directory):
#     print('Converting images to png')
#     image_files_list = list(jp2_directory.rglob('*.jp2'))
#     for file in tqdm(image_files_list):
#         image = cv2.imread(str(file))
#         filename = str((png_directory / file.stem).with_suffix('.png'))
#         cv2.imwrite(filename, image)
#     print('Done')


# ----------------------------------------------------------------------------


class Historian:
    "Classifies books"
    # model
    # methods
    pass


# ----------------------------------------------------------------------------


# class Book:
#     "Pure magic in paper"

#     def __init__(self, book_data, library):
#         # Books metadata
#         self.library = library
#         self.book_data = book_data
#         self.book_id = book_data['identifier']
#         self.book_directory = Path(self.library) / "books" / self.book_id
        
#         # Book images directory
#     # def images(self):
#     #     book_directory / 

#     # def __len__(self):
#     # return len()


# ----------------------------------------------------------------------------


class Collection:
    "Personal collection of library books"
    pass


# ----------------------------------------------------------------------------


if __name__ == '__main__':
    library = Library()
    library.load_library('alexandria')
    library.add_book('1200thedresdencodex1200ad')
    