# from django.contrib import admin
# from .models import Book

# # Custom admin configuration for Book model
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     # Display these fields in the admin list view
#     list_display = ('title', 'author', 'price', 'genre', 'published_date', 'rating')
    
#     # Add filters in the right sidebar
#     list_filter = ('genre', 'published_date')
    
#     # Add search functionality
#     search_fields = ('title', 'author')
    
#     # Make these fields editable directly in the list view
#     list_editable = ('price','rating',)
    
#     # Add ordering
#     ordering = ('title',)
    
#     # Customize the form layout
#     fieldsets = (
#         ('Book Information', {
#             'fields': ('title', 'author', 'published_year'),
#             'description': 'Enter the basic information about the book.'
#         }),
#     )
    
#     # Add pagination
#     list_per_page = 10 
    
#     # Add custom actions
#     actions = ['mark_as_classic']
    
#     def mark_as_classic(self, request, queryset):
#         """Custom admin action to mark books as classics"""
#         updated = queryset.filter(publication_year__lt=1950).update()
#         self.message_user(
#             request,
#             f'{updated} books marked as classics.',
#         )
#     mark_as_classic.short_description = "Mark selected books as classics"

# # Alternative registration method (choose one)
# # admin.site.register(Book, BookAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

class CustomUserAdmin(UserAdmin):
    """Custom admin for CustomUser model"""
    
    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # Fields to search by
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Filters for the admin list view
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Fieldsets for the user form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Fields for adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model"""
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)