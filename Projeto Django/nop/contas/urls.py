from django.urls import path
from . import views

# URLs para os HTMLs existentes
urlpatterns = [
    # home.html
    path('', views.HomeView.as_view(), name='home'),
    
    # cadastro1.html e cadastro2.html (RF1, RF2, RF3)
    path('cadastro1/', views.CadastroEtapa1View.as_view(), name='cadastro1'),
    path('cadastro2/', views.CadastroEtapa2View.as_view(), name='cadastro2'),
    
    # login.html e login1.html
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # feed.html (RF4, RF5, RF11)
    path('feed/', views.FeedView.as_view(), name='feed'),
    
    # criar_oportunidade1.html, criar_oportunidade2.html, criar_oportunidade3.html (RF6)
    path('criar-oportunidade/etapa1/', views.CriarOportunidadeEtapa1View.as_view(), name='criar_oportunidade1'),
    path('criar-oportunidade/etapa2/', views.CriarOportunidadeEtapa2View.as_view(), name='criar_oportunidade2'),
    path('criar-oportunidade/etapa3/', views.CriarOportunidadeEtapa3View.as_view(), name='criar_oportunidade3'),
    
    # perfil_aluno.html e perfil_aluno_parte2.html (RF9, RF13, RF17)
    path('perfil-aluno/', views.PerfilAlunoView.as_view(), name='perfil_aluno'),
    path('perfil-aluno-parte2/', views.PerfilAlunoParte2View.as_view(), name='perfil_aluno_parte2'),
]
