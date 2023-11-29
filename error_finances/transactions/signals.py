
from django.dispatch.dispatcher import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User  # Adjust this import if you are using a custom user model
from transactions.models import TransactionAccount, TransactionAccountTypes  # Import your model

def get_account_type(type):
    type_instance = TransactionAccountTypes.objects.get(id=type)
    return type_instance

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    accountType = get_account_type(1)
    if user.is_authenticated:
        TransactionAccount.objects.create(accountName="Wallet", accountColor="#00ff33", type=accountType, billCloseDate=0, billDueDate=0, idUser=user)

