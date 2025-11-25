from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ===============================
# 1️⃣ USUÁRIOS E PERFIS
# ===============================

class Usuario(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=20, unique=True)
    senha = models.CharField(max_length=20)
    TIPOS_USUARIO = [
        ('ALUNO', 'Aluno PUC-Rio'),
        ('PROFESSOR', 'Professor/Gestor'),
        ('ALUNO_EXTERNO', 'Aluno de Fora'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    curso = models.CharField(max_length=100, blank=True, null=True)
    periodo = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    REQUIRED_FIELDS = ['email']  # Outros campos que são obrigatórios

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
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente de Validação'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada'),
    ]

    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    descricao = models.TextField()
    carga_horaria = models.PositiveIntegerField()
    horas_complementares = models.PositiveIntegerField(default=0)
    remuneracao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exigencias = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    prazo_inscricao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')

    criador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='oportunidades_criadas'
    )

    interessados = models.ManyToManyField(
        Usuario,
        through='Participacao',
        related_name='oportunidades_participadas',
        blank=True
    )

    def __str__(self):
        return f"{self.nome} ({self.status})"

# ===============================
# 3️⃣ PARTICIPAÇÕES (RF7, RF13)
# ===============================

class Participacao(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=True, blank=True)
    horas_realizadas = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.aluno.username} - {self.oportunidade.nome}"

# ===============================
# 4️⃣ FAVORITOS (RF12)
# ===============================

class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'oportunidade')

    def __str__(self):
        return f"{self.usuario.username} ❤️ {self.oportunidade.nome}"

# ===============================
# 5️⃣ PEDIDOS DE OPORTUNIDADE (RF6.1)
# ===============================

class PedidoOportunidade(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    area = models.CharField(max_length=100)
    carga_horaria = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('AGUARDANDO', 'Aguardando Análise'),
            ('APROVADO', 'Aprovado'),
            ('REJEITADO', 'Rejeitado')
        ],
        default='AGUARDANDO'
    )
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido: {self.nome} ({self.get_status_display()})"

# ===============================
# 6️⃣ NOTIFICAÇÕES (RF10, RF11)
# ===============================

class Notificacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificação para {self.usuario.username}"

# ===============================
# 7️⃣ MENSAGENS INTERNAS (RF14)
# ===============================

class Mensagem(models.Model):
    remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.remetente} para {self.destinatario}"

# ===============================
# 8️⃣ AVALIAÇÕES / FEEDBACKS (RF15)
# ===============================

class Avaliacao(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE, related_name='avaliacoes')
    comentario = models.TextField(blank=True, null=True)
    nota = models.PositiveSmallIntegerField(default=5)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.nota}/10 por {self.autor.username}"

