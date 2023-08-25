from django.contrib import admin
from .models import Transactions

# Register your models here.

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ("userID", "transactionName")

admin.site.register(Transactions, TransactionsAdmin)
