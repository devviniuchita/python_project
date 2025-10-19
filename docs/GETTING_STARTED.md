# 🚀 Getting Started Guide - Python RAG Project

**Tempo estimado: 30 minutos**

Este guia fornece um caminho rápido e estruturado para configurar, executar e contribuir com o Python RAG Project. Se você é um desenvolvedor novo no projeto, siga estas etapas para estar pronto em menos de 30 minutos.

---

## 📋 1. Prerequisites (5 minutos)

### Requisitos de Sistema

- **Python 3.8+** (recomendado: Python 3.10 ou 3.12)
  - Verificar: `python --version`
  - Download: [python.org/downloads](https://www.python.org/downloads/)

- **Git** para controle de versão
  - Verificar: `git --version`
  - Download: [git-scm.com](https://git-scm.com/)

- **pip** (gerenciador de pacotes Python)
  - Verificar: `pip --version`
  - Incluído com Python 3.4+

### Credenciais de API (Obrigatórias)

1. **Google Cloud API Key** (para Gemini LLM e Embeddings)
   - Acesse: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Crie uma API key gratuita
   - Guarde para uso no arquivo `.env`

2. **LangSmith API Key** (opcional, mas recomendado para observabilidade)
   - Acesse: [smith.langchain.com](https://smith.langchain.com/)
   - Crie conta gratuita e obtenha API key
   - Guarde para uso no arquivo `.env`

### Ferramentas Recomendadas

- **VS Code** com extensões:
  - Python (Microsoft)
  - Pylance (análise de tipos)
  - Black Formatter
  - isort (organização de imports)

📖 **Referência**: [Architectural Guidelines](../.github/copilot-rules/project-rules.md#clean-architecture) para entender a estrutura de camadas do projeto.

---

## 📂 2. Clone & Setup (10 minutos)

### 2.1. Clone o Repositório

```bash
# Clonar repositório
git clone https://github.com/devviniuchita/python_project.git
cd python_project
```

### 2.2. Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows (PowerShell)
venv\Scripts\activate

# Windows (Git Bash)
source venv/Scripts/activate

# Linux/macOS
source venv/bin/activate
```

**Verificação**: O prompt deve mostrar `(venv)` no início.

### 2.3. Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

# Instalar pre-commit hooks (validação automática)
pre-commit install
```

**Tempo esperado**: ~3-5 minutos (depende da conexão).

📖 **Referência**: [Layer 4 Infrastructure](../.github/copilot-rules/project-codification.md#layer-4-infrastructure) documenta como as dependências são gerenciadas.

### 2.4. Configurar Variáveis de Ambiente

```bash
# Copiar template de configuração
cp .env.example .env

# Editar .env com suas credenciais
# Use seu editor preferido (nano, vim, code, notepad)
nano .env
```

**Configuração mínima** (`.env`):

```env
# === Google Cloud (OBRIGATÓRIO) ===
GOOGLE_API_KEY=AIza...sua_chave_aqui

# === LangSmith (OPCIONAL - Recomendado para dev) ===
LANGSMITH_API_KEY=ls__...sua_chave_aqui
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=rag-conversational

# === Reranker Configuration ===
RERANKER_SCORE_THRESHOLD=0.5
RERANKER_TOP_N=5

# === Logging ===
LOG_LEVEL=INFO
```

📖 **Referência**: [SessionConfig](../.github/copilot-rules/project-codification.md#sessionconfig) documenta todas as configurações disponíveis.

---

## 🧪 3. Run Tests (10 minutos)

Antes de executar a aplicação, valide que tudo está configurado corretamente rodando os testes.

### 3.1. Executar Testes Unitários

```bash
# Rodar todos os testes
pytest tests/unit/ -v

# Rodar com cobertura
pytest tests/unit/ --cov=src --cov-report=term

# Rodar testes específicos
pytest tests/unit/test_reranker.py -v
pytest tests/unit/test_session_config.py -v
```

**Resultado esperado**: ~21+ testes passando (tempo: ~30-60s).

### 3.2. Verificar Qualidade do Código

```bash
# Formatação (Black)
black src/ tests/ --check

# Organização de imports (isort)
isort src/ tests/ --check-only

# Linting (flake8)
flake8 src/ tests/ --max-line-length=88

# Type checking (mypy)
mypy src/ --ignore-missing-imports
```

**Verificação**: Todos os comandos devem retornar 0 erros.

📖 **Referência**: [Testing Requirements](../.github/copilot-rules/project-codification.md#testing-requirements) detalha as estratégias de teste do projeto.

### 3.3. Pre-commit Validation

```bash
# Executar todos os hooks de pre-commit
pre-commit run --all-files
```

**Resultado esperado**: Todos os hooks devem passar. Se falharem, os arquivos serão auto-formatados.

📖 **Troubleshooting**: Se o pre-commit falhar com erros TLS/SSL, consulte [docs/TROUBLESHOOT_PRECOMMIT_TLS.md](TROUBLESHOOT_PRECOMMIT_TLS.md).

---

## ⚡ 4. Run Application (10 minutos)

### 4.1. Opção 1: Demo Simples (app.py)

```bash
# Executar demo entry point
python app.py
```

**O que acontece:**
- Demonstra single-turn e multi-turn RAG
- Usa banco FAISS local
- Mostra reranking semântico com BGE
- Exibe logs estruturados

📖 **Referência**: [Layer 2 Orchestration](../.github/copilot-rules/project-codification.md#layer-2-orchestration) explica o fluxo LangGraph.

### 4.2. Opção 2: Chat Interativo (scripts/chat.py)

```bash
# Iniciar chat interativo
python scripts/chat.py
```

**Comandos disponíveis:**
- `/reset` - Reiniciar conversação
- `/quit` - Sair do chat
- `/help` - Mostrar comandos

**Exemplo de uso:**
```
You: O que é Retrieval-Augmented Generation?
Assistant: RAG é uma técnica que combina...

You: Como funciona o reranking semântico?
Assistant: O reranking semântico utiliza...

You: /reset
✅ Conversação reiniciada.

You: /quit
👋 Até logo!
```

📖 **Referência**: [Layer 1 Presentation](../.github/copilot-rules/project-codification.md#layer-1-presentation) documenta o CLI handler.

### 4.3. Verificar Observabilidade (LangSmith)

Se configurou `LANGSMITH_TRACING=true`:

1. Acesse: [smith.langchain.com](https://smith.langchain.com/)
2. Navegue até seu projeto (`rag-conversational`)
3. Veja traces em tempo real:
   - Latency breakdown
   - Score distributions
   - Documentos filtrados

📖 **Referência**: [LangSmith Integration](LANGSMITH_SETUP.md) para setup completo de observabilidade.

---

## 🎯 5. First Contribution (20 minutos)

Pronto para contribuir? Siga este workflow.

### 5.1. Criar Branch de Feature

```bash
# Atualizar main
git checkout main
git pull origin main

# Criar branch descritiva
git checkout -b feature/sua-feature
```

### 5.2. Fazer Alterações

Siga os padrões do projeto:

- **Clean Architecture**: Respeite as 4 camadas (ver [project-rules.md](../.github/copilot-rules/project-rules.md))
- **SOLID Principles**: Mantenha Single Responsibility (ver [SOLID Overview](../.github/copilot-rules/project-rules.md#solid-principles))
- **Type Hints**: Use type hints completos (ver [Type Safety](../.github/copilot-rules/project-codification.md#type-safety))
- **Testing**: Adicione testes unitários (cobertura >80%)

📖 **Referência**: [OOP Patterns](../.github/copilot-rules/project-rules.md#oop-principles) para patterns obrigatórios.

### 5.3. Validar Localmente

```bash
# Rodar testes
pytest tests/unit/ --cov=src

# Verificar formatação
black src/ tests/
isort src/ tests/

# Pre-commit hooks
pre-commit run --all-files
```

### 5.4. Commit com Conventional Commits

```bash
# Adicionar arquivos
git add .

# Commit com mensagem semântica
git commit -m "feat(reranker): adicionar threshold adaptativo"
```

**Formatos de commit:**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `test:` - Testes
- `refactor:` - Refatoração
- `chore:` - Manutenção

📖 **Referência**: [CONTRIBUTING.md](../CONTRIBUTING.md) para workflow completo de contribuição.

### 5.5. Abrir Pull Request

```bash
# Push branch
git push origin feature/sua-feature
```

1. Vá para GitHub
2. Abra Pull Request
3. Preencha template (gerado automaticamente)
4. Aguarde review

---

## 🔧 6. Common Tasks

### Adicionar Nova Dependência

```bash
# Instalar pacote
pip install nome-do-pacote

# Atualizar requirements.txt
pip freeze > requirements.txt
```

### Rodar Testes Específicos

```bash
# Por arquivo
pytest tests/unit/test_reranker.py -v

# Por função
pytest tests/unit/test_reranker.py::test_reranker_disabled_returns_none -v

# Por marcador
pytest -m "not slow"
```

### Gerar Relatório de Cobertura HTML

```bash
pytest tests/ --cov=src --cov-report=html
# Abrir: htmlcov/index.html
```

### Atualizar Pre-commit Hooks

```bash
pre-commit autoupdate
```

📖 **Referência**: [Tools Rules](../.github/copilot-rules/tools-rules.md) para ferramentas CLI avançadas.

---

## ⚠️ 7. Troubleshooting

### Problema: `bash: python: command not found`

**Solução:**
```bash
# Usar python3 explicitamente
python3 --version
python3 -m venv venv
```

### Problema: Pre-commit falha com erros SSL/TLS

**Solução:**
- Consulte guia completo: [docs/TROUBLESHOOT_PRECOMMIT_TLS.md](TROUBLESHOOT_PRECOMMIT_TLS.md)
- Resumo: Configure `pip.ini` com certificado CA corporativo

### Problema: `ModuleNotFoundError: No module named 'src'`

**Solução:**
```bash
# Verificar que ambiente virtual está ativo
which python  # Deve apontar para venv/bin/python

# Reinstalar dependências
pip install -r requirements.txt
```

### Problema: FAISS index não encontrado

**Solução:**
```bash
# Verificar caminho em .env
cat .env | grep FAISS_INDEX_PATH

# Deve existir: src/infrastructure/database/banco_faiss
ls -la src/infrastructure/database/banco_faiss
```

📖 **Referência**: [Architecture Documentation](architecture.md) para troubleshooting avançado.

---

## 🎓 8. Next Steps

### Aprofundar Conhecimento

1. **Arquitetura**:
   - [docs/architecture.md](architecture.md) - Visão geral da arquitetura
   - [docs/ARCHITECTURE_MAP.md](ARCHITECTURE_MAP.md) - Mapa visual de componentes

2. **Padrões de Projeto**:
   - [project-rules.md](../.github/copilot-rules/project-rules.md) - Regras arquiteturais
   - [project-codification.md](../.github/copilot-rules/project-codification.md) - Padrões de código

3. **Testes**:
   - [docs/TESTING_WITH_TESTSPRITE.md](TESTING_WITH_TESTSPRITE.md) - TestSprite automation
   - [docs/compliance/SONARQUBE_SETUP.md](compliance/SONARQUBE_SETUP.md) - Quality gates

4. **Observabilidade**:
   - [docs/LANGSMITH_SETUP.md](LANGSMITH_SETUP.md) - LangSmith integration
   - [README.md](../README.md) - Métricas de performance

### Explorar Funcionalidades Avançadas

- **Reranking Adaptativo**: `src/features/reranking/reranker.py`
- **LangGraph Orchestration**: `src/features/conversation/conversation_graph.py`
- **Logging Estruturado**: `src/infrastructure/logging/logger.py`
- **Copyright Management**: `scripts/add_copyright_headers.py`

### Contribuir com Documentação

- Melhorar este guia: abra issue ou PR
- Adicionar exemplos práticos em `examples/`
- Atualizar troubleshooting com novos casos

---

## 📞 Precisa de Ajuda?

<div align="center">

| Canal | Descrição | Tempo de Resposta |
|-------|-----------|-------------------|
| 🐛 **[GitHub Issues](https://github.com/devviniuchita/python_project/issues)** | Bugs e feature requests | 1-3 dias |
| 💬 **[GitHub Discussions](https://github.com/devviniuchita/python_project/discussions)** | Perguntas e discussões | Comunidade |
| 📧 **Email** | viniciusuchita@gmail.com | 24-48h |

</div>

---

<div align="center">

**🎉 Bem-vindo ao Python RAG Project! 🎉**

⭐ Se este guia foi útil, considere dar uma estrela no [GitHub](https://github.com/devviniuchita/python_project)!

**Construindo o futuro dos sistemas RAG, uma linha de código por vez.** 🚀

</div>
