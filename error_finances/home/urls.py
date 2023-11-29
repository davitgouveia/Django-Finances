from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('settings/', views.settings, name='settings'),
    path('help/', views.help, name='help'),
]