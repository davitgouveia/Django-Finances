from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def userData(request):
    current_user_name = request.user.username
    current_user_id = request.user

    context = {
        "current_user_id": current_user_id,
        "current_user_name": current_user_name,
    }

    return context

def main(request):
    return redirect("/transactions")

@login_required
def settings(request):
    user_data = userData(request)
    
    context = {
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],   
    }

    return render(request, 'settings.html', context)

def help(request):
    user_data = userData(request)
    
    context = {
        "current_user_id": user_data["current_user_id"],
        "current_user_name": user_data["current_user_name"],   
    }

    return render(request, 'help.html', context)