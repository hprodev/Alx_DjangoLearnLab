from django.core.management.base import BaseCommand
from bookshelf.models import Book
from datetime import date

class Command(BaseCommand):
    help = 'Create sample books for testing'

    def handle(self, *args, **options):
        sample_books = [
            {
                'title': 'The Great Adventure',
                'author': 'John Smith',
                'description': 'An amazing journey through unknown lands filled with mystery and excitement.',
                'price': 19.99,
                'genre': 'fiction',
                'published_date': date(2023, 1, 15),
                'pages': 320,
                'rating': 4.5
            },
            {
                'title': 'Python Programming Guide',
                'author': 'Jane Doe',
                'description': 'Learn Python programming from scratch with practical examples.',
                'price': 29.99,
                'genre': 'non-fiction',
                'published_date': date(2023, 3, 10),
                'pages': 450,
                'rating': 4.8
            },
            {
                'title': 'Mystery of the Lost City',
                'author': 'Bob Johnson',
                'description': 'A thrilling mystery set in ancient ruins where secrets await.',
                'price': 24.99,
                'genre': 'mystery',
                'published_date': date(2023, 2, 20),
                'pages': 280,
                'rating': 4.2
            },
            {
                'title': 'Web Development Mastery',
                'author': 'Sarah Wilson',
                'description': 'Master modern web development with Django and JavaScript.',
                'price': 34.99,
                'genre': 'non-fiction',
                'published_date': date(2023, 4, 5),
                'pages': 520,
                'rating': 4.7
            },
            {
                'title': 'The Secret Garden',
                'author': 'Emily Brown',
                'description': 'A beautiful story about friendship and hidden treasures.',
                'price': 16.99,
                'genre': 'fiction',
                'published_date': date(2023, 1, 30),
                'pages': 250,
                'rating': 4.3
            },
        ]

        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created book: {book.title}')
                )
            else:
                self.stdout.write(f'Book already exists: {book.title}')