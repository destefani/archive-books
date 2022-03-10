from bibliothek import Library, Librarian, Book


# Instantiate a librarian

library_name = 'the_library'

librarian = Librarian(library_name)



# Request book
book_id = 'superarboribusco00giov'
book_data = librarian.book_data(book_id)

print(book_data)
print(type(book_data))
print(book_data['identifier'])

<<<<<<< HEAD
book = Book(book_data, library_name)
print(book.book_id)
print(book.book_directory)


# book = librarian.get_book(book_data)
# print(book)
# print(type(book))
=======
book = librarian.get_book(book_data)
print(book)
print(type(book))
>>>>>>> c8395cba2b31f58e29c1a0de6217ebdda2c48a1a
