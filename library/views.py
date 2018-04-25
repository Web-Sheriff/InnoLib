from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# Create your views here.
from django.views import generic
from django.urls import reverse

from .forms import *

lib0 = Librarian
patron0 = User
admin0 = Admin

class patron_detail(generic.DetailView):
    model = Patron


class librarian_detail(generic.DetailView):
    model = Librarian


class user_list(generic.ListView):
    model = User


class librarian_list(generic.ListView):
    model = Librarian


class book_list(generic.ListView):
    model = Book


class user_detail(generic.DetailView):
    model = User


class copy_detail(generic.DetailView):
    model = Copy


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
            post = form.save()
            if post.status == 'Student' or post.status == 'student':
                return redirect('signup_student')
            elif post.status == 'Professor' or post.status == 'professor':
                return redirect ('signup_professor')
            elif post.status == 'Visiting Professor' or post.status == 'visiting professor' or \
                    post.status == 'visiting Professor' or post.status == 'Visiting professor':
                return redirect('signup_visiting_professor')
            elif post.status == 'Instructor' or post.status == 'instructor':
                return redirect('signup_instructor')
            elif post.status == 'ta' or post.status == 'TA' or post.status == 'Ta' or post.status == 'tA':
                return redirect('signup_ta')
            else:
                return render(request, 'library/u_account/signup_not_valid.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_student(request):
    if request.method == "POST":
        form = SignUpStudent(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpStudent()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_professor(request):
    if request.method == "POST":
        form = SignUpProfessor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpStudent()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_instructor(request):
    if request.method == "POST":
        form = SignUpInstructor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpInstructor()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_visiting_professor(request):
    if request.method == "POST":
        form = SignUpVisitingProfessor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpVisitingProfessor()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def signup_ta(request):
    if request.method == "POST":
        form = SignUpTA(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpTA()
    return render(request, 'library/u_authorization/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            post = form.save()  # Sorry, mate, this does not work: (copymmit=False)
            login_exits = False
            for i in User.objects.all():
                if post.username == i.login:
                    login_exits = True
                    if post.password == i.password:
                        if i.status == 'Librarian':
                            lib0 = i
                            return logined_for_librarian(request, i)
                        elif i.status == 'Admin':
                            admin0 = i
                            return logined_for_admin(request, i)
                        else:
                            patron0 = i
                            return logined_for_patron(request, i)
            if login_exits:
                return render(request, 'library/u_authorization/not_valid_password.html', {'form': form})
            else:
                return render(request, 'library/u_authorization/not_valid_login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'library/u_authorization/login.html', {'form': form})


def logined_for_patron(request, patron):
    return render(request, 'library/u_account/logined_for_patron.html', locals())

def checkout(request):
    if request.method == "POST":
        form1 = CheckOut(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('logined_for_librarian')
    else:
        form1 = CheckOut()
    return render(request, 'library/u_account/checkout.html', {'form1': form1}, locals())


def account(request):
    return render(request, 'library/u_account/account.html')


def logined_for_librarian(request, patron):
    users = User.objects.all()
    return render(request, 'library/u_account/logined_for_librarian.html', locals())


def lib_account_users(request):
    users = User.objects.all()
    if request.method == "POST":
        form_add_user = AddUser(request.POST)
        # Form for adding a user
        if form_add_user.is_valid():
            form_add_user.save()
            return redirect('logined_for_librarian')
    else:
        form_add_user = AddUser()
    return render(request, 'library/u_account/lib_account_users.html', {'form_add_user': form_add_user}, locals())


def lib_account_docs(request):
    books = Book.objects.all()
    if request.method == "POST":
        form1 = AddDocument(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('logined_for_librarian')
    else:
        form1 = AddDocument()
    return render(request, 'library/u_account/lib_account_docs.html', {'form1': form1}, locals())

def lib_account_delete_user(request):
    if request.method == "POST":
        form1 = DeleteUser(request.POST)
        if form1.is_valid():
            post = form1.save()
            for i in User.objects.all():
                if i.first_name == post.first_name:
                    if i.second_name == post.secondname:
                        lib0.remove_object(i)
            return redirect('logined_for_librarian')
    else:
        form1 = DeleteUser()
    return render(request, 'library/u_account/lib_account_delete_user.html', {'form1': form1}, locals())

def lib_account_delete_doc(request):
    if request.method == "POST":
        form1 = DeleteDoc(request.POST)
        if form1.is_valid():
            post = form1.save()
            for i in Document.objects.all():
                if i.title == form1.title:
                    lib0.remove_object(i)
            return redirect('logined_for_librarian')
    else:
        form1 = DeleteDoc()
    return render(request, 'library/u_account/lib_account_delete_doc.html', {'form1': form1}, locals())


def logined_for_admin(request, patron):
    return render(request, 'library/u_account/logined_for_admin.html', locals())


def admin_account(request):
    librarians = User.objects.all()
    if request.method == "POST":
        form_add_lib = AddLibrarian(request.POST)
        if form_add_lib.is_valid():
            form_add_lib.save()
            return redirect('logined_for_admin')
    else:
        form_add_lib = AddLibrarian()
    return render(request, 'library/u_account/admin_account.html', {'form_add_lib': form_add_lib}, locals())


def lib_account_delete_lib(request):
    if request.method == "POST":
        form1 = DeleteUser(request.POST)
        if form1.is_valid():
            post = form1.save()
            for i in User.objects.all():
                if i.first_name == post.first_name:
                    if i.second_name == post.secondname:
                        admin0.remove_object(i)
            return redirect('logined_for_librarian')
    else:
        form1 = DeleteUser()
    return render(request, 'library/u_account/lib_account_delete_user.html', {'form1': form1}, locals())

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
    return HttpResponseRedirect('/', locals())


def admin_delete_librarian(request, pk):
    user = Librarian.objects.get(pk=pk)
    user.delete()
    return HttpResponseRedirect('/', locals())


def adding_doc_start(request):
    return render(request, 'library/adding_doc_start.html', locals())


def adding_users_start(request):
    return render(request, 'library/adding_users_start.html', locals())
