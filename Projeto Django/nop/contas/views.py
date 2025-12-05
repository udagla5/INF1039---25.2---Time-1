from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, TemplateView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q, Max
from django.http import JsonResponse
from django.urls import reverse_lazy

# Importações dos seus modelos e forms
from .forms import (
    OportunidadeForm, CustomLoginForm, InteressesForm, 
    EditarPerfilForm, EditarPerfilProfessorForm, UsuarioForm, 
    MensagemForm, ProfessorCadastroFormParte2, BuscaOportunidadeForm
)
from .models import Oportunidade, Usuario, Mensagem, Favorito, Interesse, Notificacao, Curso

# ===============================
# PÁGINAS PRINCIPAIS E AUTENTICAÇÃO
# ===============================

def home(request):
    destaques = Oportunidade.objects.all().order_by('?')[:3]
    return render(request, 'home.html', {'destaques': destaques})

def cadastro1(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            tipo = form.cleaned_data.get('tipo')
            
            # 🔑 PASSO CRÍTICO: Logar o usuário recém-criado
            password = form.cleaned_data.get('password1')
            user_auth = authenticate(request, username=usuario.username, password=password)

            if user_auth is not None:
                login(request, user_auth)
            
            messages.success(request, 'Primeira etapa concluída! Continue o cadastro.')
            
            if tipo == 'PROFESSOR':
                return redirect('cadastro_professor_parte2', user_id=usuario.id)
            elif tipo in ['ALUNO', 'ALUNO_EXTERNO']:
                # Redirecionar para o cadastro2 agora que o usuário está logado
                return redirect('cadastro2') 
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
            return redirect('login') 
    else:
        form = ProfessorCadastroFormParte2(instance=usuario)

    cursos = Curso.objects.all().order_by('nome')
    
    return render(request, 'cadastro3.html', {
        'form': form, 
        'usuario': usuario,
        'cursos': cursos  # ← ADICIONE ESTE PARÂMETRO
    })


def cadastro2(request):
    # 🔑 CORREÇÃO CRÍTICA: Impedir AnonymousUser de prosseguir
    if not request.user.is_authenticated:
        messages.warning(request, "Você precisa estar logado para selecionar seus interesses.")
        return redirect('login')
    
    # Obtém o usuário REAL do banco de dados (não o request.user simples)
    usuario = Usuario.objects.get(id=request.user.id)
    
    # 🔑 APENAS ALUNOS SELECIONAM INTERESSES
    if usuario.tipo == 'PROFESSOR':
        messages.info(request, 'Professores não precisam selecionar interesses.')
        return redirect('feed')
    
    if request.method == 'POST':
        form = InteressesForm(request.POST)
        if form.is_valid():
            interesses_selecionados = form.cleaned_data.get('interesses')
            if interesses_selecionados:
                # LIMPA os interesses existentes e adiciona os novos
                usuario.interesses.clear()
                for interesse in interesses_selecionados:
                    usuario.interesses.add(interesse)
                
                usuario.save()  # SALVA as alterações
                messages.success(request, 'Interesses salvos com sucesso!')
                return redirect('feed')
            else:
                usuario.interesses.clear()
                usuario.save()
                messages.info(request, 'Nenhum interesse selecionado.')
                return redirect('feed')
    else:
        # Pega os IDs dos interesses atuais do usuário
        interesses_ids = list(usuario.interesses.values_list('id', flat=True))
        form = InteressesForm(initial={'interesses': interesses_ids})
    
    return render(request, 'cadastro2.html', {'form': form})

def criar_conta(request):
    return redirect('cadastro1')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('feed') # Redireciona usuários já logados
        
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a) de volta, {user.username}!')
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url) 
                
            return redirect('feed') 
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = CustomLoginForm()
        
    return render(request, 'login.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')

# ===============================
# PERFIL E EDIÇÃO
# ===============================

