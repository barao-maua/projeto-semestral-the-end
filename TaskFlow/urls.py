"""
URL configuration for TaskFlow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register', core_views.register, name='register'),
    path('dashboard/', core_views.dashboard_main, name='dashboard_main'),
    path('profile/', core_views.profile, name='profile'),
    path('profile/edit', core_views.profile_edit, name='profile_edit'),
    path('projects/', core_views.projects, name='projects'),
    path('create_project/', core_views.create_project, name='create_project'),
    path('project/<int:projeto_id>/', core_views.project, name='project'),
    path('project/<int:projeto_id>/teams/', core_views.teams, name='teams'),
    path('project/<int:projeto_id>/tasks/', core_views.tasks, name='tasks'),
    path('project/<int:projeto_id>/settings/', core_views.settings, name='settings'),
    path("about/", core_views.about, name='about'),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
