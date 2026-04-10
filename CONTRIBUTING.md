# Contribuindo com o EstudaFlow

Obrigado pelo interesse! Veja abaixo como contribuir.

## Fluxo de trabalho

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
3. Implemente sua mudança e adicione testes
4. Garanta que lint e testes passam localmente:
   ```bash
   ruff check src/ tests/
   pytest
   ```
5. Faça commit seguindo o padrão Conventional Commits
6. Abra um Pull Request descrevendo a mudança

## Padrão de commits

```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
test: adiciona ou corrige testes
refactor: melhora código sem mudar comportamento
```
