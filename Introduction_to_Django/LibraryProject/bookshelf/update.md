# Update Operation

## Command Used

```python
# Retrieve the book and update its title
book = Book.objects.get(title="1984")
print(f"Original title: {book.title}")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

print(f"Updated title: {book.title}")
print(f"Updated book: {book}")
```

## Expected Output

```#
# The book title is successfully updated in the database
# Original title: 1984
# Updated title: Nineteen Eighty-Four
# Updated book: Nineteen Eighty-Four by George Orwell (1949)
```

## Alternative Update Methods

```python
# Method 2: Update using update() method
Book.objects.filter(id=1).update(title="Nineteen Eighty-Four")

# Method 3: Update multiple fields at once
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.author = "George Orwell (Eric Blair)"
book.save()
```

## Verification

```python
# Verify the update was successful
updated_book = Book.objects.get(id=1)
print(f"Verified updated book: {updated_book}")
```
