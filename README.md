# EstudaFlow 📚

> Organizador de estudos para estudantes com dificuldade de rotina

![Build](https://github.com/SEU_USUARIO/estudaflow/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.0.0-6C63FF)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Licença](https://img.shields.io/badge/licença-MIT-green)

---

## 🎯 O Problema

Muitos estudantes — especialmente os que conciliam trabalho, responsabilidades domésticas ou condições como TDAH e ansiedade — têm dificuldade em organizar suas tarefas acadêmicas. Sem um sistema de acompanhamento claro, prazos são esquecidos, disciplinas ficam desequilibradas e a sensação de descontrole prejudica o desempenho e o bem-estar.

## 💡 A Solução

**EstudaFlow** é um organizador de estudos com interface gráfica (GUI) que permite ao estudante:

- Cadastrar e gerenciar tarefas por disciplina
- Definir prazos e prioridades
- Marcar tarefas como concluídas
- Visualizar um resumo de progresso com alertas de atraso
- Organizar disciplinas com identificação por cor

Tudo salvo localmente em JSON — sem necessidade de conta, internet ou instalação complexa.

---

## 👥 Público-alvo

- Estudantes do ensino médio e superior
- Pessoas com dificuldade de organização de rotina
- Estudantes que conciliam trabalho e faculdade
- Pessoas neurodivergentes que se beneficiam de estrutura visual clara

---

## ✨ Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| **Gerenciar tarefas** | Criar, concluir e remover tarefas de estudo |
| **Disciplinas** | Cadastrar matérias com professor e cor |
| **Prazos e prioridades** | Definir data de entrega e nível de urgência |
| **Resumo visual** | Painel com total, concluídas, pendentes e atrasadas |
| **Persistência local** | Dados salvos em `~/.estudaflow/data.json` |

---

## 🛠 Tecnologias Utilizadas

- **Python 3.11+**
- **Tkinter** — GUI nativa (stdlib, sem instalação extra)
- **JSON** — armazenamento local
- **pytest** — testes automatizados
- **Ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)

---

## 📁 Estrutura do Projeto

```
estudaflow/
├── src/
│   ├── __init__.py
│   ├── app.py        # Interface gráfica (Tkinter)
│   ├── models.py     # Modelos de dados (Task, Subject)
│   └── storage.py    # Persistência em JSON
├── tests/
│   ├── __init__.py
│   └── test_estudaflow.py   # 18 testes automatizados
├── .github/
│   └── workflows/
│       └── ci.yml    # Pipeline GitHub Actions
├── main.py           # Ponto de entrada
├── pyproject.toml    # Manifesto, versão e configurações
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.11 ou superior
- Tkinter (já incluso no Python padrão; no Linux pode ser necessário instalar)

```bash
# Linux (Ubuntu/Debian)
sudo apt install python3-tk

# macOS — já incluso no Python oficial
# Windows — já incluso no Python oficial
```

### Clonando o repositório

```bash
git clone https://github.com/Luisfilipenogue/estudaFlow.git
cd estudaflow
```

### Instalando dependências de desenvolvimento

```bash
pip install -e ".[dev]"
```

> As dependências de produção são **zero** — o EstudaFlow usa apenas a stdlib do Python.  
> As dependências de desenvolvimento (`pytest`, `pytest-cov`, `ruff`) são instaladas com o comando acima.

---

## ▶️ Execução

```bash
python main.py
```

A janela do EstudaFlow abrirá automaticamente.

---

## 🧪 Rodando os Testes

```bash
pytest
```

Para ver cobertura de código:

```bash
pytest --cov=src --cov-report=term-missing
```

O projeto possui **18 testes automatizados** cobrindo:

- Criação e serialização de modelos (`Task`, `Subject`)
- Adição, remoção e alternância de tarefas
- Validação de entradas inválidas (título vazio, índice fora do intervalo)
- Filtros por disciplina e status
- Persistência (salvar, carregar, arquivo corrompido, diretório inexistente)

---

## 🔍 Rodando o Lint

```bash
ruff check src/ tests/
```

Para verificar formatação:

```bash
ruff format --check src/ tests/
```

Para corrigir automaticamente:

```bash
ruff format src/ tests/
```

---

## 🔄 Pipeline de CI (GitHub Actions)

A cada `push` ou `pull request`, o GitHub Actions executa automaticamente:

1. Instalação do ambiente Python (3.11 e 3.12)
2. Instalação das dependências de dev
3. Lint com Ruff
4. Verificação de formatação com Ruff
5. Testes com `pytest` + cobertura

Arquivo: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

---

## 📦 Versionamento

Este projeto segue o padrão **Semantic Versioning** ([semver.org](https://semver.org)):

```
MAJOR.MINOR.PATCH
```

**Versão atual: `1.0.0`**

Veja o histórico completo em [CHANGELOG.md](CHANGELOG.md).

---

## 🖥️ Exemplo de Uso

```
1. Abra o app: python main.py
2. Vá até a aba "Disciplinas" → cadastre suas matérias (ex: Matemática, Física)
3. Vá até a aba "Tarefas" → adicione tarefas vinculadas às disciplinas
4. Defina prazo e prioridade
5. Conforme conclui, marque como ✔ Concluída
6. Na aba "Resumo" acompanhe seu progresso e veja tarefas atrasadas
```

---

## 👤 Autor

**Luis Filipe Nogueira de Moraes Araujo**  
Disciplina: Bootcamp II  
Repositório: [https://github.com/Luisfilipenogue/estudaFlow](https://github.com/Luisfilipenogue/estudaFlow)

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
