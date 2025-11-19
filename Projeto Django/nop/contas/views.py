from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.views.generic import (
    TemplateView, ListView, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView

from .models import Usuario, Interesse, Oportunidade, Favorito, Participacao
from .forms import (
    UsuarioCreationForm, InteressesForm, CustomLoginForm, BuscaOportunidadeForm,
    OportunidadeEtapa1Form, OportunidadeEtapa2Form, OportunidadeEtapa3Form,
    EditarPerfilForm
)


# ===============================
# VIEWS PARA OS HTMLS EXISTENTES
# ===============================


# ===============================
# home.html
# ===============================

class HomeView(TemplateView):
    """Página inicial do sistema (home.html)"""
    template_name = 'home.html'


# ===============================
# cadastro1.html - RF1, RF2
# ===============================

class CadastroEtapa1View(FormView):
    """RF1, RF2 - Cadastro de usuário etapa 1 (cadastro1.html)"""
    template_name = 'cadastro1.html'
    form_class = UsuarioCreationForm
    
    def form_valid(self, form):
        # Armazenar dados na sessão para próxima etapa
        self.request.session['cadastro_temp'] = {
            'username': form.cleaned_data['username'],
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password1'],
            'tipo': form.cleaned_data['tipo'],
            'matricula': form.cleaned_data.get('matricula', ''),
            'curso': form.cleaned_data.get('curso', ''),
            'periodo': form.cleaned_data.get('periodo', ''),
            'telefone': form.cleaned_data.get('telefone', ''),
        }
        return redirect('cadastro2')


# ===============================
# cadastro2.html - RF3
# ===============================

class CadastroEtapa2View(FormView):
    """RF3 - Seleção de interesses (cadastro2.html)"""
    template_name = 'cadastro2.html'
    form_class = InteressesForm
    
    def dispatch(self, request, *args, **kwargs):
        if 'cadastro_temp' not in request.session:
            return redirect('cadastro1')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        dados = self.request.session.get('cadastro_temp')
        interesses_selecionados = form.cleaned_data['interesses']
        
        # Criar usuário
        usuario = Usuario.objects.create_user(
            username=dados['username'],
            email=dados['email'],
            password=dados['password'],
            tipo=dados['tipo'],
            matricula=dados.get('matricula', ''),
            curso=dados.get('curso', ''),
            periodo=dados.get('periodo', ''),
            telefone=dados.get('telefone', ''),
        )
        
        # Adicionar interesses
        usuario.interesses.set(interesses_selecionados)
        
        # Limpar sessão
        del self.request.session['cadastro_temp']
        
        messages.success(self.request, 'Cadastro realizado com sucesso!')
        auth_login(self.request, usuario)
        return redirect('feed')


# ===============================
# login.html e login1.html
# ===============================

class CustomLoginView(AuthLoginView):
    """Login de usuário (login.html)"""
    template_name = 'login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('feed')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha inválidos')
        return super().form_invalid(form)


class CustomLogoutView(AuthLogoutView):
    """Logout de usuário"""
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Você saiu com sucesso!')
        return super().dispatch(request, *args, **kwargs)


# ===============================
# feed.html - RF4, RF5, RF11
# ===============================

class FeedView(LoginRequiredMixin, ListView):
    """RF4, RF5, RF11 - Feed de oportunidades com filtros (feed.html)"""
    model = Oportunidade
    template_name = 'feed.html'
    context_object_name = 'oportunidades'
    paginate_by = 12
    login_url = 'login'
    
    def get_queryset(self):
        queryset = Oportunidade.objects.filter(status='APROVADA')
        
        # RF4 - Filtrar por interesses do usuário
        if self.request.user.interesses.exists():
            interesses_usuario = self.request.user.interesses.values_list('nome', flat=True)
            queryset = queryset.filter(
                Q(area__in=interesses_usuario) | Q(tipo__in=interesses_usuario)
            ).distinct()
        
        # RF5 - Aplicar filtros da busca
        busca = self.request.GET.get('busca', '')
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) |
                Q(descricao__icontains=busca) |
                Q(area__icontains=busca) |
                Q(tipo__icontains=busca)
            )
        
        if self.request.GET.get('horas_min'):
            queryset = queryset.filter(horas_complementares__gte=self.request.GET.get('horas_min'))
        
        if self.request.GET.get('horas_max'):
            queryset = queryset.filter(horas_complementares__lte=self.request.GET.get('horas_max'))
        
        if self.request.GET.get('carga_horaria_min'):
            queryset = queryset.filter(carga_horaria__gte=self.request.GET.get('carga_horaria_min'))
        
        if self.request.GET.get('remunerada'):
            queryset = queryset.filter(remuneracao__gt=0)
        
        if self.request.GET.get('area'):
            queryset = queryset.filter(area__icontains=self.request.GET.get('area'))
        
        # RF11 - Priorizar prazos próximos de encerrar
        queryset = queryset.order_by('prazo_inscricao', '-data_criacao')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favoritos_ids'] = list(
            Favorito.objects.filter(usuario=self.request.user).values_list('oportunidade_id', flat=True)
        )
        context['total'] = self.get_queryset().count()
        context['form'] = BuscaOportunidadeForm(self.request.GET)
        return context


