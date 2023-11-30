from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.db.models import Sum, Count
from datetime import date, datetime, timedelta
import calendar

from .models import Transactions
from .models import Expense, Income
from .models import TransactionCategory
from .models import TransactionRepeatability
from .models import TransactionType
from .models import TransactionStatus
from .models import cnfRepeatability

from .models import TransactionAccount
from .models import TransactionAccountTypes


@login_required
def userData(request):
    current_user_name = request.user.username
    current_user_id = request.user

    context = {
        "current_user_id": current_user_id,
        "current_user_name": current_user_name,
    }

    return context


# Exibe transações do usuário
@login_required
def userTransactions(request):
    user_data = userData(request)
    user_accounts = get_user_accounts(user_data["current_user_id"])
    total_balance = calculate_total_balance(user_data["current_user_id"])
    today = date.today()
    
    current_date = today.strftime("%Y-%m-%d")
    current_month = today.strftime("%m")
    current_year = today.strftime("%Y")
    
    user_available_category = TransactionCategory.objects.filter(idUser=user_data["current_user_id"], )

    # Main
    user_transactions = Transactions.objects.filter(
        idUser=user_data["current_user_id"],
        creationDate__month=current_month,
        creationDate__year=current_year,
    ).order_by("-creationDate")

    # Filters

    if request.method == "POST":
        # Create Transaction
        if 'createTransaction' in request.POST:
            transaction_name_data = request.POST["transactionName"]
            transaction_description_data = request.POST["transactionDescription"]
            value_data = request.POST["value"]
            expense_data = True if ("expense" in request.POST) else False
            status_data = get_status(request.POST["status"])
            category_data = request.POST["category"]

            account_id = request.POST["account"]
            account_data = TransactionAccount.objects.get(id=account_id)

            creation_date_data = request.POST["creationDate"]

            if request.POST["status"] == "4" or request.POST["status"] == "6":
                due_date_data = request.POST["dueDate"]
            else:
                due_date_data = None

            createTransactionModal(
                user_data,
                transaction_name_data,
                transaction_description_data,
                value_data,
                expense_data,
                status_data,
                category_data,
                account_data,
                creation_date_data,
                due_date_data,
            )
            return redirect("/transactions/create_success")

    context = {
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],
        "user_transactions": user_transactions,
        "user_accounts": user_accounts,
        "user_available_category" : user_available_category,
        "current_date": current_date,
        "total_balance": total_balance,
    }
    return render(request, "alltransactions.html", context)


# Exibe detalhes da transação de acordo com o id dela
def detailsTransaction(request, id):
    user_data = userData(request)
    total_balance = calculate_total_balance(user_data["current_user_id"])

    transaction_fetch = Transactions.objects.get(id=id)  
    
    if transaction_fetch.idType.id == 1:
        transaction = Expense.objects.get(id=id) 
    else: 
        transaction = Income.objects.get(id=id) 

    template = loader.get_template("details.html")
    context = {
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],
        "transaction": transaction,
        "total_balance": total_balance,
    }
    return HttpResponse(template.render(context, request))


def createTransactionModal(
    user_data,
    transactionName_data,
    transactionDescription_data,
    value_data,
    expense_data,
    status_data,
    category_data,
    account_id_data,
    creation_date_data,
    due_date_data,
):
    repeatable_id = None
    type = get_type(1) if (expense_data) else get_type(2)
    color, category_name = category_data.split("/", 1)
    category_id = get_or_create_category(
        user_data["current_user_id"], category_name, color
    )

    # Create transaction
    if expense_data:
        transaction = Expense(
            idUser=user_data["current_user_id"],
            transactionName=transactionName_data,
            transactionDescription=transactionDescription_data,
            value=value_data,
            idType=type,
            idStatus=status_data,
            idCategory=category_id,
            idTransactionAccount=account_id_data,
            idRepeatable=repeatable_id,
            creationDate=creation_date_data,
            dueDate=due_date_data,
        )
    else:
        transaction = Income(
            idUser=user_data["current_user_id"],
            transactionName=transactionName_data,
            transactionDescription=transactionDescription_data,
            value=value_data,
            idType=type,
            idStatus=status_data,
            idCategory=category_id,
            idTransactionAccount=account_id_data,
            idRepeatable=repeatable_id,
            creationDate=creation_date_data,
            dueDate=due_date_data,
        )

    transaction.save()


# Create Transactions
def createSuccess(request):
    return render(request, "create_success.html")


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
        category_instance = TransactionCategory.objects.get(
            idUser=user_id, categoryName=categoryName
        )
    except TransactionCategory.DoesNotExist:
        category_instance = TransactionCategory.objects.create(
            idUser=user_id, categoryName=categoryName, categoryColor=category_color
        )

    return category_instance


