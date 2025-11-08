from django.urls import path
from . import views
urlpatterns = [
    path('cadastro1/', views.cadastro1, name='cadastro1'),
    path('cadastro2/', views.cadastro2, name='cadastro2'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('perfil_aluno/', views.perfil_aluno, name='perfil_aluno'),
    path('perfil_aluno_parte2/', views.perfil_aluno_parte2, name='perfil_aluno_parte2'),
    path('feed/', views.feed, name='feed'),
    path('criar_oportunidade1/', views.criar_oportunidade1, name='criar_oportunidade1'),
    path('criar_oportunidade2/', views.criar_oportunidade2, name='criar_oportunidade2'),
    path('criar_oportunidade3/', views.criar_oportunidade3, name='criar_oportunidade3'),
]
