from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth import login, authenticate
from .forms import LoginForm, SignUpForm,BookForm,UserForm
from library.models import *
from django.views.generic import TemplateView
# Create your views here.
from django.views import generic


class UserListView(generic.ListView):
    model = User


class BookListView(generic.ListView):
    model = Book



def library(request):
    Doc = Document.objects.all()
    return render(request, 'library/books_for_user.html', locals())


def books_for_user(request):
    Doc = Document.objects.all()
    return render(request, 'library/books_for_user.html', locals())


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list') # it should be index
    else:
        form = SignUpForm()
    return render(request, 'library/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('library/books_for_user.html')
    else:
        form = LoginForm()
    return render(request, 'library/login.html', {'form': form})


def list_of_books(request):
    Doc = Document.objects.all()
    return render(request, 'library/user_list.html', locals())


def logined_library(request):
    Doc = Document.objects.all()
    return render(request, 'library/user_list.html', locals())


def list_to_delete(request):
    Doc = Book.objects.all()
    return render(request, 'library/books_for_user.html', locals())


def librarian_add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Book()
    return render(request, 'library/librarian_add_book.html', {'form': form})


def librarian_add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = User()
    return render(request, 'library/librarian_add_user.html', {'form': form})