def create_repetability(repeatable_option, repeatable_quantity, repeatable_date):
    repeatability_instance = TransactionRepeatability.objects.create(
        idRepeatability=repeatable_option,
        quantity=repeatable_quantity,
        date=repeatable_date,
    )
    return repeatability_instance


# Edit Transactions
def editTransaction(request, id):
    user_data = userData(request)
    transaction = Transactions.objects.get(id=id)
    user_accounts = get_user_accounts(user_data["current_user_id"])
    total_balance = calculate_total_balance(user_data["current_user_id"])

    if request.method == "POST":
        name = request.POST["transactionName"]
        description = request.POST["transactionDescription"]
        value = request.POST["value"]
        status = get_status(request.POST["status"])
        category = request.POST["category"]
        account_id = request.POST["account"]
        account = TransactionAccount.objects.get(id=account_id)

        color, category_name = category.split("/", 1)
        category_id = get_or_create_category(
            user_data["current_user_id"], category_name, color
        )

        transaction.transactionName = name
        transaction.transactionDescription = description
        transaction.idTransactionAccount = account
        transaction.value = value
        transaction.idStatus = status
        transaction.idCategory = category_id
        transaction.save()

        return redirect("/transactions")  # Redirect to the transaction list

    template = loader.get_template("edit.html")
    context = {
        "transaction": transaction,
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],
        "user_accounts": user_accounts,
        "total_balance": total_balance,
    }

    return HttpResponse(template.render(context, request))


# Delete Transactions


def deleteTransaction(request, id):
    user_data = userData(request)
    transaction = Transactions.objects.get(id=id)
    total_balance = calculate_total_balance(user_data["current_user_id"])

    if request.method == "POST":
        if "confirm" in request.POST:
            transaction.delete()
            return redirect("/transactions")

    template = loader.get_template("delete.html")
    context = {
        "transaction": transaction,
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],
        "total_balance": total_balance,
    }

    return HttpResponse(template.render(context, request))


# -== Accounts ==-


def get_user_accounts(user_id):
    user_accounts_instance = TransactionAccount.objects.filter(idUser=user_id)
    return user_accounts_instance


@login_required
def userAccounts(request):
    user_data = userData(request)
    total_balance = calculate_total_balance(user_data["current_user_id"])

    user_accounts = get_user_accounts(user_data["current_user_id"])

    template = loader.get_template("accounts.html")
    context = {
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],
        "user_accounts": user_accounts,
        "total_balance": total_balance,
    }
    return HttpResponse(template.render(context, request))


# Create Accounts


def get_account_type(type):
    type_instance = TransactionAccountTypes.objects.get(id=type)
    return type_instance


def createAccounts(request):
    user_data = userData(request)
    total_balance = calculate_total_balance(user_data["current_user_id"])

    template = loader.get_template("createAccounts.html")

    if request.method == "POST":
        account_name = request.POST["account_name"]
        account_color = request.POST["account_color"]
        account_type = get_account_type(request.POST["account_type"])

        if account_type.id == 3:
            account_billCloseDate = request.POST["account_billCloseDate"]
            account_billDueDate = request.POST["account_billDueDate"]
        else:
            account_billCloseDate = 0
            account_billDueDate = 0

        newAccount = TransactionAccount(
            accountName=account_name,
            accountColor=account_color,
            type=account_type,
            billCloseDate=account_billCloseDate,
            billDueDate=account_billDueDate,
            idUser=user_data["current_user_id"],
        )

        newAccount.save()
        return redirect("/transactions/accounts")

    context = {
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],
        "total_balance": total_balance,
    }

    return HttpResponse(template.render(context, request))


# Edit Accounts


def editAccounts(request, id):
    user_data = userData(request)
    account = TransactionAccount.objects.get(id=id)
    total_balance = calculate_total_balance(user_data["current_user_id"])

    if request.method == "POST":
        color = request.POST["account_color"]
        account.accountColor = color

        if account.type.type == "Credit":
            closeDate = request.POST["account_billCloseDate"]
            dueDate = request.POST["account_billDueDate"]

            account.billCloseDate = closeDate
            account.billDueDate = dueDate

        account.save()
        return redirect("/transactions/accounts")

    template = loader.get_template("editAccounts.html")
    context = {
        "account": account,
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],
        "total_balance": total_balance,
    }

    return HttpResponse(template.render(context, request))


# -== Dashboard ==-


def calculate_total_balance(user_id):
    income_sum = (
        Income.objects.filter(transactions_ptr_id__idUser=user_id, transactions_ptr_id__idStatus__status='Received').aggregate(
            Sum("value")
        )["value__sum"]
        or 0
    )
    expense_sum = (
        Expense.objects.filter(transactions_ptr_id__idUser=user_id, transactions_ptr_id__idStatus__status='Paid').aggregate(
            Sum("value")
        )["value__sum"]
        or 0
    )
    difference = income_sum - expense_sum

    return difference


