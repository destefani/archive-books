import json
import os
from pathlib import Path # implement paths!
import sqlite3
import tarfile
import tempfile
import zipfile
import cv2 
import numpy as np
import pandas as pd
from tqdm import tqdm
from internetarchive import get_item, download

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
        book_metadata = get_item(book_id).item_metadata['metadata']

        book_date = check_metadata(book_metadata, 'date')
        book_subject = check_metadata(book_metadata, 'subject')
        book_title = check_metadata(book_metadata, 'title')
        book_year = check_metadata(book_metadata, 'year')
        book_language = check_metadata(book_metadata, 'language')

        # Download book
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            download_book(book_id, temp_dir)
            for file in os.listdir(temp_dir/ book_id):
                extract(temp_dir/ book_id / file, temp_dir / 'extracted')
                for directory in os.listdir(temp_dir / 'extracted'):
                    convert_jp2_to_png(temp_dir / 'extracted' / directory, book_directory)
        
        # Add book to the catalog
        book_dict = {'identifier': book_id,
                     'title': book_title,
                     'subject': book_subject,
                     'date': book_date,
                     'year': book_year,
                     'language': book_language}

        book_df = pd.DataFrame({k: [v] for k, v in book_dict.items()})
        
        self.catalog_df = pd.concat([self.catalog_df, book_df])
        self.catalog_df.to_csv(self.library_location / "catalog.csv", index=False)
        print('Book added to the catalog')

    def add_books(self, books: list):
        "Adds a list of books to the library"
        downloaded_books = []
        failed_books = []
        for book_id in books:
            try:
                self.add_book(book_id)
                downloaded_books.append(book_id)
            except:
                failed_books.append(book_id)
                print('Failed to download book:', book_id)
        # Log downloaded/failed books
        log_downloads(self.name, downloaded_books, error=False)
        log_downloads(self.name, failed_books, error=True)

        print(f'Downloaded {len(downloaded_books)} books')
        print(f'Failed to download {len(failed_books)} books')

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

def check_metadata(book_metadata, value):
    "Checks if the variable is in books metadata"
    try:
        return book_metadata[value]
    except:
        return np.nan

def log_downloads(library_name, downloaded_books, error=False):
    "Logs the downloaded books"
    logging_dir = Path(library_name) / 'logs'
    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)
    if error:
        logging_file = logging_dir / 'errors.csv'
    else:
        logging_file = logging_dir / 'downloaded.csv'
    downloaded_df = pd.DataFrame(downloaded_books, index=False, header=False)
    downloaded_df.to_csv(logging_file, index=False)

# Download and process book
def download_book(book_id, dest_path, verbose=True):
    "Downloads the compressed jp2 files of a book"
    print(f'Downloading {book_id}')
    download(
        book_id,
        destdir=dest_path,
        formats="Single Page Processed JP2 ZIP",
        verbose=verbose,
    )

def extract(file, dest_path):
    "Extracts a compressed file"
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
    "Converts jp2 files to png"
    print('Converting images to png')
    if not os.path.exists(png_directory):
        os.mkdir(png_directory)
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