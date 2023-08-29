from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Transactions

# Create your views here. #

# Exibe transações do usuário
@login_required
def userTransactions(request):
    current_user = request.user
    all_transactions = Transactions.objects.all().values()
    user_transactions = Transactions.objects.filter(user=current_user)

    template = loader.get_template('alltransactions.html')
    context = {
       'current_user' : current_user,
       'user_transactions': user_transactions,
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

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'teste' : ['Apple', 'Banana', 'Cherry'],
  }
  return HttpResponse(template.render(context, request))