# ===============================
# criar_oportunidade1.html - RF6 Etapa 1
# ===============================

class CriarOportunidadeEtapa1View(LoginRequiredMixin, FormView):
    """RF6 - Criar oportunidade etapa 1 (criar_oportunidade1.html)"""
    template_name = 'criar_oportunidade1.html'
    form_class = OportunidadeEtapa1Form
    login_url = 'login'
    
    def form_valid(self, form):
        self.request.session['oportunidade_temp'] = {
            'nome': form.cleaned_data['nome'],
            'tipo': form.cleaned_data['tipo'],
            'area': form.cleaned_data['area'],
        }
        return redirect('criar_oportunidade2')


# ===============================
# criar_oportunidade2.html - RF6 Etapa 2
# ===============================

class CriarOportunidadeEtapa2View(LoginRequiredMixin, FormView):
    """RF6 - Criar oportunidade etapa 2 (criar_oportunidade2.html)"""
    template_name = 'criar_oportunidade2.html'
    form_class = OportunidadeEtapa2Form
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        if 'oportunidade_temp' not in request.session:
            return redirect('criar_oportunidade1')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.request.session['oportunidade_temp'].update({
            'descricao': form.cleaned_data['descricao'],
            'carga_horaria': form.cleaned_data['carga_horaria'],
            'horas_complementares': form.cleaned_data.get('horas_complementares', 0),
            'remuneracao': str(form.cleaned_data.get('remuneracao')) if form.cleaned_data.get('remuneracao') else None,
        })
        self.request.session.modified = True
        return redirect('criar_oportunidade3')


# ===============================
# criar_oportunidade3.html - RF6 Etapa 3
# ===============================

class CriarOportunidadeEtapa3View(LoginRequiredMixin, FormView):
    """RF6 - Criar oportunidade etapa 3 (criar_oportunidade3.html)"""
    template_name = 'criar_oportunidade3.html'
    form_class = OportunidadeEtapa3Form
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        if 'oportunidade_temp' not in request.session:
            return redirect('criar_oportunidade1')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        dados = self.request.session.get('oportunidade_temp')
        dados.update({
            'exigencias': form.cleaned_data.get('exigencias', ''),
            'prazo_inscricao': form.cleaned_data.get('prazo_inscricao'),
        })
        
        # Criar oportunidade pendente de validação
        Oportunidade.objects.create(
            nome=dados['nome'],
            tipo=dados['tipo'],
            area=dados['area'],
            descricao=dados['descricao'],
            carga_horaria=dados['carga_horaria'],
            horas_complementares=dados.get('horas_complementares', 0),
            remuneracao=dados.get('remuneracao'),
            exigencias=dados.get('exigencias', ''),
            prazo_inscricao=dados.get('prazo_inscricao'),
            criador=self.request.user,
            status='PENDENTE'  # RF6 - Precisa validação
        )
        
        del self.request.session['oportunidade_temp']
        
        messages.success(self.request, 'Oportunidade criada! Aguarde a validação do sistema.')
        return redirect('feed')


# ===============================
# perfil_aluno.html - RF9, RF13, RF17
# ===============================

class PerfilAlunoView(LoginRequiredMixin, TemplateView):
    """Perfil do usuário logado (perfil_aluno.html)"""
    template_name = 'perfil_aluno.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        
        # Participações
        participacoes = Participacao.objects.filter(aluno=usuario).select_related('oportunidade')
        
        # RF13 - Horas complementares
        horas_totais = participacoes.filter(ativo=False).aggregate(
            total=Sum('horas_realizadas')
        )['total'] or 0
        
        context['usuario'] = usuario
        context['participacoes'] = participacoes
        context['horas_totais'] = horas_totais
        context['form'] = EditarPerfilForm(instance=usuario)
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Permitir edição do perfil via POST"""
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil_aluno')
        
        # Se formulário inválido, renderizar template com erros
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


# ===============================
# perfil_aluno_parte2.html
# ===============================

class PerfilAlunoParte2View(LoginRequiredMixin, TemplateView):
    """Segunda parte do perfil (perfil_aluno_parte2.html)"""
    template_name = 'perfil_aluno_parte2.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        
        # Interesses do usuário
        context['usuario'] = usuario
        context['interesses'] = usuario.interesses.all()
        context['todos_interesses'] = Interesse.objects.all()
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Permitir edição de interesses via POST (RF17)"""
        interesses_ids = request.POST.getlist('interesses')
        
        # Atualizar interesses
        request.user.interesses.clear()
        for interesse_id in interesses_ids:
            request.user.interesses.add(interesse_id)
        
        messages.success(request, 'Interesses atualizados com sucesso!')
        return redirect('perfil_aluno_parte2')
