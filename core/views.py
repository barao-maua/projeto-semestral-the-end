from django.shortcuts import render, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import Project
import datetime

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
        
        return redirect('login')
    return render(request, 'registration/register.html')

@login_required
def dashboard_projects(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        project = Project(1, name, description, start_date, end_date, datetime.datetime.now())

        project.save()
    projects = Project.objects.all()
    return render(request, 'dashboard/projects.html', {projects: projects})

# Visualização das informações do usuário
@login_required
def dashboard_main(request):
    return render(request, 'dashboard/main.html')

@login_required
def dashboard_profile(request):
    return render(request, 'dashboard/profile.html')


@login_required
def dashboard_tasks(request):
    return render(request, 'dashboard/tasks.html')

@login_required
def dashboard_analytics(request):
    return render(request, 'dashboard/analytics.html')