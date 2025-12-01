# contas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, TemplateView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q, Max
from django.http import JsonResponse
from .forms import OportunidadeForm, CustomLoginForm, InteressesForm, EditarPerfilForm, UsuarioForm, MensagemForm
from .models import Oportunidade, Usuario, Mensagem, Favorito

# ... (Todo o código anterior de Login, Cadastro, Chat, etc permanece igual até a lista_oportunidades) ...

def detalhe_oportunidade(request, id):
    oportunidade = get_object_or_404(Oportunidade, pk=id)
    return render(request, 'oportunidade.html', {'oportunidade': oportunidade})

def home(request):
    return render(request, 'home.html')

class FeedView(LoginRequiredMixin, ListView):
    model = Oportunidade
    template_name = 'feed.html'
    context_object_name = 'oportunidades'
    paginate_by = 12
    login_url = 'login'
    redirect_field_name = 'redirect_to'

def cadastro1(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('cadastro2')
    else:
        form = UsuarioForm()
    return render(request, 'cadastro1.html', {'form': form})

@login_required
def cadastro2(request):
    if request.method == 'POST':
        form = InteressesForm(request.POST)
        if form.is_valid():
            interesses = form.cleaned_data.get('interesses', [])
            if interesses:
                request.user.interesses.set(interesses)
            messages.success(request, 'Interesses salvos com sucesso!')
            return redirect('feed')
    else:
        form = InteressesForm()
    return render(request, 'cadastro2.html', {'form': form})

def criar_conta(request):
    return redirect('cadastro1')

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

@login_required
def criar_oportunidade(request):
    if request.method == 'POST':
        form = OportunidadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed') 
    else:
        form = OportunidadeForm()
    return render(request, 'criar_oportunidade.html', {'form': form})

class CriarOportunidadeView(LoginRequiredMixin, FormView):
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

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        conversas = Usuario.objects.filter(
            Q(mensagens_enviadas__destinatario=user) | 
            Q(mensagens_recebidas__remetente=user)
        ).distinct().annotate(
            ultima_mensagem_data=Max('mensagens_enviadas__data_envio')
        ).order_by('-ultima_mensagem_data')
        
        context['conversas'] = conversas
        context['form_mensagem'] = MensagemForm()
        
        conversa_com = self.request.GET.get('conversa_com')
        if conversa_com:
            try:
                destinatario = Usuario.objects.get(id=conversa_com)
                context['destinatario'] = destinatario
                mensagens = Mensagem.objects.filter(
                    Q(remetente=user, destinatario=destinatario) |
                    Q(remetente=destinatario, destinatario=user)
                ).order_by('data_envio')
                context['mensagens'] = mensagens
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
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        form = MensagemForm(request.POST)
        destinatario_id = request.POST.get('destinatario_id')
        if form.is_valid() and destinatario_id:
            try:
                destinatario = Usuario.objects.get(id=destinatario_id)
                mensagem = form.save(commit=False)
                mensagem.remetente = request.user
                mensagem.destinatario = destinatario
                mensagem.save()
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
                return JsonResponse({'success': False, 'error': 'Destinatário não encontrado'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        
    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'error': 'Método não permitido'})

class ListarUsuariosView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios_chat.html'
    context_object_name = 'usuarios'
    login_url = 'login'
    
    def get_queryset(self):
        return Usuario.objects.exclude(id=self.request.user.id).order_by('username')

@login_required
def upload_avatar(request):
    if request.method == 'POST':
        if 'avatar' in request.FILES:
            novo_avatar = request.FILES['avatar']
            try:
                profile = request.user.profile
                profile.avatar = novo_avatar
                profile.save()
                messages.success(request, 'Foto de perfil atualizada com sucesso!')
            except AttributeError:
                messages.error(request, 'Erro: O modelo de perfil não pôde ser encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao salvar a imagem: {e}')
        return redirect('perfil_aluno')
    return redirect('perfil_aluno')

@login_required
def oportunidades_salvas(request):
    oportunidades = Favorito.objects.filter(usuario=request.user)
    return render(request, 'oportunidades_salvas.html', {
        'oportunidades': [f.oportunidade for f in oportunidades]
    })

@login_required
def remover_salva(request, id):
    Favorito.objects.filter(usuario=request.user, oportunidade_id=id).delete()
    messages.info(request, 'Oportunidade removida dos seus favoritos.')
    return redirect('oportunidades_salvas')

@login_required
def favoritar_oportunidade(request, id):
    oportunidade = get_object_or_404(Oportunidade, pk=id)
    Favorito.objects.get_or_create(usuario=request.user, oportunidade=oportunidade) 
    messages.success(request, 'Oportunidade salva com sucesso! 🎉')
    return redirect('oportunidades_salvas')

# ========================================================
# FUNÇÃO LISTA OPORTUNIDADES (FEED COM FILTROS FUNCIONAIS)
# ========================================================
def lista_oportunidades(request):
    # 1. Busca TODAS as oportunidades inicialmente
    oportunidades = Oportunidade.objects.all().order_by('-data_criacao')

    # 2. Filtro de Texto (Barra de pesquisa do header)
    busca = request.GET.get('busca')
    if busca:
        oportunidades = oportunidades.filter(
            Q(titulo__icontains=busca) | Q(descricao__icontains=busca)
        )

    # 3. Filtro por TIPO (Checkbox)
    # O request.GET.getlist pega todos os marcados (ex: ['EST', 'MON'])
    tipos = request.GET.getlist('tipo')
    if tipos:
        oportunidades = oportunidades.filter(tipo__in=tipos)

    # 4. Filtro por REMUNERAÇÃO (Intervalo Min e Max)
    # Os inputs no HTML se chamam 'min_remuneracao' e 'max_remuneracao'
    min_rem = request.GET.get('min_remuneracao')
    max_rem = request.GET.get('max_remuneracao')

    # Convertendo para Inteiro para filtrar no Banco
    if min_rem:
        try:
            oportunidades = oportunidades.filter(remuneracao__gte=int(min_rem))
        except ValueError:
            pass # Ignora se não for número
            
    if max_rem:
        try:
            oportunidades = oportunidades.filter(remuneracao__lte=int(max_rem))
        except ValueError:
            pass

    # 5. Filtro por HORAS COMPLEMENTARES (Intervalo Min e Max)
    min_horas = request.GET.get('min_horas')
    max_horas = request.GET.get('max_horas')

    if min_horas:
        try:
            oportunidades = oportunidades.filter(horas_complementares__gte=int(min_horas))
        except ValueError:
            pass

    if max_horas:
        try:
            oportunidades = oportunidades.filter(horas_complementares__lte=int(max_horas))
        except ValueError:
            pass

    # 6. Filtros Extras (Carga Horária e Interesses)
    # Como Carga Horária é CharField no seu model, filtro exato é difícil, 
    # mas mantemos o estado visual para o usuário não achar que sumiu.
    cargas = request.GET.getlist('carga_horaria_check')
    interesses = request.GET.get('interesses')

    # Contexto enviado para o HTML
    context = {
        'oportunidades': oportunidades,
        # IDs dos favoritos para pintar o coraçãozinho
        'favoritos_ids': Favorito.objects.filter(usuario=request.user).values_list('oportunidade_id', flat=True) if request.user.is_authenticated else [],
        
        # DADOS PARA O FORMULÁRIO (Isso faz o filtro "lembrar" o que você escolheu)
        'filtros_selecionados': {
            'tipos': tipos,
            'cargas': cargas,
            'interesses': interesses,
            'min_remuneracao': min_rem,
            'max_remuneracao': max_rem,
            'min_horas': min_horas,
            'max_horas': max_horas,
        }
    }
    
    return render(request, 'feed.html', context)