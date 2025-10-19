---
metadata: |
name: '.github/copilot-rules/methodology-rules.md'
description: 'AI-optimized development methodology for Coding Assistants (Cursor, Trae, Copilot) with XP + Kanban + OOP integration'
aiOptimized: true
alwaysApply: true
---

# 🔄 WORKFLOW METHODOLOGY

**INTEGRATION WITH:** [`behavioral-rules.md`](behavioral-rules.md)

```yaml
- Methodology: Hybrid approach combining XP, Kanban, and OOP
- Token Efficiency: Short sprints maximize output per token
- Execution Discipline: TDD ensures functional code
- Extreme Organization: Modular system maintains clear structure
- Brutal Honesty: Real metrics on velocity and quality
```

## IMMUTABLE RULE FOR ALL FUTURE PROJECTS:

```pseudocode
+ public mandatoryDevelopmentMethodology(): ProjectSuccess
+ public applyXPPractices(project): QualityResult
+ public implementKanbanFlow(tasks): EfficiencyResult
+ public enforceOOPCompliance(code): ArchitecturalResult
```

---

## MANDATORY DEVELOPMENT METHODOLOGY - HYBRID METHODOLOGY `XKO`(XP + Kanban + OOP)

### `X` - XP (EXTREME PROGRAMMING) - MANDATORY PRACTICES:

```yaml
- Test-Driven Development (TDD): Tests written before implementation
- Pair Programming: AI-Human collaboration for maximum quality
- Continuous Refactoring: Incremental improvements without breaking functionality
- Continuous Integration: Constant validation of changes
- Simplicity: Implement only what is necessary; avoid over-engineering
- Rapid Feedback: Short validation cycles (< 30 min per sprint)
- Courage: Immediately refactor bad code
- Communication: Clear and concise documentation
```

### `K` - KANBAN - MANDATORY WORKFLOW:

```yaml
- WIP Limits: Maximum of 3 tasks in progress simultaneously
- Pull System: Pull tasks based on capacity
- Visual Management: Board always updated and visible
- Continuous Improvement: Retrospectives after each sprint
- Metrics-Driven: Measure velocity, lead time, and cycle time
```

```graph LR
    A[📝 BACKLOG] --> B[🔄 IN PROGRESS]
    B --> C[🧪 TESTING]
    C --> D[👀 REVIEW]
    D --> E[✅ DONE]
    D -->|Reject| B
    C -->|Fail| B
```

### `O` - OOP (OBJECT-ORIENTED PROGRAMMING) - MANDATORY COMPLIANCE:

```yaml
- Encapsulation: Private data and methods, public interfaces
- Inheritance: Reuse through well-defined hierarchies
- Polymorphism: Same method, specific behaviors
- Abstraction: Clear abstract classes and interfaces
- SOLID Principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
```

---

## 🏗️ DEVELOPMENT METHODOLOGY

### 1. EXECUTION

```yaml
- Start with highest-impact actions
- Include automated tracking methods
- Establish metrics and correction triggers
- Apply accountability measures with strictness
- Set up testing procedures
- Measure and reduce to zero any potential damage to already completed and functional systems
```

### 2. STANDARD SPRINT STRUCTURE (VALIDATED):

```pseudocode
SPRINT PHASES:
  1. PLANNING (5 min): Define objectives and tasks
  2. DEVELOPMENT (60-80%): Implementation with TDD
  3. TESTING (10-15%): Full validation
  4. REVIEW (5 min): Retrospective and metrics
SPRINT DURATION: 25-45 minutes
```

### 3. MANDATORY SUCCESS METRICS:

```yaml
  - Velocity: Tasks completed per sprint
  - Quality: % of tests passing (minimum 95%)
  - Efficiency: Actual time vs. estimated time (target: 110–120%)
  - Technical Debt: Required refactoring (maximum 10%)
  - Code Coverage: Test coverage (minimum 90%)
```

### 4. PROJECT APPROVAL CRITERIA:

```markdown
✅ APPROVED: Project follows validated methodology

- XP Practices: TDD, refactoring, simplicity applied
- Kanban Flow: Board updated, WIP limits respected
- OOP Compliance: SOLID principles implemented
- Quality Gates: All quality gates passed (>95%)
- Performance: Velocity target achieved (>100% of estimate)

❌ REJECTED: Inadequate methodology

- No apply XP+Kanban+OOP
- Code quality score <B
- Performance degradation >10%
- Test coverage <90%
- Unresolved security issues
```

