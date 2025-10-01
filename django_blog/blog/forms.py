from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form that includes email field.
    Inherits from Django's UserCreationForm and adds email validation.
    """
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    Allows users to update their email address.
    """
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    Includes validation for comment content.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
        labels = {
            'content': 'Comment'
        }
    
    def clean_content(self):
        """Validate that comment content is not empty or too short"""
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        return content