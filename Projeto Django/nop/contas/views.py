# contas/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UsuarioCreationForm, OportunidadeForm, CustomLoginForm, InteressesForm, EditarPerfilForm
from .models import Oportunidade

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



# ========== AUTENTICAÇÃO ==========
def cadastro1(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('cadastro2')
    else:
        form = UsuarioCreationForm()
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
def criar_oportunidade1(request):
    if request.method == 'POST':
        form = OportunidadeForm(request.POST)
        if form.is_valid():
            oportunidade = form.save(commit=False)
            oportunidade.criador = request.user
            oportunidade.status = 'PENDENTE'
            oportunidade.save()
            messages.success(request, 'Oportunidade criada com sucesso! Aguarde a validação do sistema.')
            return redirect('feed')
    else:
        form = OportunidadeForm()
    return render(request, 'criar_oportunidade1.html', {'form': form})

# Versão com Class-Based View (alternativa)
class CriarOportunidadeView(LoginRequiredMixin, FormView):
    """RF6 - Criar oportunidade em um único passo (criar_oportunidade1.html)"""
    template_name = 'criar_oportunidade1.html'
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