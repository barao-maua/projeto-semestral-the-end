from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'registration/register.html', {'error': 'Email already exists'})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        return render(request, 'registration/login.html', {'success': 'User created successfully'})
    return render(request, 'registration/register.html')

@login_required
def dashboard_main(request):
    return render(request, 'dashboard/main.html')

