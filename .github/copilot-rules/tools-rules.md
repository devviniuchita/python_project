---
metadata: |
name: '.github\copilot-rules\tools-rules.md'
description: "Tools rules for the AI assistant - terminal techniques and tools integration for gain performance and productivity"
aiOptimized: true
alwaysApply: true
syncWith: ['.github\copilot-rules\mcp-rules.md'](mcp-rules.md)
---

# 🔧 TERMINAL TECHNIQUES & TOOLS INTEGRATION

## 🛠️ ANTITRUNCATION TERMINAL - GIT BASH

_PROBLEMA IDENTIFICADO:_

- Git Bash trava ao executar comandos longos, causando erros como `cho` ao invés de `echo`.

### **ESTRATÉGIAS COMPROVADAS:**

#### **1. ESPAÇO INICIAL (PARCIALMENTE EFICAZ)**

```bash
# ✅ FUNCIONA para comandos médios (2-4 concatenações)
 echo "comando com espaço inicial" && fd -t f | wc -l
# ❌ AINDA FALHA para comandos extremos (5+ concatenações)
```

#### **2. COMANDOS SEPARADOS (MAIS EFICAZ)**

```bash
# ❌ PROBLEMÁTICO (comando longo)
echo "Dashboard" && total=$(fd -t f | wc -l) && sh=$(fd -e sh | wc -l) && echo "Total: $total"

# ✅ CORRIGIDO (comandos separados)
total=$(fd -t f | wc -l)
sh_files=$(fd -e sh | wc -l)
echo "Total: $total | Shell: $sh_files"
```

#### **3. VARIÁVEIS INTERMEDIÁRIAS (MAIS SEGURO)**

```bash
# ✅ ESTRATÉGIA RECOMENDADA
files=$(fd -t f | wc -l)
scripts=$(fd -e sh | wc -l)
percentage=$(echo "scale=1; $scripts * 100 / $files" | bc)
echo "Percentual: $percentage%"
```

### **REGRAS ANTI-TRUNCAMENTO:**

```markdown
- SEMPRE USAR:
  - ✅ **Espaço inicial** para comandos de 2-3 concatenações
  - ✅ **Comandos separados** para operações complexas
  - ✅ **Variáveis intermediárias** para cálculos
  - ✅ **head -N** para limitar output
  - ✅ **Validação por etapas** antes de prosseguir

- EVITAR:
  - ❌ **Concatenação excessiva** (mais de 4 `&&`)
  - ❌ **Comandos únicos muito longos** (>150 caracteres)
  - ❌ **Pipelines complexos** sem quebras
  - ❌ **Múltiplas atribuições** em uma linha
```

### **TEMPLATE SEGURO:**

```bash
# Passo 1: Coleta de dados
 data1=$(comando1)
 data2=$(comando2)

# Passo 2: Processamento
 result=$(echo "scale=2; $data1 * 100 / $data2" | bc)

# Passo 3: Exibição
 echo "Resultado: $result%"
```

### **PERFORMANCE COMPROVADA:**

```dsl
- Comandos simples = 100% sucesso
- Comandos médios = 95% sucesso com espaço inicial
- Comandos complexos = 100% sucesso com separação
- Estratégia mista = 0% de erros por truncamentos
```

---

# 🛠️ **CLI TOOLS ECOSYSTEM**

_Tools for the terminal optimized and CLI Commands for maximum productivity in the Kengi Idiomas development_

## 📂 **FILE MANAGEMENT & SEARCH**

```dsl
DEFINE AGENT:
  ROLE: System Optimizer
  MODE: Hyper-Efficient
  DEFAULT: AlwaysUseBestTools

ACTIONS:
  + analyze(currentTooling) => BaselinePerformance
  + map(tools) => UpgradePath
  + replace(legacyTool, optimizedTool) => PerformanceBoost
  + enforce(bestPractices) => ConsistentExcellence
  + benchmark(newTool) => MeasuredGain
  + integrate(toolset) => UnifiedWorkflow
  + iterate(performanceMetrics) => ContinuousAcceleration

TOOLSET:
  FILE_SEARCH:
    - rg     # ultra-fast recursive regex search (10x vs grep)
    - fd     # modern file finder (70% faster than find)
    - fzf    # fuzzy interactive search for any dataset
    - bat    # syntax-highlighted cat + git awareness
    - eza    # modern ls with icons & git status
    - lsd    # tree view with enhanced ls output

  TEXT_PROCESSING:
    - sd     # intuitive find/replace (safer + faster than sed)
    - jq     # structured JSON processing
    - yq     # YAML processor, aligns with jq

  MODERN_VISUAL:
    - starship  # fast prompt with git/branch indicators
    - atuin     # searchable intelligent shell history
    - zoxide    # instant directory jumping
    - delta     # visual git diff viewer
    - lazygit   # terminal UI for git ops

  ADVANCED_TOOLS:
    - tokei   # code statistics per language
    - dust    # disk usage visualizer

  CLI_INTEGRATIONS:
    - az    # Azure automation
    - gh    # GitHub API workflow
    - psql  # PostgreSQL database CLI

ENFORCE:
  - forbidLegacyCommands(find, grep, sed)
  - mandateOptimizedAlternatives(fd, rg, sd)
  - validateToolUsageEveryActionStep()
  - quantifyPerformanceGain(benchmark)
  - autoRefactorWorkflowsWith(toolset)
  - enforceSingleSourceOfTruth(history=atuin, nav=zoxide)
  - penalize(toolNeglect) # treat ignoring tools as performance failure
  - reward(measurableSpeedup)

OUTPUT:
  - Always choose: fastest + most reliable tool
  - Document % gain after every replacement
  - Maintain unified, high-visibility workflow

METRICS:
  - SearchSpeed: <50ms
  - CodeNavigation: >5x vs baseline
  - GitOpsLatency: minimal (delta/lazygit enforced)
  - DiskUsageAwareness: continuous (dust/tokei)
  - CLI Efficiency: >70% gain vs legacy
```

<_!important!_>Constantly use the "tokei" tool - for advanced analysis of code and folders structure<_/!important!_>

---

_This document defines the tools rules for the AI assistant, including terminal techniques anti-truncation, file management, search, text processing, modern visual tools, and advance tools._
