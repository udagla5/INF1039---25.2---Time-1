# contas/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import FeedView


urlpatterns = [
    # ========== PÁGINAS PRINCIPAIS ==========
    path('', views.home, name='home'),
    path('feed/', FeedView.as_view(), name='feed'),
    
    # ========== AUTENTICAÇÃO ==========
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro1/', views.cadastro1, name='cadastro1'),
    path('cadastro2/', views.cadastro2, name='cadastro2'),
    path('criar-conta/', views.criar_conta, name='criar_conta'),
    
    # ========== PERFIL ==========
    path('perfil-aluno/', views.perfil_aluno, name='perfil_aluno'),
    path('perfil-aluno-parte2/', views.perfil_aluno_parte2, name='perfil_aluno_parte2'),
    
    # ========== OPORTUNIDADES ==========
    path('criar-oportunidade/', views.criar_oportunidade, name='criar_oportunidade'),
    # Ou use a class-based view:
    # path('criar-oportunidade/', views.CriarOportunidadeView.as_view(), name='criar_oportunidade'),
    
    # ========== OUTRAS PÁGINAS ==========
    path('chat/', views.chat, name='chat'),
]