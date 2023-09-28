from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from datetime import date

from .models import Transactions
from .models import TransactionCategory
from .models import TransactionRepeatability
from .models import TransactionType
from .models import TransactionStatus
from .models import cnfRepeatability

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
    user_transactions = Transactions.objects.filter(idUser=user_data['current_user_id'])

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
        transaction_description = request.POST['transactionDescription']
        value = request.POST['value']
        type = get_type(1) if ('expense' in request.POST) else get_type(2)
        status = get_status(request.POST['status'])
        category = request.POST['category']
        creation_date = request.POST['creationDate']
        
        if('repeatable' in request.POST):
          repeatable_option = get_repeatability_option(request.POST['repeatability'])
          repeatable_quantity = request.POST['repeatable_quantity']
          repeatable_date = 0 if request.POST['repeatability-date'] == "" else request.POST['repeatability-date']
          repeatable_id = create_repetability(repeatable_option,repeatable_quantity,repeatable_date)
        else:
          repeatable_id = None
        
        
        color, category_name = category.split('/', 1)
        category_id = get_or_create_category(user_data['current_user_id'], category, color)

        # Create transaction
        transaction = Transactions(
            idUser=user_data['current_user_id'],
            transactionName=transaction_name,
            transactionDescription=transaction_description,
            value=value,
            idType=type,
            idStatus=status,
            idCategory=category_id,
            idRepeatable=repeatable_id,
            creationDate=creation_date,
        )
        transaction.save()

        return redirect('/transactions')  # Redirecione para a página desejada após a criação da transação

    template = loader.get_template('create.html')
    context = {'current_date' : current_date,
               'current_user_id' : user_data['current_user_id'],
               'current_user_name' : user_data['current_user_name'],
    }
    
    return HttpResponse(template.render(context,request))

def get_repeatability_option(option):
  repeat_option_instance = cnfRepeatability.objects.get(id=option)
  return repeat_option_instance

def get_status(status):
  status_instance = TransactionStatus.objects.get(id=status)
  return status_instance

def get_type(type):
  type_instance = TransactionType.objects.get(id=type)
  return type_instance
  
def get_or_create_category(user_id, categoryName, category_color):
    try:
        category_instance = TransactionCategory.objects.get(idUser=user_id, categoryName=categoryName)
    except TransactionCategory.DoesNotExist:
        category_instance = TransactionCategory.objects.create(idUser=user_id, categoryName=categoryName, categoryColor=category_color)

    return category_instance 
  
def create_repetability(repeatable_option, repeatable_quantity, repeatable_date):
  repeatability_instance = TransactionRepeatability.objects.create(idRepeatability=repeatable_option, quantity=repeatable_quantity,date=repeatable_date)
  return repeatability_instance
  

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

