# Create Operation

## Command Used

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```

## Expected Output

```#
# The book instance is successfully created and saved to the database
# Output: 1984 by George Orwell (1949)


## Verification:
```python
# Verify the book was created
print(f"Book ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```
