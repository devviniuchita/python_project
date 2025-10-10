# Projeto Python - Sistema RAG com Gerenciamento de Conversação

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Um sistema abrangente de RAG (Retrieval-Augmented Generation) com gerenciamento de conversação, reranking de documentos e capacidades de monitoramento construído com as melhores práticas modernas do Python.

## 🏗️ Visão Geral da Arquitetura

Este projeto segue uma **arquitetura src-layout moderna** com clara separação de responsabilidades:

```
python_project/
├── src/                          # Código fonte principal (src-layout)
│   ├── core/                     # Lógica de negócio central
│   │   ├── domain/              # Modelos de domínio e entidades
│   │   ├── services/            # Serviços de lógica de negócio
│   │   └── repositories/        # Camada de acesso a dados
│   ├── features/                # Módulos de funcionalidades
│   │   ├── rag/                 # Funcionalidade RAG
│   │   ├── conversation/        # Gerenciamento de conversação
│   │   └── reranking/           # Reranking de documentos
│   ├── infrastructure/          # Preocupações de infraestrutura
│   │   ├── config/             # Gerenciamento de configuração
│   │   ├── database/           # Conexões de banco de dados
│   │   ├── logging/            # Configuração de logging
│   │   └── external/           # Integrações de serviços externos
│   └── shared/                  # Utilitários compartilhados
├── tests/                       # Suíte de testes abrangente
│   ├── unit/                   # Testes unitários
│   ├── integration/            # Testes de integração
│   └── e2e/                    # Testes end-to-end
├── docs/                        # Documentação
├── scripts/                     # Scripts utilitários
└── .github/workflows/          # Pipelines CI/CD
```

## ✨ Principais Funcionalidades

- **🧠 Sistema RAG Avançado** - Recuperação vetorial baseada em FAISS com busca semântica
- **💬 Gerenciamento de Conversação** - Memória de conversação persistente com consciência de contexto
- **🔄 Reranking de Documentos** - Cross-encoder BGE para pontuação de relevância e filtragem por threshold
- **📊 Monitoramento de Qualidade** - Validação abrangente de qualidade e métricas de performance
- **🔍 Integração LangSmith** - Rastreamento completo e observabilidade para depuração
- **📈 Validação Estatística** - Curvas ROC, análise precision-recall e intervalos de confiança
- **⚡ Otimizado para Performance** - Processamento concorrente, monitoramento de memória e testes de escalabilidade

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- Credenciais do Google Cloud para API Gemini
- Chave da API LangSmith (opcional para rastreamento)

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone <repository-url>
   cd python_project
   ```

2. **Configure o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o ambiente:**
   ```bash
   cp .env.example .env
   # Edite o .env com suas chaves de API
   ```

5. **Execute a aplicação:**
   ```bash
   python -m src.core.services.main  # Ponto de entrada será atualizado
   ```

## 🧪 Testes

O projeto inclui testes abrangentes em múltiplas dimensões:

```bash
# Execute todos os testes
pytest tests/

# Execute categorias específicas de teste
pytest tests/unit/              # Testes unitários
pytest tests/integration/       # Testes de integração
pytest tests/e2e/              # Testes end-to-end

# Execute testes de performance
python scripts/run_threshold_tests.py

# Execute com cobertura
pytest --cov=src tests/
```

## 📚 Documentação

- **[Guia de Arquitetura](docs/architecture.md)** - Arquitetura detalhada do sistema
- **[Documentação da API](docs/api/)** - Referência e exemplos da API
- **[Guia de Desenvolvimento](docs/guides/)** - Configuração de desenvolvimento e workflows
- **[Guia de Testes](docs/guides/testing.md)** - Estratégias e melhores práticas de teste

## 🏭 Fluxo de Desenvolvimento

### Qualidade do Código

```bash
# Formate o código
black src/ tests/
isort src/ tests/

# Faça lint do código
flake8 src/ tests/
mypy src/

# Execute hooks de pre-commit
pre-commit run --all-files
```

### Diretrizes de Estrutura do Projeto

- **Módulos core** (`src/core/`) - Lógica de negócio, modelos de domínio, serviços
- **Módulos de funcionalidades** (`src/features/`) - Funcionalidades específicas (RAG, conversation, reranking)
- **Infraestrutura** (`src/infrastructure/`) - Configuração, banco de dados, logging, serviços externos
- **Utilitários compartilhados** (`src/shared/`) - Utilitários comuns e tipos

### Adicionando Novas Funcionalidades

1. Crie módulo de funcionalidade em `src/features/`
2. Defina modelos de domínio em `src/core/domain/`
3. Implemente lógica de negócio em `src/core/services/`
4. Adicione configuração em `src/infrastructure/config/`
5. Escreva testes abrangentes em `tests/unit/`
6. Atualize a documentação

## 🔧 Configuração

A aplicação utiliza configurações Pydantic para gerenciamento:

```python
# src/infrastructure/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Chaves de API
    google_api_key: str
    langsmith_api_key: Optional[str] = None

    # Configuração de Reranking
    reranker_model: str = "BAAI/bge-reranker-base"
    reranker_score_threshold: float = 0.5
    reranker_top_n: int = 5

    # Configuração de Banco de Dados
    faiss_index_path: str = "src/infrastructure/database/banco_faiss"

    class Config:
        env_file = ".env"
        case_sensitive = False
```

## 📈 Performance e Monitoramento

- **Monitoramento de memória** com psutil para rastreamento de uso de recursos
- **Benchmarks de performance** para processamento de grandes conjuntos de dados
- **Validação estatística** da precisão de pontuação por threshold
- **Rastreamento LangSmith** para monitoramento detalhado de execução
- **Logging abrangente** com logging estruturado

## 🤝 Contribuindo

1. Faça fork do repositório
2. Crie uma branch de funcionalidade (`git checkout -b feature/amazing-feature`)
3. Faça suas alterações
4. Execute os testes (`pytest tests/`)
5. Commit suas alterações (`git commit -m 'Add amazing feature'`)
6. Faça push para a branch (`git push origin feature/amazing-feature`)
7. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Construído com [LangChain](https://python.langchain.com/) para funcionalidade RAG
- Usa [LangGraph](https://langchain-ai.github.io/langgraph/) para orquestração de workflow
- Alimentado por [Google Gemini](https://ai.google.dev/) para modelos de linguagem
- Busca vetorial com [FAISS](https://faiss.ai/)
- Monitoramento com [LangSmith](https://smith.langchain.com/)

## 📞 Suporte

Para dúvidas, problemas ou contribuições, por favor:

1. Verifique a [documentação](docs/)
2. Pesquise [issues existentes](https://github.com/your-repo/issues)
3. Crie um novo issue com informações detalhadas
4. Participe das discussões da comunidade

---

**Feito com ❤️ para a comunidade Python**
