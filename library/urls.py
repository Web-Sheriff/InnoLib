from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.library, name='libsystem'),
    url(r'logined/', views.logined_library, name='logined_libsystem'),
    url(r'^login', views.login, name='login_account'),
    url(r'^signup', views.signup, name='signup_account')
]
