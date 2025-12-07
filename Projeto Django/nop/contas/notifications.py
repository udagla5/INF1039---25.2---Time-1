from datetime import timedelta
from django.utils import timezone
from contas.models import Favorito, Notificacao

def gerar_notificacoes():
    hoje = timezone.now().date()

    favoritos = Favorito.objects.select_related("usuario", "oportunidade")

    for fav in favoritos:
        oportunidade = fav.oportunidade
        usuario = fav.usuario

        # Ver se a oportunidade tem a data pra encerrar
        if not oportunidade.data_encerramento:
            continue

        dias_restantes = (oportunidade.data_encerramento - hoje).days

        # Notificação de 7 dias antes
        if dias_restantes == 7 and not fav.notificado_7_dias:
            Notificacao.objects.create(
                usuario=usuario,
                mensagem=f"A oportunidade '{oportunidade.titulo}' encerra em 7 dias!"
            )
            fav.notificado_7_dias = True
            fav.save()

        # Notificação de 1 dia antes
        if dias_restantes == 1 and not fav.notificado_1_dia:
            Notificacao.objects.create(
                usuario=usuario,
                mensagem=f"A oportunidade '{oportunidade.titulo}' encerra amanhã!"
            )
            fav.notificado_1_dia = True
            fav.save()
