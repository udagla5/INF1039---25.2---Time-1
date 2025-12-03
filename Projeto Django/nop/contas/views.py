from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, TemplateView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q, Max
from django.http import JsonResponse
from django.urls import reverse_lazy

# Ajuste suas importações de forms conforme o nome real do seu arquivo forms.py
from .forms import OportunidadeForm, CustomLoginForm, InteressesForm, EditarPerfilForm, UsuarioForm, MensagemForm, ProfessorCadastroFormParte2
from .models import Oportunidade, Usuario, Mensagem, Favorito, Notificacao

# ===============================
# PÁGINAS PRINCIPAIS E AUTENTICAÇÃO
# ===============================

def home(request):
    # Busca 3 oportunidades aleatórias do banco de dados
    destaques = Oportunidade.objects.all().order_by('?')[:3]
    
    return render(request, 'home.html', {'destaques': destaques})

def cadastro1(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            tipo = form.cleaned_data.get('tipo')
            messages.success(request, 'Primeira etapa concluída! Continue o cadastro.')
            
            if tipo == 'PROFESSOR':
                return redirect('cadastro_professor_parte2', user_id=usuario.id)
            elif tipo in ['ALUNO', 'ALUNO_EXTERNO']:
                messages.warning(request, 'O cadastro completo para Alunos está em desenvolvimento. Faça login com sua nova conta.')
                # CORREÇÃO: Usando 'login' para corresponder a urls.py
                return redirect('login') 
            else:
                return redirect('home')
    else:
        form = UsuarioForm()
    return render(request, 'cadastro1.html', {'form': form})

def cadastro_professor_parte2(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if usuario.tipo != 'PROFESSOR':
        messages.error(request, "Acesso não autorizado para o seu tipo de conta.")
        return redirect('home')
        
    if request.method == 'POST':
        form = ProfessorCadastroFormParte2(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro de Professor concluído! Por favor, faça login.')
            # CORREÇÃO: Usando 'login' para corresponder a urls.py
            return redirect('login') 
    else:
        form = ProfessorCadastroFormParte2(instance=usuario)

    return render(request, 'cadastro3.html', {'form': form, 'usuario': usuario})

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
                
                # --- ALTERAÇÃO AQUI ---
                # Verifica se existe um parâmetro 'next' na URL (ex: veio do carrossel)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url) # Redireciona para a oportunidade
                # ----------------------
                
                return redirect('feed') # Comportamento padrão (vai pro feed)
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')

# ===============================
# PERFIL E EDIÇÃO
# ===============================

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
def upload_avatar(request):
    if request.method == 'POST':
        if 'avatar' in request.FILES:
            novo_avatar = request.FILES['avatar']
            try:
                profile = request.user.profile # Verifique se seu modelo usa profile ou user direto
                profile.avatar = novo_avatar
                profile.save()
                messages.success(request, 'Foto de perfil atualizada com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao salvar a imagem: {e}')
    return redirect('perfil_aluno')

# ===============================
# OPORTUNIDADES (CRUD e Detalhes)
# ===============================

@login_required(login_url='login') # <--- CORREÇÃO: login_url é 'login'
def detalhe_oportunidade(request, id):
    oportunidade = get_object_or_404(Oportunidade, pk=id)
    return render(request, 'oportunidade.html', {'oportunidade': oportunidade})

@login_required
def criar_oportunidade(request):
    # SEGURANÇA: Só professor pode criar
    if request.user.tipo != 'PROFESSOR':
        messages.error(request, 'Apenas professores podem criar oportunidades.')
        return redirect('feed')

    if request.method == 'POST':
        # ALTERAÇÃO AQUI: Adicionado request.FILES para processar a imagem
        form = OportunidadeForm(request.POST, request.FILES)
        if form.is_valid():
            oportunidade = form.save(commit=False)
            oportunidade.criador = request.user
            oportunidade.save()
            messages.success(request, 'Oportunidade criada com sucesso!')
            return redirect('feed') 
    else:
        form = OportunidadeForm()
    return render(request, 'criar_oportunidade.html', {'form': form})

# View baseada em classe 
class CriarOportunidadeView(LoginRequiredMixin, FormView):
    template_name = 'criar_oportunidade.html'
    form_class = OportunidadeForm
    login_url = 'login' # <--- CORREÇÃO: login_url é 'login'
    
    def form_valid(self, form):
        oportunidade = form.save(commit=False)
        oportunidade.criador = self.request.user
        oportunidade.status = 'PENDENTE'
        oportunidade.save()
        messages.success(self.request, 'Oportunidade criada com sucesso! Aguarde a validação do sistema.')
        return redirect('feed')

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

# ===============================
# FEED PRINCIPAL
# ===============================

@login_required
def lista_oportunidades(request):
    # 1. Busca inicial ordenada por data de publicação
    oportunidades = Oportunidade.objects.all().order_by('-data_publicacao')

    # 2. Filtro de Texto
    busca = request.GET.get('busca')
    if busca:
        oportunidades = oportunidades.filter(
            Q(titulo__icontains=busca) | Q(descricao__icontains=busca)
        )

    # 3. Filtro por Tipo (Checkbox)
    tipos = request.GET.getlist('tipo')
    if tipos:
        oportunidades = oportunidades.filter(tipo__in=tipos)

    # 4. Filtro por Remuneração (Slider Intervalo)
    min_rem = request.GET.get('min_remuneracao')
    max_rem = request.GET.get('max_remuneracao')

    if min_rem and min_rem != '':
        try:
            oportunidades = oportunidades.filter(remuneracao__gte=int(min_rem))
        except ValueError:
            pass
            
    if max_rem and max_rem != '':
        try:
            oportunidades = oportunidades.filter(remuneracao__lte=int(max_rem))
        except ValueError:
            pass

    # 5. Filtro por Horas Complementares (Slider Intervalo)
    min_horas = request.GET.get('min_horas')
    max_horas = request.GET.get('max_horas')

    if min_horas and min_horas != '':
        try:
            oportunidades = oportunidades.filter(horas_complementares__gte=int(min_horas))
        except ValueError:
            pass

    if max_horas and max_horas != '':
        try:
            oportunidades = oportunidades.filter(horas_complementares__lte=int(max_horas))
        except ValueError:
            pass

    # 6. Outros filtros
    cargas = request.GET.getlist('carga_horaria_check')
    # Lógica de carga horária se houver...
    
    interesses = request.GET.get('interesses')
    # Lógica de interesses se houver...

    # 7. Contexto
    context = {
        'oportunidades': oportunidades,
        'favoritos_ids': Favorito.objects.filter(usuario=request.user).values_list('oportunidade_id', flat=True) if request.user.is_authenticated else [],
        'filtros_selecionados': {
            'tipos': tipos,
            'cargas': cargas,
            'interesses': interesses,
            'min_remuneracao': min_rem if min_rem else '0',
            'max_remuneracao': max_rem if max_rem else '5000',
            'min_horas': min_horas if min_horas else '0',
            'max_horas': max_horas if max_horas else '200',
        }
    }
    
    return render(request, 'feed.html', context)

# ===============================
# SISTEMA DE CHAT
# ===============================

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'
    login_url = 'login' # <--- CORREÇÃO: login_url é 'login'
    
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
                pass
        return context

class EnviarMensagemView(LoginRequiredMixin, TemplateView):
    login_url = 'login' # <--- CORREÇÃO: login_url é 'login'
    
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
        return JsonResponse({'success': False, 'errors': form.errors})
    
class ListarUsuariosView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios_chat.html'
    context_object_name = 'usuarios'
    login_url = 'login' # <--- CORREÇÃO: login_url é 'login'
    
    def get_queryset(self):
        return Usuario.objects.exclude(id=self.request.user.id).order_by('username')
    
# notificacoes

def notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user)
    return render(request, 'notificacoes.html', {"notificacoes": notificacoes})