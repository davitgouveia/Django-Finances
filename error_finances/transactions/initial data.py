def insert_initial_repeatability_data(apps, schema_editor):
    cnfRepeatability = apps.get_model('transactions', 'cnfRepeatability')  # Replace 'your_app_name' with your actual app name

    repeatability_values = [
        'Single',
        'Daily',
        'Weekly',
        'Monthly',
        'Annually',
        'Indefinitely',
        'Specific',
    ]
    
    for value in repeatability_values:
        cnfRepeatability.objects.create(repeatability=value)
        
def insert_initial_status_data(apps, schema_editor):
    TransactionStatus = apps.get_model('transactions', 'TransactionStatus')  # Replace 'your_app_name' with your actual app name

    status_values = [
        'Active',
        'Inactive',
        'Paid',
        'Not Paid',
        'Receivable',
        'Received',
    ]
    
    for value in status_values:
        TransactionStatus.objects.create(status=value)

def insert_initial_type_data(apps, schema_editor):
    TransactionType = apps.get_model('transactions', 'TransactionType')  # Replace 'your_app_name' with your actual app name

    status_values = [
        'Expense',
        'Income',
    ]
    
    for value in status_values:
        TransactionType.objects.create(type=value)