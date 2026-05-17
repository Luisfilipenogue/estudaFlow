# Changelog

## [1.1.0] — Etapa Intermediária

### Adicionado
- Conversão da interface desktop (Tkinter) para aplicação web (Flask)
- Integração com a **Nager.Date API** para feriados nacionais brasileiros
- Página dedicada de feriados com seletor de ano
- Alerta automático quando prazo de tarefa coincide com feriado
- Testes de integração (mock da API + rotas Flask)
- Configuração de deploy no Render (`render.yaml`)
- `requirements.txt` com Flask e Gunicorn

### Alterado
- Versão bumped de `1.0.0` → `1.1.0`
- CI atualizado para instalar Flask e rodar novos testes

---

## [1.0.0] — Etapa Inicial

### Adicionado
- Interface gráfica Tkinter (dark mode, 3 abas)
- Gerenciamento de tarefas e disciplinas
- Persistência em JSON
- 25 testes automatizados com pytest
- Lint com Ruff
- Pipeline CI com GitHub Actions
