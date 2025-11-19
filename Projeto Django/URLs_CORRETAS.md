# 🔗 URLs Corretas do Projeto NOP

## ⚠️ IMPORTANTE: URLs Django vs Arquivos HTML

No Django, **NÃO usamos extensões `.html` nas URLs**. O Django usa URLs limpas e amigáveis.

---

## 📋 Lista de URLs Disponíveis

### 1. **Página Inicial**
```
URL: http://localhost:8000/
Name: 'home'
Template: home.html
```

### 2. **Cadastro - Etapa 1**
```
URL: http://localhost:8000/cadastro1/
Name: 'cadastro1'
Template: cadastro1.html
```

### 3. **Cadastro - Etapa 2**
```
URL: http://localhost:8000/cadastro2/
Name: 'cadastro2'
Template: cadastro2.html
```

### 4. **Login**
```
URL: http://localhost:8000/login/
Name: 'login'
Template: login.html
```

### 5. **Logout**
```
URL: http://localhost:8000/logout/
Name: 'logout'
```

### 6. **Feed de Oportunidades**
```
URL: http://localhost:8000/feed/
Name: 'feed'
Template: feed.html
```

### 7. **Criar Oportunidade - Etapa 1**
```
URL: http://localhost:8000/criar-oportunidade/etapa1/
Name: 'criar_oportunidade1'
Template: criar_oportunidade1.html
```

### 8. **Criar Oportunidade - Etapa 2**
```
URL: http://localhost:8000/criar-oportunidade/etapa2/
Name: 'criar_oportunidade2'
Template: criar_oportunidade2.html
```

### 9. **Criar Oportunidade - Etapa 3**
```
URL: http://localhost:8000/criar-oportunidade/etapa3/
Name: 'criar_oportunidade3'
Template: criar_oportunidade3.html
```

### 10. **Perfil do Aluno - Parte 1**
```
URL: http://localhost:8000/perfil-aluno/
Name: 'perfil_aluno'
Template: perfil_aluno.html
```

### 11. **Perfil do Aluno - Parte 2**
```
URL: http://localhost:8000/perfil-aluno-parte2/
Name: 'perfil_aluno_parte2'
Template: perfil_aluno_parte2.html
```

---

## 🎯 Como Usar URLs nos Templates

### ❌ ERRADO:
```html
<a href="login.html">Login</a>
<a href="cadastro1.html">Cadastro</a>
<button onclick="window.location.href='feed.html'">IR</button>
```

### ✅ CORRETO:
```html
<a href="{% url 'login' %}">Login</a>
<a href="{% url 'cadastro1' %}">Cadastro</a>
<button onclick="window.location.href='{% url 'feed' %}'">IR</button>
```

---

## 🔧 Correções Aplicadas

Todos os templates foram corrigidos para usar `{% url %}` tag do Django:

1. ✅ `feed.html` - Botão "Editar sua Conta NOP"
2. ✅ `home.html` - Links "log in" e "sign up"
3. ✅ `home.html` - Botão "IR" para o feed
4. ✅ `login1.html` - Botão "Entrar" e link "Clique aqui para criar"
5. ✅ `perfil_aluno.html` - Seta voltar e seta avançar
6. ✅ `perfil_aluno_parte2.html` - Seta voltar

---

## 🚀 Como Testar

1. **Inicie o servidor:**
   ```bash
   cd "/home/thay/projetos/bicalho/Projeto Django/nop"
   python manage.py runserver
   ```

2. **Acesse no navegador:**
   - Página inicial: `http://localhost:8000/`
   - Login: `http://localhost:8000/login/`
   - Cadastro: `http://localhost:8000/cadastro1/`
   - Feed: `http://localhost:8000/feed/`

3. **Navegue pelos links** - Agora todos os links internos funcionam corretamente!

---

## 📝 Nota sobre login1.html

O arquivo `login1.html` existe mas não tem rota associada. Use a rota `/login/` que renderiza `login.html`.
Se quiser usar `login1.html`, adicione uma rota em `urls.py`:

```python
path('login1/', TemplateView.as_view(template_name='login1.html'), name='login1'),
```

---

## 🎨 Arquivos Estáticos

Os arquivos estáticos (CSS, JS, imagens) estão configurados corretamente em:
```
/static/css/
/static/img/
```

Todos os templates usam `{% load static %}` e `{% static 'caminho' %}`.
