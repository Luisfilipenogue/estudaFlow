# EstudaFlow 📚

> Organizador de estudos para estudantes com dificuldade de rotina

![Build](https://github.com/Luisfilipenogue/estudaFlow/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.1.0-7C6FFF)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Licença](https://img.shields.io/badge/licença-MIT-green)

**🌐 Deploy:** https://estudaflow.onrender.com

---

## 🎯 O Problema

Muitos estudantes têm dificuldade em organizar suas tarefas acadêmicas, especialmente os que conciliam trabalho, responsabilidades domésticas ou condições como TDAH e ansiedade. Sem um sistema claro, prazos são esquecidos e disciplinas ficam desequilibradas.

## 💡 A Solução

**EstudaFlow** é um organizador de estudos com interface web que permite:

- Cadastrar e gerenciar tarefas por disciplina
- Definir prazos e prioridades
- Marcar tarefas como concluídas
- Visualizar painel de progresso com alertas de atraso
- **Consultar feriados nacionais brasileiros via API** e ser alertado quando um prazo cai em feriado

---

## ✨ Novidade v1.1.0 — Integração com API de Feriados

O EstudaFlow agora consome a [**Nager.Date API**](https://date.nager.at) para listar os feriados nacionais do Brasil. Quando o prazo de uma tarefa coincide com um feriado, um aviso é exibido automaticamente — ajudando o estudante a replanejar com antecedência.

**Endpoint utilizado:**
```
GET https://date.nager.at/api/v3/PublicHolidays/{year}/BR
```

---

## 👥 Público-alvo

Estudantes do ensino médio e superior, especialmente os que conciliam trabalho, estudo e têm dificuldade de organização de rotina.

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| **Gerenciar tarefas** | Criar, concluir e remover tarefas |
| **Disciplinas** | Cadastrar matérias com professor e cor |
| **Prazos e prioridades** | Data de entrega e urgência |
| **Dashboard** | Painel com estatísticas gerais |
| **Feriados BR** | Listagem e alerta automático via API |
| **Persistência local** | Dados salvos em JSON |

---

## 🛠 Tecnologias

- **Python 3.11+**
- **Flask 3.0** — framework web
- **Jinja2** — templates HTML
- **Nager.Date API** — feriados brasileiros (sem autenticação)
- **pytest** — testes (unitários + integração)
- **Ruff** — linting e análise estática
- **GitHub Actions** — CI/CD
- **Render** — deploy em nuvem

---

## 📁 Estrutura do Projeto

```
estudaflow/
├── src/
│   ├── __init__.py
│   ├── models.py      # Modelos Task e Subject
│   ├── storage.py     # Persistência JSON
│   └── holidays.py    # Integração API Nager.Date
├── templates/
│   ├── base.html
│   ├── index.html     # Dashboard
│   ├── tarefas.html
│   ├── disciplinas.html
│   └── feriados.html
├── tests/
│   ├── test_estudaflow.py   # Testes unitários (25)
│   └── test_integration.py  # Testes de integração (20+)
├── .github/workflows/ci.yml
├── app.py             # Aplicação Flask
├── pyproject.toml     # Versão 1.1.0 e config
├── requirements.txt   # Flask + Gunicorn
├── render.yaml        # Config deploy Render
└── README.md
```

---

## ⚙️ Instalação e Execução Local

```bash
# 1. Clone o repositório
git clone https://github.com/Luisfilipenogue/estudaFlow.git
cd estudaFlow

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o servidor
python app.py
```

Acesse em: **http://localhost:5000**

---

## 🧪 Rodando os Testes

```bash
pip install pytest pytest-cov
pytest
```

Com cobertura:
```bash
pytest --cov=src --cov-report=term-missing
```

---

## 🔍 Rodando o Lint

```bash
pip install ruff
ruff check src/ tests/ app.py
ruff format --check src/ tests/ app.py
```

---

## 🚀 Deploy no Render

1. Faça fork/push do repositório para o GitHub
2. Acesse [render.com](https://render.com) e crie uma conta gratuita
3. Clique em **New → Web Service**
4. Conecte seu repositório GitHub
5. O Render detecta automaticamente o `render.yaml`
6. Clique em **Deploy** — em alguns minutos o link estará disponível
7. Cole o link no topo deste README

---

## 🔄 Pipeline CI (GitHub Actions)

A cada `push` ou `pull request` o GitHub Actions executa:

1. Instalação do ambiente (Python 3.11 e 3.12)
2. Instalação das dependências
3. Lint com Ruff
4. Verificação de formatação
5. Testes unitários + integração com cobertura

---

## 📦 Versionamento

| Versão | O que mudou |
|--------|-------------|
| **1.1.0** | Conversão para Flask (web), integração API Nager.Date, testes de integração, deploy Render |
| **1.0.0** | Versão desktop Tkinter, testes unitários, CI, lint |

---

## 👤 Autor

**Luis Filipe Nogueira de Moraes Araujo**  
Disciplina: Bootcamp II  
Repositório: [https://github.com/Luisfilipenogue/estudaFlow](https://github.com/Luisfilipenogue/estudaFlow)

---

## 📄 Licença

[MIT License](LICENSE)
