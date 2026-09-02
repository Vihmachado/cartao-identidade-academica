# 🎓 Projeto Aluno · Django | Cartão de Identidade Acadêmica

**Desafio da disciplina: Desenvolvimento Back-end**

---

## 👥 Integrantes

- Vitória Machado Silva

---

## 📖 Descrição do Tema

A coordenação do curso decidiu modernizar a forma como os alunos se apresentam dentro do ambiente acadêmico. Em vez da tradicional carteirinha estática, foi criado o **Cartão de Identidade Acadêmica digital**: um perfil no estilo "ficha de personagem", onde cada aluno é representado por informações centrais que descrevem quem ele é, sua situação no curso, seus dados de contato e seus interesses.

O projeto é um sistema acadêmico simples em **Django 6.1** para cadastro, listagem, edição e exclusão de alunos, com painel administrativo customizado **Data_Core / Admin**. Ele foi desenvolvido em duas etapas:

1. **Antes do CRUD** — modelagem inicial do aluno, estrutura do projeto e customização do painel administrativo.
2. **CRUD completo** — telas de listagem, criação, edição e exclusão, com busca e filtros, e expansão do modelo de dados para um cartão de identidade acadêmica completo (campos de texto, numéricos, booleanos e de data).

---

## 📸 Demonstração

![Dashboard Inicial de Alunos](img/img_capa_alunos.png)
![Registros Acadêmicos - Lista de Alunos](img/img_registros_alunos.png)
![Detalhes do Cartão de Identidade](img/img_detalhes_alunos.png)
![Painel Adicionar Aluno](img/img_aluno_cadastrarNovo.png)
![Painel Administrativo Data_Core](img/img_admin.png)


---

## 🛠 Tecnologias Utilizadas
- **Python 3.13**
- **Django 6.1**
- **SQLite** (incluso por padrão)
- **CSS** (Customização do Admin com `data-core-admin.css`)

---

## 🆕 Atualizações do Cartão de Identidade Acadêmica (etapa do CRUD)

A tela de registros acadêmicos e o modelo `Aluno` foram expandidos além da versão inicial (pré-CRUD). As principais adições:

### 🔍 Filtros e busca

A tela de listagem (`/aluno/`) ganhou uma barra de filtros acima da grade de alunos, permitindo refinar os registros por múltiplos critérios ao mesmo tempo:

- **Busca por nome ou matrícula** — campo de texto livre que localiza o aluno tanto pelo nome quanto pelo número de matrícula (`icontains` em `nome` e `matricula`).
- **Filtro por curso** — select preenchido dinamicamente com os cursos já cadastrados no banco.
- **Filtro por status** — select com as opções **Ativo**, **Trancado** e **Formado**.

Os filtros funcionam via `GET` (`?q=`, `?curso=`, `?status=`), então podem ser combinados entre si, compartilhados por link e continuam funcionando mesmo sem JavaScript. Quando nenhum resultado é encontrado, a tela diferencia "nenhum aluno cadastrado" de "nenhum resultado para esse filtro", já com um atalho para limpar os filtros.

### 🧾 Novos campos do Cartão de Identidade Acadêmica

O formulário de criação/edição de aluno ("Novo Aluno") foi ampliado para funcionar como um cartão de identidade completo, sem nenhum valor pré-preenchido — cada campo é digitado manualmente no cadastro. Os campos passaram a cobrir os principais tipos de dado:

| Campo | Tipo Django | Tipo de dado | Descrição |
| --- | --- | --- | --- |
| `nome` | `CharField` | Texto | Nome completo do aluno. |
| `matricula` | `CharField` | Texto | Número de matrícula (usado também na busca). |
| `email` | `CharField` | Texto | E-mail de contato do aluno. |
| `cpf` | `CharField` | Texto | CPF do aluno. |
| `curso` | `CharField` | Texto | Curso atual (ex: ADS, SI, Engenharia...). |
| `bio` | `TextField` | Texto | Breve descrição, interesses ou objetivos. |
| `status` | `CharField` (choices) | Texto | Situação do aluno: **Ativo**, **Trancado** ou **Formado**. |
| `semestre` | `IntegerField` | Numérico | Semestre atual do aluno. |
| `bolsista` | `BooleanField` | Booleano | Indica se o aluno é bolsista (Sim/Não). |
| `data_nascimento` | `DateField` | Data | Data de nascimento do aluno. |
| `criado_em` | `DateTimeField` | Data/Hora | Preenchido automaticamente no momento do cadastro. |

Ou seja, o modelo passou a contemplar, além dos campos de texto originais, um campo **numérico** (`semestre`), um campo **booleano** (`bolsista`) e campos de **data/data-hora** (`data_nascimento` e `criado_em`), cobrindo os principais tipos de dado usados em um cadastro acadêmico completo.

### 🖼️ Outras melhorias

- **Favicon** do projeto adicionado via arquivo estático (`img/favicon.png`), referenciado nos templates com `{% load static %}` / `{% static 'favicon.png' %}`.
- Proteção contra tradução automática do navegador (`translate="no"` + `meta name="google" content="notranslate"`) para preservar os textos originais da interface (ex: "Buscar", "Matrícula", "ID").

