"""
Management command para popular o banco de dados com interesses.
Execute com: python manage.py popular_interesses
"""

from django.core.management.base import BaseCommand
from contas.models import Interesse


class Command(BaseCommand):
    help = 'Popula o banco de dados com interesses comuns'

    def handle(self, *args, **options):
        self.stdout.write('Populando banco de dados com interesses...\n')
        
        interesses_lista = [
            # Tecnologia
            "Programação",
            "Inteligência Artificial",
            "Machine Learning",
            "Desenvolvimento Web",
            "Desenvolvimento Mobile",
            "Ciência de Dados",
            "Segurança da Informação",
            "Cloud Computing",
            "DevOps",
            "Blockchain",
            "Internet das Coisas (IoT)",
            "Realidade Virtual/Aumentada",
            
            # Negócios e Gestão
            "Empreendedorismo",
            "Marketing Digital",
            "Gestão de Projetos",
            "Finanças",
            "Recursos Humanos",
            "Consultoria Empresarial",
            "Vendas",
            "Administração",
            
            # Ciências
            "Pesquisa Científica",
            "Biologia",
            "Química",
            "Física",
            "Matemática",
            "Estatística",
            "Meio Ambiente",
            "Sustentabilidade",
            
            # Engenharia
            "Engenharia Civil",
            "Engenharia Mecânica",
            "Engenharia Elétrica",
            "Engenharia de Produção",
            "Engenharia Química",
            "Automação",
            
            # Design e Artes
            "Design Gráfico",
            "UX/UI Design",
            "Design de Produto",
            "Fotografia",
            "Ilustração",
            "Artes Visuais",
            "Música",
            
            # Comunicação
            "Comunicação Social",
            "Jornalismo",
            "Publicidade",
            "Relações Públicas",
            "Produção Audiovisual",
            
            # Saúde
            "Medicina",
            "Enfermagem",
            "Psicologia",
            "Nutrição",
            "Fisioterapia",
            "Saúde Pública",
            
            # Ciências Sociais e Humanas
            "Direito",
            "Educação",
            "Sociologia",
            "Filosofia",
            "História",
            "Literatura",
            
            # Outros
            "Idiomas",
            "Voluntariado",
            "Esportes",
            "Inovação Social",
            "Políticas Públicas",
        ]
        
        criados = 0
        existentes = 0
        
        for interesse_nome in interesses_lista:
            interesse, created = Interesse.objects.get_or_create(nome=interesse_nome)
            if created:
                criados += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Criado: {interesse_nome}'))
            else:
                existentes += 1
                self.stdout.write(f'  - Já existe: {interesse_nome}')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Resumo:'))
        self.stdout.write(self.style.SUCCESS(f'  Interesses criados: {criados}'))
        self.stdout.write(f'  Interesses já existentes: {existentes}')
        self.stdout.write(self.style.SUCCESS(f'  Total de interesses: {Interesse.objects.count()}'))
        self.stdout.write('='*50 + '\n')
        self.stdout.write(self.style.SUCCESS('✓ Concluído!'))
