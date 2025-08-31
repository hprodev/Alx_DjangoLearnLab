from django.contrib import admin
from .models import Book

# Custom admin configuration for Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters in the right sidebar
    list_filter = ('author', 'publication_year')
    
    # Add search functionality
    search_fields = ('title', 'author')
    
    # Make these fields editable directly in the list view
    list_editable = ('publication_year',)
    
    # Add ordering
    ordering = ('title',)
    
    # Customize the form layout
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year'),
            'description': 'Enter the basic information about the book.'
        }),
    )
    
    # Add pagination
    list_per_page = 10
    
    # Add custom actions
    actions = ['mark_as_classic']
    
    def mark_as_classic(self, request, queryset):
        """Custom admin action to mark books as classics"""
        updated = queryset.filter(publication_year__lt=1950).update()
        self.message_user(
            request,
            f'{updated} books marked as classics.',
        )
    mark_as_classic.short_description = "Mark selected books as classics"

# Alternative registration method (choose one)
# admin.site.register(Book, BookAdmin)