# relationship_app/query_samples.py

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()


def list_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return Book.objects.none()


def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


# Sample usage (for testing purposes)
if __name__ == "__main__":
    # Example queries
    
    # Query all books by a specific author
    author_books = query_books_by_author("J.K. Rowling")
    print("Books by J.K. Rowling:")
    for book in author_books:
        print(f"- {book.title}")
    
    # List all books in a library
    library_books = list_books_in_library("Central Library")
    print("\nBooks in Central Library:")
    for book in library_books:
        print(f"- {book.title} by {book.author.name}")
    
    # Retrieve the librarian for a library
    librarian = retrieve_librarian_for_library("Central Library")
    if librarian:
        print(f"\nLibrarian for Central Library: {librarian.name}")
    else:
        print("\nNo librarian found for Central Library")