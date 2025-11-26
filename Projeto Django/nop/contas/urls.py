# contas/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import FeedView
from django.urls import path
from . import views



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
    path('perfil/upload_avatar/', views.upload_avatar, name='upload_avatar'),
    # ========== OPORTUNIDADES ==========
    # URL de criação (que já deve estar funcionando)
    path('criar-oportunidade/', views.criar_oportunidade, name='criar_oportunidade'), 
    path('oportunidade/<int:id>/', views.detalhe_oportunidade, name='detalhe_oportunidade'),
    path('oportunidades/salvas/', views.oportunidades_salvas, name='oportunidades_salvas'),
    path('oportunidades/remover/<int:id>/', views.remover_salva, name='remover_salva'),

    
    # 🔑 ADICIONE ESTA LINHA: O nome 'lista_oportunidades' é o que o redirect procura.
    path('', views.lista_oportunidades, name='lista_oportunidades'),
    
    
    # ========== SISTEMA DE CHAT (RF14) ==========
    path('chat/', views.ChatView.as_view(), name='chat'),
    path('chat/enviar/', views.EnviarMensagemView.as_view(), name='enviar_mensagem'),
    path('chat/usuarios/', views.ListarUsuariosView.as_view(), name='usuarios_chat'),
]