from django.urls import path
from . import views
urlpatterns = [
    path('cadastro1/', views.cadastro1, name='cadastro1'),
    path('cadastro2/', views.cadastro2, name='cadastro2'),
]
