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
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo', 'matricula', 'curso', 'periodo', 'telefone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu.email@example.com'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
            'curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do curso'}),
            'periodo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Período'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label="Senha"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar senha'}),
        label="Confirmar Senha"
    )

    # Validar se as senhas coincidem
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        
        return cleaned_data

    # Validar se o nome de usuário (campo 'usuario') já está em uso
    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if Usuario.objects.filter(usuario=usuario).exists():  # Verificar no campo 'usuario', não 'username'
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return usuario

    def save(self, commit=True):
        # Sobrescrever o método save para garantir que a senha seja criptografada
        user = super().save(commit=False)
        
        # Definir a senha do usuário de forma segura
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        
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