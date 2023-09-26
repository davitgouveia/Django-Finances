from django.contrib import admin
from .models import Transactions

# Treating data in admin
from django import forms
from .models import TransactionType
from .models import TransactionStatus

class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].label = 'Transaction Type'
    
class TransactionStatusForm(forms.ModelForm):
    class Meta:
        model = TransactionStatus
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = 'Transaction Status'

# Register your models here.

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ("idUser", "transactionName", "value", "idCategory", "creationDate")

admin.site.register(Transactions, TransactionsAdmin)

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    form = TransactionTypeForm
    
@admin.register(TransactionStatus)
class TransactionStatusAdmin(admin.ModelAdmin):
    form = TransactionStatusForm
