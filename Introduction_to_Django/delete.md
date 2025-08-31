# Delete Operation

## Command Used

```python
# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
print(f"Book to delete: {book}")

# Delete the book
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Total books after deletion: {all_books.count()}")
print("All books:", list(all_books))
```

## Expected Output

```#
# The book is successfully deleted from the database
# Book to delete: Nineteen Eighty-Four by George Orwell (1949)
# (1, {'bookshelf.Book': 1})
# Total books after deletion: 0
# All books: []
```

## Alternative Delete Methods

```python
# Method 2: Delete by filter
deleted_count = Book.objects.filter(title="Nineteen Eighty-Four").delete()
print(f"Deleted {deleted_count[0]} book(s)")

# Method 3: Delete by ID
Book.objects.filter(id=1).delete()

# Method 4: Delete all books (be careful!)
Book.objects.all().delete()
```

## Verification of Deletion

```python
# Try to retrieve the deleted book (should raise DoesNotExist)
try:
    deleted_book = Book.objects.get(title="Nineteen Eighty-Four")
    print("Book still exists!")
except Book.DoesNotExist:
    print("Book successfully deleted - no longer exists in database")
```
