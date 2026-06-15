from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "pages/home.html")

def index(request):
    return HttpResponse("Hello, World!")