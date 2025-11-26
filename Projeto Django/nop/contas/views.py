# contas/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView, ListView
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import OportunidadeForm, CustomLoginForm, InteressesForm, EditarPerfilForm, UsuarioForm
from .models import Oportunidade, Usuario
from django.contrib.auth.models import User

# ========== AUTENTICAÇÃO ==========
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Usuario  # Importa o seu modelo Usuario personalizado

# ========== PÁGINAS PRINCIPAIS ==========
def home(request):
    return render(request, 'home.html')

class FeedView(LoginRequiredMixin, ListView):
    model = Oportunidade
    template_name = 'feed.html'
    context_object_name = 'oportunidades'
    paginate_by = 12
    login_url = 'login'  # aqui define para onde redireciona
    redirect_field_name = 'redirect_to'


def cadastro1(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Criar o usuário sem salvar ainda (commit=False)
            usuario = form.save(commit=False)
            
            # Criptografar a senha
            usuario.set_password(form.cleaned_data['password1'])
            
            # Salvar o usuário
            usuario.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')  # Direcionar para a página de login ou outra
    else:
        form = UsuarioForm()

    return render(request, 'cadastro1.html', {'form': form})

def cadastro2(request):
    if request.method == 'POST':
        form = InteressesForm(request.POST)
        if form.is_valid():
            # Processar interesses selecionados
            interesses = form.cleaned_data.get('interesses', [])
            # Aqui você pode salvar os interesses no perfil do usuário
            messages.success(request, 'Interesses salvos com sucesso!')
            return redirect('feed')
    else:
        form = InteressesForm()
    return render(request, 'cadastro2.html', {'form': form})

def criar_conta(request):
    return redirect('cadastro1')  # Redireciona para cadastro1

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('feed')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

# ========== PERFIL ==========
@login_required
def perfil_aluno(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil_aluno')
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'perfil_aluno.html', {'form': form})

@login_required
def perfil_aluno_parte2(request):
    return render(request, 'perfil_aluno_parte2.html')

# ========== OPORTUNIDADES ==========
@login_required
def criar_oportunidade(request):
    if request.method == 'POST':
        form = OportunidadeForm(request.POST)
        
        if form.is_valid():
            # Salva o novo objeto Oportunidade no banco de dados
            form.save()
            
            # ⚠️ Substitua 'lista_oportunidades' pelo nome da URL de destino no seu urls.py
            return redirect('lista_oportunidades') 
    
    else:
        form = OportunidadeForm()
    
    # Passa o objeto 'form' para o template
    return render(request, 'criar_oportunidade.html', {'form': form})

# Versão com Class-Based View (alternativa)
class CriarOportunidadeView(LoginRequiredMixin, FormView):
    """RF6 - Criar oportunidade em um único passo (criar_oportunidade.html)"""
    template_name = 'criar_oportunidade.html'
    form_class = OportunidadeForm
    login_url = 'login'
    
    def form_valid(self, form):
        oportunidade = form.save(commit=False)
        oportunidade.criador = self.request.user
        oportunidade.status = 'PENDENTE'
        oportunidade.save()
        messages.success(self.request, 'Oportunidade criada com sucesso! Aguarde a validação do sistema.')
        return redirect('feed')

# ========== OUTRAS PÁGINAS ==========
def chat(request):
    return render(request, 'chat.html')

def lista_oportunidades(request):
    # Obtém todas as oportunidades do banco de dados (ordenadas pela mais recente)
    oportunidades = Oportunidade.objects.all().order_by('-data_publicacao')
    
    # Renderiza um template chamado 'lista_oportunidades.html'
    return render(request, 'lista_oportunidades.html', {'oportunidades': oportunidades})