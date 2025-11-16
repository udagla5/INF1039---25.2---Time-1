"""
URL configuration for nop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login1, name='login1'),
    path('cadastro1/', views.cadastro1, name='cadastro1'),
    path('cadastro2/', views.cadastro2, name='cadastro2'),
    path('criar_oportunidade1/', views.criar_oportunidade1, name='criar_oportunidade1'),
    path('criar_oportunidade3/', views.criar_oportunidade3, name='criar_oportunidade3'),
    path('feed/', views.feed, name='feed'),
    path('perfil_aluno/', views.perfil_aluno, name='perfil_aluno'),
    path('perfil_aluno_parte2/', views.perfil_aluno_parte2, name='perfil_aluno_parte2'),
]

