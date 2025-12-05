"""
Management command para popular o banco de dados com cursos.
Execute com: python manage.py popular_cursos
"""

from django.core.management.base import BaseCommand
from contas.models import Curso


class Command(BaseCommand):
    help = 'Popula o banco de dados com cursos comuns'

    def handle(self, *args, **options):
        self.stdout.write('Populando banco de dados com cursos...\n')
        
        cursos_lista = [
            'Administração',
            'Arquitetura e Urbanismo',
            'Artes Cênicas',
            'Ciclo Básico do CTC',
            'Ciência da Computação',
            'Ciências Biológicas',
            'Ciências Econômicas (Economia)',
            'Ciências Sociais (Sociologia)',
            'Comunicação Social',
            'Design',
            'Direito',
            'Engenharia Ambiental',
            'Engenharia Civil',
            'Engenharia de Computação',
            'Engenharia de Controle e Automação',
            'Engenharia Elétrica',
            'Engenharia de Materiais e Nanotecnologia',
            'Engenharia Mecânica',
            'Engenharia de Produção',
            'Engenharia Química',
            'Estudos de Mídia',
            'Publicidade e Comunicação Corporativa',
            'Cinema e Audiovisual',
            'Comunicação e Tecnologia',
            'Farmácia', 
            'Filosofia',
            'Física',
            'Geografia',
            'História',
            'Inteligência Artificial', 
            'Jornalismo',
            'Português e Inglês e Respectivas Literaturas',
            'Língua Portuguesa e Respectivas Literaturas',
            'Produção Textual (Formação de Escritor)',
            'Tradutor - Inglês',
            'Matemática',
            'Matemática Aplicada e Computacional com Ênfase em Ciência de Dados', 
            'Neurociências', 
            'Nutrição',
            'Pedagogia',
            'Psicologia',
            'Química',
            'Relações Internacionais',
            'Serviço Social',
            'Sistemas de Informação',
            'Sustentabilidade',
            'Teologia',
        ]
        
        criados = 0
        existentes = 0
        
        for curso_nome in cursos_lista:
            curso_obj, created = Curso.objects.get_or_create(nome=curso_nome)
            if created:
                criados += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Criado: {curso_nome}'))
            else:
                existentes += 1
                self.stdout.write(f'  - Já existe: {curso_nome}')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Resumo:'))
        self.stdout.write(self.style.SUCCESS(f'  cursos criados: {criados}'))
        self.stdout.write(f'  cursos já existentes: {existentes}')
        self.stdout.write(self.style.SUCCESS(f'  Total de cursos: {Curso.objects.count()}'))  # Fixed: Curso.objects.count()
        self.stdout.write('='*50 + '\n')
        self.stdout.write(self.style.SUCCESS('✓ Concluído!'))