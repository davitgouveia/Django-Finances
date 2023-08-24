from django.urls import path
from . import views

urlpatterns = [
    path('', views.allTransactions, name='Alltransactions'),
    path('details/<int:id>', views.details, name='details') # Chama a view details com o parametro int "id"
]