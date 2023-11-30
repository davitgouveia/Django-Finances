from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('settings/', views.settings, name='settings'),
    path('investments/', views.investments, name='investments'),
    path('help/', views.help, name='help'),
    path('teste/', views.teste, name='teste'),
]