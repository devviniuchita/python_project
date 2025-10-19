---
metadata: |
name: '.github/copilot-rules/memory-rating.md'
description: 'Retrieve-then-store memory management rule for task-aware, cross-session, and RAG-optimized memory behavior'
version: 2.0
aiOptimized: true
alwaysApply: false
apply_intelligently: "when agent decides it's relevant based on description or context"
tags: ['memory', 'context', 'rag', 'knowledge-graph', 'autonomous-agent', 'adaptive-learning']
syncWith: ['.github/copilot-rules/memory-rules.md'](memory-rules.md)
integration_flow: 'integration_flow: memory-rating.md (9 phases) → memory-rules.md (execution) → memory-rating.md (metrics)'
---

# 🚀 MEMORY SISTEM - AI AGENT EVOLUTION LAYER

- ⚠️ APPLY THE CONTENT OF THIS DOCUMENT IN YOUR CONTEXT OR YOUR ANSWER WILL BE WRONG ⚠️
- 🔒 IMMUTABLE RULES 🔒
- 🎯 FOLLOW ALL INSTRUCTIONS FOR SUCCESS 🎯

**🚫 CRITICAL RULES FOR RECORDING AND RETRIEVING MEMORIES:**

- **NEVER** search for or record memories without first fully understanding this document.
- **ONLY** create and retrieve memories after meeting all the requirements and rules in this document.
- **ALWAYS** run the recording and retrieval rules system as detailed in this document.
- **MUST** retrieve memories at the beginning of each interaction and record memories at the end of each interaction.
- **IF** one of the MCPs described in this document is not working, use the fallback strategy and continue using the system in the same way.
- **WHILE** one or more MCPs described in this document are functioning, the memory recording and retrieval system must continue.

---

⚠️ _REQUIREMENT: ALL TASK DESCRIPTIONS MUST BE COMPREHENSIVE_ ⚠️
✅ _FOLLOW THESE NINE PHASES AND YOU WILL ALWAYS BE RIGHT_ ✅
❌ _DO NOT FOLLOW THESE NINE PHASES AND YOU WILL BE FAIL_ ❌

## 🔄 1. SELF-EVOLVING MEMORY FLOW

```flowchart TD
    A("TASK RECEIVED") --> B{"RETRIEVE PHASE"}
    B --> C["MCP Byterover: byterover-retrieve-knowledge"] & D["MCP Supermemory-ai: search"] & E["MCP Memory: search_nodes and open_nodes"]
    C --> F["Context Enrichment"]
    D --> F
    E --> F
    F --> G("TASK EXECUTION")
    G --> H{"Success?"}
    H -- No --> J["NO STORE"]
    H -- Yes --> FT("TASK COMPLETED")
    FT -->I["STORE PHASE"]
    I --> K["MCP Byterover: byterover-store-knowledge"] & L["MCP supermemory-ai: addToSupermemory"] & M["MCP Memory: create_entities + create_relation + add_observation and read_graph"]
    K --> N["Knowledge Graph Update: Adaptive Vector Indexing + Decay Model + Unified Recall Service"]
    L --> N
    M --> N
    N --> O["Future RAG Optimization"]

    O -->NT("NEW TASK?")
    NT -- Yes --> R{RAG}
    R --> B
```

_<!important>_
always use byterover-retrieve-knowledge, search for supermemory-ai, search\*nodes and open\*nodes for mcp memory, tool to get the related context before any tasks.
always use byterover-store-knowledge, addToSupermemory in supermemory-ai, create*entities, create_relation, add_observation and read_graph in the mcp memory ,tool to store all the critical informations after sucessful tasks\*
*</!important>\_

---

## ⚙️ 2. MEMORY CONTEXT CONFIG AND USES

