from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm  # <-- NOVO: Adicione PasswordResetForm
from django.contrib.auth.models import User
from .models import Usuario, Oportunidade, Interesse, Mensagem

# ===============================
# FORMS PARA OS HTMLS EXISTENTES
# ===============================

# ===============================
# cadastro1.html - PARTE 1 (Universal)
# ===============================
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # CAMPOS UNIVERSAIS: username, email, tipo, matricula
        fields = ['username', 'email', 'tipo', 'matricula']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu.email@example.com'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}), # INCLUÍDO
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label="Senha"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar senha'}),
        label="Confirmar Senha"
    )
    
    # ... (Métodos clean, clean_username e save permanecem iguais)
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        # Garante que a matrícula é única
        if self.instance and self.instance.pk:
            if Usuario.objects.filter(matricula=matricula).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Esta matrícula já está em uso.')
        elif Usuario.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError('Esta matrícula já está em uso.')
        return matricula

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# ===============================
# cadastro2.html - RF3 - REFAZER, TEM Q FAZER AÍ MAN
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
# cadastro3.html - PARTE 2 (Professor/Gestor)
# ===============================
class ProfessorCadastroFormParte2(forms.ModelForm):
    """
    Formulário para a 2ª etapa do cadastro do Professor/Gestor (Cursos e Cargos).
    """
    class Meta:
        model = Usuario
        # CAMPOS ESPECÍFICOS DO PROFESSOR (conforme design)
        fields = ['cursos_atuacao', 'cargos']
        
        widgets = {
            'cursos_atuacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Selecione o(s) seu(s) curso(s) de atuação'}),
            'cargos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Selecione o(s) seu(s) cargo(s)'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cursos_atuacao'].label = 'Curso(s) de atuação'
        self.fields['cargos'].label = 'Cargo(s)'
        # Força a obrigatoriedade dos campos de atuação e cargo na Parte 2
        self.fields['cursos_atuacao'].required = True
        self.fields['cargos'].required = True


# ===============================
# login.html e login1.html
# ===============================

class CustomLoginForm(AuthenticationForm):
    """Formulário customizado de login"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',       # Importante para o CSS
            'placeholder': 'Nome de usuário',
            'id': 'username-input'         # Importante para o JS/CSS
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',       # Importante para o CSS
            'placeholder': 'Senha',
            'id': 'senha-input'            # O JavaScript procura por ESTE id
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
    class Meta:
        model = Oportunidade
        # 🔑 ADICIONEI 'foto' NA LISTA DE CAMPOS
        fields = ['titulo', 'descricao', 'foto', 'tipo', 'local', 'cursos_elegiveis', 'carga_horaria', 'num_vagas', 'processo_seletivo', 'data_encerramento', 'horas_complementares', 'remuneracao']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título da oportunidade', 'maxlength': 100}),
            'descricao': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Descrição...', 'maxlength': 5000}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}), # Widget simples para upload
            'local': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Indique o local'}),
            'cursos_elegiveis': forms.TextInput(attrs={'placeholder': 'Cursos elegíveis'}),
            'carga_horaria': forms.TextInput(attrs={'placeholder': 'Carga horária'}),
            'num_vagas': forms.NumberInput(attrs={'placeholder': 'Vagas'}),
            'processo_seletivo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Processo seletivo'}),
            'horas_complementares': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Horas complementares'}),
            'remuneracao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Remuneracao'}),
            'data_encerramento': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔑 Aplicando a classe CSS aos campos (exceto checkbox ou datas específicas)
        for field_name, field in self.fields.items():
            if field_name not in ['tipo', 'data_encerramento', 'foto']: 
                field.widget.attrs.update({'class': 'opportunity-input'})

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

# ===============================
# chat.html - RF14 (Sistema de Mensagens)
# ===============================
class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'id': 'mensagem-input',  
                'class': 'form-control',
                'placeholder': 'Digite sua mensagem...',
                'rows': 1,
                'style': 'resize: none; min-height: 40px; width: 100%;' 
            }),
        }

# ===============================
# Esqueci Senha (password_reset_form.html) - NOVO CÓDIGO
# ===============================

class CustomPasswordResetForm(PasswordResetForm):
    """
    Formulário customizado para a primeira etapa de redefinição de senha (email).
    Usado para aplicar a classe 'input-reset' do esqueci_senha.css.
    """
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'input-reset', 
            'placeholder': 'seu.nome@aluno.puc-rio.br ou outro email institucional'
        })
    )