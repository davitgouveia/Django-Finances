from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transactionName = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100, default='Outros')
    creationDate = models.DateField(default=date.today)
    expense = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} {self.transactionName} {self.value} {self.category} {self.creationDate}"
    

    # dividas
    # dueDate = models.DateField()