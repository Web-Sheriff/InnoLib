from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# Create your views here.
from django.views import generic

from library.models import *
from .forms import LoginForm, SignUpForm, BookForm, UserForm, LibrarianForm


class user_list(generic.ListView):
    model = User


class librarian_list(generic.ListView):
    model = Librarian


class book_list(generic.ListView):
    model = Book


class user_detail(generic.DetailView):
    model = User


def library(request):
    Doc = Document.objects.all()
    return render(request, 'library/u_authorization/libsystem.html', locals())


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


def admin_add_librarian(request):
    if request.method == "POST":
        form = LibrarianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_of_librarians')
    else:
        form = LibrarianForm()
    return render(request, 'library/admin_add_librarian.html', {'form': form})


def librarian_add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'library/librarian_add_user.html', {'form': form})


def find_status(user):
    if User.u_is_instance(user, Student):
        return 'Student'
    elif User.u_is_instance(user, Instructor):
        return 'Instructor'
    elif User.u_is_instance(user, TA):
        return 'TA'
    elif User.u_is_instance(user, Professor):
        return 'Professor'
    elif User.u_is_instance(user, VisitingProfessor):
        return 'Visiting Professor'


def logined_for_patron(request, patron):
    status = find_status(patron)
    copies_list = patron.user_card.copies.all()
    return render(request, 'library/u_authorization/logined_for_patron.html', locals())


def logined_for_librarian(request, user):
    users = User.objects.all()
    status = []
    for i in users:
        status.append(find_status(i))
    return render(request, 'library/u_authorization/logined_for_librarian.html', locals())


def logined_for_admin(request, user):
    return render(request, 'library/u_authorization/logined_for_admin.html', locals())


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = SignUpForm()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


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
                        if isinstance(i, Librarian):
                            return logined_for_librarian(request, i)
                        elif isinstance(i, Admin):
                            return logined_for_admin(request, i)
                        else:
                            return logined_for_patron(request, i)
                            return logined_for_librarian(request, i)
            if login_exits:
                return render(request, 'library/u_authorization/not_valid_password.html', {'form': form})
            else:
                return render(request, 'library/u_authorization/not_valid_login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'library/u_authorization/login.html', {'form': form})


def login_not_valid(request):
    return render(request, 'library/u_authorization/not_valid_login.html')


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
