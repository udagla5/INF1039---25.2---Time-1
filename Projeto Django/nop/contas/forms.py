from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Oportunidade, Interesse

# ===============================
# FORMS PARA OS HTMLS EXISTENTES
# ===============================

# ===============================
# cadastro1.html - RF1, RF2
# ===============================

class UsuarioCreationForm(UserCreationForm):
    """Formulário de cadastro de usuário (cadastro1.html)"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu.email@example.com'
        })
    )
    
    tipo = forms.ChoiceField(
        choices=Usuario.TIPOS_USUARIO,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    matricula = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Matrícula'
        })
    )
    
    curso = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do curso'
        })
    )
    
    periodo = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 5º período'
        })
    )
    
    telefone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 
                  'tipo', 'matricula', 'curso', 'periodo', 'telefone']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })


# ===============================
# cadastro2.html - RF3
# ===============================

class InteressesForm(forms.Form):
    """Formulário de seleção de interesses (cadastro2.html)"""
    
    interesses = forms.ModelMultipleChoiceField(
        queryset=Interesse.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Selecione seus interesses'
    )


# ===============================
# login.html e login1.html
# ===============================

class CustomLoginForm(AuthenticationForm):
    """Formulário customizado de login"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'username-input',
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'senha-input',
            'class': 'form-control',
            'placeholder': 'Senha'
        })
    )


# ===============================
# feed.html - RF5
# ===============================

class BuscaOportunidadeForm(forms.Form):
    """Formulário de busca e filtros de oportunidades (feed.html)"""
    
    busca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar oportunidades...'
        })
    )
    
    area = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Área'
        })
    )
    
    horas_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Horas mínimas'
        })
    )
    
    horas_max = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Horas máximas'
        })
    )
    
    carga_horaria_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Carga horária mínima'
        })
    )
    
    remunerada = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


# ===============================
# criar_oportunidade1.html - RF6 Etapa 1
# ===============================

class OportunidadeEtapa1Form(forms.Form):
    """Etapa 1 - Informações básicas (criar_oportunidade1.html)"""
    
    nome = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da oportunidade'
        })
    )
    
    tipo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Estágio, Pesquisa, Extensão'
        })
    )
    
    area = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Tecnologia, Empreendedorismo'
        })
    )


# ===============================
# criar_oportunidade2.html - RF6 Etapa 2
# ===============================

class OportunidadeEtapa2Form(forms.Form):
    """Etapa 2 - Detalhes (criar_oportunidade2.html)"""
    
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Descreva a oportunidade...'
        })
    )
    
    carga_horaria = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Horas semanais'
        })
    )
    
    horas_complementares = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Horas complementares oferecidas'
        })
    )
    
    remuneracao = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Valor da remuneração (opcional)',
            'step': '0.01'
        })
    )


# ===============================
# criar_oportunidade3.html - RF6 Etapa 3
# ===============================

class OportunidadeEtapa3Form(forms.Form):
    """Etapa 3 - Finalização (criar_oportunidade3.html)"""
    
    exigencias = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Exigências e pré-requisitos...'
        })
    )
    
    prazo_inscricao = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


# ===============================
# perfil_aluno.html - RF17
# ===============================

class EditarPerfilForm(forms.ModelForm):
    """Formulário para editar perfil do aluno (perfil_aluno.html)"""
    
    class Meta:
        model = Usuario
        fields = ['email', 'curso', 'periodo', 'telefone']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail'
            }),
            'curso': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Curso'
            }),
            'periodo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Período'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone'
            }),
        }
