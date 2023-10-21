from django.urls import path
from . import views

urlpatterns = [
    path('', views.userTransactions, name='Alltransactions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('details/<int:id>', views.detailsTransaction, name='details'), # Chama a view details com o parametro int "id"
    path('create/', views.createTransaction, name='create'),
    path('edit/<int:id>', views.editTransaction, name='edit'),
    path('delete/<int:id>', views.deleteTransaction, name='delete'),
    path('accounts/', views.userAccounts, name='userAccounts'),
    path('accounts/create', views.createAccounts, name='createAccounts'),
    path('accounts/editaccounts/<int:id>', views.editAccounts, name='editAccounts'),
    
    path('testing/', views.testing, name='testing'),   
]