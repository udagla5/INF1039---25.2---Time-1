from django.shortcuts import render

# Create your views here.
def cadastro1(request):
    return render(request, 'cadastro1.html')

def cadastro2(request):
    return render(request, 'cadastro2.html')

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def perfil_aluno(request):
    return render(request, 'perfil_aluno.html')

def perfil_aluno_parte2(request):
    return render(request, 'perfil_aluno_parte2.html')

def feed(request):
    return render(request, 'feed.html')

def criar_oportunidade1(request):
    return render(request, 'criar_oportunidade1.html')

def criar_oportunidade2(request):
    return render(request, 'criar_oportunidade2.html')

def criar_oportunidade3(request):
    return render(request, 'criar_oportunidade3.html')