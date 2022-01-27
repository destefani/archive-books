import os
import sqlite3
import pandas as pd
from internetarchive import get_item, download


## Plan
# - input: id and list of ids of the books
# - Download images of the books
# - Classify each page (image) of the books
# - Save the results (mongodb?)

# Goal: RPG like library for managing collections

## 1. Download images of the books

identifier_list = []

# The librarian is in charge of the processing of the books
# For a book to be added to the library:
# - Make a request to add the book to the library

# The books are in the library

#----------------------------------------------------------------------------

class Library:
    'Stores books and books catalog'
    # db location
    # methods 
    def __init__(self, name):
        self.library_location = name
    
    def open_library(self):
        'Creates a database and directory to store books'
        # Create directory structure
        if not os.path.exists(self.library_location):
            os.makedirs(self.library_location + '/books')
        self.db = sqlite3.connect(self.library_location + '/catalog.db')
        # self.db.execute('''CREATE TABLE catalog
        #                     (id text, title text, author text,
        #                     publisher text, year text,
        #                     isbn text, image_url text,
        #                     image_path text,
        #                     classification text,
        #                     classification_path text,
        #                     classification_url text)''')
        # self.db.commit()
        self.db.close()


    def add_book():
        pass

    def remove_book():
        pass

    def get_book():
        pass

    def check_id():
        pass
    
    def request_catalog():
        pass


#----------------------------------------------------------------------------

class Librarian():
    'Manages the library, gets the data'
    def library():
        pass
    def add_book():
        pass
    def remove_book():
        pass
    def ask_for_book():
        pass
    def get_books():
        pass

#----------------------------------------------------------------------------

class Historian():
    'Classifies books'
    # model
    # methods
    pass

#----------------------------------------------------------------------------

class Book():
    'Pure magic in paper'
    pass

#----------------------------------------------------------------------------

class Collection():
    'Personal collection of library books'
    pass

#----------------------------------------------------------------------------




