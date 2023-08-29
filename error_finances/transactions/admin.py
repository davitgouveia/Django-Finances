from django.contrib import admin
from .models import Transactions

# Register your models here.

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ("user", "transactionName", "value", "category", "creationDate")

admin.site.register(Transactions, TransactionsAdmin)
