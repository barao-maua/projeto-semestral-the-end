from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import Project, Profile, Task, Comment, ProjectPermission
import datetime

#________________________Startup___________________________

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#________________________Login/Register___________________________

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile

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

        # Verificando se o perfil já existe antes de criá-lo
        if not Profile.objects.filter(user=user).exists():
            profile = Profile.objects.create(user=user)
            profile.save()

        return redirect('login')
    
    return render(request, 'registration/register.html')


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

@login_required
def profile(request):
    return render(request, 'profile/main.html')

#________________________Projects___________________________
"""
Dashboard
Projects
"""

@login_required
def dashboard_main(request):
    return render(request, 'dashboard/main.html')

@login_required
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        project = Project(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            owner=request.user
        )
        project.save()

        # Atribuir permissão "edit" ao criador do projeto
        ProjectPermission.objects.create(
            user=request.user,
            project=project,
            permission='edit'
        )

        return redirect('projects')

    return render(request, 'dashboard/create_project.html')

@login_required
def projects(request):
    permissions = ProjectPermission.objects.filter(user=request.user).select_related('project')
    projects_with_permissions = []

    for perm in permissions:
        projects_with_permissions.append({
            'project': perm.project,
            'permission': perm.permission,
            'permission_display': perm.get_permission_display()
        })
    
    print("PERM =",projects_with_permissions)

    return render(request, 'dashboard/projects.html', {
        'projects_with_permissions': projects_with_permissions
    })

#________________________Desktop___________________________
"""
Dashboard <- Voltar ao dashboard
Projects <- Selecionar outro projeto
Tasks
Teams
Settigns
"""

@login_required
def tasks(request, projeto_id):
    projeto = get_object_or_404(Project, id=projeto_id)

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        task_start_date = request.POST.get('task_start_date')
        task_end_date = request.POST.get('task_end_date')

        task = Task.objects.create(
            name=task_name,
            description=task_description,
            start_date=task_start_date,
            end_date=task_end_date,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

        # Associa a task ao projeto
        projeto.tasks.add(task)

        return redirect('tasks', projeto_id=projeto.id)

    # Recupera tarefas associadas ao projeto
    tasks = projeto.tasks.all().order_by('-created_at')

    return render(request, 'project/tasks.html', {
        'projeto': projeto,
        'tasks': tasks
    })

@login_required
def project(request, projeto_id):
    projeto = get_object_or_404(Project, id=projeto_id)

    return render(request, 'project/tasks.html', {
        'projeto': projeto
    })

@login_required
def teams(request, projeto_id):
    projeto = get_object_or_404(Project, id=projeto_id)

    return render(request, 'project/teams.html', {
        'projeto': projeto
    })

@login_required
def settings(request, projeto_id):
    projeto = get_object_or_404(Project, id=projeto_id)

    return render(request, 'project/settings.html', {
        'projeto': projeto
    })

#________________________End___________________________