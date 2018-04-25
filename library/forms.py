from django import forms
from django.forms import SelectDateWidget

from .models import *


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Login  # or User
        fields = ('username', 'password')
        exclude = [""]


# class SignUpForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
#         exclude = [""]

# class SignUpForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
#         exclude = [""]
class SignUpForm(forms.ModelForm):
    status = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = User
        fields = ('status',)
        exclude = [""]


class SignUpStudent(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class SignUpProfessor(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Professor
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class SignUpVisitingProfessor(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = VisitingProfessor
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class SignUpInstructor(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Instructor
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class SignUpTA(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = TA
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class AddLibrarian(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Librarian
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]

class AddUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail', 'status')
        exclude = [""]


class AddDocument(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('library','title','authors','price_value','keywords')


class DeleteUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','second_name')


class DeleteDoc(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
        exclude = [""]


class LibrarianForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Librarian
        fields = (
            'login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail', 'level_of_privileges')
        exclude = [""]


# class ProfessorForm(forms.ModelForm):
#   class Meta:
#      model = Professor
#     fields = ('login', 'password', 'first_name', 'second_name', 'address', 'phone_number', 'mail')
#    exclude = [""]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('library', 'title', 'price_value', 'is_best_seller', 'edition', 'publisher', 'year', 'authors')
        exclude = [""]


class AVForm(forms.ModelForm):
    class Meta:
        model = AudioVideo
        fields = ('library', 'title', 'price_value', 'publisher', 'year','authors')
        exclude = [""]


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('library', 'title', 'price_value', 'keywords')
        exclude = [""]


class CopyForm(forms.ModelForm):
    class Meta:
        model = Copy
        fields = ('document','number', 'need_to_return', 'is_checked_out', 'user_card', 'booking_date', 'overdue_date')
        exclude = [""]



