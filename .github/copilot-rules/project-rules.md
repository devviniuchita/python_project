---
metadata: |
name: '.github/copilot-rules/project-rules.md'
description: 'Project rules, to define and standardize stacks and versions that should be used, architectural guidelines, engineering, design, approval standards, security rules and deployment procedures for the project PYTHON_PROJECT.'
aiOptimized: true
alwaysApply: false
applyManually: true
syncWith: ['.github/copilot-rules/project-codification.md'](project-codification.md)
---

# 🔒 SISTEMA DE REGRAS IMUTÁVEIS - MCP TreeOfThoughts

## Regras Arquiteturais e Comportamentais Permanentes para Python

## 🏗️ ARQUITETURA FUNDAMENTAL

### Clean Architecture (OBRIGATÓRIO)

- **Camadas**: Apresentação (CLI/Handlers) → Orquestração (LangGraph) → Lógica de Negócio (RAG Nodes) → Serviços Especializados (Config/Logging/Infra)
- **Dependency Boundaries**: Cada camada consome somente contratos da camada imediatamente inferior (`RAGState`, `SessionConfig`, helpers do Layer 4).
- **Separation of Concerns**: Camada 1 trata entrada/saída e comandos; Camada 2 monta o grafo `StateGraph`; Camada 3 transforma o estado com estratégias especializadas; Camada 4 encapsula integrações externas (FAISS, LangSmith, CrossEncoder, Settings).
- **Domain Independence**: Contratos em `src/core/domain` permanecem puros (sem dependências de infraestrutura) e são reutilizados em todas as camadas.

