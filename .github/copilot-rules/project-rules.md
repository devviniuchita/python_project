---
metadata: |
name: '.github/copilot-rules/project-rules.md'
description: 'Project rules, to define and standardize stacks and versions that should be used, architectural guidelines, engineering, design, approval standards, security rules and deployment procedures for the project PYTHON_PROJECT.'
aiOptimized: true
alwaysApply: false
applyManually: true
syncWith: ['.github/copilot-rules/project-codification.md']
---

# 🔒 SISTEMA DE REGRAS IMUTÁVEIS - MCP TreeOfThoughts

## Regras Arquiteturais e Comportamentais Permanentes para Python

## 🏗️ ARQUITETURA FUNDAMENTAL

### Clean Architecture (OBRIGATÓRIO)

- **Camadas**: Controllers → Services → Repositories → Entities
- **Dependency Inversion**: Dependências apontam para dentro via interfaces e @Autowired
- **Separation of Concerns**: Responsabilidades bem definidas, com injeção de dependência via Spring
- **Domain Independence**: Entidades independentes de infraestrutura (use JPA annotations)

_Otimização Tips (YOLO Mode):_

-
- Evite controllers gordos: Delegue lógica para services imediatamente.
- Métrica de alavancagem: Classes <250 LOC para manutenção rápida.

### OOP Principles (SOLID - INQUEBRÁVEIS)

- **S** - Single Responsibility: Uma responsabilidade por classe (ex: @Service para lógica de negócio isolada)
- **O** - Open/Closed: Extensão sem modificação (use interfaces e subclasses)
- **L** - Liskov Substitution: Subtipos substituíveis sem quebrar contratos
- **I** - Interface Segregation: Interfaces específicas e cliente-orientadas
- **D** - Dependency Inversion: Abstrações não implementações (Spring DI obrigatório)

_Otimização Tips (YOLO Mode):_

- Verifique **S** com tool como **SonarQube**: Flag classes com >1 responsabilidade
- Para **O**, prefira composição sobre herança para evitar fragilidade
  <impact>: Reduza bugs em 40% com testes unitários em interfaces segregadas.</impact>

### OOP (OBJECT-ORIENTED PROGRAMMING) - MANDATORY COMPLIANCE:

#### **1. Abstraction - Abstract Base Classes & Protocols**

Define interfaces claras usando `abc.ABC` ou `typing.Protocol` para separar contrato de implementação.

```yaml
Pattern: ABC (Abstract Base Class) ou Protocol (Structural Subtyping)
Module: abc, typing.Protocol
Reference: PEP 3119, PEP 544
Enforcement: @abstractmethod decorator
```

**Python Example - ABC Pattern:**
```python
from abc import ABC, abstractmethod

# File: src/core/services/memory_manager.py
class ConversationManager(ABC):
    """Abstract interface para gerenciamento de conversação."""

    @abstractmethod
    def get_or_create_session(self, user_id: str) -> str:
        """Create or retrieve session ID."""
        pass

    @abstractmethod
    def reset_session(self, user_id: str) -> str:
        """Reset conversation session."""
        pass
```

**Python Example - Protocol Pattern:**
```python
from typing import Protocol

# Structural subtyping - duck typing com type hints
class Reranker(Protocol):
    """Protocol for reranking strategies."""

    def score(self, query: str, documents: list[str]) -> list[float]:
        """Score documents for relevance."""
        ...
```

_Otimização Tips:_ Use `Protocol` para interfaces implícitas (duck typing tipado), `ABC` para hierarquias explícitas.

---

#### **2. Encapsulation - Properties & Data Validation**

Proteja dados internos usando properties decorators e validação automática via Pydantic.

```yaml
Pattern: @property decorator, Pydantic BaseSettings
Module: pydantic, @property
Reference: Python data model, Pydantic v2
Enforcement: Type hints + validators
```

**Python Example - Pydantic Encapsulation:**
```python
from pydantic import BaseSettings, Field, field_validator

# File: src/infrastructure/config/settings.py (Line 18)
class Settings(BaseSettings):
    """Encapsulated configuration with automatic validation."""

    reranker_enabled: bool = Field(True, description="Enable reranking")
    reranker_model: str = Field("BAAI/bge-reranker-base", description="Model name")

    @field_validator("reranker_model")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Validate model name format."""
        if not v or "/" not in v:
            raise ValueError("Model must be in format 'org/model'")
        return v

    class Config:
        env_prefix = "PYTHON_RAG_"
```

