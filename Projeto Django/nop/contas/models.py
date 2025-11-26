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
    # Campos que você já tinha:
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=5000)
    TIPO_CHOICES = [('MON', 'Monitoria Acadêmica'), ('IC', 'Iniciação Científica'), ('EST', 'Estágio'), ('LP', 'Laboratório de Pesquisa'), ('OUT', 'Outro')]
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES, default='OUT')
    local = models.TextField(verbose_name='Local de realização da atividade') 

    # 🚀 Novos campos adicionados:
    cursos_elegiveis = models.CharField(max_length=255, verbose_name='Cursos elegíveis para participação')
    carga_horaria = models.CharField(max_length=50, verbose_name='Carga horária')
    num_vagas = models.IntegerField(verbose_name='Número de vagas disponíveis')
    horas_complementares = models.IntegerField(verbose_name='Número de horas complementares que a atividade oferece')
    processo_seletivo = models.TextField(verbose_name='Processo seletivo')
    data_encerramento = models.DateField(verbose_name='Data de encerramento do processo seletivo') 
    remuneracao = models.CharField(verbose_name='Valor da remuneracao do processo seletivo') 

    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    # Adicione outros campos, como prazo_final, criador, etc., se necessário.

    class Meta:
        verbose_name = "Oportunidade"
        verbose_name_plural = "Oportunidades"

    def __str__(self):
        return self.titulo

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

