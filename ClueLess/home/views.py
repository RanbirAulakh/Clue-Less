from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def help_page(request):
    return render(request, 'help.html')

def about_page(request):
    return render(request, 'about.html')

def statistic_page(request):
    return render(request, 'statistic.html')