**Python Example - Property Pattern:**
```python
# Domain model with encapsulation
class SessionConfig:
    def __init__(self, memory_window: int):
        self._memory_window = memory_window

    @property
    def memory_window(self) -> int:
        """Get memory window (read-only)."""
        return self._memory_window

    @property
    def max_tokens(self) -> int:
        """Compute derived value (encapsulated logic)."""
        return self._memory_window * 512  # Bytes to tokens
```

_Otimização Tips:_ Combine Pydantic para objetos complexos, @property para valores computados ou validados.

---

#### **3. Inheritance - Class Hierarchies & Extension**

Reutilize funcionalidade comum através de classes base, mantendo Liskov Substitution Principle.

```yaml
Pattern: Inheritance chains, BaseModel extension
Module: pydantic (BaseSettings, BaseModel)
Reference: SOLID L - Liskov Substitution
Enforcement: Subclass contracts via type hints
```

**Python Example - Pydantic Inheritance:**
```python
from pydantic import BaseModel, Field

# File: src/core/domain/session.py (Line 16)
class SessionConfig(BaseModel):
    """Base session configuration."""
    memory_window: int = Field(default=5, ge=1, le=50)
    user_id: str = Field(default="default")

    @field_validator("memory_window")
    @classmethod
    def validate_memory_window(cls, v: int) -> int:
        """Validate memory window bounds."""
        if v < 1 or v > 50:
            raise ValueError("Memory window must be between 1-50")
        return v

class ConversationalSessionConfig(SessionConfig):
    """Extended configuration for conversational RAG."""
    max_iterations: int = Field(default=3, ge=1, le=10)
    clarification_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
```

_Otimização Tips:_ Prefira Pydantic inheritance sobre plain classes para validação automática. Max 2 níveis de herança.

---

#### **4. Polymorphism - Multiple Implementations & Runtime Dispatch**

Permita diferentes implementações de mesma interface usando `@abstractmethod` ou `Protocol`.

```yaml
Pattern: @abstractmethod, Protocol, LangGraph nodes
Module: abc, typing.Protocol
Reference: SOLID D - Dependency Inversion
Enforcement: Interface contracts via inheritance
```

**Python Example - Strategy Pattern with @abstractmethod:**
```python
from abc import ABC, abstractmethod

# File: src/features/rag/nodes.py
class RAGNode(ABC):
    """Base class for RAG pipeline nodes."""

    @abstractmethod
    def execute(self, state: RAGState) -> RAGState:
        """Execute node transformation on state."""
        pass

class ClassifyQuestionNode(RAGNode):
    def execute(self, state: RAGState) -> RAGState:
        # Classify input question
        return state

class RetrievalNode(RAGNode):
    def execute(self, state: RAGState) -> RAGState:
        # Retrieve documents from FAISS
        return state

class RerankerNode(RAGNode):
    def execute(self, state: RAGState) -> RAGState:
        # Rerank documents with BGE
        return state

# Runtime dispatch - polymorphism
def apply_node(node: RAGNode, state: RAGState) -> RAGState:
    """Apply any RAG node - compiler ensures execute() exists."""
    return node.execute(state)
```

**Python Example - Protocol Polymorphism:**
```python
from typing import Protocol

class Reranker(Protocol):
    """Protocol - any class with score() method works."""
    def score(self, query: str, docs: list[str]) -> list[float]:
        ...

# Different implementations
class BGEReranker:
    def score(self, query: str, docs: list[str]) -> list[float]:
        # BGE CrossEncoder scoring
        pass

class MockReranker:
    def score(self, query: str, docs: list[str]) -> list[float]:
        # Test mock implementation
        pass

# Both satisfy protocol - true polymorphism
reranker1: Reranker = BGEReranker()
reranker2: Reranker = MockReranker()
```

_Otimização Tips:_ Use `Protocol` para duck typing, `ABC` para contratos explícitos. LangGraph nodes como polimorfismo funcional.

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

| Rule | Tool | Method | Trigger | Consequence |
|---|---|---|---|---|
| **Clean Architecture** | SonarQube | Module analysis | Pre-commit | Build failure |
| **SOLID Principles** | SonarQube | Complexity <15, 0% duplication | Pre-commit | Block commit |
| **Type Hints** | mypy | Strict type checking | Pre-commit | Reject commit |
| **Copyright Headers** | Workflow (python script) | add_copyright_headers.py | Pre-commit | Auto-add or block |
| **Code Review** | GitHub | Approval required | PR | Block merge |
| **DCO Sign-off** | GitHub Actions | dco-check.yml | Commit | Reject commit |
| **Imports** | isort | Auto-organization | Pre-commit | Auto-fix |
| **Code Style** | Black | 88 char lines | Pre-commit | Auto-format |

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
