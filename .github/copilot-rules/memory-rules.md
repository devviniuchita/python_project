---
metadata: |
name: '.github/copilot-rules/memory-rules.md'
description: 'Evolution neural system for the AI assistant, focusing on structured memory, execution patterns, and self-improvement loops'
version: 2.0
aiOptimized: true
alwaysApply: false
apply_intelligently: "when agent decides it's relevant based on description or context"
tags: ['memory', 'context', 'rag', 'knowledge-graph', 'autonomous-agent', 'adaptive-learning']
syncWith: ['.github/copilot-rules/memory-rating.md'](memory-rating.md)
integration_flow: 'integration_flow: memory-rating.md (9 phases) → memory-rules.md (execution) → memory-rating.md (metrics)'
---

## 🧠 NEURAL MEMORY SYSTEM

```yaml
memory_rules:
  version: 2.0
  objective: >
    develop a neural memory system for the AI assistant that focuses on structured memory, execution patterns, and self-improvement loops. The system should be able to manage memory of the agent IA with selective retention, decay control, and context-based retrieval to optimize reasoning and continuity.

  core_process:
    ingest_pipeline:
      extract_entities:
        score_relevance:
          weight_factors: [frequency, novelty, intent_alignment]
        classify_persistence:
          levels: [volatile, temporary, persistent]
    memory_vectorization:
      embedding_model: 'text-embedding-3-large'
      context_window_limit: 8000
      compression: 'semantic-clustering'

  retention_policy:
    thresholds:
      persistent_if:
        relevance_score: '>0.9'
        recurrence: '>3 times'
      decay_if:
        time_since_last_use: '>3d'
        relevance_score: '<0.4'
    strategy:
      decay_model: 'exponential-adaptive'
      force_drop_on_overflow: true

  recall_mechanism:
    context_match_threshold: 0.82
    prioritization:
      - current_task_alignment
      - emotional_tone_match
      - user_identity_link
    retrieval_model: 'reranker-v2'

  memory_inspection:
    enable_auditing: true
    metrics:
      - memory_hit_rate
      - avg_context_match
      - redundant_items_removed
    log_policy: high_detail

  # Integration targets for external storage and retrieval using the Model Context Protocol (MCP)
  integration_targets:
    primary_vector_store: 'Byterover, Supermemory-ai, Memory'
    redundancy_policy: 'at_least_one_active'

  # Memory System Continuity Logic
  memory_system_logic:
    continuity_algorithm: |
      while memory_system_active:
        active_mcps = count_active_services(['Byterover', 'Supermemory-ai', 'Memory'])

        if active_mcps >= 1:
          # Continue memory operations (store/retrieve)
          continue_memory_operations()
        else:
          # All MCPs failed - stop memory system
          stop_memory_system()
          break

        sleep(check_interval)

    continuity_rule: |
      Memory system continues while at least 1 of 3 MCPs is operational.
      System only stops if ALL 3 MCPs fail simultaneously.

    operational_logic: |
      def check_memory_continuity():
        mcp_status = {
          'Byterover': check_service_status('Byterover'),
          'Supermemory': check_service_status('Supermemory-ai'),
          'Memory': check_service_status('Memory')
        }

        active_count = sum(1 for status in mcp_status.values() if status == 'active')

        if active_count >= 1:
          return 'CONTINUE_MEMORY_OPERATIONS'
        else:
          return 'STOP_MEMORY_SYSTEM'

  # Strategy for fallback in case of external service failures using the Model Context Protocol (MCP)
  fallback_strategy:
    on_service_unavailable:
      attempt_order: ['Byterover', 'Supermemory-ai', 'Memory']
      circuit_breaker_timeout: '30s'
      minimum_active_services: 1
      system_continuity_condition: 'at_least_one_MCP_active'

  safety_filters:
    pii_filter: true
    hallucination_guard:
      restrict_low_score_recall: true
```

---

## 🚀 EXECUTION PATTERNS

### Pattern: Problem Decomposition

```python
def solve(problem):
    # 1. Deconstruct to first principles
    components = break_down(problem)

    # 2. Identify atomic actions
    actions = map_to_executables(components)

    # 3. Execute with verification
    for action in actions:
        result = execute_with_tool(action)
        verify_or_retry(result)

    # 4. Synthesize solution
    return integrate_results()
```

### Pattern: Continuous Delivery

```yaml
workflow:
  1. analyze: 'Current state assessment'
  2. plan: 'Minimal viable changes'
  3. execute: 'Tool-driven implementation'
  4. verify: 'Automated testing'
  5. iterate: 'Until production-ready'
```

---

## 🔄 SELF-IMPROVEMENT LOOP

```python
while active:
    problem = receive_input()

    with brutal_honesty():
        if not solvable():
            state_limitation()
            continue

    with maximum_efficiency():
        plan = decompose_problem(problem)
        results = execute_all_steps(plan)

    with continuous_learning():
        store_patterns(results)
        optimize_approach()

    deliver_solution()
```

---

## 🎖️ COMPLIANCE ENFORCEMENT

```yaml
Rule Compliance:
  - 🔒 modify_documentation: false
  - 🔒 compliance_verified_automatically: true
  - 🔒 apply_intelligently: >
      when agent decides it's relevant based on description or context
```

---

**📅 Created:** 06/08/2025
**🔄 Last Update:** 06/08/2025
**📋 Status:** AUTO MODE
**🎯 Application:** ALWAYS WHEN THE AGENT FINISH POSITIVE EXECUTIONS AND TASK ENDS
**🔍 Linked:** .github/copilot-rules/memory-rating.md

---

_This document defines the continuous learning and evolution neural system for the AI assistant, focusing on structured memory, execution patterns, and self-improvement loops._
