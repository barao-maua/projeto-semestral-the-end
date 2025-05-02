from django.contrib import admin
from .models import Category, Task, Comment, ProjectPermission, Project, Notification

# Register your models here.

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(ProjectPermission)
admin.site.register(Project)
admin.site.register(Notification)