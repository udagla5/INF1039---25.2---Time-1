# GUIA DE INTEGRAÇÃO DOS FORMS NOS TEMPLATES

Este guia mostra como usar os formulários criados nos templates HTML existentes.

## 📝 Como Usar os Forms Django nos Templates

### Método 1: Renderização Automática (Mais Simples)

```html
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Enviar</button>
</form>
```

### Método 2: Renderização Manual (Mais Controle)

```html
<form method="POST">
    {% csrf_token %}
    
    <div class="form-group">
        <label>{{ form.username.label }}</label>
        {{ form.username }}
        {% if form.username.errors %}
            <div class="error">{{ form.username.errors }}</div>
        {% endif %}
    </div>
    
    <button type="submit">Enviar</button>
</form>
```

---

## 1. cadastro1.html - UsuarioCreationForm

### Opção A: Renderização Automática
```html
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Próximo</button>
</form>
```

### Opção B: Campos Individuais (Recomendado)
```html
<form method="POST">
    {% csrf_token %}
    
    <div class="form-group">
        <label>Nome de Usuário</label>
        {{ form.username }}
        {% if form.username.errors %}
            <span class="error">{{ form.username.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>E-mail</label>
        {{ form.email }}
        {% if form.email.errors %}
            <span class="error">{{ form.email.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>Senha</label>
        {{ form.password1 }}
    </div>
    
    <div class="form-group">
        <label>Confirme a Senha</label>
        {{ form.password2 }}
    </div>
    
    <div class="form-group">
        <label>Tipo de Usuário</label>
        {{ form.tipo }}
    </div>
    
    <div class="form-group">
        <label>Matrícula</label>
        {{ form.matricula }}
    </div>
    
    <div class="form-group">
        <label>Curso</label>
        {{ form.curso }}
    </div>
    
    <div class="form-group">
        <label>Período</label>
        {{ form.periodo }}
    </div>
    
    <div class="form-group">
        <label>Telefone (Opcional)</label>
        {{ form.telefone }}
    </div>
    
    <button type="submit" class="btn btn-primary">Próximo</button>
</form>
```

---

## 2. cadastro2.html - InteressesForm

```html
<form method="POST">
    {% csrf_token %}
    
    <h3>Selecione seus interesses:</h3>
    
    <div class="interesses-grid">
        {% for interesse in form.interesses %}
            <div class="interesse-item">
                {{ interesse }}
            </div>
        {% endfor %}
    </div>
    
    {% if form.interesses.errors %}
        <div class="error">{{ form.interesses.errors }}</div>
    {% endif %}
    
    <button type="submit" class="btn btn-success">Finalizar Cadastro</button>
</form>
```

---

## 3. login.html - CustomLoginForm

```html
<form method="POST">
    {% csrf_token %}
    
    <div class="form-group">
        <label>Usuário</label>
        {{ form.username }}
        {% if form.username.errors %}
            <span class="error">{{ form.username.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>Senha</label>
        {{ form.password }}
        {% if form.password.errors %}
            <span class="error">{{ form.password.errors }}</span>
        {% endif %}
    </div>
    
    {% if form.non_field_errors %}
        <div class="error">{{ form.non_field_errors }}</div>
    {% endif %}
    
    <button type="submit" class="btn btn-primary">Entrar</button>
</form>
```

---

## 4. feed.html - BuscaOportunidadeForm

