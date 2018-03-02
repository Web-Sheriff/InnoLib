from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.library, name='libsystem'),
    url(r'logined/', views.logined_library, name='logined_libsystem'),  
]
