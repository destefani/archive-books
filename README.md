# Die Bibliothek

A Python library (and CLI) to download, store, manage and process books collections from [archive.org]('archive.org') easily.

The library is inspired by RPG games. It creates characters and a narrative to the process.

The characters (main classes) are:
- The `Library`: Is the place where books are stored and catalog.

- The `Librarian`: All the interactions with the library are made through the `Librarian`. She/he is in charge of keeping everything in order.

- `Book`: A book contains all the metadata and images (pages) of a book.

Other important aspect of this project is to automatically process books to create high quality and datatasets for training deep learning generative models. For this, two more characters/classes exist:

- `Collection`: You can keep your own collection of library books. This makes it easy to create and manage multiple datasets.  All the books are still stored in the library. Sharing is caring.

- `Historian`: The `Historian` is in charge of reading and analyzing books. It is an image classification model that classifies books pages into several labels: a cover, a blank page, mostly image page, text and image mixed page, and mostly text page.

## Library

A library is composed by a `catalog` and the image files from the corresponding books. 

All the files are stored with this structure:

├── library_name    
    └── catalog.db  
    └── books 
        └── book_identifier_1
        |   └── page_1.png
        |   └── page_2.png
        |   └── page_n.png
        └── book_identifier_n
            └── page_1.png
            └── page_2.png
            └── page_n.png