```html
<!-- Formulário de Busca e Filtros -->
<form method="GET" action="{% url 'feed' %}">
    <div class="search-bar">
        {{ form.busca }}
        <button type="submit" class="btn-search">🔍 Buscar</button>
    </div>
    
    <!-- Filtros Avançados -->
    <div class="filtros">
        <div class="filtro-item">
            <label>Área</label>
            {{ form.area }}
        </div>
        
        <div class="filtro-item">
            <label>Horas Mínimas</label>
            {{ form.horas_min }}
        </div>
        
        <div class="filtro-item">
            <label>Horas Máximas</label>
            {{ form.horas_max }}
        </div>
        
        <div class="filtro-item">
            <label>Carga Horária Mínima</label>
            {{ form.carga_horaria_min }}
        </div>
        
        <div class="filtro-item">
            {{ form.remunerada }}
            <label>Somente remuneradas</label>
        </div>
        
        <button type="submit" class="btn btn-primary">Aplicar Filtros</button>
    </div>
</form>

<!-- Lista de Oportunidades -->
<div class="oportunidades-lista">
    {% for oportunidade in oportunidades %}
        <div class="oportunidade-card">
            <h3>{{ oportunidade.nome }}</h3>
            <p>{{ oportunidade.descricao|truncatewords:20 }}</p>
            <div class="info">
                <span>{{ oportunidade.area }}</span>
                <span>{{ oportunidade.carga_horaria }}h/semana</span>
            </div>
        </div>
    {% endfor %}
</div>

<!-- Paginação -->
{% if is_paginated %}
    <div class="pagination">
        {% if page_obj.has_previous %}
            <a href="?page=1">Primeira</a>
            <a href="?page={{ page_obj.previous_page_number }}">Anterior</a>
        {% endif %}
        
        <span>Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
        
        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Próxima</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">Última</a>
        {% endif %}
    </div>
{% endif %}
```

---

## 5. criar_oportunidade1.html - OportunidadeEtapa1Form

```html
<form method="POST">
    {% csrf_token %}
    
    <h2>Etapa 1: Informações Básicas</h2>
    
    <div class="form-group">
        <label>Nome da Oportunidade</label>
        {{ form.nome }}
        {% if form.nome.errors %}
            <span class="error">{{ form.nome.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>Tipo</label>
        {{ form.tipo }}
        <small>Ex: Estágio, Pesquisa, Extensão</small>
        {% if form.tipo.errors %}
            <span class="error">{{ form.tipo.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>Área</label>
        {{ form.area }}
        <small>Ex: Tecnologia, Empreendedorismo</small>
        {% if form.area.errors %}
            <span class="error">{{ form.area.errors }}</span>
        {% endif %}
    </div>
    
    <button type="submit" class="btn btn-primary">Próxima Etapa →</button>
</form>
```

---

## 6. criar_oportunidade2.html - OportunidadeEtapa2Form

```html
<form method="POST">
    {% csrf_token %}
    
    <h2>Etapa 2: Detalhes</h2>
    
    <div class="form-group">
        <label>Descrição</label>
        {{ form.descricao }}
        {% if form.descricao.errors %}
            <span class="error">{{ form.descricao.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>Carga Horária (h/semana)</label>
        {{ form.carga_horaria }}
        {% if form.carga_horaria.errors %}
            <span class="error">{{ form.carga_horaria.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>Horas Complementares Oferecidas</label>
        {{ form.horas_complementares }}
        {% if form.horas_complementares.errors %}
            <span class="error">{{ form.horas_complementares.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>Remuneração (Opcional)</label>
        {{ form.remuneracao }}
        {% if form.remuneracao.errors %}
            <span class="error">{{ form.remuneracao.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-actions">
        <a href="{% url 'criar_oportunidade1' %}" class="btn btn-secondary">← Voltar</a>
        <button type="submit" class="btn btn-primary">Próxima Etapa →</button>
    </div>
</form>
```

---

## 7. criar_oportunidade3.html - OportunidadeEtapa3Form

```html
<form method="POST">
    {% csrf_token %}
    
    <h2>Etapa 3: Finalização</h2>
    
    <div class="form-group">
        <label>Exigências e Pré-requisitos (Opcional)</label>
        {{ form.exigencias }}
        {% if form.exigencias.errors %}
            <span class="error">{{ form.exigencias.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label>Prazo de Inscrição (Opcional)</label>
        {{ form.prazo_inscricao }}
        {% if form.prazo_inscricao.errors %}
            <span class="error">{{ form.prazo_inscricao.errors }}</span>
        {% endif %}
    </div>
    
    <div class="form-actions">
        <a href="{% url 'criar_oportunidade2' %}" class="btn btn-secondary">← Voltar</a>
        <button type="submit" class="btn btn-success">✓ Criar Oportunidade</button>
    </div>
</form>
```

