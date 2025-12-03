"""
Context processors para disponibilizar informações em todos os templates
"""
from .models import Notificacao


def notificacoes_nao_lidas(request):
    """
    Adiciona a contagem de notificações não lidas ao contexto de todos os templates
    """
    if request.user.is_authenticated:
        count = Notificacao.objects.filter(usuario=request.user, lida=False).count()
        return {
            'notificacoes_nao_lidas_count': count,
            'tem_notificacoes': count > 0
        }
    return {
        'notificacoes_nao_lidas_count': 0,
        'tem_notificacoes': False
    }
