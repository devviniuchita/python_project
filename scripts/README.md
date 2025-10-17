# 🔧 Scripts Utilitários

Este diretório contém scripts utilitários para manutenção, automação e documentação do projeto Python RAG.

---

## 📋 Scripts Disponíveis

### 1️⃣ **add_copyright_headers.py** 📝

Adiciona headers de copyright automaticamente em arquivos do projeto.

**Uso**:

```bash
python scripts/add_copyright_headers.py
```

**O que faz**:

- ✅ Varre todos os arquivos `.py` do projeto
- ✅ Adiciona header de copyright conforme o padrão do projeto
- ✅ Respeita arquivos que já possuem copyright
- ✅ Integra com a **Camada 3** do sistema de proteção

**Requisitos**:

- Python 3.8+

**Integração**:

- Executado automaticamente pelo git hook `.githooks/pre-commit`
- Pode ser executado manualmente a qualquer hora

---

### 2️⃣ **generate_tree.py** 🌳

Gera uma visualização em Markdown da arquitetura completa do projeto.

**Uso**:

```bash
python scripts/generate_tree.py
```

**O que faz**:

- ✅ Cria árvore visual da estrutura de pastas
- ✅ Inclui ícones para melhor visualização
- ✅ Mostra tamanho de arquivos
- ✅ Ignora pastas desnecessárias (.git, **pycache**, .venv, etc.)
- ✅ Gera markdown com legendas
- ✅ Cria/atualiza `PROJECT_STRUCTURE.md`

**Saída**:

```
PROJECT_STRUCTURE.md  # Visualização completa da arquitetura
```

**Requisitos**:

- Python 3.8+

**Quando usar**:

- Após modificações significativas na estrutura de pastas
- Para documentar nova organização
- Para compartilhar com o time a estrutura atualizada

---

### 3️⃣ **benchmark_reranking.py** 📊

Testes de benchmark para o módulo de re-ranking.

**Uso**:

```bash
python scripts/benchmark_reranking.py
```

**Funcionalidade**: Avalia performance do sistema de re-ranking.

---

### 4️⃣ **chat.py** 💬

Script interativo para testar conversas com o sistema RAG.

**Uso**:

```bash
python scripts/chat.py
```

**Funcionalidade**: Interface de chat para testes do RAG.

---

### 5️⃣ **migrate_imports.py** 🔄

Script para migração de imports e refatoração de código.

**Uso**:

```bash
python scripts/migrate_imports.py
```

---

### 6️⃣ **recreate_faiss.py** 🗄️

Recria o índice FAISS do banco de dados vetorial.

**Uso**:

```bash
python scripts/recreate_faiss.py
```

**Funcionalidade**: Reconstrói índices de busca vetorial.

---

### 7️⃣ **run_threshold_tests.py** 🎯

Executa testes com diferentes thresholds de relevância.

**Uso**:

```bash
python scripts/run_threshold_tests.py
```

**Funcionalidade**: Testa diferentes configurações de thresholds.

---

## 🎯 Como Executar Scripts

### Via Terminal Direto:

```bash
cd C:/Users/ADMIN/Desktop/python_project
python scripts/generate_tree.py
```

### Via VSCode:

1. Abra o terminal integrado (`Ctrl + `` `)
2. Execute: `python scripts/nome_do_script.py`

### Via Git Hooks (Automático):

```bash
# Alguns scripts executam automaticamente
git commit  # Dispara pre-commit hook
```

---

## 🔒 Integração com Sistema de Proteção

### Camada 3 - Proteção Local

Os scripts em `scripts/` são parte da **Camada 3** do sistema de proteção de copyright:

- ✅ **add_copyright_headers.py** - Adiciona headers automaticamente
- ✅ Integrado com `.githooks/pre-commit`
- ✅ Parte da validação de commits

### Uso nos Git Hooks:

```bash
# .githooks/pre-commit
python scripts/add_copyright_headers.py
```

---

## 📝 Estrutura dos Scripts

Cada script deve seguir o padrão:

```python
#!/usr/bin/env python3
"""
Descrição breve do script
"""

import sys
from pathlib import Path

# Adicionar caminho do projeto
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    """Função principal"""
    print("Executando script...")
    # Implementação aqui
    print("✅ Concluído!")

if __name__ == '__main__':
    main()
```

---

## 🛠️ Adicionando Novo Script

Ao criar um novo script:

1. ✅ Salve em `scripts/`
2. ✅ Siga o padrão de nomenclatura: `operation_name.py`
3. ✅ Adicione header de copyright
4. ✅ Inclua docstring no início do arquivo
5. ✅ Use `if __name__ == '__main__':` para executável
6. ✅ Atualize este README com documentação

---

## 🔗 Referências

- 📚 [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) - Arquitetura completa
- 🛡️ [docs/COPYRIGHT_PROTECTION.md](../docs/COPYRIGHT_PROTECTION.md) - Sistema de proteção
- 🔧 [.githooks/](../.githooks/) - Git hooks automáticos

---

## 📋 Checklist para Novo Script

- [ ] Arquivo criado em `scripts/`
- [ ] Headers de copyright adicionados
- [ ] Docstring no início do arquivo
- [ ] Função `main()` implementada
- [ ] `if __name__ == '__main__':` configurado
- [ ] README.md atualizado
- [ ] Testado localmente
- [ ] Commit com DCO sign-off: `git commit -s`

---

**Última atualização**: 17 de Outubro de 2025
**Versão**: 1.0.0
**Status**: ✅ Active
