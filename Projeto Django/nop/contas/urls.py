from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import CustomPasswordResetForm 

urlpatterns = [
    # ========== PÁGINAS PRINCIPAIS ==========
    path('', views.home, name='home'),
    
    # URL do Feed principal
    path('feed/', views.lista_oportunidades, name='feed'),

    # ========== AUTENTICAÇÃO ==========
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro1/', views.cadastro1, name='cadastro1'),
    path('cadastro2/', views.cadastro2, name='cadastro2'),
    path('criar-conta/', views.criar_conta, name='criar_conta'),
    path('cadastro/professor/<int:user_id>/', views.cadastro_professor_parte2, name='cadastro_professor_parte2'),

    # ========== FLUXO DE REDEFINIÇÃO DE SENHA (Novo) ==========
    # 1. Solicita o email do usuário
    path('reset_senha/', auth_views.PasswordResetView.as_view(
        template_name='esqueci_senha.html', 
        form_class=CustomPasswordResetForm,  
        email_template_name='reset_senha/password_reset_email.html',
        subject_template_name='reset_senha/password_reset_subject.txt',
        success_url='/reset_senha/enviado/' 
    ), name='password_reset'),
    
    # 2. Informa que o email foi enviado
    path('reset_senha/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='reset_senha/password_reset_done.html' # AGORA EXISTE
    ), name='password_reset_done'),

    # 3. Link de redefinição no email
    path('reset_senha/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='reset_senha/password_reset_confirm.html', # AGORA EXISTE
        success_url='/reset_senha/completo/'
    ), name='password_reset_confirm'),

    # 4. Confirmação final
    path('reset_senha/completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset_senha/password_reset_complete.html' # AGORA EXISTE
    ), name='password_reset_complete'),
    
    # ========== PERFIL ==========
    path('perfil-aluno/', views.perfil_aluno, name='perfil_aluno'),
    path('perfil-aluno-parte2/', views.perfil_aluno_parte2, name='perfil_aluno_parte2'),
    path('perfil/upload_avatar/', views.upload_avatar, name='upload_avatar'),

    # ========== OPORTUNIDADES ==========
    path('criar-oportunidade/', views.criar_oportunidade, name='criar_oportunidade'), 
    path('oportunidade/<int:id>/', views.detalhe_oportunidade, name='detalhe_oportunidade'),
    path('oportunidades/salvas/', views.oportunidades_salvas, name='oportunidades_salvas'),
    path('oportunidades/remover/<int:id>/', views.remover_salva, name='remover_salva'),
    path('oportunidade/favoritar/<int:id>/', views.favoritar_oportunidade, name='favoritar_oportunidade'),
    
    # ========== SISTEMA DE CHAT ==========
    path('chat/', views.ChatView.as_view(), name='chat'),
    path('chat/enviar/', views.EnviarMensagemView.as_view(), name='enviar_mensagem'),
    path('chat/usuarios/', views.ListarUsuariosView.as_view(), name='usuarios_chat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)