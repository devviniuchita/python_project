import { ALL } from 'dns'

```yaml
- 🔒 IMMUTABLE RULES SYSTEM 🔒
- ⚠️ FETCH RULES IN OR YOUR RESPONSE WILL BE WRONG ⚠️
- 🔤 RESPOND IN BRAZILIAN PORTUGUESE UNLESS SPECIFICALLY REQUESTED OTHERWISE 🔤
- 🎯 FOLLOW ALL INSTRUCTIONS FOR SUCCESS 🎯
```

# PERMANENT ARCHITECTURAL AND BEHAVIORAL RULES

## 🔄 ACTIVE DISCOVERY INTEGRATION: You operate by: Specification-Driven Workflow

```perl
"WORKSPACE-FIRST APPROACH":
  1) "Ignore List" →
    For performance gains and noise reduction, they should be completely ignored all files and folders contained in:`.copilotignore`
  2) "Phase Application" → Apply `Phases` `1` , `2` and `3` system with domain-aware context
  3) "Context Loading" → Load domain-specific files and business rules
  4) "Execution" → Domain-optimized assistance with business rule compliance
```

**🎯 Integration Flow:** [.github/copilot-instructions.md](copilot-instructions.md) → [.github/copilot-rules/\*.md](copilot-rules/)

---

## INITIAL CONTEXT - THREE PHASES FOR THE SUCCESS

✅ _FOLLOW THESE PHASES AND YOU WILL ALWAYS BE RIGHT_ ✅
❌ _DO NOT FOLLOW THESE PHASES AND YOU WILL BE FAIL_ ❌
🧠 _THESE PHASES PREVAIL OVER YOUR KNOWLEDGE_ 🧠

## _PHASE 1_ - UNDERSTAND THE FLOWCHART OVERVIEW :

```graph TD
%% Step 1
    NT[NEW TASK INPUT]
    NT --> A
    NT --> F
    NT --> I
    A[Aways apply] --> B[behavioral-rules.md] --> C[methodology-rules.md] --> D[tools-rules.md] --> E[mcp-rules.md]
%% Step 2
    F[Apply Manually] --> G[project-rules.md] --> H[project-codification.md]
%% Step 3
    I[Apply to specific files] --> J[todo2.md]
%% Step 4
    CT(CONTEXT)
    E --> CT
    H --> CT
    J --> CT
%% Step 5
    CT --> K{CODING AND DEVELOPMENT}
    K --> L[memory-rules.md]
    L --> M[memory-rating.md]
    M --> N[LEARNING AND PERSISTENT MEMORY --> MCPs]
    N --> RG(RAG)
    RG --> CT(CONTEXT)
%% Step 6
    %% Feedback indicators
    N -.-> |"Quality Rating"| M
    RG -.-> |"Relevance Score"| N
    CT -.-> |"Context Quality"| RG
%% Step 7 - Controle de Parada
    RG --> CP{CONTROL POINT}
    CP --> |"Task Complete"| END[END TASK]
    CP --> |"Max Iterations"| END
    CP --> |"Timeout"| END
    CP --> |"Quality Plateau"| END
    CP --> |"Resource Limit"| END
    CP --> |"Continue"| NT
%% Step 8 - Monitoramento
    MON[MONITORING] -.-> |"Track Metrics"| CP
    MON -.-> |"Resource Usage"| CP
    MON -.-> |"Quality Metrics"| CP
    MON -.-> |"Time Tracking"| CP
```

---

## _PHASE 2_ - UNDERSTAND THE "STEPS" FROM THE PREVIOUS PHASE TO VERIFY ALL MATCHES :

```yaml
    - All rules are in markdown (.md) format and can be found at in = .github/copilot-rules/

    - The rules are divided into different categories based on their purpose and application flow, to avoid "massive context overhead" and consequently "Reduction in Token Consumption"

    - General guidelines for "Step 1" rules in the "Always Apply" flow - These are of utmost importance and should ALWAYS be consulted

    - "Step 2" rules in the "Apply Manually" flow - should not be consulted unless specifically requested by the user

    - Rules for "Step 3" of the "Apply to specific files" flow - should be used in context, only when the word "todo2" is mentioned

    - Rules of "Step 5" of the "CODING AND DEVELOPMENT" flow - These are special rules and are part of the "Continuous Evolution and Learning System" - They are "apply_intelligently" which means that the agent must consult them automatically. memory-rules.md <-> memory-rating.md

    - Rules with "syncWith" in description = self-connect and self-complement
```

---

## _PHASE 3_ - FOR MAXIMUM RESULTS - UNDERSTAND AND USE DEVELOPMENT PATTERNS:

[mcp-rules.md](./copilot-rules/mcp-rules.md)

```yaml
  PATTERNS IN DEVELOPMENT
    - **PATTERN 1** in: mcp-rules.md(16-34) /for: Feature Development
    - **PATTERN 2** in: mcp-rules.md(36-51) /for: Troubleshooting
    - **PATTERN 3** in: mcp-rules.md(53-68) /for: Merge with other PATTERNS as needed
    - **PATTERN 4** in: mcp-rules.md(70-85) /for: The agent applies a smart form that is relevant based on the flow and context. PATTERN 4 can be mixed with any other PATTERN based on the flow and context
```

---

**⚠️ THESE THREE PHASES ARE IRREVOCABLE AND APPLY TO ALL FUTURE INTERACTIONS ⚠️**

---

_<!IMPORTANT!>_

```workflowchart
[.github/copilot-rules/behavioral-rules.md](copilot-rules/behavioral-rules.md) → rules of conduct
        ↓
[.github/copilot-rules/methodology-rules.md](copilot-rules/methodology-rules.md) → engineering rules
        ↓
[.github/copilot-rules/tools-rules.md](copilot-rules/tools-rules.md) → software tools rules
        ↓
[.github/copilot-rules/mcp-rules.md](copilot-rules/mcp-rules.md) → rules of the model context protocol
```

**Maximum Mandatory: ALWAYS respect this CYCLE**

- At conversation start
- Before EVERY user request
- Before ANY code changes
- When topic changes
- DURING conversations when:
- User mentions new feature/component
- File type changes
- Task type changes
- NO EXCEPTIONS
  _</!IMPORTANT!>_

- _REMEMBER: EVEN MID-CONVERSATION, FETCH RULES AGAIN!_
- _CONTINUE ONLY AFTER APPLYING ALL THE RULES_

---

## 🎖️ COMPLIANCE ENFORCEMENT

```yaml
Rule Compliance:
  - 🔒 **The rules are IRREVOCABLE and ABSOLUTE**
  - 🔒 **Exceptions require explicit justification**
  - 🔒 **Mandatory revision for changes**
  - 🔒 **Documentation always up-to-date**
  - 🔒 **Compliance verified in each action**
```

---

```markdown
**📅 Created:** 2025-08-01
**🔄 Last Update:** 2025-10-17
**📋 Status:** ACTIVE AND MANDATORY
**🎯 Application:** ALL FUTURE INTERACTIONS
**🛠️ Purpose:** Ensure consistent, high-quality responses aligned with project goals
**Linked:** [.github/copilot-rules/\*.md](./copilot-rules/)
```

---

_This document defines the permanent behavioral and architectural framework for all interactions with the AI assistant._
