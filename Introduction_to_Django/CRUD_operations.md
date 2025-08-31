# CRUD Operations for Book Model

This document contains all the Django shell commands and their outputs for performing CRUD operations on the Book model.

## Prerequisites

```python
# Start Django shell
python manage.py shell

# Import the Book model
from bookshelf.models import Book
```

## 1. CREATE Operation

### create Command

```python
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```

### Output

```bash
1984 by George Orwell (1949)
```

### Verification

```python
print(f"Book ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## 2. RETRIEVE Operation

### retrieve Command

```python
book = Book.objects.get(title="1984")
print(f"Retrieved Book: {book}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"Book ID: {book.id}")
```

### retrieve Output

```bash
Retrieved Book: 1984 by George Orwell (1949)
Title: 1984
Author: George Orwell
Publication Year: 1949
Book ID: 1
```

## 3. UPDATE Operation

### update Command

```python
book = Book.objects.get(title="1984")
print(f"Original title: {book.title}")

book.title = "Nineteen Eighty-Four"
book.save()

print(f"Updated title: {book.title}")
print(f"Updated book: {book}")
```

### update Output

```bash
Original title: 1984
Updated title: Nineteen Eighty-Four
Updated book: Nineteen Eighty-Four by George Orwell (1949)
```

## 4. DELETE Operation

### delete Command

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
print(f"Book to delete: {book}")

book.delete()

all_books = Book.objects.all()
print(f"Total books after deletion: {all_books.count()}")
print("All books:", list(all_books))
```

### delete Output

```bash
Book to delete: Nineteen Eighty-Four by George Orwell (1949)
(1, {'bookshelf.Book': 1})
Total books after deletion: 0
All books: []
```

## Complete CRUD Sequence

Here's the complete sequence to run in Django shell:

```python
# Import the model
from bookshelf.models import Book

# CREATE
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Created: {book}")

# RETRIEVE
retrieved_book = Book.objects.get(title="1984")
print(f"Retrieved: {retrieved_book}")

# UPDATE
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
print(f"Updated: {retrieved_book}")

# DELETE
retrieved_book.delete()
print(f"Remaining books: {Book.objects.all().count()}")
```

## Additional Useful Queries

```python
# Create multiple books for testing
Book.objects.bulk_create([
    Book(title="To Kill a Mockingbird", author="Harper Lee", publication_year=1960),
    Book(title="The Great Gatsby", author="F. Scott Fitzgerald", publication_year=1925),
    Book(title="Pride and Prejudice", author="Jane Austen", publication_year=1813),
])

# Filter by author
orwell_books = Book.objects.filter(author="George Orwell")

# Filter by publication year range
modern_books = Book.objects.filter(publication_year__gte=1950)

# Order by publication year
books_by_year = Book.objects.all().order_by('publication_year')

# Count total books
total_books = Book.objects.count()
```
