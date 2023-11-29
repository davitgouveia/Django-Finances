from django.urls import path
from . import views

urlpatterns = [
    path('', views.userTransactions, name='Alltransactions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('details/<int:id>', views.detailsTransaction, name='details'), # Chama a view details com o parametro int "id"
    path('create_success', views.createSuccess, name='createSuccess'),
    path('edit/<int:id>', views.editTransaction, name='edit'),
    path('delete/<int:id>', views.deleteTransaction, name='delete'),
    path('accounts/', views.userAccounts, name='userAccounts'),
    path('accounts/create', views.createAccounts, name='createAccounts'),
    path('accounts/editaccounts/<int:id>', views.editAccounts, name='editAccounts'),
    
    #Charts JSON#
    path('category-pie-chart', views.category_pie_chart, name='category-pie-chart'),
    path('expense-doughnut-chart', views.expense_doughnut_chart, name='expense-doughnut-chart'),
    
    path('testing/', views.testing, name='testing'),   
]