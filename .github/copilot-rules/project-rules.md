<!-- CHUNK: rules-metadata | Lines: 1-76 | Keywords: metadata, quick-navigation-index, search-shortcuts | Tokens: ~600 -->
<!-- CHUNK: rules-metadata | Lines: 1-76 | Keywords: metadata, quick-navigation-index, search-shortcuts | Tokens: ~600 -->
---
metadata: |
name: '.github/copilot-rules/project-rules.md'
description: 'Project rules, to define and standardize stacks and versions that should be used, architectural guidelines, engineering, design, approval standards, security rules and deployment procedures for the project PYTHON_PROJECT.'
aiOptimized: true
alwaysApply: false
applyManually: true
syncWith: ['.github/copilot-rules/project-codification.md'](project-codification.md)
---

# 🗺️ QUICK NAVIGATION INDEX

> **For AI Agents:** Use `read_file(offset, limit)` with line ranges below for token-efficient context retrieval (70% reduction vs full file read)

## 📂 ARCHITECTURE & DESIGN (Lines 77-119)

- [Clean Architecture](#clean-architecture-obrigatório) → Lines 79-95 | **Keywords:** Layer1-4, Dependency Boundaries, RAGState, SessionConfig, Separation of Concerns
- [SOLID Principles Overview](#-solid-principles---overview) → Lines 96-119 | **Keywords:** Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion

## 🏛️ OOP PATTERNS (Lines 120-594)

- [Abstraction - TypedDict Contracts](#1-abstraction---contratos-tipados-que-isolam-responsabilidades) → Lines 124-171 | **Keywords:** TypedDict, Literal, RAGState, ConversationalRAGState, PEP 589
- [Encapsulation - Pydantic Validation](#2-encapsulation---validação-automática--propriedades-calculadas) → Lines 172-218 | **Keywords:** BaseSettings, Field, ConfigDict, computed_field, lazy_load
- [Inheritance - BaseSettings Reuse](#3-inheritance---reuso-seguro-com-classes-base-pydantic) → Lines 219-254 | **Keywords:** SessionConfig, Settings, pydantic inheritance, model_validate
- [Polymorphism - Strategy Pattern](#4-polymorphism---implementações-intercambiáveis-no-pipeline-rag) → Lines 255-311 | **Keywords:** Callable, adaptive_retrieval, rerank_documents, strategy pattern
- [ABC - Protocol Enforcement](#5-abstract-base-classes-abc---contratos-rígidos-com-enforcement) → Lines 312-443 | **Keywords:** abstractmethod, MetricsCollector, EmbeddingProvider, ABC, Protocol
- [Composition - Aggregation Patterns](#6-composition-vs-inheritance---trade-offs-e-decision-framework) → Lines 444-594 | **Keywords:** dependency injection, SessionConfig composition, aggregation, decision matrix

## 🎖️ COMPLIANCE (Lines 595-773)

- [Immutable Rules & Validation](#immutable-rules--validation) → Lines 597-632 | **Keywords:** approval criteria, code quality, SonarQube, B grade minimum
- [Validation Tools](#validation-tools--methods) → Lines 633-645 | **Keywords:** sonar-scanner, pytest-cov, ruff check
- [Pre-Commit Hooks](#pre-commit-hooks-enforcement) → Lines 646-682 | **Keywords:** .pre-commit-config.yaml, ruff format, pytest coverage 80%
- [Git Commit Hooks](#git-commit-hook-enforcement) → Lines 683-711 | **Keywords:** conventional commits, semantic versioning, .githooks
- [GitHub Actions](#github-actions-automation) → Lines 712-738 | **Keywords:** CI/CD, automated testing, quality gates
- [Compliance Checklist](#compliance-verification-checklist) → Lines 739-773 | **Keywords:** verification steps, approval matrix, rollback procedures

## 🔍 SEARCH SHORTCUTS

### By Concept

- **Architecture Layers:** Lines 79-95 (Clean Architecture + 4 camadas)
- **SOLID Principles:** Lines 96-119 (S.O.L.I.D overview + Quick Wins)
- **State Contracts:** Lines 124-171 (RAGState, ConversationalRAGState)
- **Validation Patterns:** Lines 172-218 (Pydantic BaseSettings + Field)
- **Strategy Pattern:** Lines 255-311 (Polymorphism + Callable signatures)
- **ABC Protocols:** Lines 312-443 (abstractmethod + enforcement)
- **Composition Pattern:** Lines 444-594 (SessionConfig + decision framework)
- **Quality Gates:** Lines 597-632 (Approval criteria + metrics)

### By File Reference

- **State Definitions:** `src/core/domain/state.py` → Lines 124-171 (RAGState examples)
- **Session Config:** `src/core/domain/session.py` → Lines 172-218, 219-254, 444-594
- **RAG Nodes:** `src/features/rag/nodes.py` → Lines 255-311 (retrieve_adaptive, rerank_documents)
- **Metrics ABC:** `src/shared/types/protocols.py` → Lines 312-443 (MetricsCollector, EmbeddingProvider)
- **Infrastructure:** `src/infrastructure/config/settings.py` → Lines 219-254 (Settings implementation)
- **Compliance Tools:** `.pre-commit-config.yaml`, `.githooks/`, `.github/workflows/` → Lines 646-738

### By Keyword (Grep-Optimized)

- **RAGState:** Lines 124-171, 255-311 (definition + usage)
- **SessionConfig:** Lines 172-218, 219-254, 444-594 (validation + composition)
- **Pydantic:** Lines 172-218, 219-254 (BaseSettings + Field + computed_field)
- **LangGraph:** Lines 79-95, 255-311 (architecture + node signatures)
- **abstractmethod:** Lines 312-443 (ABC protocols + enforcement)
- **dependency injection:** Lines 444-594 (composition patterns)
- **SonarQube:** Lines 597-632, 633-645 (quality criteria + commands)
- **pre-commit:** Lines 646-682 (hook configuration + enforcement)
- **conventional commits:** Lines 683-711 (commit message format)

---

## Regras Arquiteturais e Comportamentais Permanentes para Python

<!-- END CHUNK: rules-metadata -->
<!-- CHUNK: rules-clean-arch | Lines: 77-95 | Keywords: clean-architecture, 4-layers, dependency-boundaries | Tokens: ~200 -->
## 🏗️ ARQUITETURA FUNDAMENTAL
<!-- END CHUNK: rules-metadata -->
<!-- CHUNK: rules-clean-arch | Lines: 77-95 | Keywords: clean-architecture, 4-layers, dependency-boundaries | Tokens: ~200 -->

### Clean Architecture (OBRIGATÓRIO)

- **Camadas**: Apresentação (CLI/Handlers) → Orquestração (LangGraph) → Lógica de Negócio (RAG Nodes) → Serviços Especializados (Config/Logging/Infra)
- **Dependency Boundaries**: Cada camada consome somente contratos da camada imediatamente inferior (`RAGState`, `SessionConfig`, helpers do Layer 4).
- **Separation of Concerns**: Camada 1 trata entrada/saída e comandos; Camada 2 monta o grafo `StateGraph`; Camada 3 transforma o estado com estratégias especializadas; Camada 4 encapsula integrações externas (FAISS, LangSmith, CrossEncoder, Settings).
- **Domain Independence**: Contratos em `src/core/domain` permanecem puros (sem dependências de infraestrutura) e são reutilizados em todas as camadas.

📖 **Implementação Detalhada**: Ver [project-codification.md - Arquitetura Enterprise](project-codification.md#arquitetura-enterprise-hierárquica---padrões-validados) para implementação completa das 4 camadas com exemplos de código e arquivos específicos.

_Quick Wins (Implementation Tips):_

- Novo handler? implemente em `scripts/` ou `src/features/conversation/` e delegue tudo para o grafo.
- Monitore dependências com `python -m compileall` + `pip install import-linter` para garantir fluxo unidirecional (Layer 1 → Layer 4).
- Métrica prática: nenhum módulo deve importar camadas superiores; falhas nessa regra aumentam o acoplamento e devem ser bloqueadas.

<!-- END CHUNK: rules-clean-arch -->
<!-- CHUNK: rules-solid-overview | Lines: 96-123 | Keywords: solid-principles, srp, ocp, lsp, isp, dip | Tokens: ~300 -->
---

## 🎯 SOLID PRINCIPLES - OVERVIEW
<!-- END CHUNK: rules-clean-arch -->
<!-- CHUNK: rules-solid-overview | Lines: 96-123 | Keywords: solid-principles, srp, ocp, lsp, isp, dip | Tokens: ~300 -->

**SOLID** são 5 princípios fundamentais de design orientado a objetos que garantem código manutenível, escalável e testável. Cada princípio é aplicado rigorosamente no Python RAG Project:

- **S - Single Responsibility**: Cada módulo/classe tem uma única razão para mudar. Ex: `retrieve_adaptive` só busca documentos, `rerank_documents` só reordena.
- **O - Open/Closed**: Código aberto para extensão, fechado para modificação. Ex: Adicione novos nodes ao LangGraph sem alterar nodes existentes.
- **L - Liskov Substitution**: Subclasses podem substituir suas classes base sem quebrar funcionalidade. Ex: `SessionConfig(BaseSettings)` mantém contrato da base.
- **I - Interface Segregation**: Clientes não devem depender de interfaces que não usam. Ex: `RAGState` expõe apenas campos necessários por camada.
- **D - Dependency Inversion**: Dependa de abstrações, não de implementações concretas. Ex: Layer 2 depende de assinaturas `state -> dict`, não de classes específicas.

📖 **Implementação Detalhada**: Ver [OOP Implementation Patterns](#oop-implementation-patterns) abaixo para exemplos Python completos e [project-codification.md](project-codification.md#pattern_applied) para padrões aplicados no código.

_Quick Wins (Implementation Tips):_

- Verifique **S** com ferramentas como **SonarQube**/cognitive complexity (<15 por método).
- Para **O**, adicione novas estratégias em módulos separados e integre via LangGraph.
- **L** validation: subclasses devem passar nos mesmos testes da base.
- **I** enforcement: use `TypedDict` para contratos mínimos, evite "God interfaces".
- **D** pattern: Layer 2 recebe callables `Callable[[RAGState], RAGState]`, não classes concretas.

<impact>Reduza bugs em 40% com testes unitários focados em contratos pequenos (SOLID S+I).</impact>

---

<!-- END CHUNK: rules-solid-overview -->
<!-- CHUNK: rules-abstraction | Lines: 124-171 | Keywords: typeddict, ragstate, literal, pep-589 | Tokens: ~500 -->
## 🏛️ OOP IMPLEMENTATION PATTERNS - DEEP DIVE

Os 4 pilares de Programação Orientada a Objetos aplicados ao Python RAG Project, com exemplos executáveis e integração com SOLID principles.

### **1. Abstraction - Contratos Tipados que isolam responsabilidades**
<!-- END CHUNK: rules-solid-overview -->
<!-- CHUNK: rules-abstraction | Lines: 124-171 | Keywords: typeddict, ragstate, literal, pep-589 | Tokens: ~500 -->

**Conceito**: Separar o **"o quê"** do **"como"**, expondo apenas interfaces essenciais e ocultando detalhes de implementação.

**No Projeto**: Usamos `TypedDict` e `Literal` para declarar contratos imutáveis, reforçando **S (Single Responsibility)** e **I (Interface Segregation)** de SOLID.

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

<!-- END CHUNK: rules-abstraction -->
<!-- CHUNK: rules-encapsulation | Lines: 172-218 | Keywords: pydantic, basesettings, field, computed-field | Tokens: ~500 -->
📌 **Como aplicar:** qualquer novo node da Camada 3 deve aceitar `RAGState` e retornar apenas os campos que realmente altera. Isso mantém o fluxo de dados coerente e fácil de testar. Ver [Polymorphism](#4-polymorphism---implementações-intercambiáveis-no-pipeline-rag) para exemplos de nodes plugáveis.

_Quick Wins:_ reutilize `TypedDict` sempre que precisar de contratos leves; `BaseModel` só é indicado quando validação em runtime for indispensável (cuidado com o overhead de ~2.5x).

---

### **2. Encapsulation - Validação automática + propriedades calculadas**
<!-- END CHUNK: rules-abstraction -->
<!-- CHUNK: rules-encapsulation | Lines: 172-218 | Keywords: pydantic, basesettings, field, computed-field | Tokens: ~500 -->

**Conceito**: Ocultar detalhes internos e expor apenas métodos/propriedades públicas, garantindo que o estado interno permaneça consistente.

**No Projeto**: Configurações e modelos de sessão usam Pydantic para encapsular validação, reforçando **I (Interface Segregation)** - expõe somente o que o cliente precisa.

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
<!-- END CHUNK: rules-encapsulation -->
<!-- CHUNK: rules-inheritance | Lines: 219-254 | Keywords: sessionconfig, settings, pydantic-inheritance | Tokens: ~400 -->
```

📌 **Como aplicar:** exponha apenas métodos de leitura (`get_config`, `memory_ratio`) e deixe que Pydantic rejeite estados inválidos automaticamente — evita `if` redundante em cada camada. Ver [SOLID Overview](#solid-principles---overview) para conexão com princípios S e I.

_Quick Wins:_ Em objetos de configuração, use `frozen=True` para forçar imutabilidade; para campos derivados (ex.: métricas) crie propriedades calculadas ao invés de duplicar valores no estado.

---

### **3. Inheritance - Reuso seguro com classes base Pydantic**
<!-- END CHUNK: rules-encapsulation -->
<!-- CHUNK: rules-inheritance | Lines: 219-254 | Keywords: sessionconfig, settings, pydantic-inheritance | Tokens: ~400 -->

**Conceito**: Criar hierarquias de classes onde subclasses herdam comportamento da classe base, permitindo reuso de código.

**No Projeto**: Aplicamos herança quando o framework já entrega comportamento reutilizável (ex.: `BaseSettings`, `BaseModel`), garantindo **L (Liskov Substitution)** de SOLID - subclasses não quebram o contrato da base.

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
<!-- END CHUNK: rules-inheritance -->
<!-- CHUNK: rules-polymorphism | Lines: 255-311 | Keywords: callable, strategy-pattern, adaptive-retrieval | Tokens: ~600 -->
    env_file = ".env"
    env_prefix = "PYTHON_RAG_"
```

📌 **Como aplicar:** herde apenas quando o framework oferece comportamento valioso (validação automática, carregamento de `.env`, etc.). Evite cadeias >2 níveis — prefira composição com helpers do Layer 4. Ver [project-codification.md - Composition vs Inheritance](project-codification.md#composition-vs-inheritance) para trade-offs detalhados.

_Quick Wins:_ Centralize toda configuração sensível em subclasses de `BaseSettings` para aproveitar caching interno e evitar boilerplate manual.

---

### **4. Polymorphism - Implementações intercambiáveis no pipeline RAG**
<!-- END CHUNK: rules-inheritance -->
<!-- CHUNK: rules-polymorphism | Lines: 255-311 | Keywords: callable, strategy-pattern, adaptive-retrieval | Tokens: ~600 -->

**Conceito**: Permitir que diferentes implementações sejam usadas de forma intercambiável através de uma interface comum.

**No Projeto**: LangGraph trata cada node como algo que recebe `RAGState` e devolve um diff de estado. Isso permite trocar implementações sem alterar a orquestração — polimorfismo funcional alinhado ao **D (Dependency Inversion)** de SOLID.

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

📌 **Como aplicar:** qualquer nova estratégia (ex.: sumarização, filtragem) deve seguir a mesma assinatura `def node(state: RAGState) -> RAGState:`. O grafo decide a ordem; nós são plugáveis, possibilitando testes A/B sem alterar a Camada 2. Ver [Abstraction](#1-abstraction---contratos-tipados-que-isolam-responsabilidades) para contratos TypedDict.

_Quick Wins:_ Concentre-se em manter nodes puros (sem efeitos colaterais) — isso facilita swap entre implementações e permite mocks simples em testes unitários.

**🔗 Cross-Pattern Integration:**

- **Abstraction + Polymorphism**: `TypedDict` contratos permitem nodes intercambiáveis
- **Encapsulation + Inheritance**: `BaseSettings` herda validação Pydantic encapsulada
<!-- END CHUNK: rules-polymorphism -->
<!-- CHUNK: rules-abc-part1 | Lines: 312-380 | Keywords: abstractmethod, metricscollector, abc-protocol | Tokens: ~700 -->
- **SOLID D + Polymorphism**: Camadas superiores dependem de assinaturas, não implementações

---

_Quick Wins (Architectural):_

- Evite herança profunda (>2 níveis) para prevenir violações Liskov
- Máximo 3 níveis: Base → Parent → Child
- Prefira composição sobre herança quando possível (Strategy pattern) - Ver [Composition vs Inheritance](#6-composition-vs-inheritance---trade-offs-e-decision-framework) abaixo

---

### **5. Abstract Base Classes (ABC) - Contratos Rígidos com Enforcement**
<!-- END CHUNK: rules-polymorphism -->
<!-- CHUNK: rules-abc-part1 | Lines: 312-380 | Keywords: abstractmethod, metricscollector, abc-protocol | Tokens: ~700 -->

**Conceito**: ABC (Abstract Base Classes) fornecem contratos de interface que subclasses **devem** implementar, garantindo **O (Open/Closed)** de SOLID - aberto para extensão, fechado para modificação.

**No Projeto**: Usamos ABC para definir interfaces de RAG nodes, garantindo que todas as implementações sigam o mesmo contrato `execute(state: RAGState) -> RAGState`.

```yaml
Pattern: abc.ABC + @abstractmethod
Module: abc.ABC, abc.abstractmethod
Reference: PEP 3119 (Abstract Base Classes)
Enforcement: Python raises TypeError se subclass não implementar métodos abstratos
SOLID Connection: Open/Closed Principle (O) - extensível via novas subclasses sem modificar base
```

📖 **Implementação no Codebase**: Ver [project-codification.md - RAGNodeStrategy](project-codification.md#ragnodestrategy) para padrão aplicado em LangGraph nodes.

**Python Example 1 - Interface Abstract para RAG Nodes:**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

# File: src/core/domain/strategies.py (exemplo proposto)
class RAGNodeStrategy(ABC):
    """
    Abstract interface for RAG workflow nodes.

    All nodes must implement execute() to be compatible with LangGraph.
    Enforces SOLID O: new strategies extend this base without modifying it.
    """

    @abstractmethod
    def execute(self, state: RAGState) -> Dict[str, Any]:
        """
        Process RAG state and return updated fields.

        Args:
            state: Current RAG state (TypedDict contract)

        Returns:
            Dict with updated state fields (merged by LangGraph)

        Raises:
            NotImplementedError: If subclass doesn't implement
        """
        pass

    def validate_state(self, state: RAGState) -> bool:
        """Optional: Common validation logic (não-abstrato)."""
        return "question" in state and len(state["question"]) > 0
```

**Python Example 2 - Implementações Concretas:**

```python
<!-- END CHUNK: rules-abc-part1 -->
<!-- CHUNK: rules-abc-part2 | Lines: 381-443 | Keywords: embeddingprovider, protocol-enforcement | Tokens: ~650 -->
from langsmith import traceable

# File: src/features/rag/strategies/retrieval.py (exemplo proposto)
class AdaptiveRetrievalStrategy(RAGNodeStrategy):
    """Concrete implementation: adaptive document retrieval."""

    def __init__(self, vector_store, top_k: int = 10):
        self.vector_store = vector_store
        self.top_k = top_k

    @traceable(run_type="retriever", name="Adaptive Retrieval")
    def execute(self, state: RAGState) -> Dict[str, Any]:
        """Retrieve documents based on question complexity."""
        complexity = state.get("complexity", "simple")
        k = self.top_k * 2 if complexity == "complex" else self.top_k
<!-- END CHUNK: rules-abc-part1 -->
<!-- CHUNK: rules-abc-part2 | Lines: 381-443 | Keywords: embeddingprovider, protocol-enforcement | Tokens: ~650 -->

        documents = self.vector_store.similarity_search(
            state["question"], k=k
        )

        return {"documents": [doc.page_content for doc in documents]}


# File: src/features/reranking/strategies/semantic.py (exemplo proposto)
class SemanticRerankingStrategy(RAGNodeStrategy):
    """Concrete implementation: BGE semantic reranking."""

    def __init__(self, reranker_model: str = "BAAI/bge-reranker-base"):
        self.reranker = get_reranker(reranker_model)

    @traceable(run_type="chain", name="Semantic Reranking")
    def execute(self, state: RAGState) -> Dict[str, Any]:
        """Rerank documents using cross-encoder."""
        if not self.reranker:
            return {}  # Graceful degradation

        reranked = rerank_documents(
            query=state["question"],
            documents=state["documents"],
            threshold=0.5
        )

        return {"documents": reranked, "quality_score": 0.9}
```

📌 **Como aplicar:**

1. Defina interface ABC para cada categoria de strategy (Retrieval, Reranking, Generation)
2. Implemente múltiplas variantes concretas (ex: `DenseRetrieval`, `HybridRetrieval`)
3. LangGraph recebe strategy via dependency injection, não hard-coded class
4. Teste cada strategy isoladamente (ABC garante compatibilidade)

_Quick Wins:_

- ABC > Protocol quando você quer **enforcement** (Python raises TypeError)
- Protocol > ABC quando você quer **duck typing** (mais flexível)
- Use ABC para **core abstractions** (RAGNodeStrategy), Protocol para **helpers**
- Combine com [Polymorphism](#4-polymorphism---implementações-intercambiáveis-no-pipeline-rag) para nodes plugáveis

**🔗 ABC vs Protocol Comparison:**

<!-- END CHUNK: rules-abc-part2 -->
<!-- CHUNK: rules-composition-part1 | Lines: 444-520 | Keywords: dependency-injection, aggregation, composition | Tokens: ~800 -->
| Critério        | ABC (`abc.ABC`)                       | Protocol (`typing.Protocol`) |
| --------------- | ------------------------------------- | ---------------------------- |
| **Enforcement** | Runtime TypeError se não implementado | Type checker warning only    |
| **Flexibility** | Requires explicit inheritance         | Duck typing (structural)     |
| **Use Case**    | Core contracts, mandatory interface   | Optional helpers, type hints |
| **Performance** | Slight overhead (isinstance checks)   | Zero overhead (compile-time) |
| **Projeto**     | RAGNodeStrategy (core)                | Helper protocols (optional)  |

**⚠️ Edge Cases:**

- **Multiple Inheritance**: ABC suporta, mas cuidado com diamond problem (use `super()` corretamente)
- **Python <3.8**: ABC funciona, mas type hints podem precisar `from __future__ import annotations`
- **Abstract Properties**: Use `@property + @abstractmethod` para propriedades abstratas obrigatórias

---

### **6. Composition vs Inheritance - Trade-offs e Decision Framework**
<!-- END CHUNK: rules-abc-part2 -->
<!-- CHUNK: rules-composition-part1 | Lines: 444-520 | Keywords: dependency-injection, aggregation, composition | Tokens: ~800 -->

**Conceito**: Escolher entre **"Is-a"** (Inheritance) e **"Has-a"** (Composition) é uma decisão arquitetural crítica que impacta flexibilidade, testabilidade e manutenção.

**No Projeto**: Usamos **Inheritance** para reutilizar validação Pydantic (`SessionConfig(BaseSettings)`) e **Composition** para combinar funcionalidades independentes (`RAGState` possui `List[Document]`, não herda de `Document`).

```yaml
Decision Rule: Favor Composition over Inheritance (GoF principle)
Exception: Inherit quando framework já oferece comportamento valioso (Pydantic, ABC)
Reference: "Design Patterns" (Gang of Four), Effective Python (Item 37)
SOLID Connection: Liskov Substitution (L) - herança segura quando subclass não quebra contrato
```

**Decision Framework - Quando usar cada um:**

| Critério            | Use Inheritance                        | Use Composition                        |
| ------------------- | -------------------------------------- | -------------------------------------- |
| **Relacionamento**  | "Is-a" claro (Circle IS-A Shape)       | "Has-a" ou "Uses-a" (Car HAS-A Engine) |
| **Reuso**           | Comportamento da base é 80%+ relevante | Precisa apenas parte da funcionalidade |
| **Flexibilidade**   | Hierarquia estável, poucas variações   | Múltiplas combinações de componentes   |
| **Acoplamento**     | Aceitável (framework bem estabelecido) | Desacoplamento crítico                 |
| **Testabilidade**   | Base já tem testes completos           | Mock de componentes independentes      |
| **Exemplo Projeto** | `SessionConfig(BaseSettings)`          | `RAGState` has `List[Document]`        |

**Python Example 1 - Inheritance (quando apropriado):**

```python
from pydantic import BaseSettings, Field

# ✅ CORRETO: Herança quando framework oferece valor
# File: src/infrastructure/config/settings.py
class Settings(BaseSettings):
    """
    Herda de BaseSettings para aproveitar:
    - Validação automática de tipos
    - Carregamento de .env
    - Caching de configuração
    - Type hints enforcement
    """
    langsmith_api_key: str = Field(..., description="LangSmith API Key")
    llm_model: str = Field(default="gemini-2.0-flash-exp")
    reranker_enabled: bool = Field(default=True)

    class Config:
        env_file = ".env"
        env_prefix = "PYTHON_RAG_"

    # ✅ Liskov Substitution: Settings pode substituir BaseSettings
    # ✅ Open/Closed: Extensível via novos campos sem modificar BaseSettings
```

**Python Example 2 - Composition (alternativa moderna):**

```python
from dataclasses import dataclass
from typing import Protocol

# File: src/core/domain/protocols.py (exemplo proposto)
class VectorStore(Protocol):
<!-- END CHUNK: rules-composition-part1 -->
<!-- CHUNK: rules-composition-part2 | Lines: 521-594 | Keywords: decision-matrix, trade-offs | Tokens: ~750 -->
    """Interface para vector stores (Protocol, não ABC)."""
    def similarity_search(self, query: str, k: int) -> list: ...

class Reranker(Protocol):
    """Interface para rerankers."""
    def rerank(self, query: str, docs: list) -> list: ...

# ✅ CORRETO: Composição para combinar componentes independentes
# File: src/features/rag/pipeline.py (exemplo proposto)
@dataclass
class RAGPipeline:
    """
    Composição: HAS-A VectorStore, HAS-A Reranker.

    Vantagens vs Herança:
    - Flexibilidade: swap vector_store sem alterar classe
    - Testabilidade: mock components facilmente
    - Desacoplamento: components não dependem de RAGPipeline
    """
<!-- END CHUNK: rules-composition-part1 -->
<!-- CHUNK: rules-composition-part2 | Lines: 521-594 | Keywords: decision-matrix, trade-offs | Tokens: ~750 -->
    vector_store: VectorStore  # Composition: HAS-A
    reranker: Reranker          # Composition: HAS-A
    llm: Any                    # Composition: HAS-A

    def execute(self, question: str) -> str:
        """Pipeline usando componentes compostos."""
        # 1. Retrieval (usa vector_store)
        documents = self.vector_store.similarity_search(question, k=10)

        # 2. Reranking (usa reranker)
        reranked = self.reranker.rerank(question, documents)

        # 3. Generation (usa llm)
        context = "\n".join(reranked)
        answer = self.llm.generate(question, context)

        return answer

# ✅ Dependency Injection: componentes injetados via construtor
pipeline = RAGPipeline(
    vector_store=FAISSStore(),
    reranker=BGEReranker(),
    llm=GeminiLLM()
)
```

📌 **Como aplicar no Projeto:**

1. **Herde de Pydantic** quando precisar validação (`BaseModel`, `BaseSettings`)
2. **Herde de ABC** quando precisar enforcement de interface ([ver ABC acima](#5-abstract-base-classes-abc---contratos-rígidos-com-enforcement))
3. **Use Composition** para combinar funcionalidades independentes (RAGPipeline com VectorStore + Reranker)
4. **Prefira Protocol** sobre ABC quando flexibilidade > enforcement
5. **Evite herança >2 níveis** - cria acoplamento rígido

_Quick Wins:_

- **Refactoring smell**: Se você herda mas override 50%+ dos métodos → use Composition
- **Test smell**: Se mockar base class é difícil → use Composition
- **Design smell**: Se subclass quebra testes da base → viola Liskov (L), use Composition
- **Performance**: Composition é ~5-10% mais rápido (sem overhead de method resolution order)

**🔗 Cross-References:**

- Ver [Inheritance](#3-inheritance---reuso-seguro-com-classes-base-pydantic) para padrão Pydantic
- Ver [Abstract Base Classes](#5-abstract-base-classes-abc---contratos-rígidos-com-enforcement) para interfaces rígidas
- Ver [Polymorphism](#4-polymorphism---implementações-intercambiáveis-no-pipeline-rag) para strategy injection
- Ver [project-codification.md - Composition Patterns](project-codification.md#composition-patterns) para exemplos reais do código

**⚠️ Anti-Patterns (Evitar):**

```python
# ❌ ERRADO: Herança profunda (>2 níveis)
class Animal: pass
<!-- END CHUNK: rules-composition-part2 -->
<!-- CHUNK: rules-compliance-immutable | Lines: 595-632 | Keywords: immutable-rules, approval-criteria, quality-gates | Tokens: ~400 -->
class Mammal(Animal): pass
class Dog(Mammal): pass
class Labrador(Dog): pass  # ❌ 4 níveis = frágil

# ❌ ERRADO: Herdar só para reusar 1 método
class Logger:
    def log(self, msg): print(msg)

class Service(Logger):  # ❌ Só usa log(), não IS-A Logger
    def process(self): self.log("processing")

# ✅ CORRETO: Composição
class Service:
    def __init__(self, logger: Logger):
        self.logger = logger  # HAS-A Logger
    def process(self): self.logger.log("processing")
```

---

## 🎖️ COMPLIANCE ENFORCEMENT
<!-- END CHUNK: rules-composition-part2 -->
<!-- CHUNK: rules-compliance-immutable | Lines: 595-632 | Keywords: immutable-rules, approval-criteria, quality-gates | Tokens: ~400 -->

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
<!-- END CHUNK: rules-compliance-immutable -->
<!-- CHUNK: rules-compliance-tools | Lines: 633-682 | Keywords: validation-tools, pre-commit, sonarqube | Tokens: ~500 -->

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
<!-- END CHUNK: rules-compliance-immutable -->
<!-- CHUNK: rules-compliance-tools | Lines: 633-682 | Keywords: validation-tools, pre-commit, sonarqube | Tokens: ~500 -->

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
<!-- END CHUNK: rules-compliance-tools -->
<!-- CHUNK: rules-compliance-git | Lines: 683-738 | Keywords: git-commit-hooks, github-actions, ci-cd | Tokens: ~600 -->

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
<!-- END CHUNK: rules-compliance-tools -->
<!-- CHUNK: rules-compliance-git | Lines: 683-738 | Keywords: git-commit-hooks, github-actions, ci-cd | Tokens: ~600 -->

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
<!-- END CHUNK: rules-compliance-git -->
<!-- CHUNK: rules-compliance-checklist | Lines: 739-773 | Keywords: compliance-checklist, verification-steps | Tokens: ~350 -->

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
<!-- END CHUNK: rules-compliance-git -->
<!-- CHUNK: rules-compliance-checklist | Lines: 739-773 | Keywords: compliance-checklist, verification-steps | Tokens: ~350 -->

**Before Every Commit:**

- [ ] Type hints added (mypy strict)
- [ ] SOLID principles respected (<15 cognitive complexity)
- [ ] Clean Architecture maintained (4 layers)
<!-- END CHUNK: rules-compliance-checklist -->
<!-- CHUNK: rules-cross-reference | Lines: 774-811 | Keywords: cross-reference-table, bidirectional-links | Tokens: ~400 -->
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

## 🔗 CROSS-REFERENCE TABLE

> **Quick Navigation:** Jump between architectural concepts (this doc) and their implementations ([project-codification.md](project-codification.md))

| Concept                        | This Doc (Lines) | project-codification.md (Lines)       | Files                                                                 |
| ------------------------------ | ---------------- | ------------------------------------- | --------------------------------------------------------------------- |
| **Clean Architecture**         | 79-95            | 91-1087 (4 layers overview)           | Multiple (see layers below)                                           |
| Layer 1: Presentation          | 79-95            | 91-303                                | `scripts/chat.py`, `src/features/conversation/conversation.py`        |
| Layer 2: Orchestration         | 79-95            | 304-655                               | `src/features/conversation/graph.py`, `src/features/rag/graph.py`     |
| Layer 3: Business Logic        | 79-95            | 656-887                               | `src/features/rag/nodes.py`, `src/features/reranking/reranker.py`     |
| Layer 4: Services              | 79-95            | 888-1087                              | `src/infrastructure/config/settings.py`, `src/core/services/`         |
| **SOLID Principles**           | 96-119           | Implicit (see patterns)               | Applied throughout codebase                                           |
<!-- END CHUNK: rules-compliance-checklist -->
<!-- CHUNK: rules-cross-reference | Lines: 774-811 | Keywords: cross-reference-table, bidirectional-links | Tokens: ~400 -->
| Single Responsibility          | 96-119           | 1471-1504 (Rule 3)                    | All modules                                                           |
| Dependency Inversion           | 96-119           | 1294-1380 (DI pattern)                | `src/core/domain/session.py`                                          |
| **Abstraction (TypedDict)**    | 124-171          | 91-303 (RAGState examples)            | `src/core/domain/state.py`                                            |
| **Encapsulation (Pydantic)**   | 172-218          | 1294-1380 (SessionConfig)             | `src/core/domain/session.py`, `src/infrastructure/config/settings.py` |
| **Inheritance (BaseSettings)** | 219-254          | 1294-1380 (DI pattern)                | `src/core/domain/session.py`, `src/infrastructure/config/settings.py` |
| **Polymorphism (Strategy)**    | 255-311          | 1222-1293 (Strategy pattern)          | `src/features/rag/nodes.py`                                           |
| **ABC (Protocols)**            | 312-443          | Implicit in interfaces                | `src/shared/types/protocols.py`                                       |
<!-- END CHUNK: rules-cross-reference -->
| **Composition**                | 444-594          | 1294-1380 (SessionConfig composition) | `src/core/domain/session.py`                                          |
| **RAGState**                   | 124-171          | 91-303, 304-655, 656-887              | `src/core/domain/state.py`                                            |
| **SessionConfig**              | 172-218, 444-594 | 1294-1380                             | `src/core/domain/session.py`                                          |
| **LangGraph Integration**      | 79-95, 255-311   | 304-655 (Layer 2)                     | `src/features/conversation/graph.py`, `src/features/rag/graph.py`     |
| **Strategy Pattern**           | 255-311          | 1222-1293                             | `src/features/rag/nodes.py` (retrieve_adaptive, rerank_documents)     |
| **Dependency Injection**       | 444-594          | 1294-1380                             | `src/core/domain/session.py` (SessionConfig composition)              |
| **Compliance Enforcement**     | 595-773          | 1531-1554                             | `.pre-commit-config.yaml`, `.githooks/`, `.github/workflows/`         |

## 📚 RELATED DOCUMENTS

| Document                                           | Relevant Sections                                                         | Description                                                                |
| -------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [behavioral-rules.md](behavioral-rules.md)         | Lines 45-78 (ROI Framework), Lines 135-175 (Token Efficiency)             | Execution protocols, efficiency standards, ROI decision framework          |
| [methodology-rules.md](methodology-rules.md)       | Lines 25-60 (TDD), Lines 85-120 (XP+Kanban+OOP)                           | Development methodology, sprint structure, quality metrics                 |
| [tools-rules.md](tools-rules.md)                   | Lines 30-80 (CLI tools), Lines 120-180 (Terminal techniques)              | Tool usage standards, anti-truncation strategies, performance optimization |
| [mcp-rules.md](mcp-rules.md)                       | Lines 16-34 (Pattern 1), Lines 36-51 (Pattern 2), Lines 53-68 (Pattern 3) | MCP integration patterns, workflow examples, enforcement rules             |
| [project-codification.md](project-codification.md) | Lines 91-1087 (Architecture), Lines 1222-1470 (Patterns)                  | Implementation details, code examples, enterprise patterns                 |

---

```markdown
**📅 Created:** 2025-08-06
**🔄 Last Update:** 2025-10-19
**📋 Status:** ACTIVE AND MANDATORY
**🎯 Application:** ALWAYS WHEN THE USER MENTIONS OR WHEN THE AGENT NEEDS CONTEXT OR RELEVANT INFORMATION ABOUT THE PROJECT
**🔍 Linked:** .github/copilot-rules/project-codification.md
```

---

_This document defines the development, coding, security and deployment rules for the PROJECT PYTHON PROJECT_
<!-- END CHUNK: rules-cross-reference -->
