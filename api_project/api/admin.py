from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'pages']
    list_filter = ['author', 'publication_date']
    search_fields = ['title', 'author', 'isbn']
    ordering = ['title']