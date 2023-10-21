from django.db import models
from django.contrib.auth.models import User
from datetime import date


class TransactionType(models.Model):
    type = models.CharField(max_length=10)
    
    def __str__(self):
        return self.type

class TransactionStatus(models.Model):
    status = models.CharField(max_length=10)
    
    def __str__(self):
        return self.status

class TransactionCategory(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryName = models.CharField(max_length=50)
    categoryColor = models.CharField(max_length=20)
    
class TransactionAccountTypes(models.Model):
    type = models.CharField(max_length=10)

class TransactionAccount(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField # 1 = Active, 0 = Inactive
    accountName = models.CharField(max_length=50)
    accountColor = models.CharField(max_length=10)
    type = models.ForeignKey(TransactionAccountTypes, on_delete=models.PROTECT)
    billCloseDate = models.IntegerField()
    billDueDate = models.IntegerField()

class cnfRepeatability(models.Model):
    repeatability = models.CharField(max_length=15)
    
class TransactionRepeatability(models.Model):
    idRepeatability = models.ForeignKey(cnfRepeatability, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    date = models.IntegerField(default=0)
    
class Transactions(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    transactionName = models.CharField(max_length=100)
    transactionDescription = models.CharField(max_length=100, null=True)
    value = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    idType = models.ForeignKey(TransactionType, on_delete=models.PROTECT, default=1)
    idStatus = models.ForeignKey(TransactionStatus, on_delete=models.SET(2), default=1)
    idCategory = models.ForeignKey(TransactionCategory, on_delete=models.SET(1), null=True)
    idTransactionAccount = models.ForeignKey(TransactionAccount, on_delete=models.PROTECT, null=True)
    idRepeatable = models.ForeignKey(TransactionRepeatability, on_delete=models.SET(1), null=True)
    creationDate = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.user.username} {self.transactionName} {self.value} {self.idCategory} {self.creationDate}"

class Expense(Transactions):
    dueDate = models.DateField(null=True)
    
class Income(Transactions):
    dueDate = models.DateField(null=True)