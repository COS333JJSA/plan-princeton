from django.urls import path
from . import views
from django.conf.urls import url
import django_cas_ng.views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