@login_required
def perfil_aluno(request):
    # Determina qual formulário usar baseado no tipo de usuário
    if request.user.tipo == 'PROFESSOR':
        FormClass = EditarPerfilProfessorForm
    else:
        FormClass = EditarPerfilForm
    
    if request.method == 'POST':
        form = FormClass(request.POST, instance=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            # Salvar os interesses (Many-to-Many) - APENAS PARA ALUNOS
            if request.user.tipo != 'PROFESSOR':
                form.save_m2m()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil_aluno')
    else:
        form = FormClass(instance=request.user)
    
    # Adiciona informação sobre tipo de usuário ao contexto
    context = {
        'form': form,
        'is_professor': request.user.tipo == 'PROFESSOR'
    }
    return render(request, 'perfil_aluno.html', context)

@login_required
def perfil_aluno_parte2(request):
    return render(request, 'perfil_aluno_parte2.html')

@login_required
def upload_avatar(request):
    if request.method == 'POST':
        # O nome 'avatar' vem do input name="avatar" no seu HTML
        nova_foto = request.FILES.get('avatar')
        
        if nova_foto:
            try:
                user = request.user
                # Se já existir uma foto antiga, o Django substitui ou você pode deletar manualmente se quiser
                user.foto_perfil = nova_foto
                user.save()
                messages.success(request, 'Foto de perfil atualizada com sucesso!')
            except AttributeError:
                pass
            except Exception as e:
                messages.error(request, 'Erro ao salvar a imagem.')
        else:
            messages.warning(request, 'Nenhuma imagem selecionada.')
            
    return redirect('perfil_aluno')

# ===============================
# OPORTUNIDADES (CRUD e Detalhes)
# ===============================

@login_required(login_url='login') 
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
        form = OportunidadeForm(request.POST, request.FILES)
        if form.is_valid():
            # AQUI: O .save(commit=False) não salva relações Many-to-Many
            oportunidade = form.save(commit=False) 
            oportunidade.criador = request.user
            oportunidade.save()
            
            # SALVANDO RELAÇÃO MANY-TO-MANY (Interesses)
            form.save_m2m() # Salva as relações M2M (como related_interests)
            
            # CRIAR NOTIFICAÇÕES para usuários interessados
            notificar_nova_oportunidade(oportunidade)
            
            messages.success(request, 'Oportunidade criada com sucesso!')
            return redirect('feed') 
    else:
        form = OportunidadeForm()
    return render(request, 'criar_oportunidade.html', {'form': form})

# View baseada em classe (manter apenas uma, se possível)
class CriarOportunidadeView(LoginRequiredMixin, FormView):
    template_name = 'criar_oportunidade.html'
    form_class = OportunidadeForm
    login_url = 'login' 
    
    def form_valid(self, form):
        oportunidade = form.save(commit=False)
        oportunidade.criador = self.request.user
        oportunidade.status = 'PENDENTE'
        oportunidade.save()
        
        # SALVANDO RELAÇÃO MANY-TO-MANY (Interesses)
        form.save_m2m() # Salva as relações M2M (como related_interests)
        
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
    favorito, created = Favorito.objects.get_or_create(usuario=request.user, oportunidade=oportunidade)
    
    if created:
        messages.success(request, 'Oportunidade salva com sucesso! 🎉')
    else:
        messages.info(request, 'Você já salvou esta oportunidade.')
    
    return redirect('oportunidades_salvas')

# ===============================
# FEED PRINCIPAL
# ===============================

@login_required
def lista_oportunidades(request):
    # 1. Busca inicial ordenada por data de publicação
    oportunidades = Oportunidade.objects.all().order_by('-data_publicacao')

    # 2. Filtro de Texto (BUSCA) - AGORA MAIS COMPLETO
    busca = request.GET.get('busca')
    
    # 🔑 NOVO: Normalizar o termo de busca para comparar com códigos de tipo
    tipos_mapeados = {
        'MONITORIA': 'MON',
        'ESTAGIO': 'EST',
        'INICIACAO CIENTIFICA': 'IC',
        'TRABALHO MEIO PERIODO': 'TMP',
        'VOLUNTARIADO': 'VOL',
        'PALESTRA': 'PAL',
        'EQUIPE DE COMPETICAO': 'EQC',
        'BOLSA': 'BOL',
        'LABORATORIO DE PESQUISA': 'LP',
        'OUTRO': 'OUT',
        # Adicione mais mapeamentos conforme necessário (em português e sem acento)
    }
    
    tipo_busca_codificado = ''
    if busca:
        # Lógica para normalizar o termo de busca
        busca_upper = busca.upper().replace('ÃO', 'AO').replace('Ç', 'C').replace('Í', 'I').strip()
        
        for nome_completo, codigo in tipos_mapeados.items():
            if busca_upper in nome_completo or codigo in busca_upper:
                tipo_busca_codificado = codigo
                break

        # AQUI ESTÁ O BLOCO DE CORREÇÃO
        query = (
            Q(titulo__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(local__icontains=busca) |
            
            # ✅ CORREÇÃO APLICADA: Assume-se que o modelo Curso tem um campo 'nome'
            Q(cursos_elegiveis__nome__icontains=busca) | 
            
            # Este já estava correto, pois atravessa a relação Many-to-Many 'related_interests' para o campo 'nome' do modelo 'Interesse'
            Q(related_interests__nome__icontains=busca) 
        )
        
        # 🔑 CORREÇÃO: Adicionar filtro por código de tipo se encontrado
        if tipo_busca_codificado:
             query = query | Q(tipo__icontains=tipo_busca_codificado)
        
        # Filtro final (Linha 336 da sua trace original)
        oportunidades = oportunidades.filter(query).distinct()

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

    # 6. Filtro por Carga Horária (Checkbox)
    cargas = request.GET.getlist('carga_horaria_check')
    if cargas:
        # Aqui você precisa implementar a lógica para filtrar por carga horária
        # Vou deixar um placeholder - você precisa adaptar para seu modelo
        # Exemplo básico:
        for carga in cargas:
            if carga == '<2':
                oportunidades = oportunidades.filter(carga_horaria__lt=2)
            elif carga == '>2':
                oportunidades = oportunidades.filter(carga_horaria__gt=2)
            elif carga == '>4':
                oportunidades = oportunidades.filter(carga_horaria__gt=4)
            elif carga == '>6':
                oportunidades = oportunidades.filter(carga_horaria__gt=6)
            elif carga == '>8':
                oportunidades = oportunidades.filter(carga_horaria__gt=8)
            # 'compativel' pode ser uma lógica mais complexa que você precisa definir

    # 7. Filtro por Interesses (Checkbox/Lista)
    interesses_selecionados = request.GET.getlist('interesses') # Pega 'meus', 'tudo' ou IDs
    
    ids_para_filtrar = []

    # Se 'tudo' está presente, IGNORA o filtro por interesses
    if interesses_selecionados and 'tudo' not in interesses_selecionados:
        
        # 7a. Lógica para o checkbox "Meus interesses"
        if 'meus' in interesses_selecionados and request.user.tipo in ['ALUNO', 'ALUNO_EXTERNO']:
            # Pega os IDs dos interesses do usuário
            ids_de_usuario = list(request.user.interesses.values_list('id', flat=True))
            ids_para_filtrar.extend(ids_de_usuario)

        # 7b. Adiciona quaisquer outros IDs de interesse selecionados (que não são 'meus' ou 'tudo')
        for id_str in interesses_selecionados:
            try:
                # Se for um ID de interesse (inteiro)
                ids_para_filtrar.append(int(id_str))
            except ValueError:
                # Ignora valores não numéricos, como 'meus' ou 'tudo'
                continue  

        # Filtra oportunidades que possuam QUALQUER UM dos interesses selecionados
        if ids_para_filtrar:
            oportunidades = oportunidades.filter(related_interests__id__in=ids_para_filtrar).distinct()

    # 8. Contexto
    context = {
        'oportunidades': oportunidades,
        'todos_interesses': Interesse.objects.all().order_by('nome'), # Envia para o template para montar os filtros
        'favoritos_ids': Favorito.objects.filter(usuario=request.user).values_list('oportunidade_id', flat=True) if request.user.is_authenticated else [],
        'filtros_selecionados': {
            'tipos': tipos,
            'interesses': interesses_selecionados, # Strings: ['meus', '2', '3']
            'min_remuneracao': min_rem if min_rem else '0',
            'max_remuneracao': max_rem if max_rem else '5000',
            'min_horas': min_horas if min_horas else '0',
            'max_horas': max_horas if max_horas else '200',
            'cargas': cargas,
            'busca': busca,  # ADICIONE ISSO PARA MANTER O TERMO NA BARRA
        }
    }
    
    return render(request, 'feed.html', context)

# ===============================
# SISTEMA DE CHAT
# ===============================

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
                pass
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
                
                # CRIAR NOTIFICAÇÃO para o destinatário
                notificar_nova_mensagem(request.user, destinatario)
                
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
    login_url = 'login' 
    
    def get_queryset(self):
        return Usuario.objects.exclude(id=self.request.user.id).order_by('username')

# ===============================
# SISTEMA DE NOTIFICAÇÕES
# ===============================

@login_required
def notificacoes(request):
    """Exibe todas as notificações do usuário"""
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-data')
    
    # Conta notificações não lidas
    nao_lidas = notificacoes.filter(lida=False).count()
    
    context = {
        'notificacoes': notificacoes,
        'nao_lidas': nao_lidas,
    }
    return render(request, 'notificacoes.html', context)

@login_required
def marcar_notificacao_lida(request, id):
    """Marca uma notificação como lida"""
    notificacao = get_object_or_404(Notificacao, id=id, usuario=request.user)
    notificacao.lida = True
    notificacao.save()
    return JsonResponse({'success': True})

@login_required
def marcar_todas_lidas(request):
    """Marca todas as notificações como lidas"""
    Notificacao.objects.filter(usuario=request.user, lida=False).update(lida=True)
    messages.success(request, 'Todas as notificações foram marcadas como lidas.')
    return redirect('notificacoes')

@login_required
def deletar_notificacao(request, id):
    """Deleta uma notificação"""
    notificacao = get_object_or_404(Notificacao, id=id, usuario=request.user)
    notificacao.delete()
    messages.success(request, 'Notificação removida.')
    return redirect('notificacoes')

@login_required
def limpar_notificacoes(request):
    """Remove todas as notificações lidas"""
    Notificacao.objects.filter(usuario=request.user, lida=True).delete()
    messages.success(request, 'Notificações lidas foram removidas.')
    return redirect('notificacoes')

# ===============================
# FUNÇÕES AUXILIARES PARA CRIAR NOTIFICAÇÕES
# ===============================

def criar_notificacao(usuario, mensagem, tipo='info'):
    """
    Cria uma notificação para um usuário
    Tipos: 'info', 'success', 'warning', 'error'
    """
    Notificacao.objects.create(
        usuario=usuario,
        mensagem=mensagem
    )

def notificar_nova_oportunidade(oportunidade):
    """Notifica alunos interessados sobre nova oportunidade"""
    # Encontra alunos com interesses relacionados
    interesses_oportunidade = oportunidade.related_interests.all()
    
    if interesses_oportunidade.exists():
        # Busca usuários que têm esses interesses
        usuarios_interessados = Usuario.objects.filter(
            interesses__in=interesses_oportunidade,
            tipo__in=['ALUNO', 'ALUNO_EXTERNO']
        ).exclude(id=oportunidade.criador.id).distinct()
        
        for usuario in usuarios_interessados:
            mensagem = f"Nova oportunidade de {oportunidade.get_tipo_display()}: {oportunidade.titulo}"
            criar_notificacao(usuario, mensagem)

def notificar_favorito_atualizado(oportunidade, tipo_atualizacao):
    """Notifica usuários que favoritaram uma oportunidade sobre atualizações"""
    usuarios_favoritos = Usuario.objects.filter(
        favorito__oportunidade=oportunidade
    ).distinct()
    
    mensagens = {
        'editada': f'A oportunidade "{oportunidade.titulo}" que você salvou foi atualizada.',
        'encerrada': f'A oportunidade "{oportunidade.titulo}" foi encerrada.',
        'vagas': f'Novas vagas disponíveis em "{oportunidade.titulo}"!',
    }
    
    mensagem = mensagens.get(tipo_atualizacao, f'Atualização em "{oportunidade.titulo}"')
    
    for usuario in usuarios_favoritos:
        criar_notificacao(usuario, mensagem)

def notificar_nova_mensagem(remetente, destinatario):
    """Notifica sobre nova mensagem recebida"""
    mensagem = f"Você recebeu uma nova mensagem de {remetente.username}"
    criar_notificacao(destinatario, mensagem)


@login_required
def busca_oportunidades_ajax(request):
    """View para busca AJAX de oportunidades (autocomplete)"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'success': False, 'error': 'Termo muito curto'})
    
    # Filtra oportunidades com base na query
    oportunidades = Oportunidade.objects.filter(
        Q(titulo__icontains=query) | 
        Q(descricao__icontains=query) |
        Q(local__icontains=query) |
        
        # ✅ CORREÇÃO APLICADA AQUI TAMBÉM
        Q(cursos_elegiveis__nome__icontains=query) | 
        
        Q(tipo__icontains=query)
    )[:10]  # Limita a 10 resultados
    
    results = []
    for op in oportunidades:
        results.append({
            'id': op.id,
            'titulo': op.titulo,
            'tipo': op.get_tipo_display(),
            'local': op.local,
            'remuneracao': op.remuneracao,
            'url': reverse_lazy('detalhe_oportunidade', kwargs={'id': op.id})
        })
    
    return JsonResponse({'success': True, 'results': results})