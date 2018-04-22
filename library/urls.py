from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    url(r'^$', views.library, name='libsystem'),
    url(r'^account', views.logined_for_patron, name='logined_for_patron'),
    url(r'^lib_account', views.logined_for_librarian, name='logined_for_librarian'),
    url(r'^lib_admin', views.logined_for_admin, name='logined_for_admin'),
    url(r'libsystem_logined/', views.logined_library, name='libsystem_logined'),
    url(r'^innolib', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^login_not_valid', views.login_not_valid, name='login_not_valid'),
    url(r'^user_list', views.UserListView.as_view, name='user_list'),
    url(r'^librarian_list', views.list_to_delete, name='librarian_list'),
    url(r'^librarian_add_book', views.librarian_add_book, name='librarian_add_book'),
    url(r'^librarian_add_user', views.librarian_add_user, name='librarian_add_user'),
    url(r'^books_for_user', views.books_for_user, name='books_for_user'),
    url(r'^books_for_librarian', views.books_for_librarian, name='books_for_librarian'),
    url(r'^books_for_librarian', views.books_for_librarian, name='books_for_librarian'),
    url(r'^starter_page_for_librarian', views.starter_page_for_librarian, name='starter_page_for_librarian'),
    url(r'^starter_page_for_admin', views.starter_page_for_admin, name='starter_page_for_admin'),
    url(r'^starter_page_for_user', views.starter_page_for_user, name='starter_page_for_user'),
    url(r'^list_of_librarians', views.list_of_librarians, name='list_of_librarians'),
    url(r'^admin_add_librarian', views.admin_add_librarian, name='admin_add_librarian'),
    path('users/<int:pk>/', views.user_detail.as_view, name='user_detail'),
    path('users/<int:pk>/delete_user/', views.librarian_delete_user, name='delete_user'),
]
