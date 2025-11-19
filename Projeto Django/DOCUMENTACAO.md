# Sistema de Oportunidades - Documentação

## 📋 Resumo do Sistema

Sistema Django com **Class-Based Views (CBV)** implementando os requisitos funcionais para gerenciamento de oportunidades acadêmicas.

## ✅ HTMLs Existentes e Views Implementadas

### 1. home.html
- **View:** `HomeView` (TemplateView)
- **URL:** `/`
- **Descrição:** Página inicial do sistema

### 2. cadastro1.html (RF1, RF2)
- **View:** `CadastroEtapa1View` (FormView)
- **Form:** `UsuarioCreationForm`
- **URL:** `/cadastro1/`
- **Descrição:** Primeira etapa do cadastro (dados do usuário)

### 3. cadastro2.html (RF3)
- **View:** `CadastroEtapa2View` (FormView)
- **Form:** `InteressesForm`
- **URL:** `/cadastro2/`
- **Descrição:** Segunda etapa do cadastro (seleção de interesses)

### 4. login.html
- **View:** `CustomLoginView` (AuthLoginView)
- **Form:** `CustomLoginForm`
- **URL:** `/login/`
- **Descrição:** Página de login

### 5. login1.html
- **Descrição:** Template alternativo de login (usa a mesma view)

### 6. feed.html (RF4, RF5, RF11)
- **View:** `FeedView` (ListView)
- **Form:** `BuscaOportunidadeForm`
- **URL:** `/feed/`
- **Descrição:** Feed de oportunidades com filtros e busca

### 7. criar_oportunidade1.html (RF6)
- **View:** `CriarOportunidadeEtapa1View` (FormView)
- **Form:** `OportunidadeEtapa1Form`
- **URL:** `/criar-oportunidade/etapa1/`
- **Descrição:** Etapa 1 - Informações básicas

### 8. criar_oportunidade2.html (RF6)
- **View:** `CriarOportunidadeEtapa2View` (FormView)
- **Form:** `OportunidadeEtapa2Form`
- **URL:** `/criar-oportunidade/etapa2/`
- **Descrição:** Etapa 2 - Detalhes da oportunidade

### 9. criar_oportunidade3.html (RF6)
- **View:** `CriarOportunidadeEtapa3View` (FormView)
- **Form:** `OportunidadeEtapa3Form`
- **URL:** `/criar-oportunidade/etapa3/`
- **Descrição:** Etapa 3 - Finalização

### 10. perfil_aluno.html (RF9, RF13, RF17)
- **View:** `PerfilAlunoView` (TemplateView)
- **Form:** `EditarPerfilForm`
- **URL:** `/perfil-aluno/`
- **Descrição:** Perfil do usuário logado com participações e horas

### 11. perfil_aluno_parte2.html (RF17)
- **View:** `PerfilAlunoParte2View` (TemplateView)
- **URL:** `/perfil-aluno-parte2/`
- **Descrição:** Edição de interesses do usuário

## 📁 Arquivos Criados/Modificados

```
contas/
├── models.py          # 8 modelos principais (já existia)
├── forms.py           # 8 formulários Django (CRIADO)
├── views.py           # 10 Class-Based Views (CRIADO)
├── urls.py            # Rotas mapeadas (ATUALIZADO)
└── admin.py           # Admin Django (já existia)

templates/             # Todos já existentes
├── home.html
├── cadastro1.html
├── cadastro2.html
├── login.html
├── login1.html
├── feed.html
├── criar_oportunidade1.html
├── criar_oportunidade2.html
├── criar_oportunidade3.html
├── perfil_aluno.html
└── perfil_aluno_parte2.html
```

## 🎨 Formulários Criados

### 1. UsuarioCreationForm
- **Campos:** username, email, password1, password2, tipo, matricula, curso, periodo, telefone
- **Uso:** cadastro1.html

### 2. InteressesForm
- **Campos:** interesses (Multiple Choice)
- **Uso:** cadastro2.html

### 3. CustomLoginForm
- **Campos:** username, password
- **Uso:** login.html

