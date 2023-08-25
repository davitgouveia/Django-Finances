from django.db import models

# Create your models here.

class Transactions(models.Model):
    userID = models.IntegerField()
    transactionName = models.CharField(max_length=100)

    # Altera a representação de strings de objetos em Python
    def __str__(self):
        return f"{self.userID} {self.transactionName}"