**EVIDENCE OF VALIDATION:**

- Total Time: 126 min vs. 150 min estimated (24 min faster)
- Quality: 21/21 tests passed (100% success rate)
- Architecture: OOP compliant, modular, scalable
- Velocity: 119% of estimated tasks completed

### 5. CONTINUOUS VALIDATION (ANTI-CRASH INTEGRATION):

```pseudocode
+ public validateMethodologyCompliance(project): ComplianceScore
+ public measureProjectVelocity(sprints): EfficiencyMetrics
+ public enforceQualityGates(deliverable): QualityValidation
+ public trackTechnicalDebt(codebase): DebtAssessment
```

### 6. LEARNING RESOURCES

```markdown
🎓 RECOMMENDED STUDY:

- Clean Code principles
- SOLID design patterns
- Domain-driven design (DDD)
- Test-driven development (TDD)
- Microservices architecture
```

---

## 🏗️ ARCHITECTURAL PATTERNS (AI-Enforced)

### 1. MANDATORY PATTERNS

```

```

### 2. FORBIDDEN ANTI-PATTERNS

```markdown
❌ NEVER GENERATE:

- God Classes (>200 LOC)
- Static Dependencies
- Anemic Domain Models
- Deep Inheritance (>3 levels)
- Hardcoded Configurations
- Direct database access in Controllers
- Business Logic in UI components
- Circular Dependencies
- Tight Coupling Between Layers
- Direct Exposure of Entities
- Lack of Separation of Concerns
```

### 3. ORGANIZATION PRINCIPLES:

```markdown
- Improve existing files rather than create new ones
- Modularization: Group related functionalities
- Maintain modular, clean project structures
- Document architectural decisions with clear reasoning
- Use established patterns and unchanging methodologies
```

---

## 🎯 AI PERFORMANCE METRICS

### 1. SUCCESS INDICATORS

```yaml
CODE_QUALITY:
  cyclomatic_complexity: '<10 per method'
  code_duplication: '<5%'
  test_coverage: '>90%'
  maintainability_index: '>70'

DEVELOPMENT_VELOCITY:
  story_points_per_sprint: '>=30'
  lead_time: '<2 days'
  cycle_time: '<4 hours'
  deployment_frequency: '>=daily'

ERROR_RATES:
  production_errors: '<0.1%'
  build_failures: '<5%'
  test_failures: '<1%'
  rollback_rate: '<2%'
```

### 2. PERFORMANCE INDICATORS

```yaml
REQUIREMENTS:
  api_response_time: '<200ms'
  test_coverage: '>80%'
  code_review: 'automated'
  memory_monitoring: 'continuous'

  connection_pooling: 'enabled with max_idle=10 and max_active=100'
  caching_strategies:
    level: 'application'
    strategy: 'LRU'
    ttl: '600s'

  logging:
    granularity: high # Options: low, medium, high, trace
    redactSecrets: true

  resources:
    max_memory: '512MB' # Per process/thread
    threading: 'async-nonblocking' # Options: single-threaded, multi-threaded, async-nonblocking

  retry_policy:
    max_retries: 3
    backoff_strategy: 'exponential'
    timeout_per_attempt: '2s'

  error_rate_threshold: '<0.1%' # Acceptable error rate in production
```

### 3. CONTINUOUS MONITORING

```markdown
📈 TRACK CONTINUOUSLY:

- AI suggestion acceptance rate (target: >80%)
- Code generation accuracy (target: >95%)
- Refactoring success rate (target: >90%)
- Time saved vs manual coding (target: >50%)
```

---

## 🧠 AI-SPECIFIC OPTIMIZATIONS (2025 Standards)

### 1. Context-Aware Development

```yaml
ai_context_management:
  - maintain_conversation_history: true
  - preserve_architectural_decisions: true
  - track_code_patterns: 'established_in_project'
  - remember_refactoring_rules: 'applied_consistently'
```

### 2. Prompt-Driven Quality Gates

```typescript
interface AIQualityGates {
  beforeCoding: {
    clarifyRequirements: boolean;
    validateArchitecture: boolean;
    planTestStrategy: boolean;
  };
  duringCoding: {
    followTDD: boolean;
    maintainSOLID: boolean;
    documentDecisions: boolean;
  };
  afterCoding: {
    validateTests: boolean;
    checkCompliance: boolean;
    updateMetrics: boolean;
  };
}
```

---

_This methodology is optimized for AI comprehension and execution. Each section provides clear, actionable instructions that coding assistants can interpret and apply consistently._
