from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# Create your views here.
from django.views import generic

from library.models import *
from .forms import *


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


def librarian_add_journal(request):
    if request.method == "POST":
        form = JournalForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('books_for_librarian')
    else:
        form = Journal()
    return render(request, 'library/librarian_add_journal.html', {'form': form})


def librarian_add_av(request):
    if request.method == "POST":
        form = AVForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('books_for_librarian')
    else:
        form = Journal()
    return render(request, 'library/librarian_add_av.html', {'form': form})


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

def librarian_add_copy(request):
    if request.method == "POST":
        form = CopyForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('books_for_librarian')
    else:
        form = Copy()
    return render(request, 'library/librarian_add_copy.html', {'form': form})


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

def librarian_add_instructor(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'library/librarian_add_instructor.html', {'form': form})


def librarian_add_professor(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'library/librarian_add_professor.html', {'form': form})


def librarian_add_visprofessor(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'library/librarian_add_visprofessor.html', {'form': form})



def librarian_add_ta(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'library/librarian_add_ta.html', {'form': form})


def librarian_add_student(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'library/librarian_add_student.html', {'form': form})


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


# def signup(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = SignUpForm()
#     return render(request, 'library/u_authorization/signup.html', {'form': form})

# def signup_not_valid(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             post = form
#             if post.status == 'Student' or post.status == 'student':
#                 return signup_student(request)
#             elif post.status == 'Professor' or post.status == 'professor':
#                 return signup_professor(request)
#             elif post.status == 'Visiting Professor' or post.status == 'visiting professor' or \
#                     post.status == 'visiting Professor' or post.status == 'Visiting professor':
#                 return signup_visiting_professor(request)
#             elif post.status == 'Instructor' or post.status == 'instructor':
#                 return signup_instructor(request)
#             elif post.status == 'ta' or post.status == 'TA' or post.status == 'Ta' or post.status == 'tA':
#                 return signup_ta(request)
#             else:
#                 return signup_not_valid(request)
#     else:
#         form = SignUpForm()
#     return render(request, 'library/u_authorization/signup_not_valid.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.status == 'Student' or form.status == 'student':
                return signup_student(request)
            elif form.status == 'Professor' or form.status == 'professor':
                return signup_professor(request)
            elif form.status == 'Visiting Professor' or form.status == 'visiting professor' or \
                    form.status == 'visiting Professor' or form.status == 'Visiting professor':
                return signup_visiting_professor(request)
            elif form.status == 'Instructor' or form.status == 'instructor':
                return signup_instructor(request)
            elif form.status == 'ta' or form.status == 'TA' or form.status == 'Ta' or form.status == 'tA':
                return signup_ta(request)
            else:
                return render(request, 'library/u_authorization/signup_not_valid.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_student(request):
    if request.method == "POST":
        form = SignUpStudent(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = SignUpStudent()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_professor(request):
    if request.method == "POST":
        form = SignUpProfessor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = SignUpStudent()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_instructor(request):
    if request.method == "POST":
        form = SignUpInstructor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = SignUpInstructor()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_visiting_professor(request):
    if request.method == "POST":
        form = SignUpVisitingProfessor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = SignUpVisitingProfessor()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_ta(request):
    if request.method == "POST":
        form = SignUpTA(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = SignUpTA()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            post = form.save() #Sorry, mate, this does not work: (copymmit=False)
            login_exits = False
            for i in User.objects.all():
                if post.username == i.login:
                    login_exits = True
                    if post.password == i.password:
                        if isinstance(i, Librarian):
                            return logined_for_librarian
                        elif isinstance(i, Admin):
                            return logined_for_admin(request, i)
                        else:
                            return logined_for_patron(request, i)
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

def adding_doc_start(request):
    return render(request, 'library/adding_doc_start.html', locals())

def adding_users_start(request):
    return render(request, 'library/adding_users_start.html', locals())
