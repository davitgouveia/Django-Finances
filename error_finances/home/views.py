from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def main(request):
    context = {}  # Initialize an empty context dictionary

    if request.user.is_authenticated:
        context['username'] = request.user.username
        # You can add more user-related information to the context if needed

    return render(request, 'main.html', context)