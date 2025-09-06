# Retrieve Operation

## Command Used

```python
# Retrieve the specific book we created
book = Book.objects.get(title="1984")
print(f"Retrieved Book: {book}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"Book ID: {book.id}")
```

## Expected Output

```#
# Successfully retrieves the book and displays all attributes
# Retrieved Book: 1984 by George Orwell (1949)
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
# Book ID: 1
```

## Alternative Retrieve Methods

```python
# Get all books
all_books = Book.objects.all()
print(f"Total books: {all_books.count()}")

# Get by ID
book_by_id = Book.objects.get(id=1)
print(book_by_id)

# Filter method (returns QuerySet)
books_by_author = Book.objects.filter(author="George Orwell")
for book in books_by_author:
    print(book)
```
