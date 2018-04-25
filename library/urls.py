from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.library, name='libsystem'),
    url(r'libsystem_logined/', views.logined_library, name='libsystem_logined'),
    url(r'^innolib$', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^login_not_valid', views.login_not_valid, name='login_not_valid'),
    url(r'^innolib/admin_account', views.admin_account, name='admin_account'),
    url(r'^innolib/lib_account_users', views.lib_account_users, name='lib_account1'),
    url(r'^innolib/lib_account_books', views.lib_account_docs, name='lib_account2'),
    url(r'^innolib/lib_account/delete_user', views.lib_account_delete_user, name='delete_user'),
    url(r'^innolib/lib_account/delete_doc', views.lib_account_delete_doc, name='delete_doc'),
    url(r'^innolib/account', views.account, name='account'),

    url(r'^user_list', views.user_list.as_view(), name='user_list'),
    url(r'^librarian_list', views.list_to_delete, name='librarian_list'),
    url(r'^librarian_add_book', views.librarian_add_book, name='librarian_add_book'),
    url(r'^librarian_add_user', views.librarian_add_user, name='librarian_add_user'),
    ##url(r'^librarian_delete_user', views.librarian_delete_user, name='librarian_delete_user'),
    url(r'^books_for_user', views.books_for_user, name='books_for_user'),
    url(r'^books_for_librarian', views.books_for_librarian, name='books_for_librarian'),
    url(r'^librarian_add_journal', views.librarian_add_journal, name='librarian_add_journal'),
    url(r'^librarian_add_student', views.librarian_add_student, name='librarian_add_student'),
    url(r'^librarian_add_ta', views.librarian_add_ta, name='librarian_add_ta'),
    url(r'^librarian_add_instructor', views.librarian_add_instructor, name='librarian_add_instructor'),
    url(r'^librarian_add_visprofessor', views.librarian_add_visprofessor, name='librarian_add_visprofessor'),
    url(r'^librarian_add_professor', views.librarian_add_professor, name='librarian_add_professor'),
    url(r'^librarian_add_av', views.librarian_add_av, name='librarian_add_av'),
    url(r'^librarian_add_copy', views.librarian_add_copy, name='librarian_add_copy'),
    url(r'^books_for_librarian', views.books_for_librarian, name='books_for_librarian'),
    url(r'^logined_for_librarian', views.logined_for_librarian, name='logined_for_librarian'),
    url(r'^logined_for_admin', views.logined_for_admin, name='logined_for_admin'),
    url(r'^logined_for_patron', views.logined_for_patron, name='logined_for_patron'),
    url(r'^list_of_librarians', views.list_of_librarians, name='list_of_librarians'),
    url(r'^adding_doc_start', views.adding_doc_start, name='adding_doc_start'),
    url(r'^adding_users_start', views.adding_users_start, name='adding_users_start'),
    path('users/<int:pk>/', views.user_detail.as_view(), name='user_detail'),
    path('users/<int:pk>/librarian_delete_user/', views.librarian_delete_user, name='librarian_delete_user'),
    path('librarians/<int:pk>/admin_delete_librarian/', views.admin_delete_librarian, name='admin_delete_librarian'),
    path('patrons/<int:pk>/', views.patron_detail.as_view(), name='patron_detail'),
    path('librarians/<int:pk>/', views.librarian_detail.as_view(), name='librarian_detail'),
    path('copies/<int:pk>/', views.copy_detail.as_view(), name='patron_detail'),
    #path('signup/student/', views.signup_student, name='aaa')
]
