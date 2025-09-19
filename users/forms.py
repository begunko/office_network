# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'position', 'skills')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'position', 'skills')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'position', 'skills')
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Опишите ваши навыки...'}),
            'position': forms.TextInput(attrs={'placeholder': 'Ваша должность'}),
        }