### 4. BuscaOportunidadeForm
- **Campos:** busca, area, horas_min, horas_max, carga_horaria_min, remunerada
- **Uso:** feed.html (filtros)

### 5. OportunidadeEtapa1Form
- **Campos:** nome, tipo, area
- **Uso:** criar_oportunidade1.html

### 6. OportunidadeEtapa2Form
- **Campos:** descricao, carga_horaria, horas_complementares, remuneracao
- **Uso:** criar_oportunidade2.html

### 7. OportunidadeEtapa3Form
- **Campos:** exigencias, prazo_inscricao
- **Uso:** criar_oportunidade3.html

### 8. EditarPerfilForm
- **Campos:** email, curso, periodo, telefone
- **Uso:** perfil_aluno.html

## 🎯 Class-Based Views Criadas

| View | Tipo | Template | Descrição |
|------|------|----------|-----------|
| HomeView | TemplateView | home.html | Página inicial |
| CadastroEtapa1View | FormView | cadastro1.html | Cadastro etapa 1 |
| CadastroEtapa2View | FormView | cadastro2.html | Cadastro etapa 2 |
| CustomLoginView | AuthLoginView | login.html | Login |
| CustomLogoutView | AuthLogoutView | - | Logout |
| FeedView | ListView | feed.html | Feed com filtros |
| CriarOportunidadeEtapa1View | FormView | criar_oportunidade1.html | Criar etapa 1 |
| CriarOportunidadeEtapa2View | FormView | criar_oportunidade2.html | Criar etapa 2 |
| CriarOportunidadeEtapa3View | FormView | criar_oportunidade3.html | Criar etapa 3 |
| PerfilAlunoView | TemplateView | perfil_aluno.html | Perfil do usuário |
| PerfilAlunoParte2View | TemplateView | perfil_aluno_parte2.html | Editar interesses |

## 🔐 Funcionalidades Implementadas

### ✅ RF1, RF2 - Cadastro em 2 etapas
- Etapa 1: Dados pessoais e tipo de usuário
- Etapa 2: Seleção de interesses
- Armazenamento em sessão entre etapas
- Criação de usuário após completar ambas etapas

### ✅ RF3 - Interesses do usuário
- Seleção de múltiplos interesses no cadastro
- Interesses armazenados via ManyToMany

### ✅ RF4 - Feed personalizado
- Feed filtrado por interesses do usuário
- Exibe apenas oportunidades aprovadas

### ✅ RF5 - Busca e filtros
- Busca por texto (nome, descrição, área, tipo)
- Filtros: horas complementares, carga horária, área, remuneração
- Formulário de busca integrado

### ✅ RF6 - Criar oportunidade em 3 etapas
- Etapa 1: Nome, tipo, área
- Etapa 2: Descrição, carga horária, horas, remuneração
- Etapa 3: Exigências, prazo de inscrição
- Status inicial: PENDENTE (aguarda validação)

### ✅ RF9 - Perfil do usuário
- Visualização de dados pessoais
- Lista de participações em oportunidades
- Edição de dados do perfil

### ✅ RF11 - Priorização de prazos
- Oportunidades ordenadas por prazo de inscrição
- Prazos mais próximos aparecem primeiro

### ✅ RF13 - Horas complementares
- Cálculo automático de horas realizadas
- Exibição no perfil do aluno

### ✅ RF17 - Editar interesses
- Atualização de interesses via perfil_aluno_parte2.html
- Atualiza recomendações do feed

## 🔧 Mixins Utilizados

- **LoginRequiredMixin:** Proteção de rotas (feed, criar oportunidade, perfis)
- **AuthLoginView/LogoutView:** Autenticação nativa do Django

## 🚀 Como Usar

### 1. Rodar Migrações
```bash
cd "Projeto Django/nop"
python manage.py makemigrations
python manage.py migrate
```

### 2. Criar Superusuário
```bash
python manage.py createsuperuser
```