---

## 🗃️ Campos do Model `Aluno`

| Campo | Tipo Django | Regra | Descrição |
| --- | --- | --- | --- |
| `nome` | `CharField` | Obrigatório | Nome completo do aluno. |
| `matricula` | `CharField` | Opcional | Número de matrícula. |
| `email` | `CharField` | Opcional | E-mail de contato. |
| `cpf` | `CharField` | Opcional | CPF do aluno. |
| `curso` | `CharField` | Obrigatório | Curso atual (ex: ADS, SI, Engenharia...). |
| `semestre` | `IntegerField` | Obrigatório | Semestre atual (padrão: 1). |
| `status` | `CharField` (choices) | Obrigatório | Ativo, Trancado ou Formado (padrão: Ativo). |
| `bolsista` | `BooleanField` | Obrigatório | Aluno bolsista (padrão: Não). |
| `data_nascimento` | `DateField` | Opcional | Data de nascimento. |
| `bio` | `TextField` | Opcional | Breve descrição, interesses ou objetivos (limite sugerido: 280 caracteres). |
| `criado_em` | `DateTimeField` | Automático | Data e hora do cadastro. |

---

## 🚀 Instruções de Execução

### Pré-requisitos
- Python 3.13 instalado na máquina.

### Passo a passo

1. **Clonar o repositório e acessar a pasta do projeto**
   ```powershell
   git clone <url-do-repositorio>
   cd cartao-identidade-academica
   ```

2. **Criar ambiente virtual**
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. **Instalar dependências**
   ```powershell
   pip install django
   ```

4. **Criar projeto Django** *(pule este passo se o projeto já vier pronto no repositório)*
   ```powershell
   django-admin startproject core .
   ```

5. **Criar app aluno** *(pule este passo se o projeto já vier pronto no repositório)*
   ```powershell
   python manage.py startapp aluno
   ```

6. **Registrar app em settings.py**
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'aluno',
   ]
   ```

   Certifique-se também de que `STATICFILES_DIRS` inclui as pastas usadas pelo projeto (`static/` para o CSS do admin e `img/` para o favicon e demais imagens):
   ```python
   STATIC_URL = 'static/'

   STATICFILES_DIRS = [
       BASE_DIR / 'static',
       BASE_DIR / 'img',
   ]
   ```

7. **Configurar rotas**
   ```python
   # core/urls.py
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('aluno/', include("aluno.urls")),
   ]
   ```

   ```python
   # aluno/urls.py
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.aluno, name='listar_alunos'),
       path('novo/', views.criar_aluno, name='criar_aluno'),
       path('<int:pk>/editar/', views.editar_aluno, name='editar_aluno'),
       path('<int:pk>/excluir/', views.excluir_aluno, name='excluir_aluno'),
   ]
   ```

8. **Aplicar as migrações do banco de dados**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

9. **Registrar admin**
   ```python
   from django.contrib import admin
   from .models import Aluno

   admin.site.register(Aluno)
   ```

10. **(Opcional) Criar um superusuário para acessar o admin**
    ```powershell
    python manage.py createsuperuser
    ```

11. **Rodar o servidor**
    ```powershell
    python manage.py runserver
    ```

12. **Acessar no navegador**
    - Lista de alunos: `http://127.0.0.1:8000/aluno/`
    - Painel administrativo: `http://127.0.0.1:8000/admin/`

---

## 🌐 Endpoints

| Endpoint | Descrição |
| --- | --- |
| `/admin/` | Painel administrativo Django (customizado Data_Core) |
| `/aluno/` | Lista todos os alunos cadastrados |
| `/aluno/?q=&curso=&status=` | Lista filtrada por nome/matrícula, curso e/ou status |
| `/aluno/novo/` | Cadastra um novo aluno |
| `/aluno/<id>/editar/` | Edita um aluno existente |
| `/aluno/<id>/excluir/` | Confirma e exclui um aluno |
| `/admin/aluno/aluno/add/` *(via admin)* | Adiciona novo aluno pelo painel administrativo |
| `/admin/aluno/aluno/<id>/change/` | Edita aluno existente pelo painel administrativo |

---

## 📁 Estrutura do Projeto

```
cartao-identidade-academica/
│
├── aluno/
│   ├── templates/
│   │   ├── aluno.html
│   │   ├── confirmar_exclusao.html
│   │   └── form_aluno.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── core/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── img/
│   ├── favicon.png
│   ├── img_capa_alunos.png
│   ├── img_registros_alunos.png
│   ├── img_detalhes_alunos.png
│   ├── img_admin.png
│   ├── img_adicionar_aluno.png
│   └── img_aluno_cadastrado.png
│
├── static/
│   └── admin/
│       └── css/
│           └── data-core-admin.css
│
├── templates/
│   └── admin/
│       ├── base_site.html
│       └── index.html
│
├── venv/
│
├── .gitattributes
├── db.sqlite3
├── LICENSE
├── manage.py
└── README.md
```