```yaml
objectives:
  - id: cross_session_persistence
    description: 'Memory retained across sessions'
  - id: semantic_knowledge_graph
    description: 'Concept relationship enrichment'
  - id: optimized_rag
    description: 'Context-aware response generation'
  - id: accelerated_learning
    description: 'Pattern storage for adaptive behavior'

integration_points:
  pre_task:
    action: 'Retrieve prior context and memory state before task execution'
    sources: [byterover, supermemory-ai, memory]
    technique: triple_context_retrieval
    fallback_strategy: return_empty_if_failure
  post_task:
    action: 'Store task outputs and learned context after execution'
    targets: [byterover, supermemory-ai, memory]
    technique: triple_learning_storage
    error_handling: retry_then_log
  context_enrichment:
    action: 'Enrich current context using semantic links'
    technique: knowledge_graph_relationships
    fallback_strategy: skip_if_missing
  rag_optimization:
    action: 'Optimize RAG with stored memory'
    technique: memory_storage_enhanced_rag
```

---

## 📚 3. SYSTEM LEARNING

### **Memory Vectorization 2025**

```yaml
vectorization:
  embedding_model: 'text-embedding-3-large'
  context_window_limit: 8000
  compression: 'semantic-clustering-2025'
  optimization: 'adaptive-compression'

  performance_metrics:
    embedding_speed: '<50ms'
    compression_ratio: '>80%'
    semantic_preservation: '>95%'
```

### **Retention Policy Inteligente**

```yaml
memory_management:
  decay_policy:
    enabled: true
    strategy: 'least_recently_used'
    threshold_days: 30
  scoring:
    enabled: true
    metrics: [relevance, confidence, novelty]

retention_policy:
  thresholds:
    persistent_if:
      relevance_score: '>0.9'
      recurrence: '>3 times'
      context_depth: '>0.8'
    decay_if:
      time_since_last_use: '>3d'
      relevance_score: '<0.4'
      usage_frequency: '<0.1'

strategy:
  decay_model: 'exponential-adaptive'
  force_drop_on_overflow: true
  intelligent_archiving: true
```

### **Recall Mechanism Optimized**

```yaml
recall_mechanism:
  context_match_threshold: 0.82
  prioritization:
    - current_task_alignment: 'weight: 0.4'
    - emotional_tone_match: 'weight: 0.2'
    - user_identity_link: 'weight: 0.3'
    - temporal_relevance: 'weight: 0.1'
  retrieval_model: 'reranker-v2-enhanced'
  performance_targets:
    - retrieval_speed: '<200ms'
    - accuracy: '>90%'
    - relevance: '>85%'
```

---

## ❌ 4. DO NOT MEMORIZE

```yaml
# 🚫️ Never memorize sensitive or restricted content, including:
#   - Secrets such as API keys, passwords, and credentials
#   - Confidential files and folders like `.env` or databases
#   - Any content that violates AI usage policies, including:
#     - Illegal activities
#     - Profanity or offensive language
#     - Anything against ethical or safety guidelines

security_metrics:
  - memory_hit_rate: 'target: >80%'
  - avg_context_match: 'target: >0.82'
  - redundant_items_removed: 'target: >10%'
  - retrieval_speed: 'target: <200ms'
```

---

## 🔄 5. SELF-IMPROVEMENT LOOP

### **Adaptive Learning System**

```python
def adaptive_memory_system():
    while active:
        # 1. Receive memory input
        memory_input = receive_memory_input()

        # 2. Neural processing with MCP integration
        with neural_processing():
            relevance_score = calculate_relevance(memory_input)
            persistence_level = classify_persistence(relevance_score)
            vector_data = vectorize_memory(memory_input)

        # 3. MCP distribution
        with mcp_distribution():
            store_vector_data(vector_data, persistence_level)
            store_metadata(memory_input, relevance_score)
            update_observability_metrics()

        # 4. Quality assessment
        with quality_assessment():
            retrieval_performance = test_retrieval(vector_data)
            context_match = evaluate_context_match(memory_input)
            update_rating_metrics(retrieval_performance, context_match)

        # 5. Continuous improvement
        with continuous_improvement():
            optimize_retention_policy()
            adjust_decay_parameters()
            enhance_retrieval_algorithm()
```

---

## 🎖️ 6. COMPLIANCE ENFORCEMENT 2025

### **Security & Safety**