### 3. Criar Interesses Iniciais
```python
python manage.py shell
from contas.models import Interesse
interesses = ['Empreendedorismo', 'Artístico', 'Jogos Digitais', 'IA', 
              'Ciência de Dados', 'Tecnologia', 'Pesquisa', 'Extensão']
for nome in interesses:
    Interesse.objects.get_or_create(nome=nome)
exit()
```

### 4. Rodar Servidor
```bash
python manage.py runserver
```

### 5. Acessar o Sistema
- Home: http://localhost:8000/
- Cadastro: http://localhost:8000/cadastro1/
- Login: http://localhost:8000/login/
- Feed: http://localhost:8000/feed/ (requer login)

## 📝 Fluxos de Uso

### Cadastro de Novo Usuário
1. Acessa `/cadastro1/`
2. Preenche dados e tipo de usuário
3. Clica em "Próximo"
4. Seleciona interesses em `/cadastro2/`
5. Sistema cria usuário e faz login automático
6. Redireciona para `/feed/`

### Criar Nova Oportunidade
1. Usuário logado acessa `/criar-oportunidade/etapa1/`
2. Preenche nome, tipo e área
3. Continua para etapa 2 (descrição e horas)
4. Finaliza na etapa 3 (exigências e prazo)
5. Oportunidade criada com status PENDENTE
6. Aguarda validação de administrador

### Buscar Oportunidades
1. Acessa `/feed/`
2. Vê oportunidades filtradas por seus interesses
3. Pode aplicar filtros adicionais
4. Oportunidades com prazo próximo aparecem primeiro

## 💡 Recursos Especiais

- ✅ Sistema de sessões para cadastro multi-etapa
- ✅ Feed personalizado por interesses do usuário
- ✅ Priorização automática por prazo de inscrição
- ✅ Validação de oportunidades (status PENDENTE)
- ✅ Formulários com Bootstrap classes
- ✅ Messages framework integrado
- ✅ Login/Logout com redirecionamento
- ✅ Paginação no feed (12 itens por página)

## 🔄 Próximos Passos (Templates Faltantes)

Para implementar os demais requisitos, você precisará criar templates para:
- Detalhes da oportunidade (RF7, RF8)
- Perfil de outros usuários (RF9)
- Notificações (RF10, RF11)
- Favoritos (RF12)
- Minhas horas (RF13)
- Mensagens (RF14)
- Avaliações (RF15)
- Painel administrativo (RF16)

## 📌 Observações Importantes

- Todos os forms usam Bootstrap classes para estilização
- Views protegidas com `LoginRequiredMixin`
- Sistema de mensagens do Django está integrado
- Dados temporários armazenados em sessão
- Código documentado com docstrings
- Segue as melhores práticas do Django

## ✅ Requisitos Funcionais Implementados

### RF1-RF3: Cadastro e Autenticação
- ✅ Cadastro em 2 etapas (dados + interesses)
- ✅ Tipos de usuário: Aluno, Professor/Gestor, Aluno Externo
- ✅ Sistema de login/logout
- **Views:** `CadastroEtapa1View`, `CadastroEtapa2View`, `CustomLoginView`, `CustomLogoutView`

### RF4-RF5: Feed e Busca
- ✅ Feed personalizado por interesses
- ✅ Filtros avançados (horas, carga horária, área, remuneração)
- ✅ Busca por texto
- **View:** `FeedView`

### RF6: Criar Oportunidades
- ✅ Criação em 3 etapas
- ✅ Validação pendente antes de publicar
- **Views:** `CriarOportunidadeEtapa1View`, `CriarOportunidadeEtapa2View`, `CriarOportunidadeEtapa3View`

### RF6.1: Pedidos de Oportunidade
- ✅ Alunos podem solicitar cadastro de oportunidades
- ✅ Aprovação por administradores
- **Views:** `CriarPedidoOportunidadeView`, `MeusPedidosView`, `ValidarPedidoView`

### RF7-RF8: Participação
- ✅ Registro de participação em oportunidades
- ✅ Detalhes com lista de participantes
- **Views:** `ParticiparOportunidadeView`, `DetalheOportunidadeView`

### RF9: Perfis de Usuário
- ✅ Visualização de perfis
