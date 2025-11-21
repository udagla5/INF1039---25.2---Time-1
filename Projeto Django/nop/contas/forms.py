from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # ← UserCreationForm importado
from django.contrib.auth.models import User  # ← Importar User também
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
    
    # Se Usuario.TIPOS_USUARIO não existir, defina aqui:
    TIPOS_USUARIO = [
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('COORDENADOR', 'Coordenador'),
    ]
    
    tipo = forms.ChoiceField(
        choices=TIPOS_USUARIO,
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
        model = User  # ← Usar User do Django se Usuario não existir
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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Se você tiver modelo Usuario personalizado, crie aqui
            # Usuario.objects.create(user=user, tipo=self.cleaned_data['tipo'], ...)
        return user


# ===============================
# cadastro2.html - RF3
# ===============================

class InteressesForm(forms.Form):
    """Formulário de seleção de interesses (cadastro2.html)"""
    
    # Se Interesse não existir, use ChoiceField como fallback
    INTERESSES_CHOICES = [
        ('TECNOLOGIA', 'Tecnologia'),
        ('ENGENHARIA', 'Engenharia'),
        ('SAUDE', 'Saúde'),
        ('NEGOCIOS', 'Negócios'),
        ('ARTES', 'Artes'),
        ('CIENCIAS', 'Ciências'),
    ]
    
    interesses = forms.MultipleChoiceField(
        choices=INTERESSES_CHOICES,
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
# criar_oportunidade.html - RF6 ÚNICO
# ===============================

class OportunidadeForm(forms.ModelForm):
    """Formulário ÚNICO para criar oportunidade (criar_oportunidade.html)"""
    
    # ETAPA 1 - Informações Básicas
    nome = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da oportunidade'
        }),
        label='Nome da Oportunidade*'
    )
    
    TIPO_CHOICES = [
        ('MONITORIA', 'Monitoria'),
        ('ESTAGIO', 'Estágio'),
        ('INICIACAO_CIENTIFICA', 'Iniciação Científica'),
        ('TRABALHO_MEIO_PERIODO', 'Trabalho Meio Período'),
        ('VOLUNTARIADO', 'Voluntariado'),
        ('PALESTRA', 'Palestra'),
        ('EQUIPE_COMPETICAO', 'Equipe de Competição'),
        ('BOLSA', 'Bolsa'),
    ]
    
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Tipo*'
    )
    
    area = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Tecnologia, Empreendedorismo, Saúde'
        }),
        label='Área*'
    )
    
    # ETAPA 2 - Detalhes
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Descreva detalhadamente a oportunidade...'
        }),
        label='Descrição*'
    )
    
    carga_horaria = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 4 horas/dia, 20 horas/semana'
        }),
        label='Carga Horária*'
    )
    
    horas_complementares = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0'
        }),
        label='Horas Complementares'
    )
    
    remuneracao = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0,00',
            'step': '0.01'
        }),
        label='Remuneração (R$)'
    )
    
    # ETAPA 3 - Finalização
    exigencias = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Exigências, pré-requisitos, conhecimentos necessários...'
        }),
        label='Exigências e Pré-requisitos'
    )
    
    prazo_inscricao = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Prazo de Inscrição'
    )

    class Meta:
        model = Oportunidade
        fields = [
            'nome', 'tipo', 'area', 'descricao', 'carga_horaria',
            'horas_complementares', 'remuneracao', 'exigencias', 'prazo_inscricao'
        ]


# ===============================
# perfil_aluno.html - RF17
# ===============================

class EditarPerfilForm(forms.ModelForm):
    """Formulário para editar perfil do aluno (perfil_aluno.html)"""
    
    class Meta:
        model = User  # ← Usar User como fallback
        fields = ['email', 'first_name', 'last_name']  # Campos básicos do User
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
        }