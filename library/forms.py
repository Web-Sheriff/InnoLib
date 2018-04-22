from django import forms
from .models import *


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Login  # or User
        fields = ('username', 'password')
        exclude = [""]


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('library','title', 'price_value', 'authors','is_best_seller', 'edition', 'publisher','year')
        exclude = [""]


class CopyForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('library','title', 'price_value', 'is_best_seller', 'edition', 'publisher','year')
        exclude = [""]

