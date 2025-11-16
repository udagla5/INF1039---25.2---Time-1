from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login  # necessario para login

# Views de cadastro e home
def cadastro1(request):
    return render(request, 'cadastro1.html')

def cadastro2(request):
    return render(request, 'cadastro2.html')

def home(request):
    return render(request, 'home.html')

# View de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            next_url = request.POST.get('next') or '/feed'
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

# Views protegidas por login
@login_required
def perfil_aluno(request):
    return render(request, 'perfil_aluno.html')

@login_required
def perfil_aluno_parte2(request):
    return render(request, 'perfil_aluno_parte2.html')

# Outras 
def feed(request):
    return render(request, 'feed.html')

def criar_oportunidade1(request):
    return render(request, 'criar_oportunidade1.html')

def criar_oportunidade2(request):
    return render(request, 'criar_oportunidade2.html')

def criar_oportunidade3(request):
    return render(request, 'criar_oportunidade3.html')
