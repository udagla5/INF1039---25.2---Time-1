from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Curso, Usuario, Oportunidade, Interesse, Mensagem # Importe Interesse

# ===============================
# cadastro1.html - PARTE 1 (Universal)
# ===============================
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo', 'matricula', 'curso']  # Added 'curso'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu.email@example.com'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),  # Changed to Select
        }
    

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label="Senha"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar senha'}),
        label="Confirmar Senha"
    )
    
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
# cadastro2.html - INTERESSES
# ===============================

class InteressesForm(forms.Form):
    """Formulário de seleção de interesses (cadastro2.html)"""
    
    interesses = forms.ModelMultipleChoiceField(
        queryset=Interesse.objects.all().order_by('nome'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',  # Adiciona classe
            'style': 'margin-right: 8px;'  # Estilo inline
        }),
        required=False,
        label='Selecione seus interesses'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Força os checkboxes a serem renderizados como <input> visíveis
        self.fields['interesses'].widget.choices = [
            (obj.id, obj.nome) for obj in Interesse.objects.all()
        ]
# ===============================
# cadastro3.html - PARTE 2 (Professor/Gestor)
# ===============================
class ProfessorCadastroFormParte2(forms.ModelForm):
    """
    Formulário para a 2ª etapa do cadastro do Professor/Gestor (Cursos e Cargos).
    """
    class Meta:
        model = Usuario
        fields = ['cursos_atuacao', 'cargos']
        widgets = {
            'cursos_atuacao': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cargos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Selecione o(s) seu(s) cargo(s)'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cursos_atuacao'].label = 'Curso(s) de atuação'
        self.fields['cargos'].label = 'Cargo(s)'
        self.fields['cursos_atuacao'].required = True
        self.fields['cargos'].required = True
        
        # 🔴 IMPORTANTE: Popula as opções do select manualmente
        # Cria as opções com base nos cursos do banco
        cursos_opcoes = [('', 'Selecione um curso')] + [
            (curso.nome, curso.nome) for curso in Curso.objects.all().order_by('nome')
        ]
        self.fields['cursos_atuacao'].widget.choices = cursos_opcoes
        
        # 🔴 Se estiver editando, define o valor atual
        if self.instance and self.instance.cursos_atuacao:
            self.initial['cursos_atuacao'] = self.instance.cursos_atuacao

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
# criar_oportunidade.html - RF6 ÚNICO - ATUALIZADO
# ===============================

class OportunidadeForm(forms.ModelForm):
    # ... (related_interests)
    
    # Add cursos_elegiveis as ModelMultipleChoiceField
    cursos_elegiveis = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all().order_by('nome'),
        # Mudar para CheckboxSelectMultiple para melhor seleção:
        widget=forms.CheckboxSelectMultiple, 
        required=False,
        label='Cursos Elegíveis'
    )
    
    class Meta:
        model = Oportunidade
        # REMOVE 'cursos_elegiveis' from this list since we're defining it above
        fields = ['titulo', 'descricao', 'foto', 'tipo', 'local', 'carga_horaria', 'num_vagas', 'processo_seletivo', 'data_encerramento', 'horas_complementares', 'remuneracao', 'related_interests', 'cursos_elegiveis']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔑 Aplicando a classe CSS aos campos (exceto checkbox ou datas específicas)
        for field_name, field in self.fields.items():
            if field_name not in ['tipo', 'data_encerramento', 'foto', 'related_interests']: 
                field.widget.attrs.update({'class': 'opportunity-input'})

# ===============================
# perfil_aluno.html - RF17 - APENAS ALUNOS
# ===============================

class EditarPerfilForm(forms.ModelForm):
    """Formulário para editar perfil do aluno (perfil_aluno.html) - APENAS ALUNOS"""
    
    # Campo para editar interesses (APENAS ALUNOS)
    interesses = forms.ModelMultipleChoiceField(
        queryset=Interesse.objects.all().order_by('nome'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        }),
        required=False,
        label='Meus Interesses'
    )
    
    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'curso', 'periodo', 'telefone', 'interesses']
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
            'curso': forms.Select(attrs={  # Changed from TextInput to Select
                'class': 'form-control'
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the curso field with actual Curso objects
        self.fields['curso'].queryset = Curso.objects.all().order_by('nome')
        self.fields['curso'].label_from_instance = lambda obj: obj.nome
# ===============================
# perfil - PROFESSORES (SEM INTERESSES)
# ===============================

class EditarPerfilProfessorForm(forms.ModelForm):
    """Formulário para editar perfil do professor - SEM INTERESSES"""
    
    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'cursos_atuacao', 'cargos', 'telefone']
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
            'cursos_atuacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cursos de Atuação'
            }),
            'cargos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargos'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone'
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
# Esqueci Senha (password_reset_form.html)
# ===============================

class CustomPasswordResetForm(PasswordResetForm):
    """
    Formulário customizado para a primeira etapa de redefinição de senha (email).
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