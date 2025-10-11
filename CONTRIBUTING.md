<div align="center">

# 🚀 Guia de Contribuição

> **Bem-vindo!** Obrigado por seu interesse em contribuir para o **Python RAG Project**. Juntos, estamos construindo um sistema RAG de classe enterprise com as melhores práticas da indústria.

[![Contributors](https://img.shields.io/github/contributors/devviniuchita/python_project?style=for-the-badge&color=brightgreen)](https://github.com/devviniuchita/python_project/graphs/contributors)
[![Pull Requests](https://img.shields.io/github/issues-pr/devviniuchita/python_project?style=for-the-badge&color=blue)](https://github.com/devviniuchita/python_project/pulls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## 📚 Navegação Rápida

- [💖 Bem-vindo à Nossa Comunidade](#-bem-vindo-à-nossa-comunidade)
- [📜 Governança & Regras](#-governança--regras)
- [🤝 Como Contribuir](#-como-contribuir)
- [⚡ Padrões Técnicos](#-padrões-técnicos)
- [🧪 Requisitos de Teste](#-requisitos-de-teste)
- [🎯 Checklist do Pull Request](#-checklist-do-pull-request)
- [🌟 Reconhecimento](#-reconhecimento)

---

## 💖 Bem-vindo à Nossa Comunidade

Python RAG Project é mais que código — é um **movimento em direção a sistemas RAG de produção**. Seja corrigindo um bug, adicionando uma funcionalidade ou melhorando a documentação, cada contribuição conta.

### 🌟 Nossa Visão

Criar um **sistema RAG completo e escalável** com:

- 🧠 Reranking semântico inteligente
- 📊 Logging estruturado e observabilidade
- 🔍 Integração LangSmith para debugging
- ⚡ Performance otimizada (<500ms end-to-end)
- 🏗️ Arquitetura src-layout profissional

---

## 📜 Governança & Regras

Antes de contribuir, conheça nossas políticas:

### 📋 Documentos de Governança

| Documento                    | Descrição                                          | Link                                                         |
| ---------------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| **🤝 Código de Conduta**     | Padrões de comportamento respeitoso e inclusivo    | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)                     |
| **🔒 Segurança**             | Reporte vulnerabilidades de forma responsável      | [SECURITY.md](SECURITY.md)                                   |
| **📄 Licença**               | MIT License - uso livre com atribuição             | [LICENSE](LICENSE)                                           |
| **📜 NOTICE**                | Requisitos de atribuição Apache-style obrigatórios | [NOTICE](NOTICE)                                             |
| **📚 CITATION.cff**          | Como citar este projeto academicamente             | [CITATION.cff](CITATION.cff)                                 |
| **✍️ DCO**                   | Developer Certificate of Origin v1.1               | [.github/DCO](.github/DCO)                                   |
| **🛡️ Proteção de Copyright** | Guia completo de proteção e licenciamento          | [docs/COPYRIGHT_PROTECTION.md](docs/COPYRIGHT_PROTECTION.md) |
| **🔐 Assinatura GPG**        | Como assinar commits com GPG                       | [docs/GPG_SIGNING.md](docs/GPG_SIGNING.md)                   |
| **📋 TODO2 System**          | Sistema de gerenciamento de tarefas do projeto     | `.todo2/state.todo2.json`                                    |

**Pontos Importantes**:

- 🤝 **Respeito**: Siga o Código de Conduta em todas as interações
- 🔒 **Segurança**: Reporte vulnerabilidades via canais privados
- 📋 **Workflow**: Use TODO2 para rastrear progresso de tarefas
- ✅ **Quality**: Todos os PRs passam por code review obrigatório
- ✍️ **DCO**: Todos os commits DEVEM ter Developer Certificate of Origin sign-off

### ✍️ Developer Certificate of Origin (DCO) - OBRIGATÓRIO

**Este projeto requer DCO sign-off em TODOS os commits.**

#### 🎯 O que é DCO?

O Developer Certificate of Origin é uma certificação leve que confirma que você:

1. ✅ **Criou a contribuição** ou tem direito de submetê-la sob a licença do projeto
2. ✅ **Entende e concorda** que a contribuição seja pública e permanente
3. ✅ **Tem direitos legais** para fazer a contribuição sob a licença MIT
4. ✅ **Aceita** que o projeto pode redistribuir seu código sob a licença MIT

Texto completo do DCO: [.github/DCO](.github/DCO)

#### 📝 Como Fazer Sign-off

**Método 1: Flag `-s` no commit** (Recomendado)

```bash
# Fazer commit com DCO sign-off
git commit -s -m "feat: adicionar nova funcionalidade"

# Isso adiciona automaticamente:
# Signed-off-by: Seu Nome <seu.email@exemplo.com>
```

**Método 2: Amend em commit já feito**

```bash
# Adicionar sign-off ao último commit
git commit --amend --signoff

# Adicionar sign-off e manter mensagem
git commit --amend --signoff --no-edit
```

**Método 3: Rebase para múltiplos commits**

```bash
# Adicionar sign-off em múltiplos commits
git rebase HEAD~3 --signoff

# Forçar push (necessário após rebase)
git push --force-with-lease
```

#### ⚙️ Configurar Git Automaticamente

```bash
# Configurar nome e email (usado no sign-off)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"

# Criar alias para commit com sign-off automático
git config --global alias.cs 'commit -s'

# Agora use: git cs -m "sua mensagem"
```

#### ✅ Verificar Sign-off

```bash
# Ver último commit com sign-off
git log -1

# Verificar se tem "Signed-off-by:"
git log --format='%h %s%n%b' -1
```

#### 🚫 O que Acontece Sem DCO?

- ❌ **GitHub Action falhará**: `dco-check.yml` bloqueia PRs sem DCO
- ❌ **PR não será aceito**: Revisor solicitará correção
- ❌ **CI/CD bloqueado**: Pipeline não prosseguirá

#### 🛠️ Git Hooks Automáticos

O projeto possui hooks que validam DCO:

```bash
# Ativar hooks locais (recomendado)
git config core.hooksPath .githooks
chmod +x .githooks/*  # Linux/macOS

# Hooks disponíveis:
# - .githooks/commit-msg: Valida DCO e formato Conventional Commits
# - .githooks/pre-commit: Valida copyright headers e formata código
```

#### 📚 Recursos Adicionais

- **DCO Oficial**: [developercertificate.org](https://developercertificate.org/)
- **Linux Foundation DCO**: [GitHub Apps](https://github.com/apps/dco)
- **Nosso DCO**: [.github/DCO](.github/DCO)

---

## 🤝 Como Contribuir

### 🐛 Reportando Bugs

Encontrou um problema? Ajude-nos a corrigi-lo:

**Template de Bug Report**:

```markdown
**🐛 Descrição do Bug**
Descrição clara e concisa do problema

**📋 Passos para Reproduzir**

1. Configure ambiente com...
2. Execute comando...
3. Observe erro...

**✅ Comportamento Esperado**
O que deveria acontecer

**❌ Comportamento Atual**
O que realmente acontece

**💻 Ambiente**

- OS: [Windows/Linux/macOS]
- Python: [versão]
- Dependências: [requirements.txt]

**📸 Screenshots/Logs**
Se aplicável, adicione capturas de tela ou logs
```

### 💡 Sugerindo Funcionalidades

Tem uma ideia? Adoraríamos ouvi-la!

**Template de Feature Request**:

```markdown
**🎯 Solicitação de Funcionalidade**
Título descritivo e claro

**❓ Problema que Resolve**
Que problema ou limitação isso endereça?

**💡 Solução Proposta**
Descreva sua abordagem sugerida

**🔄 Alternativas Consideradas**
Outras opções que você pensou

**📊 Impacto**
Como isso beneficiará os usuários?

**📝 Implementação (Opcional)**
Esboço técnico de como implementar
```

### 🔧 Seu Primeiro Pull Request

Pronto para codificar? Siga este workflow:

```bash
# 1. Fork do repositório no GitHub

# 2. Clone seu fork
git clone https://github.com/SEU_USUARIO/python_project.git
cd python_project

# 3. Configure upstream
git remote add upstream https://github.com/devviniuchita/python_project.git

# 4. Crie branch da feature
git checkout -b feature/nome-da-feature

# 5. Configure ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 6. Instale dependências
pip install -r requirements.txt

# 7. Ative git hooks (IMPORTANTE!)
git config core.hooksPath .githooks
chmod +x .githooks/*  # Linux/macOS

# 8. Adicione copyright headers em arquivos novos
python scripts/add_copyright_headers.py src/ --dry-run
python scripts/add_copyright_headers.py src/  # Aplicar

# 9. Faça suas alterações seguindo padrões do projeto

# 10. Execute testes
pytest tests/
python scripts/run_threshold_tests.py

# 11. Formate código
black src/ tests/
isort src/ tests/
flake8 src/ tests/

# 12. Commit com DCO sign-off (OBRIGATÓRIO!)
git commit -s -m "feat: adicionar clustering semântico ao reranker"

# 13. Push para seu fork
git push origin feature/nome-da-feature

# 14. Abra Pull Request no GitHub
```

**📝 Nota Importante**: O passo 12 usa `-s` para DCO sign-off. Sem isso, o PR será rejeitado!

### 📚 Melhorando Documentação

A documentação é crucial:

- ✅ Corrigir erros de digitação e gramática
- ✅ Melhorar clareza de explicações
- ✅ Adicionar exemplos práticos
- ✅ Atualizar informações desatualizadas
- ✅ Criar tutoriais para casos de uso
- ✅ Traduzir conteúdo (PT-BR ↔ EN)

---

## ⚡ Padrões Técnicos

### 🏗️ Arquitetura do Projeto

Siga a estrutura **src-layout**:

```
python_project/
├── src/                          # Código fonte
│   ├── core/                     # Lógica de negócio
│   │   ├── domain/              # Modelos de domínio
│   │   ├── services/            # Serviços
│   │   └── repositories/        # Acesso a dados
│   ├── features/                # Funcionalidades
│   │   ├── rag/                 # RAG system
│   │   ├── conversation/        # Gestão de conversação
│   │   └── reranking/           # Reranking BGE
│   ├── infrastructure/          # Infraestrutura
│   │   ├── config/             # Configuração
│   │   ├── database/           # Banco de dados
│   │   ├── logging/            # Logging estruturado
│   │   └── external/           # APIs externas
│   └── shared/                  # Utilitários
└── tests/                       # Testes
    ├── unit/                   # Testes unitários
    ├── integration/            # Testes de integração
    └── e2e/                    # Testes end-to-end
```

### 📋 Convenções de Código

**Python Style Guide**:

```python
# ✅ Boas Práticas

# 1. Type hints obrigatórios
def rerank_documents(
    query: str,
    documents: List[str],
    threshold: float = 0.5
) -> List[Tuple[str, float]]:
    """
    Rerank documents using BGE cross-encoder.

    Args:
        query: Search query
        documents: List of documents to rerank
        threshold: Minimum relevance score (default: 0.5)

    Returns:
        List of (document, score) tuples above threshold
    """
    pass

# 2. Docstrings em Google Style
# 3. Imports organizados (isort)
from typing import List, Tuple

import numpy as np
from langchain.schema import Document

from src.core.services import reranker

# 4. Nomenclatura clara
class BGERerankerService:  # PascalCase para classes
    def __init__(self):
        self.model_name = "BAAI/bge-reranker-base"  # snake_case para variáveis

    def score_documents(self):  # snake_case para métodos
        pass

# 5. Logging estruturado
import structlog

logger = structlog.get_logger(__name__)
logger.info("reranking_completed", num_docs=10, avg_score=0.85)
```

**Formatação**:

```bash
# Black (formatação automática)
black src/ tests/ --line-length 88

# isort (organização de imports)
isort src/ tests/ --profile black

# flake8 (linting)
flake8 src/ tests/ --max-line-length 88 --extend-ignore E203,W503

# mypy (type checking)
mypy src/ --strict
```

### 📝 Convenções de Commit

Seguimos **Conventional Commits**:

```bash
# Formato
<tipo>(<escopo>): <descrição>

# Tipos
feat:      # Nova funcionalidade
fix:       # Correção de bug
docs:      # Documentação
test:      # Testes
refactor:  # Refatoração sem mudança de funcionalidade
perf:      # Melhoria de performance
chore:     # Manutenção (deps, config)
style:     # Formatação (sem mudança de código)

# Exemplos
feat(reranker): adicionar threshold adaptativo baseado em percentil
fix(logging): corrigir serialização de numpy arrays em JSON
docs(readme): atualizar instruções de instalação
test(integration): adicionar testes E2E para workflow RAG completo
refactor(nodes): extrair lógica de reranking para service layer
perf(faiss): otimizar busca vetorial com IVF index
chore(deps): atualizar langchain para v0.1.0
```

---

## 🧪 Requisitos de Teste

### 🎯 Cobertura Mínima

| Categoria       | Cobertura Mínima | Comandos                                |
| --------------- | ---------------- | --------------------------------------- |
| **Unit Tests**  | 80%              | `pytest tests/unit/ --cov=src`          |
| **Integration** | 70%              | `pytest tests/integration/`             |
| **E2E**         | 60%              | `pytest tests/e2e/`                     |
| **Performance** | -                | `python scripts/run_threshold_tests.py` |

### ✅ Tipos de Teste Obrigatórios

**1. Testes Unitários** (para toda nova lógica):

```python
# tests/unit/test_reranker.py
import pytest
from src.features.reranking.reranker import rerank_documents

def test_rerank_filters_by_threshold():
    """Testa filtro por threshold de relevância."""
    query = "What is Python?"
    documents = [
        "Python is a programming language",
        "Java is also a language",
        "Completely unrelated text"
    ]

    results = rerank_documents(query, documents, threshold=0.6)

    assert len(results) <= len(documents)
    assert all(score >= 0.6 for _, score in results)
    assert results[0][1] > results[-1][1]  # Ordenação decrescente
```

**2. Testes de Integração** (para fluxos completos):

```python
# tests/integration/test_rag_workflow.py
def test_full_rag_workflow():
    """Testa workflow RAG completo: retrieve → rerank → generate."""
    # Setup
    query = "Como funciona RAG?"

    # Execute
    response = execute_rag_workflow(query)

    # Assert
    assert response["answer"] is not None
    assert len(response["sources"]) > 0
    assert all(s["score"] >= 0.5 for s in response["sources"])
    assert response["latency_ms"] < 500  # Performance SLA
```

**3. Testes de Performance** (para componentes críticos):

```python
# scripts/run_threshold_tests.py
def benchmark_reranking_performance():
    """Benchmark de performance do reranking."""
    import time

    # Setup
    query = "test query"
    documents = generate_test_documents(100)

    # Benchmark
    start = time.time()
    results = rerank_documents(query, documents)
    elapsed_ms = (time.time() - start) * 1000

    # Assert SLAs
    assert elapsed_ms < 200  # <200ms para 100 docs
    assert len(results) > 0
```

### 🔍 Executando Testes

```bash
# Todos os testes com cobertura
pytest tests/ --cov=src --cov-report=html

# Testes específicos
pytest tests/unit/test_reranker.py -v
pytest tests/integration/ -v --log-cli-level=INFO

# Testes de performance
python scripts/run_threshold_tests.py

# Com marcadores
pytest -m "not slow"  # Pula testes lentos
pytest -m integration  # Só integração
```

---

## 🎯 Checklist do Pull Request

Antes de enviar seu PR, verifique:

### ✅ Checklist Obrigatório

- [ ] **Código segue style guide** (Black, isort, flake8)
- [ ] **Type hints adicionados** em todas as funções novas
- [ ] **Docstrings completas** (Google Style)
- [ ] **Testes unitários** com cobertura >80%
- [ ] **Testes de integração** para fluxos novos
- [ ] **Performance validada** (SLAs atendidos)
- [ ] **Documentação atualizada** (README, docs/)
- [ ] **Changelog atualizado** (se aplicável)
- [ ] **Commits seguem Conventional Commits**
- [ ] **Sem breaking changes** (ou justificados)
- [ ] **CI/CD pipeline passou** (GitHub Actions)

### 📝 Template de Pull Request

````markdown
## 📋 Descrição

Descrição clara e concisa das mudanças

## 🎯 Motivação e Contexto

Por que essas mudanças são necessárias?

## 🔗 Issue Relacionada

Fixes #123

## 🧪 Como Foi Testado?

- [ ] Testes unitários adicionados
- [ ] Testes de integração adicionados
- [ ] Teste manual realizado
- [ ] Performance benchmarked

**Comandos executados:**

```bash
pytest tests/unit/test_nova_feature.py -v
python scripts/run_threshold_tests.py
```
````

## 📸 Screenshots (se aplicável)

Adicione screenshots se houver mudanças visuais

## 📊 Impacto de Performance

| Métrica            | Antes   | Depois  | Mudança |
| ------------------ | ------- | ------- | ------- |
| Latência Reranking | 150ms   | 120ms   | -20%    |
| Throughput         | 100 q/s | 125 q/s | +25%    |

## 🔍 Checklist

- [ ] Código segue style guide
- [ ] Testes adicionados (cobertura >80%)
- [ ] Documentação atualizada
- [ ] Performance validada
- [ ] Breaking changes documentadas

```

---

## 🌟 Reconhecimento

### 🏆 Hall da Fama de Contribuidores

Celebramos todos os contribuidores! Contribuições destacadas incluem:

| Tipo de Contribuição    | Reconhecimento                       |
| ----------------------- | ------------------------------------ |
| 🌟 **Primeira PR**      | Badge "First PR" no perfil           |
| 🐛 **Bug Critical Fix** | Menção em Release Notes              |
| ✨ **Feature Major**    | Destaque na documentação             |
| 📚 **Documentação**     | Agradecimentos especiais             |
| 🧪 **Testes**           | Badge "Test Champion"                |
| 🎨 **UI/UX**            | Showcase em exemplos                 |

### 📞 Obter Ajuda

Precisa de assistência?

- 💬 **GitHub Discussions**: Perguntas gerais e ideias
- 🐛 **Issues**: Bugs e feature requests
- 📧 **Email**: viniciusuchita@gmail.com
- 💼 **LinkedIn**: [Vinícius Uchita](https://www.linkedin.com/in/viniciusuchita/)

---

## 📄 Código de Conduta

Estamos comprometidos em fornecer um ambiente acolhedor. Leia nosso [Código de Conduta](CODE_OF_CONDUCT.md).

**Em Resumo**:

| ✅ Faça                          | ❌ Não Faça                      |
| -------------------------------- | -------------------------------- |
| Seja respeitoso e inclusivo      | Linguagem ofensiva               |
| Ajude novatos                    | Assédio ou bullying              |
| Foque no melhor para a comunidade | Ataques pessoais                |
| Mostre empatia                   | Compartilhar informações privadas |

---

## 📚 Ferramentas e Padrões Utilizados

Este projeto segue padrões reconhecidos da indústria e utiliza ferramentas modernas:

### 🔧 Ferramentas de Desenvolvimento

<div align="center">

| Ferramenta | Descrição | Documentação |
|------------|-----------|--------------|
| **Black** | Formatador automático de código Python (PEP 8) | [black.readthedocs.io](https://black.readthedocs.io/) |
| **isort** | Organizador inteligente de imports | [pycqa.github.io/isort](https://pycqa.github.io/isort/) |
| **flake8** | Linter para verificação de estilo | [flake8.pycqa.org](https://flake8.pycqa.org/) |
| **mypy** | Type checker estático para Python | [mypy-lang.org](https://mypy-lang.org/) |
| **pytest** | Framework de testes robusto | [docs.pytest.org](https://docs.pytest.org/) |
| **pre-commit** | Framework para git hooks | [pre-commit.com](https://pre-commit.com/) |

</div>

### 📋 Padrões e Convenções

<div align="center">

| Padrão | Descrição | Link Oficial |
|--------|-----------|--------------|
| **Conventional Commits** | Especificação para mensagens de commit | [conventionalcommits.org](https://www.conventionalcommits.org/) |
| **Google Python Style Guide** | Guia de estilo para docstrings e código | [google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html) |
| **Semantic Versioning** | Versionamento semântico (MAJOR.MINOR.PATCH) | [semver.org](https://semver.org/) |
| **Keep a Changelog** | Formato de changelog | [keepachangelog.com](https://keepachangelog.com/) |
| **Contributor Covenant** | Código de conduta padrão | [contributor-covenant.org](https://www.contributor-covenant.org/) |

</div>

### 🏗️ Arquitetura e Design

- **src-layout**: [setuptools.pypa.io/en/latest/userguide/package_discovery.html](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html)
- **Clean Architecture**: Martin, Robert C. - "Clean Architecture: A Craftsman's Guide to Software Structure and Design"
- **SOLID Principles**: [wikipedia.org/wiki/SOLID](https://en.wikipedia.org/wiki/SOLID)

### 📖 Referências Python

- **PEP 8 - Style Guide**: [peps.python.org/pep-0008](https://peps.python.org/pep-0008/)
- **PEP 484 - Type Hints**: [peps.python.org/pep-0484](https://peps.python.org/pep-0484/)
- **PEP 257 - Docstring Conventions**: [peps.python.org/pep-0257](https://peps.python.org/pep-0257/)

---

## 🎉 Obrigado!

Cada contribuição torna este projeto melhor. Obrigado por fazer parte desta jornada!

**Pronto para contribuir?** 🚀

- [Abra sua primeira issue](../../issues/new)
- [Envie um pull request](../../compare)
- [Junte-se às discussões](../../discussions)

---

**Última Atualização**: Janeiro 2025
**Mantenedores**: [@devviniuchita](https://github.com/devviniuchita)
```
