---
metadata: |
name: '.github/copilot-rules/project-codification.md'
description: 'Coding standards, security rules, UI/UX guidelines, API conventions, logging practices, testing strategies, deployment configurations, and documentation requirements for the PYTHON_PROJECT.'
aiOptimized: true
alwaysApply: false
applyManually: true
syncWith: ['.github\copilot-rules\project-rules.md'](project-rules.md)
---

**🎯 OBJETIVO**: Garantir padrões de design, arquitetura, engenharia e DNA de codificação do PYTHON_PROJECT estabelecidos e padronizados. Para manter um código limpo, modular, seguro, performático e fácil de manter, evoluir com escalabilidade.

---

# 🗺️ QUICK NAVIGATION INDEX

> **For AI Agents:** Use `read_file(offset, limit)` with line ranges below for token-efficient context retrieval (70% reduction vs full file read). For architectural concepts, see [project-rules.md](project-rules.md#quick-navigation-index).

## 🏗️ CLEAN ARCHITECTURE - 4 LAYERS (Lines 85-1087)

- [Layer 1: Presentation (CLI/HTTP)](#1-camada-apresentação-presentation-layer) → Lines 91-303 | **Files:** `scripts/chat.py`, `src/features/conversation/conversation.py` | **Keywords:** Command Pattern, @traceable, graph.invoke()
- [Layer 2: Orchestration (LangGraph)](#2-camada-orquestração-orchestrationgraph-layer) → Lines 304-655 | **Files:** `src/features/conversation/graph.py`, `src/features/rag/graph.py` | **Keywords:** StateGraph, add_node, add_edge, compile()
- [Layer 3: Business Logic (RAG Nodes)](#3-camada-lógica-business-logic--rag-nodes) → Lines 656-887 | **Files:** `src/features/rag/nodes.py`, `src/features/reranking/reranker.py` | **Keywords:** retrieve_adaptive, rerank_documents, generate_answer
- [Layer 4: Specialized Services](#4-camada-especializada) → Lines 888-1087 | **Files:** `src/infrastructure/`, `src/core/services/` | **Keywords:** Settings, FAISS, LangSmith, CrossEncoder

## 📊 IMPLEMENTATION PATTERNS (Lines 1088-1470)

- [Inventário Estruturado](#-inventário-estruturado-atende-t-20) → Lines 1088-1123 | **Context:** File organization, module mapping
- [Linguagem Universal](#-linguagem-universal) → Lines 1124-1219 | **Keywords:** Communication patterns, thread-safety, validation
- [Strategy Pattern](#1-strategy-pattern-obrigatório-para-algoritmos) → Lines 1222-1293 | **Files:** `src/features/rag/nodes.py` | **Keywords:** Callable, adaptive_retrieval, complexity routing
- [Dependency Injection](#2-dependency-injection-obrigatório-para-gerentes) → Lines 1294-1380 | **Files:** `src/core/domain/session.py` | **Keywords:** SessionConfig, Settings, lazy_load
- [Exception Hierarchy](#3-exception-hierarchy-obrigatório-para-erros) → Lines 1381-1470 | **Keywords:** Custom exceptions, error handling, retry logic

## 🎖️ ARCHITECTURAL RULES (Lines 1471-1530)

- [Immutable Rules](#regra-1-hierarquia-sem-bypass) → Lines 1471-1504 | **Keywords:** Hierarchy enforcement, no bypass, single responsibility, dependency direction
- [Architectural Validation](#-validação-arquitetural-obrigatória) → Lines 1505-1514 | **Keywords:** Compliance tests, import-linter, architecture violations
- [Compliance Metrics](#-métricas-de-compliance-obrigatórias) → Lines 1515-1530 | **Keywords:** Test coverage, cyclomatic complexity, code duplication

## 🔧 COMPLIANCE ENFORCEMENT (Lines 1531-1554)

- See [project-rules.md - COMPLIANCE](project-rules.md#-compliance-lines-595-773) for detailed enforcement rules (pre-commit, git hooks, GitHub Actions)

## 🔍 SEARCH SHORTCUTS

### By Layer (Clean Architecture)

- **Layer 1 (Presentation):** Lines 91-303 → `scripts/chat.py`, `src/features/conversation/conversation.py`
- **Layer 2 (Orchestration):** Lines 304-655 → `src/features/conversation/graph.py`, `src/features/rag/graph.py`
- **Layer 3 (Business Logic):** Lines 656-887 → `src/features/rag/nodes.py`, `src/features/reranking/reranker.py`
- **Layer 4 (Services):** Lines 888-1087 → `src/infrastructure/`, `src/core/services/`

### By Pattern (Enterprise)

- **Strategy Pattern:** Lines 1222-1293 (adaptive retrieval, complexity routing)
- **Dependency Injection:** Lines 1294-1380 (SessionConfig, Settings composition)
- **Exception Hierarchy:** Lines 1381-1470 (custom exceptions, error handling)
- **Communication Pattern:** Lines 1124-1219 (thread-safety, validation)

### By File Reference

- **CLI Handler:** `scripts/chat.py` → Lines 91-303 (Layer 1 example)
- **Conversation Graph:** `src/features/conversation/graph.py` → Lines 304-655 (Layer 2 example)
- **RAG Nodes:** `src/features/rag/nodes.py` → Lines 656-887, 1222-1293 (Layer 3 + Strategy)
- **Reranker:** `src/features/reranking/reranker.py` → Lines 656-887 (CrossEncoder integration)
- **Session Config:** `src/core/domain/session.py` → Lines 1294-1380 (DI pattern)
- **Settings:** `src/infrastructure/config/settings.py` → Lines 888-1087 (Layer 4)
- **State Definition:** `src/core/domain/state.py` → Lines 91-303 (RAGState, ConversationalRAGState)

### By Class/Function (Grep-Optimized)

- **RAGState:** Lines 91-303 (definition), 304-655 (graph usage), 656-887 (node transformations)
- **SessionConfig:** Lines 1294-1380 (DI pattern), 888-1087 (Layer 4 integration)
- **graph.invoke():** Lines 91-303 (Layer 1 call), 304-655 (graph compilation)
- **retrieve_adaptive:** Lines 656-887, 1222-1293 (implementation + Strategy pattern)
- **rerank_documents:** Lines 656-887 (CrossEncoder reranking)
- **generate_answer:** Lines 656-887 (LLM generation node)
- **@traceable:** Lines 91-303 (LangSmith observability)
- **StateGraph:** Lines 304-655 (LangGraph orchestration)
- **BaseSettings:** Lines 1294-1380 (Pydantic DI), 888-1087 (Layer 4 Settings)

### Cross-Reference to project-rules.md

- **SOLID Principles:** [project-rules.md Lines 96-119](project-rules.md#-solid-principles---overview)
- **OOP Patterns (Abstract):** [project-rules.md Lines 120-594](project-rules.md#-oop-implementation-patterns---deep-dive)
- **Compliance Details:** [project-rules.md Lines 595-773](project-rules.md#-compliance-lines-595-773)

---

## 🏗️ ARQUITETURA ENTERPRISE HIERÁRQUICA - PADRÕES VALIDADOS

### ✅ **CAMADA 1: APRESENTAÇÃO (CLI/HTTP Interface)**

A arquitetura do PYTHON_PROJECT segue **Clean Architecture** com 4 camadas hierárquicas independentes:

#### **1. CAMADA APRESENTAÇÃO (Presentation Layer)**

```yaml
Responsabilidade: |
  - Parse input do usuário (CLI ou HTTP)
  - Dispatch comandos (/reset, /quit, /help)
  - Formatar requests para Layer 2
  - Formatar responses do Layer 2
  - Gerenciar sessões de usuário

Conversa_com: |
  - UP: Usuário/Cliente (CLI stdin/stdout ou HTTP requests)
  - DOWN: Layer 2 (Orchestration) via graph.invoke()
  - SIDE: Layer 4 (Memory Manager) via get_conversation_config()

Pattern_Applied: |
  - Command Pattern: CLI command dispatch (/reset, /quit, /help)
  - Handler Pattern: Conversational node handlers (@traceable nodes)
  - Orchestration Pattern: Wraps Layer 2 graph invocation
  - Dependency Injection: Session config passed from Layer 4

Regra_Rígida: |
  - NÃO contém lógica de negócio (delegue para Layer 2+)
  - NÃO contém estado persistente (delegue para Layer 4)
  - DEVE validar entrada antes de passar para Layer 2
  - DEVE formatar saída de maneira legível ao usuário
  - DEVE rastrear observabilidade com @traceable
```

**Arquivos Implementadores:**

- `scripts/chat.py` - CLI handler principal (linhas 1-150)
- `src/features/conversation/conversation.py` - Handler nodes (linhas 1-240)
- `src/features/conversation/conversation_graph.py` - Orchestration wrapper (linhas 146-210)
- `src/core/services/memory_manager.py` - Session management (linhas 1-100)

```python
# ✅ PADRÃO CORRETO - Presentation Layer Flow

# 1. INPUT PARSING (scripts/chat.py, Line 60-75)
def run_interactive_conversation(user_id: str = "cli_user"):
    config = get_conversation_config(user_id)  # Layer 4: get session
    while True:
        user_input = input("You: ").strip()  # Parse user input

        # 2. COMMAND DISPATCH (Command Pattern)
        if user_input.startswith("/"):
            command = user_input.lower()
            if command == "/reset":
                reset_conversation(user_id)  # Layer 4: reset session
                config = get_conversation_config(user_id)
            elif command == "/quit":
                break
            continue

        # 3. REQUEST FORMATTING + LAYER 2 INVOCATION
        # File: src/features/conversation/conversation_graph.py (Line 146-165)
        def run_conversational_query(question: str, user_id: str, config: dict) -> str:
            graph = create_conversational_rag_graph()  # Layer 2: create graph
            initial_state = {
                "messages": [HumanMessage(content=question)],  # Format as message
                "question": question,
                "complexity": "",
                "documents": [],
                "generation": "",
            }
            final_state = graph.invoke(initial_state, config)  # Layer 2: invoke

            # 4. RESPONSE FORMATTING
            answer = final_state["generation"]  # Extract response
            print(f"Assistant:\\n{answer}")  # Format for user

# Handler Nodes Pattern (Handler Pattern + Decorator)
# File: src/features/conversation/conversation.py (Line 26-60)
@traceable(run_type="chain", name="Analyze Context for Follow-up")
def analyze_context(state: ConversationalRAGState) -> Dict[str, Any]:
    """Handler: Parse state input → process → return updated state."""
    messages = state["messages"]
    current_question = messages[-1].content if messages else ""

    # Parse + Process
    if len(messages) <= 1:
        is_followup = False
    else:
        # LLM-based analysis (Layer 2 responsibility)
        is_followup = llm_analyze(messages)

    # Return formatted update
    return {"is_followup": is_followup, "question": current_question}

# ✅ PADRÃO CORRETO - Session Management (Delegation to Layer 4)
# File: src/core/services/memory_manager.py (Line 90-100)
def get_conversation_config(user_id: str = "default") -> dict:
    """Delegate session retrieval to Layer 4."""
    return conversation_manager.get_config(user_id)

def reset_conversation(user_id: str = "default") -> None:
    """Delegate session reset to Layer 4."""
    conversation_manager.reset_session(user_id)
```

**Fluxo de Comunicação (Layer 1):**

```
┌─── User Input (CLI) ───────────────────────────┐
│                                                 │
├─ Input Parser (Line 60-75)                    │
│  └─ Valida e limpa entrada                    │
│                                                │
├─ Command Dispatcher (Line 80-95)              │
│  ├─ /reset → Layer 4 reset_conversation()    │
│  ├─ /quit → Exit loop                         │
│  ├─ /help → Print help                        │
│  └─ question → Layer 2 invocation              │
│                                                │
├─ Request Formatter (Line 146-165)             │
│  └─ Convert string → HumanMessage + state    │
│                                                │
├─ [Layer 2 Processing] ← Graph invocation      │
│                                                │
├─ Response Formatter (Line 205-210)            │
│  └─ Extract generation + format               │
│                                                │
├─ [Output] Print formatted response            │
└─────────────────────────────────────────────────┘
```

**Exemplos Reais de Código:**

_Exemplo 1: CLI Command Handler (Command Pattern)_

```python
# File: scripts/chat.py (Line 70-100)
if user_input.startswith("/"):
    command = user_input.lower()
    if command in ["/quit", "/exit"]:
        print("\\n👋 Goodbye!")
        break
    elif command == "/reset":
        reset_conversation(user_id)
        config = get_conversation_config(user_id)
        conversation_count = 0
        print("\\n🔄 Conversation reset!")
    elif command == "/help":
        print_help()
    else:
        print(f"❌ Unknown command: {user_input}")
    continue
```

_Exemplo 2: Question Handler (Orchestration Pattern)_

```python
# File: scripts/chat.py (Line 110-125)
conversation_count += 1
print(f"\\n[Turn {conversation_count}] Processing...\\n")

answer = run_conversational_query(user_input, user_id, config)

print(f"\\n{'='*80}")
print("Assistant:")
print("-" * 80)
print(answer)
print("=" * 80 + "\\n")
```

_Exemplo 3: Handler Node (Handler Pattern + Decorator)_

```python
# File: src/features/conversation/conversation.py (Line 26-60)
@traceable(run_type="chain", name="Analyze Context for Follow-up")
def analyze_context(state: ConversationalRAGState) -> Dict[str, Any]:
    messages = state["messages"]
    current_question = messages[-1].content if messages else ""
    original_question = current_question

    if len(messages) <= 1:
        return {
            "is_followup": False,
            "question": current_question,
            "original_question": original_question,
        }

    # Get recent history
    history_text = "\\n".join([f"{m.type}: {m.content}" for m in messages[-5:]])

    # LLM analysis
    prompt = ChatPromptTemplate.from_template(...)
    response = (prompt | llm).invoke({"history": history_text, "question": current_question})

    return {"is_followup": "sim" in response.content.lower(), "question": current_question}
```

**Constraints & Métricas (Layer 1):**

```yaml
Performance_Targets:
  Input_Parsing: '< 10ms (regex-based)'
  Command_Dispatch: '< 5ms (dict lookup)'
  State_Formatting: '< 5ms (dict construction)'
  Response_Formatting: '< 50ms (string extraction)'

Layer_1_Boundaries:
  '✅ Includes': 'CLI parsing, command dispatch, request formatting, response formatting, session mgmt'
  '❌ Excludes': 'LLM processing, vector search, database ops, reranking'

Dependency_Direction:
  'UP': 'Receives from user/client'
  'DOWN': 'Delegates to Layer 2 (Orchestration)'
  'SIDE': 'Uses Layer 4 (Memory Manager) for sessions'
  'NEVER': 'Circular dependencies, direct Layer 3/4 business logic'
```

#### **2. CAMADA ORQUESTRAÇÃO (Orchestration/Graph Layer)**

```yaml
Responsabilidade: |
  - Definir schema de estado (TypedDict com tipos seguros)
  - Registrar nós (funções como nodes do grafo)
  - Definir arestas (connections entre nós)
  - Implementar lógica de roteamento (conditional edges)
  - Compilar grafo em estado máquina executável
  - Executar grafo com estado inicial
  - Integrar persistência (memory/checkpointer)

Conversa_com: |
  - UP: Layer 1 (Orchestrator) via graph.invoke()
  - DOWN: Layer 3 (Node functions) via node registration
  - SIDE: Layer 4 (MemorySaver) via checkpointer

Pattern_Applied: |
  - StateGraph Pattern: Typed state machine assembly
  - Node Composition Pattern: Functions as nodes
  - Conditional Routing Pattern: add_conditional_edges
  - Graph Compilation Pattern: build → execute
  - Memory Integration Pattern: checkpointer + thread_id

Regra_Rígida: |
  - NÃO contém lógica de negócio (delegue para Layer 3)
  - DEVE usar TypedDict (performance vs Pydantic)
  - DEVE registrar TODOS os nós explicitamente
  - DEVE definir TODOS os edges (sem ambiguidade)
  - DEVE compilar grafo UMA VEZ (reutilize instância)
  - DEVE suportar loop detection (MAX_ITERATIONS)
  - DEVE manter type safety (Literal, Annotated)
```

**Arquivos Implementadores:**

- `src/features/rag/graph_rag.py` - Grafo RAG básico (linhas 1-133)
- `src/features/conversation/conversation_graph.py` - Grafo conversacional (linhas 1-210)
- `src/core/domain/state.py` - Definições de estado (linhas 1-80)
- `src/core/services/memory_manager.py` - Persistência (linhas 1-50)

```python
# ✅ PADRÃO CORRETO - StateGraph Assembly Pattern

# 1. STATE DEFINITION (Type-safe schema)
# File: src/core/domain/state.py (Lines 20-45)
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import BaseMessage

class RAGState(TypedDict):
    """Typed state for RAG workflow - ensures compile-time safety."""
    question: str
    complexity: Literal["simple", "complex"]  # Enum-like safety
    documents: list  # Retrieved documents
    generation: str  # Generated answer
    quality_score: Annotated[float, Field(ge=0.0, le=1.0)]  # Bounded 0-1
    iterations: Annotated[int, Field(ge=0)]  # Non-negative

class ConversationalRAGState(TypedDict):
    """Extended state with memory for multi-turn conversations."""
    messages: Annotated[Sequence[BaseMessage], add_messages]  # Chat history (reducer)
    question: str
    complexity: Literal["simple", "complex"]
    documents: list
    generation: str
    quality_score: Annotated[float, Field(ge=0.0, le=1.0)]
    iterations: Annotated[int, Field(ge=0)]
    is_followup: bool  # Follow-up detection
    original_question: str  # Raw input

# 2. GRAPH ASSEMBLY (StateGraph construction)
# File: src/features/rag/graph_rag.py (Lines 51-95)
from langgraph.graph import StateGraph, START, END

def create_rag_graph():
    """Creates and compiles RAG workflow state machine."""
    # Initialize with typed state
    workflow = StateGraph(RAGState)

    # Register nodes (Layer 3 functions)
    workflow.add_node("classify", classify_question)
    workflow.add_node("retrieve", retrieve_adaptive)
    workflow.add_node("rerank", rerank_documents)
    workflow.add_node("generate", generate_answer)
    workflow.add_node("validate", validate_quality)
    workflow.add_node("refine", refine_answer)

    # Define edges (connections between nodes)
    workflow.add_edge(START, "classify")  # Entry point
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "rerank")
    workflow.add_edge("rerank", "generate")
    workflow.add_edge("generate", "validate")

    # Conditional edge (routing logic based on state)
    workflow.add_conditional_edges(
        "validate",  # Source node
        should_refine,  # Routing function
        {"refine": "refine", END: END}  # Options map
    )
    workflow.add_edge("refine", "validate")  # Loop back

    # Compile into executable state machine
    graph = workflow.compile()
    return graph

# 3. CONDITIONAL ROUTING (Decision logic)
# File: src/features/rag/graph_rag.py (Lines 27-45)
def should_refine(state: RAGState) -> str:
    """Routing function: decides if answer needs refinement or exit."""
    quality_score = state.get("quality_score", 0.0)
    iterations = state.get("iterations", 0)

    if quality_score >= 0.7:
        return END  # Quality good - exit

    if iterations >= MAX_ITERATIONS:
        return END  # Max iterations - exit

    return "refine"  # Low quality - refine answer

# 4. GRAPH EXECUTION (State machine invocation)
# File: src/features/rag/graph_rag.py (Lines 96-130)
def run_rag_query(question: str) -> str:
    """Executes RAG query through LangGraph workflow."""
    graph = create_rag_graph()

    # Initialize state (clean slate for each query)
    initial_state = {
        "question": question,
        "complexity": "",
        "documents": [],
        "generation": "",
        "quality_score": 0.0,
        "iterations": 0,
    }

    # Invoke graph (state machine execution)
    final_state = graph.invoke(initial_state)

    # Extract result
    return final_state["generation"]

# 5. MEMORY INTEGRATION (Persistence)
# File: src/features/conversation/conversation_graph.py (Lines 72-140)
from langgraph.checkpoint.memory import MemorySaver

def create_conversational_rag_graph():
    """Creates conversational RAG with memory persistence."""
    workflow = StateGraph(ConversationalRAGState)

    # Add nodes (conversational + RAG)
    workflow.add_node("analyze_context", analyze_context)
    workflow.add_node("expand_question", expand_question)
    workflow.add_node("check_clarification", check_clarification)
    workflow.add_node("classify", classify_question)
    workflow.add_node("retrieve", retrieve_adaptive)
    workflow.add_node("rerank", rerank_documents)
    workflow.add_node("generate", generate_answer)
    workflow.add_node("validate", validate_quality)
    workflow.add_node("refine", refine_answer)

    # Define edges
    workflow.add_edge(START, "analyze_context")
    workflow.add_edge("analyze_context", "expand_question")
    workflow.add_edge("expand_question", "check_clarification")

    # Conditional: proceed or ask clarification
    workflow.add_conditional_edges(
        "check_clarification",
        should_proceed_or_clarify,
        {"classify": "classify", END: END}
    )

    # RAG flow
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "rerank")
    workflow.add_edge("rerank", "generate")
    workflow.add_edge("generate", "validate")

    # Conditional refinement
    workflow.add_conditional_edges(
        "validate",
        should_refine,
        {"refine": "refine", END: END}
    )
    workflow.add_edge("refine", "validate")

    # Compile WITH memory checkpointer
    memory = get_memory_saver()
    graph = workflow.compile(checkpointer=memory)
    return graph

# 6. EXECUTION WITH PERSISTENCE
# File: src/features/conversation/conversation_graph.py (Lines 146-196)
def run_conversational_query(question: str, user_id: str, config: dict) -> str:
    """Executes conversational query with memory context."""
    graph = create_conversational_rag_graph()

    # Initial state with HumanMessage for chat history
    initial_state = {
        "messages": [HumanMessage(content=question)],
        "question": question,
        "complexity": "",
        "documents": [],
        "generation": "",
        "quality_score": 0.0,
        "iterations": 0,
        "is_followup": False,
        "original_question": question,
    }

    # Invoke WITH config (thread_id for session persistence)
    final_state = graph.invoke(initial_state, config)

    return final_state["generation"]
```

**Fluxo de Comunicação (Layer 2):**

```
┌──────────── Layer 2: Orchestration ────────────┐
│                                                │
├─ Input from Layer 1 (question, user_id, config)
│                                                │
├─ Create StateGraph(ConversationalRAGState)    │
│  └─ Typed schema with 9 fields               │
│                                                │
├─ Register Nodes (add_node)                    │
│  ├─ Conversational: analyze, expand, clarify │
│  ├─ RAG: classify, retrieve, rerank          │
│  ├─ Generation: generate, validate, refine  │
│  └─ All imported from Layer 3                │
│                                                │
├─ Define Edges (add_edge)                      │
│  ├─ Simple edges: node → next_node           │
│  ├─ Conditional edges: state → routing func  │
│  ├─ Entry point: START → first node          │
│  └─ Exit points: END                          │
│                                                │
├─ Conditional Routing (add_conditional_edges) │
│  ├─ should_proceed_or_clarify()              │
│  │  └─ If needs_clarification → END          │
│  │  └─ Else → continue to RAG               │
│  └─ should_refine()                          │
│     └─ If quality >= 0.7 → END               │
│     └─ If iterations >= MAX → END             │
│     └─ Else → loop to refine                 │
│                                                │
├─ Compile Graph (compile)                      │
│  └─ Optional: with checkpointer=MemorySaver  │
│                                                │
├─ Execute Graph (invoke)                       │
│  ├─ Initialize state (empty → pre-filled)   │
│  ├─ Pass config with thread_id (if memory)   │
│  ├─ State flows through all nodes            │
│  ├─ Each node updates specific fields        │
│  └─ Final state returned                      │
│                                                │
└─ Output to Layer 1 (final_state[generation])─┘
```

**Exemplos Reais de Código:**

_Exemplo 1: StateGraph with Typed State_

```python
# File: src/core/domain/state.py (Line 20-45)
class RAGState(TypedDict):
    question: str
    complexity: Literal["simple", "complex"]  # Type-safe enum
    documents: list
    generation: str
    quality_score: Annotated[float, Field(ge=0.0, le=1.0)]  # Bounded
    iterations: Annotated[int, Field(ge=0)]  # Non-negative

# File: src/features/rag/graph_rag.py (Line 51-70)
workflow = StateGraph(RAGState)
workflow.add_node("classify", classify_question)
workflow.add_node("retrieve", retrieve_adaptive)
workflow.add_edge(START, "classify")
workflow.add_edge("classify", "retrieve")
```

_Exemplo 2: Conditional Routing_

```python
# File: src/features/rag/graph_rag.py (Line 27-45)
def should_refine(state: RAGState) -> str:
    quality_score = state.get("quality_score", 0.0)
    iterations = state.get("iterations", 0)
    if quality_score >= 0.7:
        return END
    if iterations >= MAX_ITERATIONS:
        return END
    return "refine"

workflow.add_conditional_edges(
    "validate",
    should_refine,
    {"refine": "refine", END: END}
)
```

_Exemplo 3: Graph Execution_

```python
# File: src/features/rag/graph_rag.py (Line 96-115)
def run_rag_query(question: str) -> str:
    graph = create_rag_graph()
    initial_state = {"question": question, ...}
    final_state = graph.invoke(initial_state)
    return final_state["generation"]
```

_Exemplo 4: Memory Integration_

```python
# File: src/features/conversation/conversation_graph.py (Line 133-140)
memory = get_memory_saver()
graph = workflow.compile(checkpointer=memory)

# File: src/features/conversation/conversation_graph.py (Line 196)
final_state = graph.invoke(initial_state, config)  # config has thread_id
```

**Constraints & Métricas (Layer 2):**

```yaml
Performance_Targets:
  Graph_Compilation: '< 50ms (once per workflow)'
  State_Initialization: '< 10ms per query'
  Node_Invocation: '< 10ms routing logic'
  Graph_Invocation: '< 100ms total overhead (excludes Layer 3)'

Layer_2_Boundaries:
  '✅ Includes': 'StateGraph, node registration, edge definition, routing logic, memory integration'
  '❌ Excludes': 'Individual node business logic, LLM calls, database operations'

Dependency_Direction:
  'UP': 'Receives from Layer 1 (initial state, config)'
  'DOWN': 'Delegates to Layer 3 (node functions)'
  'SIDE': 'Uses Layer 4 (MemorySaver, session config)'
  'NEVER': 'Direct knowledge of UI, business logic, data access'

Type_Safety:
  'TypedDict': 'Compile-time schema validation'
  'Literal': 'Enum-safe values (simple/complex)'
  'Annotated': 'Field constraints (0.0-1.0, ge=0)'
  'Mypy': 'All type hints checked'
```

#### **3. CAMADA LÓGICA (Business Logic / RAG Nodes)**

```yaml
Responsabilidade: |
  - Implementar a lógica de negócio do fluxo RAG (classificar → recuperar → rerank → gerar → validar → refinar)
  - Converter contratos de estado (TypedDict) em instruções para LLMs, vetores e rerankers
  - Orquestrar prompts, thresholds e ajustes de parâmetros específicos por tipo de pergunta
  - Aplicar validação de qualidade, loops de refinamento e estratégias de fallback quando a pontuação é baixa
  - Medir e registrar métricas operacionais (scores, tempo de execução, contadores de iteração)
  - Normalizar dados vindos da Camada 4 (FAISS, reranker, settings) antes de repassar à Camada 2

Conversa_com: |
  - UP: Layer 2 (StateGraph) recebe e devolve dicionários parciais de estado
  - DOWN: Layer 4 (FAISS, BGE CrossEncoder, configuration) via wrappers utilitários
  - SIDE: Core Domain (`src/core/domain/state.py`) para contratos tipados e validadores

Pattern_Applied: |
  - Strategy Pattern: cada node encapsula uma estratégia de processamento independente
  - Repository Pattern: acesso indireto ao FAISS via `FAISS.load_local` com abstração de dados
  - Singleton Pattern: `get_reranker()` carrega uma única instância compartilhada de CrossEncoder
  - Template Method Pattern: prompts padronizados com placeholders definidos em `ChatPromptTemplate`
  - Circuit Breaker / Fallback Pattern: rerankers e refinadores retornam pass-through quando indisponíveis

Regra_Rígida: |
  - Cada função é especialista em UMA tarefa apenas (manter SRP)
  - NÃO acessar UI ou orquestração diretamente (comunicação apenas via estado)
  - SEM manipular sessão persistente (delegar para Camada 4)
  - DEVE retornar apenas diffs de estado (dict parcial) compatíveis com TypedDict
  - DEVE registrar métricas/prints controladas para observabilidade
```

**Arquivos Implementadores:**

- `src/features/rag/nodes.py` — 6 nós especializados do pipeline RAG (Linhas 1-210)
- `src/features/reranking/reranker.py` — Singleton + estratégia de reranking (Linhas 1-210)
- `src/core/domain/state.py` — Contratos `RAGState` e validadores (Linhas 20-75)
- `tests/unit/test_reranker.py` — Cobertura unitária do reranker (Linhas 1-200)

```python
# ✅ PADRÃO CORRETO - Especialização + Strategy Pattern (exemplos reais)

# 1. Classificação da pergunta (strategy: classificação)
# File: src/features/rag/nodes.py (Linhas 26-64)
@traceable(run_type="chain", name="Classify Question Complexity")
def classify_question(state: RAGState) -> RAGState:
    question = state["question"]
    prompt = ChatPromptTemplate.from_template("Classifique a seguinte pergunta como 'simple' ou 'complex'.\n\n...")
    response = (prompt | llm).invoke({"question": question})
    complexity = response.content.strip().lower()
    if complexity not in ["simple", "complex"]:
        complexity = "complex"
    return {"complexity": complexity}

# 2. Recuperação adaptativa (strategy: retrieval)
# File: src/features/rag/nodes.py (Linhas 68-118)
@traceable(run_type="retriever", name="Adaptive Document Retrieval")
def retrieve_adaptive(state: RAGState) -> RAGState:
    question = state["question"]
    complexity = state["complexity"]
    k = 10 if complexity == "simple" else 15 if settings.reranker_enabled else (3 if complexity == "simple" else 7)
    vectordb = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    docs = vectordb.similarity_search(question, k=k)
    documents = [doc.page_content for doc in docs]
    return {"documents": documents}

# 3. Reranking BGE (strategy: reranker com fallback)
# File: src/features/rag/nodes.py (Linhas 120-185)
@traceable(run_type="chain", name="BGE Semantic Reranking")
def rerank_documents(state: RAGState) -> RAGState:
    if not settings.reranker_enabled or not state["documents"]:
        return {}
    reranker = get_reranker()
    if reranker is None:
        return {}
    doc_objects = [Document(page_content=doc) for doc in state["documents"]]
    top_n = 5 if state["complexity"] == "simple" else 7
    original_top_n = reranker.top_n
    reranker.top_n = top_n
    reranked_docs = reranker.compress_documents(doc_objects, state["question"])
    reranker.top_n = original_top_n
    return {"documents": [doc.page_content for doc in reranked_docs]}

# 4. Geração de respostas (strategy: generation)
# File: src/features/rag/nodes.py (Linhas 187-228)
@traceable(run_type="llm", name="Generate Answer")
def generate_answer(state: RAGState) -> RAGState:
    contexto = "\n\n".join([f"Documento {i+1}: {doc}" for i, doc in enumerate(state["documents"])])
    prompt = ChatPromptTemplate.from_template("Você é um assistente especializado em responder perguntas ...")
    generation = (prompt | llm).invoke({"contexto": contexto, "pergunta": state["question"]}).content
    return {"generation": generation}

# 5. Validação de qualidade (strategy: quality gate)
# File: src/features/rag/nodes.py (Linhas 230-272)
@traceable(run_type="chain", name="Validate Answer Quality")
def validate_quality(state: RAGState) -> RAGState:
    prompt = ChatPromptTemplate.from_template("Avalie a qualidade da resposta abaixo em uma escala de 0 a 1.\n\n...")
    response = (prompt | llm).invoke({
        "question": state["question"],
        "contexto": "\n".join(state["documents"][:3]),
        "generation": state["generation"],
    })
    try:
        quality_score = float(response.content.strip())
        quality_score = max(0.0, min(1.0, quality_score))
    except ValueError:
        quality_score = 0.6
    return {"quality_score": quality_score}

# 6. Refinamento iterativo (strategy: refinement loop)
# File: src/features/rag/nodes.py (Linhas 274-323)
@traceable(run_type="chain", name="Refine Answer with Feedback")
def refine_answer(state: RAGState) -> RAGState:
    prompt = ChatPromptTemplate.from_template("Você precisa MELHORAR a resposta anterior que recebeu score de qualidade {score:.2f}.\n\n...")
    refined = (prompt | llm).invoke({
        "score": state["quality_score"],
        "previous": state["generation"],
        "contexto": "\n\n".join([f"Documento {i+1}: {doc}" for i, doc in enumerate(state["documents"])]) ,
        "pergunta": state["question"],
    }).content
    return {"generation": refined, "iterations": state.get("iterations", 0) + 1}

# 7. Singleton do reranker (strategy provider)
# File: src/features/reranking/reranker.py (Linhas 32-120)
@traceable(run_type="tool", name="Load BGE Reranker Model")
def get_reranker() -> Optional[CrossEncoder]:
    global _reranker_instance
    if not settings.reranker_enabled:
        return None
    if _reranker_instance is None:
        _reranker_instance = CrossEncoder(settings.reranker_model, activation_fn=torch.nn.Sigmoid())
    return _reranker_instance

# 8. Threshold + top-N filtering (business rule)
# File: src/features/reranking/reranker.py (Linhas 122-220)
@traceable(run_type="chain", name="BGE Semantic Reranking with Threshold")
def rerank_documents(query: str, documents: List[str], top_n: Optional[int] = None) -> List[str]:
    reranker = get_reranker()
    if reranker is None or not documents:
        return documents
    effective_top_n = top_n if top_n is not None else settings.reranker_top_n
    scores = reranker.predict([(query, doc) for doc in documents])
    threshold = settings.reranker_score_threshold
    mask = scores >= threshold if threshold > 0 else np.ones_like(scores, dtype=bool)
    filtered_docs = [doc for doc, keep in zip(documents, mask) if keep]
    if not filtered_docs:
        best_idx = int(np.argmax(scores))
        return [documents[best_idx]]
    sorted_indices = np.argsort(scores[mask])[::-1][:effective_top_n]
    return [filtered_docs[i] for i in sorted_indices]
```

**Contrato de Estado & Especialização**

- `RAGState` e `ConversationalRAGState` (src/core/domain/state.py, Linhas 20-75) definem campos obrigatórios e limites (`Literal`, `Annotated`) consumidos por todos os nodes.
- Cada node recebe `state: RAGState` e retorna apenas as chaves que modifica, mantendo imutabilidade parcial e isolamento.
- A Camada 2 cuida da fusão (`state.update(node_result)`) garantindo que nenhuma função escreva em campos que não controla.

**Pipeline Camada 3 (Pseudocódigo)**

```python
def business_logic_pipeline(question: str) -> str:
    state = {"question": question, "documents": [], "iterations": 0}
    state |= classify_question(state)
    state |= retrieve_adaptive(state)
    state |= rerank_documents(state)
    state |= generate_answer(state)
    state |= validate_quality(state)
    while state["quality_score"] < 0.7 and state["iterations"] < MAX_ITERATIONS:
        state |= refine_answer(state)
        state |= validate_quality(state)
    return state["generation"]
```

**Fluxo Camada 3 (ASCII)**

```
[Layer 2] → classify_question → retrieve_adaptive → (optional) rerank_documents →
    generate_answer → validate_quality → [score >= 0.7?]
        ├─ Sim → retorna geração final para Layer 2
        └─ Não → refine_answer → validate_quality (loop até score ≥ 0.7 ou iterations ≥ 2)
           └─ Se atingir limite → devolve melhor geração disponível com flag de baixa qualidade
```

**Métricas & Limites (Business Logic)**

```yaml
Quality_Gates:
  Minimum_Quality_Score: '>= 0.70 (validado por validate_quality)'
  Max_Iterations: '2 (evita loops infinitos em refine_answer)'
  Retrieval_Docs:
    Simple: 'k=10 (rerank) ou 3 (sem rerank)'
    Complex: 'k=15 (rerank) ou 7 (sem rerank)'
  Reranker_Top_N:
    Simple: '5 documentos'
    Complex: '7 documentos'
  Threshold_Default: 'settings.reranker_score_threshold (0.0 → sem filtro)'
Performance_Targets:
  classify_question: '< 400ms (LLM curto)'
  retrieve_adaptive: '< 150ms (FAISS local)'
  rerank_documents: '< 250ms (top-15 → top-7)'
  generate_answer: '< 2.5s (LLM principal)'
  validate_quality: '< 1.5s (LLM judge)'
  refine_answer: '< 2.5s (LLM com feedback)'
Observability:
  Traceable_Decorators: '100% dos nodes possuem @traceable'
  Logging: 'Structured logs via structlog (reranker, thresholds, tempos)'
```

**Testes Essenciais (Cobertura atual)**

- `tests/unit/test_reranker.py` — valida singleton, top-N, threshold, fallback e conversões de documentos.
- `tests/unit/test_threshold_filtering.py` — garante estatísticas de corte e distribuição de scores.
- `tests/unit/test_threshold_performance.py` — mede tempo de reranking e garante cumprimento dos SLAs.
- `tests/unit/test_threshold_real_world_integration.py` — cenários reais com scores variados.
- `tests/unit/test_state_types.py` — confirma contrato de TypedDict para todos os campos usados pelos nodes.

**Checklist de Validação antes do Deploy**

1. ✅ Todos os nodes retornam apenas campos declarados em `RAGState`/`ConversationalRAGState`.
2. ✅ Threshold e top_n configurados via `settings` (sem valores mágicos no código).
3. ✅ Reranker carrega uma única vez (`get_reranker` + `reset_reranker` para testes).
4. ✅ Logs e traces ativos para cada node (`@traceable`).
5. ✅ Testes unitários mencionados executados e passando.
6. ✅ Métricas (tempo, score) monitoradas via LangSmith e logs estruturados.
7. ✅ Fallbacks funcionando (quando reranker desabilitado ou sem documentos).

**Limites e Fronteiras**

- Inclui: prompts, heurísticas, thresholds, manipulação de documentos, cálculos de score, loops de refinamento.
- Exclui: definição do grafo (Layer 2), gerenciamento de sessões (Layer 4), UI/IO (Layer 1).
- Qualquer novo algoritmo → implementar como novo node seguindo Strategy Pattern e adicionar testes dedicados.

#### **4. CAMADA ESPECIALIZADA**

```yaml
Responsabilidade: |
  - Fornecer serviços técnicos especializados (configuração, logging estruturado,
      vetores FAISS, LangSmith, memória de sessão, reranker BGE)
  - Encapsular integrações externas em contratos estáveis (adapters/facades)
  - Garantir validação, observabilidade, segurança e performance de recursos críticos
  - Disponibilizar utilitários resilientes para consumo da Camada 3 sem vazar detalhes

Conversa_com: |
  - UP: Nenhuma (não conhece quem consome)
  - DOWN: Serviços externos (LangSmith, FAISS, Torch, ambientes, FS)
  - SIDE: Bibliotecas utilitárias (structlog, pydantic, langgraph)
  - EXPÕE: Funções/helpers síncro-nos para Camada 3 consumir via importação

Pattern_Applied: |
  - Adapter Pattern: `monitoring.get_langsmith_client`, `memory_manager.ConversationManager`
  - Facade Pattern: `logging.configure_logging` + `get_logger`
  - Provider/Singleton Pattern: `reranking.get_reranker`
  - Configuration as Code: `Settings(BaseSettings)`

Regra_Rígida: |
  - NÃO conhecem quem os usa - apenas fornecem serviços (contratos estáveis)
  - NÃO devem importar camadas superiores (Presentation, Orchestration, Business)
  - DEVEM validar entradas e falhas externas antes de retornar
  - DEVEM ser observáveis (logs, métricas) e resilientes (fallbacks)
```

**Propósito da camada:** Consolidar toda dependência especializada (APIs externas, recursos
de infraestrutura, validação de ambiente) em módulos dedicados que podem ser
reutilizados por qualquer fluxo da aplicação sem acoplar a lógica de negócio. A camada
atua como fronteira com o mundo externo, garantindo contratos estáveis, validação
fail-fast e observabilidade consistente.

**Arquivos Implementadores:**

- `src/infrastructure/config/settings.py` — `Settings(BaseSettings)` com validação
  estrita (linhas 1-95)
- `src/infrastructure/logging/logger.py` — Configuração `structlog` + `get_logger`
  (linhas 1-180)
- `src/core/services/memory_manager.py` — `ConversationManager` (MemorySaver) e
  helpers (linhas 1-140)
- `src/core/services/monitoring.py` — Adapter LangSmith + tratamento de erros
  estruturados (linhas 1-200)
- `src/features/reranking/reranker.py` — Provider do CrossEncoder BGE e filtros
  semânticos (linhas 1-220)
- `src/features/rag/nodes.py` — Uso indireto de FAISS via `FAISS.load_local(...)`
  (linhas 70-110) consumindo serviços expostos por esta camada

```python
# ✅ CONFIGURAÇÃO CENTRALIZADA (Settings + validação fail-fast)
# File: src/infrastructure/config/settings.py (Linhas 18-95)
class Settings(BaseSettings):
        langsmith_api_key: str = Field(..., description="LangSmith API Key")
        google_api_key: str = Field(..., description="Google Gemini API Key")
        llm_model: str = Field(default="gemini-2.0-flash-exp")
        reranker_enabled: bool = Field(default=True)
        reranker_model: str = Field(default="BAAI/bge-reranker-base")
        log_level: str = Field(default="INFO")
        log_format: str = Field(default="auto")

settings = Settings()  # Instância única validada no import

# ✅ FACADE PARA LOGGING ESTRUTURADO (structlog + auto formatação)
# File: src/infrastructure/logging/logger.py (Linhas 35-160)
def configure_logging() -> None:
        shared_processors = [
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.format_exc_info,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.CallsiteParameterAdder({...}),
        ]
        if settings.log_format.lower() == "json":
                processors = shared_processors + [json_renderer]
        elif settings.log_format.lower() == "console":
                processors = shared_processors + [structlog.dev.ConsoleRenderer(colors=True)]
        else:
                processors = shared_processors + ([structlog.dev.ConsoleRenderer(colors=True)]
                                                                                    if sys.stderr.isatty() else [json_renderer])
        log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
        structlog.configure(
            cache_logger_on_first_use=True,
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            processors=processors,
            logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        )

# ✅ ADAPTER DE MEMÓRIA (MemorySaver + sessões isoladas)
# File: src/core/services/memory_manager.py (Linhas 10-110)
class ConversationManager:
        def __init__(self):
                self.memory = MemorySaver()
                self.active_sessions: Dict[str, str] = {}

        def get_config(self, user_id: str = "default") -> dict:
                thread_id = self.get_or_create_session(user_id)
                return {"configurable": {"thread_id": thread_id}}

conversation_manager = ConversationManager()

# ✅ PROVIDER DO RERANKER (lazy load + fallback)
# File: src/features/reranking/reranker.py (Linhas 32-145)
@traceable(run_type="tool", name="Load BGE Reranker Model")
def get_reranker() -> Optional[CrossEncoder]:
        global _reranker_instance
        if not settings.reranker_enabled:
                return None
        if _reranker_instance is None:
                _reranker_instance = CrossEncoder(
                        settings.reranker_model,
                        activation_fn=torch.nn.Sigmoid(),
                )
        return _reranker_instance

# ✅ ADAPTER LANGSMITH (observabilidade externa)
# File: src/core/services/monitoring.py (Linhas 25-120)
def list_recent_runs(limit: int = 10) -> List:
        try:
                client = get_langsmith_client()
                runs = list(client.list_runs(project_name=settings.langsmith_project, limit=limit))
                return runs
        except Exception as e:
                logger.error(
                        "error_listing_runs",
                        project_name=settings.langsmith_project,
                        error_type=type(e).__name__,
                        error_message=str(e),
                        exc_info=True,
                )
                return []
```

**Fluxo Camada 4 (Consumo pela Camada 3):**

```
┌────────────── Layer 3 (Nodes/RAG) ───────────────┐
│                                                  │
│  retrieve_adaptive → FAISS.load_local() ─┐       │
│  rerank_documents → get_reranker() ─────┤       │
│  validate_quality → settings.* configs ─┤       │
│  analyze_context → get_logger() ────────┤       │
│  run_graph(...) → get_memory_saver() ───┘       │
│                                                  │
└────────────── Layer 4 (Infra Services) ──────────┘
                     │            │             │             │
                     │            │             │             │
         FAISS Index   BGE CrossEncoder   LangSmith API  Pydantic Settings
                     │            │             │             │
                (Disco)      (Torch)        (HTTP)       (.env → validação)
```

**Métricas & Limites (Camada 4):**

```yaml
Performance_Targets:
  Settings_Load: '< 15ms (validação BaseSettings)'
  Logging_Configuration: '< 30ms (structlog configure)'
  Reranker_First_Load: '< 3.5s (download/carregar modelo BGE)'
  Reranker_Subsequent: '< 5ms (instância cacheada)'
  Memory_Config_Fetch: '< 2ms (dict simples com thread_id)'
  LangSmith_ListRuns: '< 1.2s (timeout configurado pelo client)'

Resiliência_Falhas:
  Reranker_Disabled: 'Retorna pass-through sem quebrar pipeline'
  LangSmith_Error: 'Log estruturado + [] (fallback seguro)'
  Settings_Invalid: 'Falha no import (fail-fast) -> impedir boot inseguro'
  FAISS_Load: 'Requer allow_dangerous_deserialization=True → validar índice confiável'

Segurança:
  Secrets: 'Nunca logar API keys; usar Pydantic para validação'
  IO: 'Carregar índices FAISS apenas de diretórios versionados (./banco_faiss/)'
  Observabilidade: 'Logs JSON incluem correlation ids via contextvars'
```

**Testes Essenciais & Cobertura:**

- `tests/unit/test_settings.py` — valida defaults, obrigatoriedade de API keys e
  serialização
- `tests/unit/test_logging.py` — garante formatos JSON/console e performance
- `tests/unit/test_session_config.py` — assegura `thread_id` único por usuário
- `tests/unit/test_reranker.py` + `tests/unit/test_threshold_*` — validam singleton,
  thresholds e fallback do reranker
- `tests/unit/test_state_types.py` — garante compatibilidade dos contratos com o
  consumo da Camada 3

**Checklist de Validação Camada 4:**

1. ✅ `settings` carregado sem exceções (env válido) antes de iniciar aplicação
2. ✅ `configure_logging()` executado uma vez e `get_logger` usado em todos adapters
3. ✅ `ConversationManager` expõe apenas dicts (`thread_id`) para LangGraph
4. ✅ `get_reranker()` suporta primeira carga lenta, demais instantâneas
5. ✅ `FAISS.load_local` documentado com requisito de índices confiáveis
6. ✅ Falhas externas (LangSmith, FAISS, Torch) são logadas e retornam fallback seguro

> 🔐 **Nota:** Caso novos serviços especializados sejam adicionados (cache Redis,
> webhooks, filas), manter o mesmo contrato: módulo isolado, sem imports para camadas
> superiores e com testes unitários dedicados que comprovem resiliência.

### 📊 Inventário estruturado (Atende T-20)

**Controllers / Handlers (5+):**

- `scripts/chat.py::run_interactive_conversation` — loop CLI principal com dispatch de comandos (/reset, /help, /quit).
- `scripts/chat.py::print_header` — controller de apresentação, inicializa instruções e branding.
- `scripts/chat.py::print_help` — endpoint de ajuda exposto via `/help`.
- `src/features/conversation/conversation_graph.py::run_conversational_query` — façade orquestradora chamada pela CLI (entrada/saída de Layer 1).
- `src/features/conversation/conversation.py::{analyze_context, expand_question, check_clarification}` — tratadores de entrada responsáveis por preparar o estado antes da Layer 2.

**Services / Business Logic (5+):**

- `src/features/rag/nodes.py::classify_question`
- `src/features/rag/nodes.py::retrieve_adaptive`
- `src/features/rag/nodes.py::rerank_documents`
- `src/features/rag/nodes.py::generate_answer`
- `src/features/rag/nodes.py::validate_quality`
- `src/features/rag/nodes.py::refine_answer`

**Repositories / Data Access (5+):**

- `src/core/services/memory_manager.py::ConversationManager.get_or_create_session` — provê `thread_id` persistente via MemorySaver.
- `src/core/services/memory_manager.py::get_memory_saver` — expõe storage LangGraph para camadas superiores.
- `src/features/reranking/reranker.py::get_reranker` — gerencia lifecycle do CrossEncoder (carregamento e caching).
- `src/features/reranking/reranker.py::rerank_documents` — aplica threshold/ordenação e devolve subconjuntos (dados prontos para consumo).
- `src/core/services/monitoring.py::list_recent_runs` — consulta LangSmith e retorna coleções de runs/tags para diagnóstico.

**Domain Entities / Contracts (3+):**

- `src/core/domain/session.py::SessionConfig` — entidade imutável que descreve parâmetros de sessão.
- `src/core/domain/state.py::RAGState`
- `src/core/domain/state.py::ConversationalRAGState`
- `src/infrastructure/config/settings.py::Settings` — agregado de configuração com validação automática.

---

### ✅ **LINGUAGEM UNIVERSAL: **

#### **PADRÃO DE COMUNICAÇÃO**

```yaml
Regra_Absoluta: 'Cada camada só conversa com a imediatamente inferior por meio de contratos estáveis; Layer 4 nunca chama Layers 1-3.'
Benefício: |
  - Evita dependências circulares e facilita auditorias de segurança
  - Permite substituir infraestrutura (FAISS, LangSmith) sem alterar camadas superiores
  - Simplifica testes ao permitir mocks por camada
  - Mantém mensagens de observabilidade consistentes em todo o stack
```

```python
from langchain_community.vectorstores import FAISS
from langsmith import traceable

from src.core.domain.state import RAGState
from src.core.services.memory_manager import get_conversation_config  # Layer 4
from src.features.conversation.conversation_graph import create_conversational_rag_graph  # Layer 2
from src.features.rag.nodes import embeddings, db_path, retrieve_adaptive  # Layer 3


def cli_loop(user_id: str = "cli_user") -> None:
  config = get_conversation_config(user_id)          # Layer 1 → Layer 4 (session)
  graph = create_conversational_rag_graph()          # Layer 1 → Layer 2 (orquestração)
  state = {
      "messages": [],
      "question": "Olá",
      "complexity": "simple",
      "documents": [],
      "generation": "",
      "quality_score": 0.0,
      "iterations": 0,
  }
  final_state = graph.invoke(state, config)          # Layer 2 chama apenas nodes da Layer 3
  print(final_state["generation"])                  # Layer 1 apresenta resposta


@traceable(run_type="retriever", name="Adaptive Document Retrieval")
def retrieve_adaptive(state: RAGState) -> RAGState:
  vectordb = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)  # Layer 3 → Layer 4
  docs = vectordb.similarity_search(state["question"], k=10)
  return {"documents": [doc.page_content for doc in docs]}


# Qualquer tentativa de Layer 4 acessar Layer 1 dispara alerta de lint/pipeline.
```

#### **THREAD-SAFETY E VALIDAÇÃO EMPRESARIAL**

```python
from threading import Lock
from typing import Any, Optional
from uuid import uuid4

from structlog import get_logger

from src.core.domain.session import SessionConfig
from src.features.reranking.reranker import get_reranker


logger = get_logger(__name__)


class ThreadSafeRerankerPool:
  """Garante instância única do CrossEncoder mesmo em cenários multi-thread."""

  _instance: Optional[Any] = None
  _lock = Lock()

  @classmethod
  def acquire(cls) -> Optional[Any]:
    with cls._lock:  # 🔒 evita corrida durante o download do modelo
      if cls._instance is None:
        cls._instance = get_reranker()
      return cls._instance


def build_session_config(max_turns: int = 10, memory_window: int = 6) -> SessionConfig:
  """Validação empresarial usando Pydantic antes de expor configuração a outras camadas."""

  try:
    config = SessionConfig(thread_id=uuid4(), max_turns=max_turns, memory_window=memory_window)
    logger.info("session_config_ready", thread_id=str(config.thread_id), max_turns=config.max_turns)
    return config
  except ValueError as exc:
    logger.error("session_config_invalid", error=str(exc), max_turns=max_turns, memory_window=memory_window)
    raise


# Uso combinado: Layer 4 monta dependências thread-safe e validadas antes de entregá-las às camadas superiores.
```

---

### ✅ **PADRÕES ENTERPRISE IMPLEMENTADOS**

#### **1. STRATEGY PATTERN (Obrigatório para Algoritmos)**

- **Objetivo:** Desacoplar heurísticas de RAG para permitir troca dinâmica sem alterar a orquestração.
- **Uso real:** `src/features/rag/nodes.py` (cada node é uma estratégia independente) e `src/features/reranking/reranker.py` (CrossEncoder BGE plugável).

```python
# 🚫 ERRADO - if/else diretamente no node (dificulta novos algoritmos)
def rerank_documents(state: RAGState) -> RAGState:
  provider = settings.reranker_provider  # valor imaginário
  if provider == "bge":
    return _rerank_with_bge(state)
  if provider == "bm25":
    return _rerank_with_bm25(state)
  return {}


# ✅ CORRETO - estratégias intercambiáveis com contrato explícito
from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document

from config.settings import settings
from src.core.domain.state import RAGState
from src.features.reranking.reranker import get_reranker


class RerankingStrategy(ABC):
  @abstractmethod
  def rerank(self, question: str, documents: List[str]) -> List[str]: ...


class BgeCrossEncoderStrategy(RerankingStrategy):
  def __init__(self) -> None:
    self._model = get_reranker()  # src/features/reranking/reranker.py

  def rerank(self, question: str, documents: List[str]) -> List[str]:
    if self._model is None:
      return documents
    doc_objects = [Document(page_content=d) for d in documents]
    return [doc.page_content for doc in self._model.compress_documents(doc_objects, question)]


class PassThroughStrategy(RerankingStrategy):
  def rerank(self, question: str, documents: List[str]) -> List[str]:
    return documents


class RerankingEngine:
  def __init__(self, strategy: RerankingStrategy) -> None:
    self._strategy = strategy

  def execute(self, question: str, documents: List[str]) -> List[str]:
    return self._strategy.rerank(question, documents)


def build_reranking_engine() -> RerankingEngine:
  strategy: RerankingStrategy = BgeCrossEncoderStrategy() if settings.reranker_enabled else PassThroughStrategy()
  return RerankingEngine(strategy)


def rerank_documents(state: RAGState) -> RAGState:
  engine = build_reranking_engine()
  reranked = engine.execute(state["question"], state["documents"])
  return {"documents": reranked}
```

- **Benefícios comprovados:**
  - Testes independentes por estratégia (`tests/unit/test_reranker.py`).
  - Toggle em runtime via `settings.reranker_enabled` sem alterar `graph_rag.py`.
  - Facilita adicionar novos rerankers híbridos sem quebrar camadas superiores.

#### **2. DEPENDENCY INJECTION (Obrigatório para Gerentes)**

- **Objetivo:** Inverter o controle para que serviços de camada superior operem sobre contratos, mantendo infraestrutura plugável.
- **Uso real:**
  - `create_conversational_rag_graph()` recebe `MemorySaver` via `checkpointer=memory` (injeção pela Camada 4).
  - `scripts/chat.py` injeta `config` obtida de `get_conversation_config()` antes de chamar Layer 2.

```python
# 🚫 ERRADO - Serviço cria dependências internas (dificulta testes e troca de providers)
class RagController:
  def answer(self, question: str) -> str:
    vectordb = FAISS.load_local(db_path, embeddings)
    reranker = get_reranker()
    docs = vectordb.similarity_search(question)
    return generate_answer({"question": question, "documents": [d.page_content for d in docs]})["generation"]


# ✅ CORRETO - Dependências entram pelo construtor (injeção explícita + fácil de mockar)
from dataclasses import dataclass
from typing import Protocol

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from src.features.rag.nodes import db_path, embeddings, generate_answer, retrieve_adaptive
from src.features.reranking.reranker import get_reranker


class RetrievalStrategy(Protocol):
  def __call__(self, question: str) -> list[str]: ...


class RerankingStrategy(Protocol):
  def __call__(self, question: str, documents: list[str]) -> list[str]: ...


class GenerationStrategy(Protocol):
  def __call__(self, question: str, documents: list[str]) -> str: ...


@dataclass(slots=True)
class RagService:
  retrieve: RetrievalStrategy
  rerank: RerankingStrategy
  generate: GenerationStrategy

  def run(self, question: str) -> str:
    documents = self.retrieve(question)
    reranked = self.rerank(question, documents)
    return self.generate(question, reranked)


# Layer 4 efetua o wiring com adapters existentes
def _retrieve_documents(question: str) -> list[str]:
  state = {"question": question, "complexity": "simple", "documents": []}
  return retrieve_adaptive(state)["documents"]


def _rerank_with_bge(question: str, documents: list[str]) -> list[str]:
  model = get_reranker()
  if model is None:
    return documents
  doc_objects = [Document(page_content=d) for d in documents]
  return [doc.page_content for doc in model.compress_documents(doc_objects, question)]


def _generate_answer(question: str, documents: list[str]) -> str:
  return generate_answer({"question": question, "documents": documents})["generation"]


rag_service = RagService(
  retrieve=_retrieve_documents,
  rerank=_rerank_with_bge,
  generate=_generate_answer,
)


def handle_question(question: str, *, service: RagService = rag_service) -> str:
  """Camada 1 consome serviço pré-configurado; testes podem injetar mock."""
  return service.run(question)
```

- **Benefícios comprovados:**
  - Permite substituir implementações em testes/unit (mocks de retriever e reranker).
  - Evita instanciar recursos pesados repetidamente (CrossEncoder, FAISS).
  - Torna explícito quais dependências cada serviço precisa, reduzindo acoplamento oculto.

#### **3. EXCEPTION HIERARCHY (Obrigatório para Erros)**

- **Objetivo:** Unificar tratamento de erros, garantindo logs estruturados e propagação coerente entre as camadas.
- **Hierarquia Recomendada:**
  - `BaseProjectError(Exception)` → raiz para todo erro do projeto (localizada em `src/shared/exceptions.py`).
  - `InfrastructureError(BaseProjectError)` → falhas Layer 4 (FAISS, LangSmith, MemorySaver, rede).
  - `BusinessRuleViolation(BaseProjectError)` → inconsistências Layer 3 (ex.: score inválido, ausência de documentos).
  - `OrchestrationError(BaseProjectError)` → erros de ligação na Layer 2 (state graph, config faltante).
  - `PresentationError(BaseProjectError)` → I/O inválido na Layer 1 (comandos CLI, payload HTTP).
  - _Nota:_ centralizar a hierarquia em `src/shared/exceptions.py` (criar o módulo caso não exista) para evitar duplicação entre camadas.

```python
# 🚫 ERRADO - Captura genérica e silêncio (perde contexto e dificulta observabilidade)
def list_recent_runs(limit: int = 10) -> list:
  try:
    client = get_langsmith_client()
    return list(client.list_runs(project_name=settings.langsmith_project, limit=limit))
  except Exception:
    return []  # Swallow: quem chama não sabe o que ocorreu


# ✅ CORRETO - Hierarquia explícita + log estruturado + rethrow contextualizado
import structlog

from config.settings import settings
from src.core.services.memory_manager import get_conversation_config
from src.core.services.monitoring import get_langsmith_client
from src.features.conversation.conversation_graph import create_conversational_rag_graph
from src.shared.exceptions import BaseProjectError, InfrastructureError, OrchestrationError, PresentationError

logger = structlog.get_logger(__name__)


def list_recent_runs(limit: int = 10) -> list:
  try:
    client = get_langsmith_client()
    return list(client.list_runs(project_name=settings.langsmith_project, limit=limit))
  except BaseProjectError:  # Já tratado em camada inferior (não duplicar log)
    raise
  except Exception as exc:  # Erro inesperado → empacotar como InfrastructureError
    logger.error(
      "langsmith_runs_error",
      error_type=type(exc).__name__,
      error_message=str(exc),
      limit=limit,
      exc_info=True,
    )
    raise InfrastructureError("Failed to list LangSmith runs") from exc


# Layer 2 decide se converte para OrchestrationError ou propaga para Layer 1
def run_conversational_query(question: str, user_id: str, config: dict) -> str:
  try:
    graph = create_conversational_rag_graph()
    state = {
      "messages": [],
      "question": question,
      "complexity": "simple",
      "documents": [],
      "generation": "",
      "quality_score": 0.0,
      "iterations": 0,
    }
    final_state = graph.invoke(state, config)
    return final_state["generation"]
  except InfrastructureError as exc:  # já logado em Layer 4
    raise OrchestrationError("External dependency unavailable") from exc
  except Exception as exc:
    logger.error("graph_invoke_error", user_id=user_id, exc_info=True)
    raise OrchestrationError("Failure during graph execution") from exc


# Layer 1 converte para resposta amigável mantendo rastreabilidade
def handle_cli(question: str, user_id: str = "cli_user") -> None:
  try:
    answer = run_conversational_query(question, user_id, get_conversation_config(user_id))
    print(answer)
  except OrchestrationError as exc:
    print("⚠️  Não foi possível concluir a conversa agora. Consulte os logs." )
    raise PresentationError("Conversation aborted") from exc
```

- **Diretrizes:**
  - Logs devem usar `exc_info=True` e campos estruturados (`error_type`, `error_message`, `dependency`).
  - Somente a camada que adiciona contexto loga; camadas superiores reempacotam sem duplicar logs.
  - `BaseProjectError` (e derivados) SEMPRE devem ser propagados intactos para preservar o encadeamento.
  - Exceções de validação (`ValueError`, `ValidationError`) devem ser convertidas em `BusinessRuleViolation` antes de retornar à Layer 2.

---

### 🔒 **REGRAS ARQUITETURAIS IMUTÁVEIS**

#### **REGRA 1: HIERARQUIA SEM BYPASS**

```yaml
OBRIGATÓRIO:
PROIBIDO:
PROIBIDO:
```

#### **REGRA 2:**

```yaml
OBRIGATÓRIO: ""
PROIBIDO: ""
OBRIGATÓRIO: ""
```

#### **REGRA 3: SINGLE RESPONSIBILITY**

```yaml

```

#### **REGRA 4: DEPENDENCY DIRECTION**

```yaml
PERMITIDO: "Camada superior → Camada inferior"
PROIBIDO: "Camada inferior → Camada superior"
PROIBIDO: "Dependências circulares entre camadas"
```

---

### 🧪 **VALIDAÇÃO ARQUITETURAL OBRIGATÓRIA**

#### **TESTES DE COMPLIANCE**

```python

```

---

### 📊 **MÉTRICAS DE COMPLIANCE OBRIGATÓRIAS**

#### **QUALITY GATES ENTERPRISE**

```yaml
Complexity_Cognitive: '< 15 (SonarQube compliant)'
Exception_Handling: 'Específico - sem Exception genérico'
Code_Duplication: 'Zero duplicação via Constants Factory'
Architecture_Layers: 'Máximo 4 camadas na hierarquia'
GraphState_Usage: '100% nas funções principais'
Strategy_Pattern: 'Obrigatório para algoritmos plugáveis'
Thread_Safety: 'Obrigatório para estado compartilhado'
```

---

## 🎖️ COMPLIANCE ENFORCEMENT

```yaml
Rule Compliance:
  - 🔒 revision_mandatory_for_changes: true
  - 🔒 documentation_always_updated: true
  - 🔒 compliance_verified_automatically: true
  - 🔒 apply_manually: >
      this rule needs to be mentioned to be included
```

---

## 🔗 CROSS-REFERENCE TABLE

> **Quick Navigation:** Jump between implementations (this doc) and architectural concepts ([project-rules.md](project-rules.md))

| Implementation                    | This Doc (Lines)          | project-rules.md (Lines)   | Files                                                                 |
| --------------------------------- | ------------------------- | -------------------------- | --------------------------------------------------------------------- |
| **Clean Architecture (4 Layers)** | 91-1087                   | 79-95                      | Multiple (see below)                                                  |
| Layer 1: Presentation             | 91-303                    | 79-95                      | `scripts/chat.py`, `src/features/conversation/conversation.py`        |
| Layer 2: Orchestration            | 304-655                   | 79-95                      | `src/features/conversation/graph.py`, `src/features/rag/graph.py`     |
| Layer 3: Business Logic           | 656-887                   | 79-95                      | `src/features/rag/nodes.py`, `src/features/reranking/reranker.py`     |
| Layer 4: Services                 | 888-1087                  | 79-95                      | `src/infrastructure/config/settings.py`, `src/core/services/`         |
| **RAGState (TypedDict)**          | 91-303, 304-655, 656-887  | 124-171 (Abstraction)      | `src/core/domain/state.py`                                            |
| **SessionConfig (Pydantic)**      | 1294-1380 (DI pattern)    | 172-218, 444-594           | `src/core/domain/session.py`                                          |
| **LangGraph Integration**         | 304-655 (Layer 2)         | 79-95, 255-311             | `src/features/conversation/graph.py`, `src/features/rag/graph.py`     |
| **Strategy Pattern**              | 1222-1293                 | 255-311 (Polymorphism)     | `src/features/rag/nodes.py` (retrieve_adaptive, rerank_documents)     |
| **Dependency Injection**          | 1294-1380                 | 444-594 (Composition)      | `src/core/domain/session.py` (SessionConfig composition)              |
| **Exception Hierarchy**           | 1381-1470                 | Implicit in error handling | Custom exceptions, retry logic                                        |
| **Communication Patterns**        | 1124-1219                 | Implicit                   | Thread-safety, validation enterprise                                  |
| **Architectural Rules**           | 1471-1504                 | 595-773 (Compliance)       | Hierarchy enforcement, no bypass, single responsibility               |
| **Validation & Metrics**          | 1505-1530                 | 595-773 (Compliance)       | Compliance tests, import-linter, coverage metrics                     |
| **SOLID Principles**              | Applied throughout        | 96-119                     | All implementation files                                              |
| **Abstraction (TypedDict)**       | 91-303 (RAGState)         | 124-171                    | `src/core/domain/state.py`                                            |
| **Encapsulation (Pydantic)**      | 1294-1380 (SessionConfig) | 172-218                    | `src/core/domain/session.py`, `src/infrastructure/config/settings.py` |
| **Inheritance (BaseSettings)**    | 1294-1380 (DI)            | 219-254                    | `src/core/domain/session.py`, `src/infrastructure/config/settings.py` |
| **Polymorphism (Strategy)**       | 1222-1293                 | 255-311                    | `src/features/rag/nodes.py`                                           |
| **Composition**                   | 1294-1380 (SessionConfig) | 444-594                    | `src/core/domain/session.py`                                          |

## 📚 RELATED DOCUMENTS

| Document                                     | Relevant Sections                                               | Description                                          |
| -------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------- |
| [project-rules.md](project-rules.md)         | Lines 79-119 (Architecture+SOLID), Lines 124-594 (OOP Patterns) | Architectural concepts, SOLID principles, OOP theory |
| [behavioral-rules.md](behavioral-rules.md)   | Lines 45-78 (ROI Framework), Lines 135-175 (Token Efficiency)   | Execution protocols, efficiency standards            |
| [methodology-rules.md](methodology-rules.md) | Lines 25-60 (TDD), Lines 85-120 (XP+Kanban+OOP)                 | Development workflow, quality metrics                |
| [tools-rules.md](tools-rules.md)             | Lines 30-80 (CLI tools), Lines 120-180 (Terminal)               | Tool usage, performance optimization                 |
| [mcp-rules.md](mcp-rules.md)                 | Lines 16-34 (Pattern 1), Lines 36-51 (Pattern 2)                | MCP integration patterns, workflow                   |

---

**📅 Created:** 06/08/2025
**🔄 Last Update:** 17/10/2025
**📋 Status:** ACTIVE AND MANDATORY
**🎯 Application:** AWAYS WHEN THE USER MENTIONS OR WHEN THE AGENT NEEDS CONTEXT OR RELEVANT INFORMATION ABOUT THE PROJECT

- **🔍 Linked:** [.github\copilot-rules\project-rules.md](project-rules.md)

---

_Este padrão arquitetural é **IMUTÁVEL** e deve ser seguido em toda expansão futura do projeto._
