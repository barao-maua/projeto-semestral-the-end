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
from django.contrib.auth import views as auth_views

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register', core_views.register, name='register'),
    path('dashboard', core_views.dashboard_main, name='dashboard_main'),
    path("about", core_views.about, name='about'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('projects', core_views.dashboard_projects, name='dashboard_projects')
]
