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
    # 1. list_display: Exibe os campos na lista de oportunidades no Admin
    list_display = (
        'titulo',       # Substitui 'nome'
        'tipo',         # Campo existente
        'data_publicacao', # Substitui 'data_criacao'
        # Removido 'area', 'status', 'criador' pois não existem no modelo atual
    )

    # 2. list_filter: Permite filtrar por tipo e data de publicação
    list_filter = (
        'tipo',
        'data_publicacao', # Substitui 'data_criacao' e 'status', 'area'
    )
    
    # 3. readonly_fields: Torna a data de publicação somente leitura no formulário de edição
    readonly_fields = (
        'data_publicacao', # Substitui 'data_criacao'
    )

    # 4. date_hierarchy: Adiciona uma navegação hierárquica por data
    date_hierarchy = 'data_publicacao' # Substitui 'data_criacao'

    # 5. search_fields (Opcional, mas útil): Permite buscar por título e descrição
    search_fields = ('titulo', 'descricao', 'local')

    # 6. fieldsets (Opcional): Organiza o formulário de edição
    fieldsets = (
        (None, {
            'fields': ('titulo', 'tipo', 'local', 'descricao')
        }),
        ('Informações de Sistema', {
            'fields': ('data_publicacao',),
            'classes': ('collapse',),
        })
    )


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

