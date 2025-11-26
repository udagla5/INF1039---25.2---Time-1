from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Interesse, Oportunidade, Participacao,
    Favorito, PedidoOportunidade, Notificacao, Mensagem, Avaliacao
)

# ===============================
# USUÁRIOS
# ===============================

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin customizado para Usuario"""
    list_display = ['username', 'email', 'tipo', 'matricula', 'curso']
    list_filter = ['tipo', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'matricula', 'curso']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('tipo', 'matricula', 'curso', 'periodo', 'telefone', 'interesses')
        }),
    )


@admin.register(Interesse)
class InteresseAdmin(admin.ModelAdmin):
    """Admin para Interesses"""
    list_display = ['nome']
    search_fields = ['nome']


# ===============================
# OPORTUNIDADES
# ===============================

@admin.register(Oportunidade)
class OportunidadeAdmin(admin.ModelAdmin):
    """Admin para Oportunidades"""
    list_display = ['nome', 'tipo', 'area', 'status', 'criador', 'data_criacao']
    list_filter = ['status', 'tipo', 'area', 'data_criacao']
    search_fields = ['nome', 'descricao', 'criador__username']
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo', 'area', 'status', 'criador')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'exigencias', 'carga_horaria', 'horas_complementares', 'remuneracao')
        }),
        ('Prazos', {
            'fields': ('prazo_inscricao', 'data_criacao')
        }),
    )
    readonly_fields = ['data_criacao']


@admin.register(Participacao)
class ParticipacaoAdmin(admin.ModelAdmin):
    """Admin para Participações"""
    list_display = ['aluno', 'oportunidade', 'data_inicio', 'ativo', 'horas_realizadas']
    list_filter = ['ativo', 'data_inicio']
    search_fields = ['aluno__username', 'oportunidade__nome']
    date_hierarchy = 'data_inicio'


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    """Admin para Favoritos"""
    list_display = ['usuario', 'oportunidade', 'data_adicionado']
    list_filter = ['data_adicionado']
    search_fields = ['usuario__username', 'oportunidade__nome']
    date_hierarchy = 'data_adicionado'


# ===============================
# PEDIDOS
# ===============================

@admin.register(PedidoOportunidade)
class PedidoOportunidadeAdmin(admin.ModelAdmin):
    """Admin para Pedidos de Oportunidade"""
    list_display = ['nome', 'solicitante', 'area', 'status', 'data_solicitacao']
    list_filter = ['status', 'area', 'data_solicitacao']
    search_fields = ['nome', 'solicitante__username', 'descricao']
    date_hierarchy = 'data_solicitacao'


# ===============================
# NOTIFICAÇÕES E MENSAGENS
# ===============================

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    """Admin para Notificações"""
    list_display = ['usuario', 'mensagem', 'data', 'lida']
    list_filter = ['lida', 'data']
    search_fields = ['usuario__username', 'mensagem']
    date_hierarchy = 'data'


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    """Admin para Mensagens"""
    list_display = ['remetente', 'destinatario', 'data_envio', 'lida']
    list_filter = ['lida', 'data_envio']
    search_fields = ['remetente__username', 'destinatario__username', 'conteudo']
    date_hierarchy = 'data_envio'


# ===============================
# AVALIAÇÕES
# ===============================

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    """Admin para Avaliações"""
    list_display = ['autor', 'oportunidade', 'nota', 'data']
    list_filter = ['nota', 'data']
    search_fields = ['autor__username', 'oportunidade__nome', 'comentario']
    date_hierarchy = 'data'

