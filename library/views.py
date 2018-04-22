from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib import auth
from django.template import loader, RequestContext
from .forms import LoginForm, SignUpForm,BookForm,UserForm, LibrarianForm
from django.http import  HttpResponseRedirect
from library.models import *
# from django.views.generic import TemplateView
# Create your views here.
from django.views import generic


class UserListView(generic.ListView):
    model = User


class LibrarianListView(generic.ListView):
    model = Librarian


class BookListView(generic.ListView):
    model = Book


class user_detail(generic.DetailView):
    model = User


def library(request):
    Doc = Document.objects.all()
    return render(request, 'library/libsystem.html', locals())


def books_for_user(request):
    all_documents = Document.objects.all()
    return render(request, 'library/books_for_user.html', locals())


def books_for_librarian(request):
    all_documents = Document.objects.all()
    return render(request, 'library/books_for_user.html', locals())


def librarian_add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('books_for_librarian')
    else:
        form = Book()
    return render(request, 'library/librarian_add_book.html', {'form': form})


def logined_for_librarian(request):
    return render(request, 'library/logined_for_librarian.html', locals())

def logined_for_patron(request):
    return render(request, 'library/logined_for_patron.html', locals())

def logined_for_admin(request):
    return render(request, 'library/logined_for_admin.html', locals())


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = SignUpForm()
    return render(request, 'library/signup.html', {'form': form})


def librarian_add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'library/librarian_add_user.html', {'form': form})


def admin_add_librarian(request):
    if request.method == "POST":
        form = LibrarianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_of_librarians')
    else:
        form = LibrarianForm()
    return render(request, 'library/admin_add_librarian.html', {'form': form})


# def login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.save()
#             return redirect('library/books_for_user.html')
#     else:
#         form = LoginForm()
#     return render(request, 'library/login.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            login_exits = False
            for i in User.objects.all():
                if post.username == i.login:
                    login_exits = True
                    if post.password == i.password:
                        return redirect('logined_for_patron')
            if login_exits:
                return render(request, 'library/not_valid_password.html', {'form': form})
            else:
                return render(request, 'library/not_valid_login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'library/login.html', {'form': form})


def login_not_valid(request):
    return render(request, 'library/not_valid_login.html')


def list_of_books(request):
    Doc = Document.objects.all()
    return render(request, 'library/user_list.html', locals())


def list_of_librarians(request):
    lib = Librarian.objects.all()
    return render(request, 'library/list_of_librarians.html', locals())

def starter_page_for_librarian(request):
    return render(request, 'library/starter_page_for_librarian.html', locals())

def starter_page_for_user(request):
    return render(request, 'library/starter_page_for_user.html', locals())

def starter_page_for_admin(request):
    return render(request, 'library/starter_page_for_admin.html', locals())

def logined_library(request):
    Doc = Document.objects.all()
    return render(request, 'library/user_list.html', locals())


def list_to_delete(request):
    Doc = Document.objects.all()
    return render(request, 'library/books_for_user.html', locals())


def librarian_delete_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    print('\n\n\n')
    return HttpResponseRedirect('/')
