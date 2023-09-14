from django.urls import path
from . import views

urlpatterns = [
    path('', views.userTransactions, name='Alltransactions'),
    path('details/<int:id>', views.detailsTransaction, name='details'), # Chama a view details com o parametro int "id"
    path('create/', views.createTransaction, name='create'),
    path('edit/<int:id>', views.editTransaction, name='edit'),
    path('delete/<int:id>', views.deleteTransaction, name='delete'),
    
    path('testing/', views.testing, name='testing'),   
]