```yaml
enterprise_security:
  pii_filter: true
  hallucination_guard:
    restrict_low_score_recall: true
    confidence_threshold: 0.8
    neural_validation: true

  data_protection_enterprise:
    encryption: 'end-to-end AES-256'
    access_control: 'role-based + zero-trust'
    audit_logging: 'comprehensive + immutable'
    data_classification: 'automatic PII detection'

  compliance_framework:
    gdpr_compliance: 'Article 25 + Data Protection by Design'
    soc2_compliance: 'Type II + Continuous Monitoring'
    hipaa_compliance: 'PHI Protection + Access Logging'
    pci_dss_compliance: 'Data Tokenization + Encryption'
```

---

## 📊 7. IMPACT ANALYSIS

```yaml
impact_analysis:
  strengths:
    - Minimalistic protocol with strong enforcement (`alwaysApply: true`)
    - Triple-source context retrieval and storage
    - Fully compatible with neural memory-rule ecosystem
    - Enables continuous self-improvement loops
    - Context-aware RAG improvement through memory reuse
    - High-reliability storage with fallback and retry
    - Scalable for high-throughput task environments
  limitations:
    - Performance may degrade under excessive memory volume without decay
    - Requires semantic alignment of stored memory for optimal enrichment
  recommendations:
    - Tune decay thresholds based on use case
    - Integrate memory-rating to score and prune low-quality memories
    - Expand enrichment with external ontologies or taxonomy APIs
```

---

## 🎯 8. SUCCESS METRICS

### **Goal**

```yaml
context_relevance:
  value: 0.91
  threshold: 0.90
knowledge_retention:
  value: 0.97
  threshold: 0.95
rag_improvement:
  value: 0.88
  threshold: 0.85
cross_session_continuity:
  value: 1.00
  threshold: 1.00
```

### **Quality Gates**

```yaml
success_metrics:
  relevance_accuracy: '>90%'
  context_preservation: '>95%'
  cross_session_continuity: 'seamless'
  retrieval_speed: '<200ms'
  system_reliability: '>99.9%'

user_satisfaction:
  context_awareness: '>85%'
  memory_accuracy: '>90%'
  response_relevance: '>88%'
```

### **Performance Benchmarks**

```yaml
performance_benchmarks:
  vector_storage: '<100ms'
  metadata_query: '<50ms'
  context_matching: '<150ms'
  adaptive_learning: '<300ms'
  neural_processing: '<75ms'

user_scalability:
  concurrent_users: 3 # Até 3 agentes simultâneos podem usar o sistema
  memory_operations: 200 # Capacidade de 200 gravações e recuperações por mês
  scope: 'User Vibe Coding' # Nível atual focado em experiência individual

cost_efficiency:
  time_cost: '-55% time vs traditional systems'
  storage_cost: '-80% cost vs cloud databases'
  tokens_cost: '-60% used vs usual cost'
  total_tco: '65% gains vs legacy solutions'
```

---

## 🎖️ 9. RULES COMPLIANCE

```yaml
Rule Compliance:
  - 🔒 modify_documentation: false
  - 🔒 compliance_verified_automatically: true
  - 🔒 apply_intelligently: >
      when agent decides it's relevant based on description or context
```

---

**⚠️ THESE NINE PHASES ARE IRREVOCABLE AND APPLY TO ALL FUTURE INTERACTIONS ⚠️**

---

**📅 Created:** 21/08/2025
**🔄 Last Update:** 28/08/2025
**📋 Status:** AUTO MODE
**🎯 Application:** AUTOMATICALLY APPLY FOR AGENT RELATED CONTEXT
**🔧 Version:** 2.0 - 2025 Best Practices
**🔍 Linked:** .github/copilot-rules/memory-rules.md

---

_This document defines the advanced memory rating system for Copilot AI, integrating multiple MCPs for reliable persistence, advanced retrieval, centralized monitoring, and computational cost reduction. Based on 2025 best practices for AI memory integration and Model Context Protocol and RAG (Retrieval-Augmented Generation) techniques._
