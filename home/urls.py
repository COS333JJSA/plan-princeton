from django.urls import path
from . import views
from django.conf.urls import url
import django_cas_ng.views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('scheduler/', views.scheduler, name='scheduler'),
    path('sampleschedules/', views.sampleschedules, name='sampleschedules'),
    path('aas/', views.aas, name='aas'),
    path('logout/', views.logout, name='logout')
]
