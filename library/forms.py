from django import forms
from .models import Login, User, Book


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login  # or User
        fields = ('username', 'password')
        exclude = [""]


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('library','title', 'price_value', 'is_best_seller', 'edition', 'publisher',)
        exclude = [""]


class CopyForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('library','title', 'price_value', 'is_best_seller', 'edition', 'publisher')
        exclude = [""]

