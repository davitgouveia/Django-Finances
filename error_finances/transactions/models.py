from django.db import models

# Create your models here.

class Transactions(models.Model):
    userID = models.IntegerField()
    transactionName = models.CharField(max_length=100)