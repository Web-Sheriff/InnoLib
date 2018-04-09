from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.library, name='libsystem'),
    url(r'libsystem_logined/', views.logined_library, name='libsystem_logined'),
    url(r'^login', views.login, name='login_account'),
    url(r'^signup', views.signup, name='signup_account'),
    # url(r'^user_list', views.list_of_books, name='user_list'),
    # url(r'^librarian_list', views.list_to_delete, name='librarian_list'),
    # url(r'^librarian_add', views.librarian_add, name='librarian_add'),
]
