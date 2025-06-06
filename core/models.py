from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def has_photo(self):
        return bool(self.photo)

# Modelos
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class TaskCategory(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='task_categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.project.name})"

class Status(models.Model):
    CHOICES = [
        ('not_started', 'Não Iniciado'),
        ('in_progress', 'Em Progresso'),
        ('completed', 'Concluído'),
        ('on_hold', 'Em Espera'),
        ('cancelled', 'Cancelado'),
    ]
    name = models.CharField(max_length=100, choices=CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    states = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # valida se a categoria pertence ao mesmo projeto da tarefa
        if self.category and self.category.project != self.project:
            raise ValidationError("A categoria da tarefa deve pertencer ao mesmo projeto da tarefa.")

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    def get_user(self):
        return self.user

class ProjectPermission(models.Model):
    PERMISSION_CHOICES = [
        ('edit', 'Pode Editar'),
        ('view', 'Pode Visualizar')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name='unique_user_project_permission')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.get_permission_display()})"

    def has_permission(self, permission_type):
        return self.permission == permission_type

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_owned')
    tasks = models.ManyToManyField(Task, related_name='projects')
    comments = models.ManyToManyField(Comment, related_name='projects')
    team_members = models.ManyToManyField(User, related_name='projects_team_members')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    states = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('A data de término não pode ser anterior à data de início.')
        
    def get_tasks(self):
        return self.tasks.all()
    
    def get_comments(self):
        return self.comments.all()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.created_at}"
