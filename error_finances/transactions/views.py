from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from datetime import date

from .models import Transactions

@login_required
def userData(request):
  current_user_name = request.user.first_name
  current_user_id = request.user
  
  context = {
       'current_user_id' : current_user_id,
       'current_user_name' : current_user_name}

  return(context)

# Exibe transações do usuário
@login_required
def userTransactions(request):
    user_data = userData(request)
    
    all_transactions = Transactions.objects.all().values()
    user_transactions = Transactions.objects.filter(user=user_data['current_user_id'])

    template = loader.get_template('alltransactions.html')
    context = {
       'current_user_id' : user_data['current_user_id'],
       'current_user_name' : user_data['current_user_name'],
       'user_transactions': user_transactions,
       'all_transactions': all_transactions,
    }
    return HttpResponse(template.render(context, request))

# Exibe detalhes da transação de acordo com o id dela
def detailsTransaction(request, id):
  user_data = userData(request)
  
  transaction = Transactions.objects.get(id = id)
  
  template = loader.get_template('details.html')
  context = {
    'current_user_id' : user_data['current_user_id'],
    'current_user_name' : user_data['current_user_name'],
    'transaction': transaction
  }
  return HttpResponse(template.render(context, request))

# CRUD
def createTransaction(request):
    today = date.today()
    current_date = today.strftime('%Y-%m-%d')
    user_data = userData(request)
    
    if request.method == 'POST':
        transaction_name = request.POST['transactionName']
        value = request.POST['value']
        category = request.POST['category']
        creation_date = request.POST['creationDate']
        expense = 'expense' in request.POST  # Verifique se a caixa de despesas está marcada

        transaction = Transactions(
            user=user_data['current_user_id'],
            transactionName=transaction_name,
            value=value,
            category=category,
            creationDate=creation_date,
            expense=expense
        )
        transaction.save()

        return redirect('/transactions')  # Redirecione para a página desejada após a criação da transação

    template = loader.get_template('create.html')
    context = {'current_date' : current_date,
               'current_user_id' : user_data['current_user_id'],
               'current_user_name' : user_data['current_user_name'],
    }
    
    return HttpResponse(template.render(context,request))

def editTransaction(request, id):
  user_data = userData(request)
  transaction = Transactions.objects.get(id = id)
  
  if request.method == 'POST':
    transaction_name = request.POST['transactionName']
    value = request.POST['value']
    category = request.POST['category']
    creation_date = request.POST['creationDate']
    expense = 'expense' in request.POST
        
    transaction.transactionName = transaction_name
    transaction.value = value
    transaction.category = category
    transaction.creationDate = creation_date
    transaction.expense = expense
    transaction.save()
        
    return redirect('/transactions')  # Redirect to the transaction list
  template = loader.get_template('edit.html')
  context = {'transaction' : transaction,
             'current_user_id' : user_data['current_user_id'],
             'current_user_name' : user_data['current_user_name']}
  
  return HttpResponse(template.render(context,request))

def deleteTransaction(request, id):
  user_data = userData(request)
  transaction = Transactions.objects.get(id = id)
  
  if request.method == 'POST':
    
        if 'confirm' in request.POST:
            transaction.delete()
            return redirect('/transactions')
  
  template = loader.get_template('delete.html')
  context = {'transaction' : transaction,
             'current_user_id' : user_data['current_user_id'],
             'current_user_name' : user_data['current_user_name']}
        
  return HttpResponse(template.render(context,request))

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'teste' : ['Apple', 'Banana', 'Cherry'],
  }
  return HttpResponse(template.render(context, request))

