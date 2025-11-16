from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login1(request):
    return render(request, 'login1.html')

def cadastro1(request):
    return render(request, 'cadastro1.html')

def cadastro2(request):
    return render(request, 'cadastro2.html')

def criar_oportunidade1(request):
    return render(request, 'criar_oportunidade1.html')

def criar_oportunidade3(request):
    return render(request, 'criar_oportunidade3.html')

def feed(request):
    return render(request, 'feed.html')

def perfil_aluno(request):
    return render(request, 'perfil_aluno.html')

def perfil_aluno_parte2(request):
    return render(request, 'perfil_aluno_parte2.html')
