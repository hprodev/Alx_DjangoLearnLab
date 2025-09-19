from django.core.management.base import BaseCommand
from api.models import Book

class Command(BaseCommand):
    help = 'Populate the database with sample books'

    def handle(self, *args, **options):
        books_data = [
            {
                'title': 'Django for Beginners',
                'author': 'William S. Vincent',
                'isbn': '1234567890123',
                'pages': 300
            },
            {
                'title': 'Two Scoops of Django',
                'author': 'Daniel Roy Greenfeld',
                'isbn': '1234567890124',
                'pages': 500
            },
            {
                'title': 'Django REST Framework',
                'author': 'Tom Christie',
                'isbn': '1234567890125',
                'pages': 250
            },
            {
                'title': 'Python Crash Course',
                'author': 'Eric Matthes',
                'isbn': '1234567890126',
                'pages': 544
            },
            {
                'title': 'Automate the Boring Stuff',
                'author': 'Al Sweigart',
                'isbn': '1234567890127',
                'pages': 504
            }
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created book: {book.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Book already exists: {book.title}')
                )