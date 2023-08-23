from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def transactions(request):
    return HttpResponse("Hello, World")