---

## 8. perfil_aluno.html - EditarPerfilForm

```html
<div class="perfil-info">
    <h2>Meu Perfil</h2>
    
    <!-- Exibição dos dados -->
    <div class="info-display">
        <p><strong>Usuário:</strong> {{ usuario.username }}</p>
        <p><strong>Tipo:</strong> {{ usuario.get_tipo_display }}</p>
        <p><strong>Horas Complementares:</strong> {{ horas_totais }}h</p>
    </div>
    
    <!-- Formulário de Edição -->
    <h3>Editar Informações</h3>
    <form method="POST">
        {% csrf_token %}
        
        <div class="form-group">
            <label>E-mail</label>
            {{ form.email }}
            {% if form.email.errors %}
                <span class="error">{{ form.email.errors }}</span>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Curso</label>
            {{ form.curso }}
            {% if form.curso.errors %}
                <span class="error">{{ form.curso.errors }}</span>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Período</label>
            {{ form.periodo }}
            {% if form.periodo.errors %}
                <span class="error">{{ form.periodo.errors }}</span>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Telefone</label>
            {{ form.telefone }}
            {% if form.telefone.errors %}
                <span class="error">{{ form.telefone.errors }}</span>
            {% endif %}
        </div>
        
        <button type="submit" class="btn btn-primary">Salvar Alterações</button>
    </form>
</div>

<!-- Lista de Participações -->
<div class="participacoes">
    <h3>Minhas Participações</h3>
    {% for participacao in participacoes %}
        <div class="participacao-item">
            <h4>{{ participacao.oportunidade.nome }}</h4>
            <p>{{ participacao.oportunidade.area }}</p>
            {% if participacao.ativo %}
                <span class="badge badge-success">Em andamento</span>
            {% else %}
                <span class="badge badge-secondary">Concluída ({{ participacao.horas_realizadas }}h)</span>
            {% endif %}
        </div>
    {% endfor %}
</div>
```

---

## 9. perfil_aluno_parte2.html - Editar Interesses

```html
<h2>Meus Interesses</h2>

<form method="POST">
    {% csrf_token %}
    
    <div class="interesses-atuais">
        <h3>Interesses Selecionados:</h3>
        {% for interesse in interesses %}
            <span class="badge">{{ interesse.nome }}</span>
        {% empty %}
            <p>Nenhum interesse selecionado.</p>
        {% endfor %}
    </div>
    
    <div class="editar-interesses">
        <h3>Atualizar Interesses:</h3>
        <div class="interesses-grid">
            {% for interesse in todos_interesses %}
                <div class="interesse-checkbox">
                    <input type="checkbox" 
                           name="interesses" 
                           value="{{ interesse.id }}"
                           {% if interesse in interesses %}checked{% endif %}
                           id="interesse_{{ interesse.id }}">
                    <label for="interesse_{{ interesse.id }}">{{ interesse.nome }}</label>
                </div>
            {% endfor %}
        </div>
    </div>
    
    <button type="submit" class="btn btn-primary">Salvar Interesses</button>
</form>
```

---

## 💡 Dicas Importantes

### 1. Sempre use {% csrf_token %}
```html
<form method="POST">
    {% csrf_token %}
    <!-- resto do form -->
</form>
```

### 2. Exibir Mensagens do Django
```html
{% if messages %}
    <div class="messages">
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    </div>
{% endif %}
```

### 3. Verificar Erros do Form
```html
{% if form.errors %}
    <div class="alert alert-danger">
        <p>Por favor, corrija os erros abaixo:</p>
        {{ form.errors }}
    </div>
{% endif %}
```

### 4. Forms GET vs POST
- **POST:** Cadastros, edições, deletar → `<form method="POST">`
- **GET:** Buscas, filtros → `<form method="GET">`

---

## 🎨 Classes CSS Automáticas

Os forms já vêm com `class="form-control"`, então funcionam com Bootstrap:

```html
<!-- Já renderiza com class="form-control" -->
{{ form.username }}

<!-- Resultado HTML: -->
<input type="text" name="username" class="form-control" placeholder="Nome de usuário">
```
