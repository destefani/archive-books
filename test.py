from bibliothek import Library, Librarian


# Instantiate a librarian
librarian = Librarian('the_library')

# Request book
book_id = 'superarboribusco00giov'
book_data = librarian.book_data(book_id)
print(book_data)
print(type(book_data))
print(book_data['identifier'])

book = librarian.get_book(book_data)
print(book)
print(type(book))







# librarian.get_book('superarboribusco00giov')



