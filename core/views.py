from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def Sobre(request):
    return render(request, 'sobre.html')