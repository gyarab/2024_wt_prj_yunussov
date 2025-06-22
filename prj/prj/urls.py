"""
URL configuration for prj project.

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
from string import Template
from django import template
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from main.views import get_homepage, match_detail, teams_list, team_stats, team_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_homepage, name="home"),
    path('match/<int:match_id>/', match_detail, name="match_detail"),
    path('teams/', teams_list, name="teams_list"),
    path('stats/', team_stats, name='team_stats'),
    path('one', TemplateView.as_view(template_name='main/home.html')),
    path('two', TemplateView.as_view(template_name='main/home.html')),
    path('teams/<int:team_id>/', team_detail, name="team_detail"),
]