from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Transactions

# Create your views here.

# Exibe todas as transações
def allTransactions(request):
  all_transactions = Transactions.objects.all().values()
  template = loader.get_template('alltransactions.html')
  context = {
    'all_transactions': all_transactions,
  }
  return HttpResponse(template.render(context, request))

# Exibe detalhes da transação de acordo com o id dela
def details(request, id):
  all_transactions = Transactions.objects.get(id = id)
  template = loader.get_template('details.html')
  context = {
    'all_transactions': all_transactions
  }
  return HttpResponse(template.render(context, request))

