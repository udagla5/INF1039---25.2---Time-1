from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ===============================
# 1️⃣ USUÁRIOS E PERFIS
# ===============================

class Usuario(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)
    
    TIPOS_USUARIO = [
        ('ALUNO', 'Aluno PUC-Rio'),
        ('PROFESSOR', 'Professor/Gestor'),
        ('ALUNO_EXTERNO', 'Aluno de Fora'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='ALUNO')
    
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    curso = models.CharField(max_length=100, blank=True, null=True)
    periodo = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    cursos_atuacao = models.CharField(max_length=255, verbose_name='Curso(s) de Atuação', blank=True, null=True)
    cargos = models.CharField(max_length=255, verbose_name='Cargo(s)', blank=True, null=True)

    interesses = models.ManyToManyField('Interesse', blank=True, related_name='usuarios')

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"


class Interesse(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

# ===============================
# 2️⃣ OPORTUNIDADES
# ===============================

class Oportunidade(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=5000)
    
    TIPO_CHOICES = [
        ('MON', 'Monitoria Acadêmica'),
        ('IC', 'Iniciação Científica'),
        ('EST', 'Estágio'),
        ('LP', 'Laboratório de Pesquisa'),
        ('TMP', 'Trabalho Meio Período'),
        ('VOL', 'Voluntariado'),
        ('PAL', 'Palestra'),
        ('EQC', 'Equipe de Competição'),
        ('BOL', 'Bolsa'),
        ('OUT', 'Outro')
    ]
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES, default='OUT')
    
    local = models.TextField(verbose_name='Local de realização da atividade') 
    cursos_elegiveis = models.CharField(max_length=255, verbose_name='Cursos elegíveis', blank=True, null=True)
    
    carga_horaria = models.CharField(max_length=50, verbose_name='Carga horária (Texto)')
    num_vagas = models.IntegerField(verbose_name='Número de vagas', default=1)
    
    # === CAMPOS DE FILTRO ===
    horas_complementares = models.IntegerField(verbose_name='Horas Complementares (Total)', default=0)
    remuneracao = models.IntegerField(verbose_name='Remuneração (R$)', default=0)
    
    processo_seletivo = models.TextField(verbose_name='Processo seletivo', blank=True, null=True)
    data_encerramento = models.DateField(verbose_name='Data de encerramento', null=True, blank=True) 
    
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='oportunidades_criadas', null=True, blank=True)
    
    # CORREÇÃO AQUI: Renomeado para data_publicacao para satisfazer o admin.py
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        max_length=20, 
        choices=[('PENDENTE', 'Pendente'), ('APROVADA', 'Aprovada'), ('ENCERRADA', 'Encerrada')],
        default='APROVADA' 
    )

    class Meta:
        verbose_name = "Oportunidade"
        verbose_name_plural = "Oportunidades"

    def __str__(self):
        return self.titulo

# ===============================
# 3️⃣ OUTROS MODELOS (Sem alterações)
# ===============================

class Participacao(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=True, blank=True)
    horas_realizadas = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.aluno.username} - {self.oportunidade.titulo}"

class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'oportunidade')

    def __str__(self):
        return f"{self.usuario.username} ❤️ {self.oportunidade.titulo}"

class PedidoOportunidade(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    area = models.CharField(max_length=100)
    carga_horaria = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[('AGUARDANDO', 'Aguardando'), ('APROVADO', 'Aprovado'), ('REJEITADO', 'Rejeitado')],
        default='AGUARDANDO'
    )
    data_solicitacao = models.DateTimeField(auto_now_add=True)

class Notificacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

class Mensagem(models.Model):
    remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

class Avaliacao(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE, related_name='avaliacoes')
    comentario = models.TextField(blank=True, null=True)
    nota = models.PositiveSmallIntegerField(default=5)
    data = models.DateTimeField(auto_now_add=True)