def calculate_monthly_balance(user_id):
    current_date = datetime.now()

    first_day_of_month = current_date.replace(day=1)
    last_day_of_month = first_day_of_month.replace(
        month=first_day_of_month.month + 1, day=1
    ) - timedelta(days=1)

    income_sum = (
        Income.objects.filter(
            transactions_ptr_id__creationDate__range=(
                first_day_of_month,
                last_day_of_month,
            ),
            transactions_ptr_id__idUser=user_id, transactions_ptr_id__idStatus__status='Received'
        ).aggregate(Sum("value"))["value__sum"]
        or 0
    )
    expense_sum = (
        Expense.objects.filter(
            transactions_ptr_id__creationDate__range=(
                first_day_of_month,
                last_day_of_month,
            ),
            transactions_ptr_id__idUser=user_id, transactions_ptr_id__idStatus__status='Paid'
        ).aggregate(Sum("value"))["value__sum"]
        or 0
    )
    difference = income_sum - expense_sum

    context = {
        "difference": difference,
        "income_sum": income_sum,
        "expense_sum": expense_sum,
    }

    return context


def category_pie_chart(request):
    user_data = userData(request)
    labels = []
    data = []
    color = []
    
    queryset = Expense.objects.values('idCategory__categoryName', 'idCategory__categoryColor').filter(transactions_ptr_id__idUser=user_data["current_user_id"]).annotate(transactions=Count('id'))
    
    for entry in queryset:
        labels.append(entry['idCategory__categoryName'])
        color.append('#' + entry['idCategory__categoryColor'])
        data.append(entry['transactions'])
        
    return JsonResponse(data={
        'labels' : labels,
        'color' : color,
        'data' : data,
    })
    
def expense_doughnut_chart(request):
    user_data = userData(request)
    labels = []
    data = []
    color = []
    
    queryset = Expense.objects.values('idStatus__status').filter(transactions_ptr_id__idUser=user_data["current_user_id"]).annotate(transactions=Count('id'))
    
    for entry in queryset:
        labels.append(entry['idStatus__status'])
        if(entry['idStatus__status'] == 'Paid'):
            color.append('#1ec92f')
        else:
            color.append('#f74c4c')
        data.append(entry['transactions'])
        
    return JsonResponse(data={
        'labels' : labels,
        'color' : color,
        'data' : data,
    })
    
def get_days_in_month(year, month):
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    all_days = [first_day + timedelta(days=x) for x in range((last_day - first_day).days + 1)]
    
    return all_days

def expenseIncome_line_chart(request):
    year = 2023
    month = 11
    user_data = userData(request)
    labelsExpense = []
    dataExpense = []
    
    labelsIncome = []
    dataIncome = []
    
    # Get all days in the specified month and year
    all_days = get_days_in_month(year, month)
    
    for day in all_days:
        # Filter expenses by date
        querysetExpense = Expense.objects.filter(
            transactions_ptr_id__idUser=user_data["current_user_id"],
            creationDate__year=day.year,
            creationDate__month=day.month,
            creationDate__day=day.day
        ).values('id').annotate(transactions=Sum('value'))
        
        # Filter incomes by date
        querysetIncome = Income.objects.filter(
            transactions_ptr_id__idUser=user_data["current_user_id"],
            creationDate__year=day.year,
            creationDate__month=day.month,
            creationDate__day=day.day
        ).values('id').annotate(transactions=Sum('value'))
        
        # Append data for each day
        labelsExpense.append(day.strftime('%Y-%m-%d'))
        dataExpense.append(sum(entry['transactions'] or 0 for entry in querysetExpense))
        
        labelsIncome.append(day.strftime('%Y-%m-%d'))
        dataIncome.append(sum(entry['transactions'] or 0 for entry in querysetIncome))
    
    return JsonResponse({
        'dataExpense': {
            'labelsExpense': labelsExpense,
            'dataExpense': dataExpense,
        },
        'dataIncome': {
            'labelsIncome': labelsIncome,
            'dataIncome': dataIncome,
        }
    }
    )


@login_required
def dashboard(request):
    user_data = userData(request)

    monthly_balance = calculate_monthly_balance(user_data["current_user_id"])
    total_balance = calculate_total_balance(user_data["current_user_id"])

    template = loader.get_template("dashboard.html")
    context = {
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],
        "total_balance": total_balance,
        "monthly_balance": monthly_balance["difference"],
        "monthly_expense": monthly_balance["expense_sum"],
        "monthly_income": monthly_balance["income_sum"],
    }

    return HttpResponse(template.render(context, request))


def testing(request):
    template = loader.get_template("template.html")
    context = {
        "teste": ["Apple", "Banana", "Cherry"],
    }
    return HttpResponse(template.render(context, request))
