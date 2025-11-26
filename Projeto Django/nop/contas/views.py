# contas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, TemplateView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q, Max
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import OportunidadeForm, CustomLoginForm, InteressesForm, EditarPerfilForm, UsuarioForm, MensagemForm
from .models import Oportunidade, Usuario, Mensagem
from django.shortcuts import render, get_object_or_404
from .models import Oportunidade

def detalhe_oportunidade(request, id):
    # Busca a oportunidade pelo ID ou retorna erro 404 se não existir
    oportunidade = get_object_or_404(Oportunidade, pk=id)
    return render(request, 'oportunidade.html', {'oportunidade': oportunidade})

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
            # O método save() do form já cuida da criptografia da senha
            usuario = form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('cadastro2')  # Ir para etapa 2 (interesses)
    else:
        form = UsuarioForm()

    return render(request, 'cadastro1.html', {'form': form})

@login_required
def cadastro2(request):
    if request.method == 'POST':
        form = InteressesForm(request.POST)
        if form.is_valid():
            # Processar interesses selecionados
            interesses = form.cleaned_data.get('interesses', [])
            if interesses:
                # Salvar os interesses no perfil do usuário
                request.user.interesses.set(interesses)
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

def custom_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')

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

# ========== SISTEMA DE CHAT (RF14) ==========

class ChatView(LoginRequiredMixin, TemplateView):
    """RF14 - Sistema de chat/mensagens integrado com banco de dados"""
    template_name = 'chat.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Buscar todas as conversas do usuário (com últimas mensagens)
        conversas = Usuario.objects.filter(
            Q(mensagens_enviadas__destinatario=user) | 
            Q(mensagens_recebidas__remetente=user)
        ).distinct().annotate(
            ultima_mensagem_data=Max('mensagens_enviadas__data_envio')
        ).order_by('-ultima_mensagem_data')
        
        context['conversas'] = conversas
        context['form_mensagem'] = MensagemForm()
        
        # Se há um usuário selecionado na conversa
        conversa_com = self.request.GET.get('conversa_com')
        if conversa_com:
            try:
                destinatario = Usuario.objects.get(id=conversa_com)
                context['destinatario'] = destinatario
                
                # Buscar mensagens entre os dois usuários
                mensagens = Mensagem.objects.filter(
                    Q(remetente=user, destinatario=destinatario) |
                    Q(remetente=destinatario, destinatario=user)
                ).order_by('data_envio')
                
                context['mensagens'] = mensagens
                
                # Marcar mensagens como lidas
                Mensagem.objects.filter(
                    remetente=destinatario, 
                    destinatario=user, 
                    lida=False
                ).update(lida=True)
                
            except Usuario.DoesNotExist:
                context['destinatario'] = None
                context['mensagens'] = []
        
        return context

class EnviarMensagemView(LoginRequiredMixin, TemplateView):
    """Class-based view para enviar mensagens via AJAX"""
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        form = MensagemForm(request.POST)
        destinatario_id = request.POST.get('destinatario_id')
        
        if form.is_valid() and destinatario_id:
            try:
                destinatario = Usuario.objects.get(id=destinatario_id)
                
                # Criar a mensagem
                mensagem = form.save(commit=False)
                mensagem.remetente = request.user
                mensagem.destinatario = destinatario
                mensagem.save()
                
                # Retornar resposta JSON para AJAX
                return JsonResponse({
                    'success': True,
                    'mensagem': {
                        'id': mensagem.id,
                        'conteudo': mensagem.conteudo,
                        'remetente': mensagem.remetente.username,
                        'data_envio': mensagem.data_envio.strftime('%H:%M')
                    }
                })
                
            except Usuario.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Destinatário não encontrado'
                })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'error': 'Método não permitido'})

class ListarUsuariosView(LoginRequiredMixin, ListView):
    """View para listar usuários disponíveis para conversa"""
    model = Usuario
    template_name = 'usuarios_chat.html'
    context_object_name = 'usuarios'
    login_url = 'login'
    
    def get_queryset(self):
        # Excluir o próprio usuário da lista
        return Usuario.objects.exclude(id=self.request.user.id).order_by('username')

def lista_oportunidades(request):
    # Obtém todas as oportunidades do banco de dados (ordenadas pela mais recente)
    oportunidades = Oportunidade.objects.all().order_by('-data_criacao')
    
    # Renderiza o template feed.html que já existe
    return render(request, 'feed.html', {'oportunidades': oportunidades})

@login_required
def upload_avatar(request):
    if request.method == 'POST':
        # 1. Tenta obter o arquivo enviado
        if 'avatar' in request.FILES:
            novo_avatar = request.FILES['avatar']
            
            # 2. Salva o avatar no modelo do usuário
            # (A lógica exata depende do seu modelo de Usuário/Perfil)
            try:
                # Exemplo, assumindo que o campo 'avatar' está no Profile
                profile = request.user.profile
                profile.avatar = novo_avatar
                profile.save()
                
                messages.success(request, 'Foto de perfil atualizada com sucesso!')
            
            except AttributeError:
                messages.error(request, 'Erro: O modelo de perfil não pôde ser encontrado.')
            
            except Exception as e:
                # Trata erros de validação ou outros erros de upload
                messages.error(request, f'Erro ao salvar a imagem: {e}')
        
        # 3. Redireciona de volta para a página de edição de perfil
        return redirect('perfil_aluno') 

    # Se alguém acessar diretamente via GET, redireciona ou retorna erro
    return redirect('perfil_aluno')