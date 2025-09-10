from django import forms
from .models import Book, CustomUser

class BookForm(forms.ModelForm):
    """Form for creating and editing books"""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year'
            }),
        }

    def clean_publication_year(self):
        """Custom validation for publication year"""
        year = self.cleaned_data.get('publication_year')
        if year and year < 1000:
            raise forms.ValidationError("Publication year must be realistic.")
        return year

class ExampleForm(forms.Form):
    """Example form with CSRF protection"""
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Your message'
        })
    )

    def clean_name(self):
        """Sanitize name input"""
        name = self.cleaned_data.get('name')
        if name:
            # Basic input sanitization
            name = name.strip()
            if len(name) < 2:
                raise forms.ValidationError("Name must be at least 2 characters long.")
        return name