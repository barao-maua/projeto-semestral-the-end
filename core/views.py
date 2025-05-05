from django.shortcuts import render, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import Project, Profile, Task, Comment, ProjectPermission
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
        
        # Verificando se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error': 'Username already exists'})
        
        # Verificando se o email já está registrado
        if User.objects.filter(email=email).exists():
            return render(request, 'registration/register.html', {'error': 'Email already exists'})
        
        # Criando o usuário
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Criando um perfil para o usuário
        profile = Profile.objects.create(user=user)
        profile.save()

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
def task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        task = Task(1, title, description, start_date, end_date, datetime.datetime.now())

        task.save()
    tasks = Task.objects.all()
    return render(request, 'dashboard/tasks.html')

@login_required
def dashboard_analytics(request):
    return render(request, 'dashboard/analytics.html')

@login_required
def profile(request):
    return render(request, 'profile/main.html')

@login_required
def teams(request):
    return render(request, 'dashboard/teams.html')

@login_required
def profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()

        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        profile.save()

        return redirect('profile_edit')

    return render(request, 'profile/edit.html', {'profile': profile})
