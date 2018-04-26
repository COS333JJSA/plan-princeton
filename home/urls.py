from django.urls import path
from . import views
import django_cas_ng.views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
]