📖 **Implementação Detalhada**: Ver [project-codification.md - Arquitetura Enterprise](project-codification.md#arquitetura-enterprise-hierárquica---padrões-validados) para implementação completa das 4 camadas com exemplos de código e arquivos específicos.

_Otimização Tips (YOLO Mode):_

- Novo handler? implemente em `scripts/` ou `src/features/conversation/` e delegue tudo para o grafo.
- Monitore dependências com `python -m compileall` + `pip install import-linter` para garantir fluxo unidirecional (Layer 1 → Layer 4).
- Métrica prática: nenhum módulo deve importar camadas superiores; falhas nessa regra aumentam o acoplamento e devem ser bloqueadas.

### OOP Principles (SOLID - INQUEBRÁVEIS)

- **S** - Single Responsibility: Cada módulo com escopo único (`retrieve_adaptive` só cuida de buscar documentos).
- **O** - Open/Closed: Extensão via novos nodes/serviços sem modificar comportamento existente.
- **L** - Liskov Substitution: Subclasses e contratos (ex.: `Settings(BaseSettings)`) substituem a base sem quebrar consumidores.
- **I** - Interface Segregation: Camadas consomem apenas os campos necessários (`SessionConfig`, `RAGState`), evitando APIs gordas.
- **D** - Dependency Inversion: Layer 2 depende de assinaturas (`state -> dict`) ao invés de implementações concretas.

📖 **Implementação Prática**: Ver [project-codification.md - Pattern Applied](project-codification.md#pattern_applied) para exemplos Python concretos de cada princípio SOLID em ação no projeto.

_Otimização Tips (YOLO Mode):_

- Verifique **S** com ferramentas como **SonarQube**/cognitive complexity.
- Para **O**, adicione novas estratégias em módulos separados e integre via LangGraph.
  <impact>: Reduza bugs em 40% com testes unitários focados em contratos pequenos.</impact>

### OOP (OBJECT-ORIENTED PROGRAMMING) - MANDATORY COMPLIANCE:

#### **1. Abstraction - Contratos Tipados que isolam responsabilidades**

Usamos `TypedDict` e `Literal` para declarar contratos imutáveis que separam o **o quê** do **como**, reforçando o `S` (Single Responsibility) de SOLID.

```yaml
Pattern: TypedDict + Literal (contrato estático)
Module: typing.TypedDict, typing.Literal, pydantic.Field
Reference: PEP 589 (TypedDict)
Enforcement: Camada 2 (LangGraph) aceita apenas dicionários compatíveis com RAGState
```

📖 **Arquivo de Implementação**: Ver [project-codification.md - RAGState](project-codification.md#ragstate) (linhas específicas com implementação completa e validação Pydantic).

**Python Example - Contrato de estado compartilhado:**

```python
from typing import Annotated, List, Literal, Sequence, TypedDict
from pydantic import Field

# File: src/core/domain/state.py (Linhas 10-38)
class RAGState(TypedDict):
  question: str
  complexity: Literal["simple", "complex"]
  documents: List[str]
  generation: str
  quality_score: Annotated[float, Field(ge=0.0, le=1.0)]
  iterations: Annotated[int, Field(ge=0)]

class ConversationalRAGState(TypedDict):
  messages: Annotated[Sequence[BaseMessage], add_messages]
  question: str
  complexity: Literal["simple", "complex"]
  documents: List[str]
  generation: str
  quality_score: Annotated[float, Field(ge=0.0, le=1.0)]
  iterations: Annotated[int, Field(ge=0)]
  is_followup: bool
  original_question: str
```

📌 **Como aplicar:** qualquer novo node da Camada 3 deve aceitar `RAGState` e retornar apenas os campos que realmente altera. Isso mantém o fluxo de dados coerente e fácil de testar.

_Otimização Tips:_ reutilize `TypedDict` sempre que precisar de contratos leves; `BaseModel` só é indicado quando validação em runtime for indispensável (cuidado com o overhead de ~2.5x).

---

#### **2. Encapsulation - Validação automática + propriedades calculadas**

Configurações e modelos de sessão ocultam detalhes internos via Pydantic, garantindo que somente estados válidos circulem entre camadas.

```yaml
Pattern: Pydantic BaseModel/BaseSettings + propriedades read-only
Module: pydantic.BaseModel, pydantic.Field, pydantic.field_validator
Reference: SOLID I (Interface Segregation) – expõe somente o que o cliente precisa
Enforcement: `model_config = ConfigDict(frozen=True)` evita mutação após criação
```

**Python Example - Configuração imutável com validação:**

```python
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo

# File: src/core/domain/session.py (Linhas 12-78)
class SessionConfig(BaseModel):
  thread_id: UUID = Field(..., description="Unique UUID for conversation thread")
  max_turns: int = Field(default=10, ge=1, description="Maximum turns")
  memory_window: int = Field(default=6, ge=1, le=20, description="Context window")

  model_config = ConfigDict(frozen=True, validate_assignment=True)

  @field_validator('memory_window')
  @classmethod
  def validate_memory_window(cls, v: int, info: ValidationInfo) -> int:
    max_turns = info.data.get('max_turns', 10)
    if v > max_turns:
      raise ValueError("memory_window cannot exceed max_turns")
    return v

  @property
  def memory_ratio(self) -> float:
    """Return utilization ratio between memory window and max_turns."""
    return self.memory_window / self.max_turns
```

📌 **Como aplicar:** exponha apenas métodos de leitura (`get_config`, `memory_ratio`) e deixe que Pydantic rejeite estados inválidos automaticamente — evita `if` redundante em cada camada.

_Otimização Tips:_ Em objetos de configuração, use `frozen=True` para forçar imutabilidade; para campos derivados (ex.: métricas) crie propriedades calculadas ao invés de duplicar valores no estado.

---

#### **3. Inheritance - Reuso seguro com classes base Pydantic**

Aplicamos herança quando o framework já entrega comportamento reutilizável (ex.: `BaseSettings`, `BaseModel`). Isso garante substituição segura (L de SOLID) sem criar hierarquias profundas.

```yaml
Pattern: Subclasse especializada herdando validação/base behavior
Module: pydantic.BaseSettings, pydantic.BaseModel
Reference: SOLID L - Subclasses não quebram o contrato da base
Enforcement: Validadores e campos herdados permanecem compatíveis
```

**Python Example - Configuração derivada de BaseSettings:**

```python
from pydantic import BaseSettings, Field

# File: src/infrastructure/config/settings.py (Linhas 18-52)
class Settings(BaseSettings):
  langsmith_api_key: str = Field(..., description="LangSmith API Key")
  llm_model: str = Field(default="gemini-2.0-flash-exp")
  reranker_enabled: bool = Field(default=True)
  reranker_model: str = Field(default="BAAI/bge-reranker-base")

  class Config:
    env_file = ".env"
    env_prefix = "PYTHON_RAG_"
```

📌 **Como aplicar:** herde apenas quando o framework oferece comportamento valioso (validação automática, carregamento de `.env`, etc.). Evite cadeias >2 níveis — prefira composição com helpers do Layer 4.

_Otimização Tips:_ Centralize toda configuração sensível em subclasses de `BaseSettings` para aproveitar caching interno e evitar boilerplate manual.

---

#### **4. Polymorphism - Implementações intercambiáveis no pipeline RAG**

LangGraph trata cada node como algo que recebe `RAGState` e devolve um diff de estado. Isso nos permite trocar implementações sem alterar a orquestração — polimorfismo funcional alinhado ao `D` (Dependency Inversion) de SOLID.

```yaml
Pattern: Funções puras com mesma assinatura (state in → state diff out)
Module: langsmith.traceable (decorator), state.RAGState
Reference: SOLID D - camadas superiores dependem de abstrações (assinatura comum)
Enforcement: StateGraph só aceita callables `Callable[[RAGState], RAGState]`
```

**Python Example - Nós intercambiáveis no LangGraph:**

```python
from langsmith import traceable

# File: src/features/rag/nodes.py
@traceable(run_type="chain", name="Classify Question Complexity")
def classify_question(state: RAGState) -> RAGState:
  question = state["question"]
  ...
  return {"complexity": complexity}

@traceable(run_type="retriever", name="Adaptive Document Retrieval")
def retrieve_adaptive(state: RAGState) -> RAGState:
  complexity = state["complexity"]
  ...
  return {"documents": documents}

@traceable(run_type="chain", name="BGE Semantic Reranking")
def rerank_documents(state: RAGState) -> RAGState:
  ...
  return {"documents": reranked_docs}
```

📌 **Como aplicar:** qualquer nova estratégia (ex.: sumarização, filtragem) deve seguir a mesma assinatura `def node(state: RAGState) -> RAGState:`. O grafo decide a ordem; nós são plugáveis, possibilitando testes A/B sem alterar a Camada 2.

_Otimização Tips:_ Concentre-se em manter nodes puros (sem efeitos colaterais) — isso facilita swap entre implementações e permite mocks simples em testes unitários.

---

_Otimização Tips (YOLO Mode):_

- Evite herança profunda (>2 níveis) para prevenir violações Liskov
- Máximo 3 níveis: Base → Parent → Child
- Prefira composição sobre herança quando possível (Strategy pattern)

---

## 🎖️ COMPLIANCE ENFORCEMENT

### Immutable Rules & Validation

```yaml
Rule Compliance:
  Immutable_Rules:
    - 🔒 Clean_Architecture_Mandatory: true
      Validation: SonarQube (architecture module analysis)
      Trigger: Pre-commit hook + CI/CD
      Consequence: Block merge if violated

    - 🔒 SOLID_Principles_Required: true
      Validation: SonarQube (cognitive complexity <15, duplication 0%)
      Trigger: Every commit via pre-commit hook
      Consequence: Build failure if S/O/I/D violated

    - 🔒 Type_Hints_Mandatory: true
      Validation: mypy strict mode, SonarQube
      Trigger: Pre-commit hook (.githooks/pre-commit)
      Consequence: Commit rejected

    - 🔒 Documentation_Always_Updated: true
      Validation: GitHub Actions copyright-check.yml
      Trigger: Pull request
      Consequence: PR blocked until resolved

    - 🔒 OOP_Implementation_Required: true
      Validation: Code review + SonarQube patterns
      Trigger: Pull request
      Consequence: Require approval from lead

    - 🔒 DCO_Sign_Off_Mandatory: true
      Validation: GitHub Actions dco-check.yml
      Trigger: Every commit
      Consequence: Commit rejected without "Signed-off-by"
```

### Validation Tools & Methods

| Rule                   | Tool                     | Method                         | Trigger    | Consequence       |
| ---------------------- | ------------------------ | ------------------------------ | ---------- | ----------------- |
| **Clean Architecture** | SonarQube                | Module analysis                | Pre-commit | Build failure     |
| **SOLID Principles**   | SonarQube                | Complexity <15, 0% duplication | Pre-commit | Block commit      |
| **Type Hints**         | mypy                     | Strict type checking           | Pre-commit | Reject commit     |
| **Copyright Headers**  | Workflow (python script) | add_copyright_headers.py       | Pre-commit | Auto-add or block |
| **Code Review**        | GitHub                   | Approval required              | PR         | Block merge       |
| **DCO Sign-off**       | GitHub Actions           | dco-check.yml                  | Commit     | Reject commit     |
| **Imports**            | isort                    | Auto-organization              | Pre-commit | Auto-fix          |
| **Code Style**         | Black                    | 88 char lines                  | Pre-commit | Auto-format       |

### Pre-Commit Hooks Enforcement

```bash
# Location: .githooks/pre-commit

#!/bin/bash
set -e

echo "🔒 COMPLIANCE CHECKS - Starting validation..."

# 1. Type hints
echo "📌 Checking type hints with mypy..."
mypy src/ --strict || exit 1

# 2. Code style
echo "🎨 Formatting code with Black..."
black src/ tests/ --line-length 88 || exit 1

# 3. Import organization
echo "📦 Organizing imports with isort..."
isort src/ tests/ --profile black || exit 1

# 4. Linting
echo "✅ Linting with flake8..."
flake8 src/ tests/ --max-line-length 88 || exit 1

# 5. Copyright headers
echo "🛡️ Adding copyright headers..."
python scripts/add_copyright_headers.py || exit 1

# 6. SonarQube analysis (local)
echo "🔍 Running SonarQube analysis..."
sonar-scanner || exit 1

echo "✅ All compliance checks passed!"
```

### Git Commit Hook Enforcement

```bash
# Location: .githooks/commit-msg

#!/bin/bash

# Validate Conventional Commits format
MESSAGE=$(cat "$1")
PATTERN="^(feat|fix|docs|style|refactor|perf|test|chore|ci)(\(.+\))?!?:\s[a-z]"

if ! echo "$MESSAGE" | grep -qE "$PATTERN"; then
    echo "❌ Commit message must follow Conventional Commits:"
    echo "   feat(scope): description"
    echo "   fix(scope): description"
    echo "   docs: update documentation"
    exit 1
fi

# Validate DCO sign-off
if ! echo "$MESSAGE" | grep -q "Signed-off-by:"; then
    echo "❌ Commit must include DCO sign-off:"
    echo "   git commit -s"
    exit 1
fi

echo "✅ Commit message valid"
```

### GitHub Actions Automation

```yaml
# Location: .github/workflows/copyright-check.yml
name: Copyright Protection
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Verify copyright headers
        run: python scripts/add_copyright_headers.py --verify

# Location: .github/workflows/dco-check.yml
name: DCO Check
on: [pull_request]
jobs:
  dco:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: amannn/action-semantic-pull-request@v5
```

### Compliance Verification Checklist

**Before Every Commit:**

- [ ] Type hints added (mypy strict)
- [ ] SOLID principles respected (<15 cognitive complexity)
- [ ] Clean Architecture maintained (4 layers)
- [ ] Code formatted (Black 88 chars)
- [ ] Imports organized (isort)
- [ ] Copyright headers present
- [ ] Tests passing (>80% coverage)
- [ ] Commit message follows Conventional Commits
- [ ] DCO sign-off included (`git commit -s`)

**Before Every PR:**

- [ ] All pre-commit checks passing
- [ ] GitHub Actions passing
- [ ] Code review approved
- [ ] Copyright check passed
- [ ] DCO signed by all commits

---

```markdown
**📅 Created:** 06/08/2025
**🔄 Last Update:** 17/10/2025
**📋 Status:** ACTIVE AND MANDATORY
**🎯 Application:** AWAYS WHEN THE USER MENTIONS OR WHEN THE AGENT NEEDS CONTEXT OR RELEVANT INFORMATION ABOUT THE PROJECT
**🔍 Linked:** .github/copilot-rules/project-codification.md
```

---

_This document defines the development, coding, security and deployment rules for the PROJEC PYTHON_
