from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.login, name='login_account'),
    url(r'^signup', views.signup, name='signup_account')  
]
