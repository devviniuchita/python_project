---
metadata: |
name: '.github/copilot-rules/mcp-rules.md'
description: 'MCP Matrix decision, Pipeline Workflow, Integration Protocol, Security & Validation, Usage examples & Patterns and Enforcement Rules'
aiOptimized: true
alwaysApply: true
syncWith: [.github/copilot-rules/tools-rules.md](tools-rules.md)
---

# MCP RULES

## 📊 MCP USAGE EXAMPLES & PATTERNS - 4 PATTERNS

<_!IMPORTANT!_>

### 1. **PATTERN 1: Feature Development**

_Flow Architecture_

```
Memory Retrieval → Task Analysis → Research & Validation → Context Building → Strategic Planning → Risk Assessment → Implementation → Knowledge Storage
```

```yaml
- 1. [byterover, supermemory-ai, memory]: Extract information and memories from recent implementations
- 2. Todo2: Analyze and define the task to be developed
- 3. exa and Brave-search: Search for the best and most current practices on the topic related to the task to be developed
- 4. exa and Context7: Deepen the context of the task to be developed with official documentation
- 5. Sequential Thinking: After acquiring the maximum context > Plan the Implementation Strategy
- 6. exa and Brave-search: Search for Solutions or Ideas for Possible Errors or Difficulties
- 7. Sequential Thinking: Expand the Context
- 8. Todo2: Schedule the Task Update
- 9. [byterover, supermemory-ai, memory, memory-plus]: Store Learned Patterns and Task Update + Knowledge Graph in a structured format of representing knowledge, organizing information as entities and their relationships, forming a network of facts to create a comprehensive strategy
```

### **PATTERN 2: Troubleshooting**

_Flow Architecture_

```
Memory Retrieval → Research the problem → Search for documentation on the framework with the problem → Strategic Planning for the solution → Execute the Problem Solution → Store Knowledge of the executed solution
```

```yaml
- 1. [byterover, supermemory-ai, memory, memory-plus]: 'similar error patterns'
- 2. Exa and Brave-search: 'error message 2025 solutions'
- 3. exa and Context7: 'framework specific documentation'
- 4. Sequential-Thinking: Analyze root cause
- 5. Execution: Troubleshoot
- 6. [byterover, supermemory-ai, memory]: Store solution pattern
```

### **PATTERN 3: Research and Planning**

_Flow Architecture_

```
Search and acquire context → Deep planning → Greater context with documentation → Strategic planning for execution → Create tasks → Store memories of created tasks
```

```yaml
- 1. exa and Brave-search: 'Research best practices and recommendations'
- 2. Sequential Thinking: Structure research questions according to recommendations
- 3. exa and Context 7: 'Research official documentation'
- 4. Sequential-Thinking: Group all acquired context to execute next actions
- 5. Todo2: Based on every user request versus all knowledge gained from the research and context acquired from steps 1 through 4 - Create and divide tasks into "T1, T2, T3, etc." tasks strategically and intelligently. Not neglecting or forgetting ANY information
- 6. [byterover, supermemory-ai, memory, memory-plus]: Memorize how tasks were created
```

### **PATTERN 4: Merge with other PATTERNS as needed**

_Flow Architecture_

```
The agent applies a smart form that is relevant based on the flow and context. PATTERN 4 can be mixed with any other PATTERN
```

```yaml
Tools:
  - Filesystem: For file and directory operations
  - Microservices docs: To get context or find solutions in the official documentation for Microsoft products and frameworks (e.g., Python, C#, VsCode, etc.)
  - Firecrawl: Intelligent Web Scraping
  - @21st-dev/magic: Fast generation of modern UI components
  - shadcn-ui: Library of components for React and UI design systems
```

<_/!IMPORTANT!_>

---

## 🚨 ENFORCEMENT RULES

### 1. **MANDATORY MCP USAGE:**

```yaml
Always_Use:
  - Sequential Thinking: Conversational Analysis and Planning
  - Byteover / Supermemory: Beginning and Ending Meaningful Implementations
  - Memory / Memory-Plus: Maps for Knowledge, Entities, and Relationships
  - Exa: Enrich context and acquire more information

Context_Dependent:
  - Todo2: For development tasks
  - Context7: Retrieval documentation and libraries
  - Brave-search / Exa: For latest information 2025 and troubleshooting
  - Microsoft-docs: Microsoft products best practices documentation

Reforcement:
  - Filesystem: File and directory operations

Database:
  - PostgreSQL: Database operations and queries

Azure:
  - Azure-CLI (az): Azure command-line interface operations
  - MCP Server Azure: Azure functions and resources management
  - Azure Resources: Azure logs, queues, and storage management

Never_Skip:
  - Validation next tool calls
  - Error handling in all MCP
  - Context limits enforcement
  - Token usage optimization
```

### 2. **QUALITY METRICS:**

```yaml
Success_Indicators:
  - Relevance_Score: '>0.4 (Byterover, memory, memory-plus, supermemory)'
  - Trust_Score: '>7.0 (Context7, Exa, Brave-search and microsoft docs)'
  - Implementation_Success: 'Error-free validation'

Failure_Triggers:
  - Timeout em critical MCPs
  - Relevance_Score: '<0.3'
  - Multiple consecutive MCP failures
```
