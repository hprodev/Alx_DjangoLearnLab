from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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