from django.contrib import admin
from .models import Transactions

# Register your models here.

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ("idUser", "transactionName", "value", "idCategory", "creationDate")

admin.site.register(Transactions, TransactionsAdmin)
