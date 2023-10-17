from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum
from datetime import date, datetime, timedelta

from .models import Transactions
from .models import Expense,Income
from .models import TransactionCategory
from .models import TransactionRepeatability
from .models import TransactionType
from .models import TransactionStatus
from .models import cnfRepeatability

from .models import TransactionAccount

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

# Create Transactions
def createTransaction(request):
    today = date.today()
    current_date = today.strftime('%Y-%m-%d')
    user_data = userData(request)
    user_accounts = get_user_accounts(user_data['current_user_id'])
    
    if request.method == 'POST':
        transaction_name = request.POST['transactionName']
        transaction_description = request.POST['transactionDescription']
        value = request.POST['value']
        type = get_type(1) if ('expense' in request.POST) else get_type(2)
        status = get_status(request.POST['status'])
        category = request.POST['category']
        
        # Account
        account_id = request.POST['account']
        account = TransactionAccount.objects.get(id=account_id)
        
        creation_date = request.POST['creationDate']
        
        # Due Date
        if request.POST['status'] == "4" or request.POST['status'] == "6":
          due_date = request.POST['dueDate']
        else:
          due_date = None
        
        # Repeatable
        if('repeatable' in request.POST):
          repeatable_option = get_repeatability_option(request.POST['repeatability'])
          print("repeatable_quantity: " + request.POST['repeatable_quantity'])
          print("repeatable_date: " + request.POST['repeatability-date'])
          repeatable_quantity = 0 if('indefinite' in request.POST) else request.POST['repeatable_quantity']
          repeatable_date = 0 if request.POST['repeatability'] != "7" else request.POST['repeatability-date']
          repeatable_id = create_repetability(repeatable_option,repeatable_quantity,repeatable_date)
        else:
          repeatable_id = None
        
        
        color, category_name = category.split('/', 1)
        category_id = get_or_create_category(user_data['current_user_id'], category, color)

        # Create transaction
        if ('expense' in request.POST):
          transaction = Expense(
              idUser=user_data['current_user_id'],
              transactionName=transaction_name,
              transactionDescription=transaction_description,
              value=value,
              idType=type,
              idStatus=status,
              idCategory=category_id,
              idTransactionAccount=account,
              idRepeatable=repeatable_id,
              creationDate=creation_date,
              dueDate=due_date,
          )
        else:
          transaction = Income(
              idUser=user_data['current_user_id'],
              transactionName=transaction_name,
              transactionDescription=transaction_description,
              value=value,
              idType=type,
              idStatus=status,
              idCategory=category_id,
              idTransactionAccount=account,
              idRepeatable=repeatable_id,
              creationDate=creation_date,
              dueDate=due_date,
          )
        
        transaction.save()

        return redirect('/transactions')  # Redirecione para a página desejada após a criação da transação

    template = loader.get_template('create.html')
    context = {'current_date' : current_date,
               'current_user_id' : user_data['current_user_id'],
               'current_user_name' : user_data['current_user_name'],
               'user_accounts': user_accounts,
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
  
# Edit Transactions

def editTransaction(request, id):
  user_data = userData(request)
  transaction = Transactions.objects.get(id = id)
  user_accounts = get_user_accounts(user_data['current_user_id'])
  print(transaction.idType)
  
  if request.method == 'POST':
    name = request.POST['transactionName']
    description = request.POST['transactionDescription']
    value = request.POST['value']
    status = get_status(request.POST['status'])
    category = request.POST['category']
    account_id = request.POST['account']
    account = TransactionAccount.objects.get(id=account_id)
    
    color, category_name = category.split('/', 1)
    category_id = get_or_create_category(user_data['current_user_id'], category, color)
        
    transaction.transactionName = name
    transaction.transactionDescription = description
    transaction.idTransactionAccount = account
    transaction.value = value
    transaction.idStatus = status
    transaction.idCategory = category_id
    transaction.save()
        
    return redirect('/transactions')  # Redirect to the transaction list
  template = loader.get_template('edit.html')
  context = {'transaction' : transaction,
             'current_user_id' : user_data['current_user_id'],
             'current_user_name' : user_data['current_user_name'],
             'user_accounts': user_accounts,}
  
  return HttpResponse(template.render(context,request))

# Delete Transactions

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

# -== Accounts ==-

def get_user_accounts(user_id):
  user_accounts_instance = TransactionAccount.objects.filter(idUser=user_id)
  return user_accounts_instance

# Create Accounts

@login_required
def userAccounts(request):
    user_data = userData(request)
    
    user_accounts = get_user_accounts(user_data['current_user_id'])

    template = loader.get_template('accounts.html')
    context = {
       'current_user_id' : user_data['current_user_id'],
       'current_user_name' : user_data['current_user_name'],
       'user_accounts': user_accounts,
    }
    return HttpResponse(template.render(context, request))


# -== Dashboard ==-

def calculate_total_balance(user_id):

  income_sum = Income.objects.filter(transactions_ptr_id__idUser=user_id).aggregate(Sum('value'))['value__sum'] or 0
  expense_sum = Expense.objects.filter(transactions_ptr_id__idUser=user_id).aggregate(Sum('value'))['value__sum'] or 0
  difference = income_sum - expense_sum
  
  return difference

def calculate_monthly_balance(user_id):
  current_date = datetime.now()

  first_day_of_month = current_date.replace(day=1)
  last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month + 1, day=1) - timedelta(days=1)

  income_sum = Income.objects.filter(transactions_ptr_id__creationDate__range=(first_day_of_month, last_day_of_month),transactions_ptr_id__idUser=user_id).aggregate(Sum('value'))['value__sum'] or 0
  expense_sum = Expense.objects.filter(transactions_ptr_id__creationDate__range=(first_day_of_month, last_day_of_month),transactions_ptr_id__idUser=user_id).aggregate(Sum('value'))['value__sum'] or 0
  difference = income_sum - expense_sum
  
  context = {
       'difference' : difference,
       'income_sum' : income_sum,
       'expense_sum' : expense_sum}
  
  return (context)

@login_required
def dashboard(request):
  user_data = userData(request)
  
  monthly_balance = calculate_monthly_balance(user_data['current_user_id'])
  total_balance = calculate_total_balance(user_data['current_user_id'])
  
  template = loader.get_template('dashboard.html')
  context = {
    'current_user_id' : user_data['current_user_id'],
    'current_user_name' : user_data['current_user_name'],
    'total_balance' : total_balance,
    'monthly_balance' : monthly_balance['difference'],
    'monthly_expense' : monthly_balance['expense_sum'],
    'monthly_income' : monthly_balance['income_sum']
  }
  
  return HttpResponse(template.render(context, request))

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'teste' : ['Apple', 'Banana', 'Cherry'],
  }
  return HttpResponse(template.render(context, request))

