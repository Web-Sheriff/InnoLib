from django import forms

from .models import Login, User


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login  # or User
        fields = ('username', 'password')
        exclude = [""]


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number')
        exclude = [""]
