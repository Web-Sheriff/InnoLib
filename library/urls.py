from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    url(r'^$', views.library, name='libsystem'),
    url(r'libsystem_logined/', views.logined_library, name='libsystem_logined'),
    url(r'^login', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^login_not_valid', views.login_not_valid, name='login_not_valid'),
    url(r'^user_list', views.UserListView.as_view(), name='user_list'),
    url(r'^librarian_list', views.list_to_delete, name='librarian_list'),
    url(r'^librarian_add_book', views.librarian_add_book, name='librarian_add_book'),
    url(r'^librarian_add_user', views.librarian_add_user, name='librarian_add_user'),
    url(r'^books_for_user', views.books_for_user, name='books_for_user'),
    path('users/<int:pk>/', views.user_detail.as_view(), name='user_detail'),
    path('users/<int:pk>/delete_user/', views.librarian_delete_user, name='delete_user'),
    path('accounts/', include('django.contrib.auth.urls'))
]
