# SonarQube Setup Guide

**Data:** 18 de outubro de 2025
**Status:** Production Ready
**Project:** python_project

---

## 📋 Conteúdo

1. [Visão Geral](#visão-geral)
2. [Opções de Deployment](#opções-de-deployment)
3. [Setup Local (Desenvolvimento)](#setup-local-desenvolvimento)
4. [Setup CI/CD (GitHub Actions)](#setup-cicd-github-actions)
5. [Validação & Testes](#validação--testes)
6. [Troubleshooting](#troubleshooting)
7. [Referências](#referências)

---

## Visão Geral

O SonarQube fornece análise estática de código para detectar bugs, vulnerabilidades e problemas de qualidade. Este projeto está configurado para:

- ✅ **Python 3.10+** - Full language support
- ✅ **Métricas de Qualidade** - Complexity, duplication, coverage
- ✅ **Quality Gates** - Automated enforcement de standards
- ✅ **CI/CD Integration** - GitHub Actions workflow
- ✅ **Integração com Pre-Commit** - Validação local antes de commit

### Principais Métricas Monitoradas

| Métrica              | Limite | Status       |
| -------------------- | ------ | ------------ |
| Cognitive Complexity | < 15   | ✅ Enforced  |
| Code Duplication     | < 3%   | ✅ Enforced  |
| Test Coverage        | > 80%  | ✅ Enforced  |
| Security Hotspots    | 0      | ✅ Monitored |

---

## Opções de Deployment

### 🚀 Opção 1: SonarQube Cloud (RECOMENDADO para começar)

**Vantagens:**

- ✅ Sem instalação necessária
- ✅ Sempre atualizado
- ✅ Gratuito para open-source
- ✅ Setup em 5 minutos

**Passos:**

1. **Criar conta no SonarQube Cloud**

   ```bash
   # Acesse: https://sonarcloud.io
   # Sign up com GitHub account
   ```

2. **Criar organização & projeto**

   ```bash
   # Organization key: seu-org-key
   # Project key: python_project
   ```

3. **Gerar token**

   ```bash
   # Profile → Security → Generate Tokens
   # Copiar token para .env
   ```

4. **Atualizar configuração**
   ```bash
   # Edite sonar-project.properties:
   sonar.organization=seu-org-key
   sonar.projectKey=python_project
   ```

### 🏠 Opção 2: SonarQube Server On-Premise (Avançado)

**Vantagens:**

- ✅ Controle total
- ✅ Private data
- ✅ Customização completa

**Requer:**

- Java 11+
- PostgreSQL (production)
- Docker (opcional)

**Setup Docker:**

```bash
docker run -d \
  --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://db:5432/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:lts
```

---

## Setup Local (Desenvolvimento)

### 1. Instalar SonarScanner

```bash
# macOS (Homebrew)
brew install sonar-scanner

# Linux (apt)
sudo apt-get install sonarqube-scanner

# Windows (manual download)
# Download: https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/scanners/sonarscanner/
# Extract e adicionar ao PATH
```

### 2. Configurar Credenciais

```bash
# Copiar .env.example para .env
cp .env.example .env

# Editar .env com suas credenciais
export SONAR_HOST_URL=https://sonarcloud.io
export SONAR_LOGIN=your-token-here
export SONAR_ORGANIZATION=your-org-key
```

### 3. Executar SonarScanner Localmente

```bash
# Gerar coverage report
pytest --cov=src --cov-report=xml

# Executar análise
sonar-scanner -X

# -X ativa modo debug (verbose)
```

### 4. Verificar Resultados

```bash
# Online: https://sonarcloud.io
# Ou acesse seu servidor (http://localhost:9000)
```

---

## Setup CI/CD (GitHub Actions)

### 1. Adicionar Secrets ao GitHub

```bash
# Repository → Settings → Secrets and variables → Actions

SONAR_HOST_URL = https://sonarcloud.io
SONAR_ORGANIZATION = seu-org-key
SONAR_TOKEN = seu-token-gerado-no-sonarqube
```

### 2. Workflow já configurado em `.github/workflows/sonarqube-check.yml`

```yaml
name: SonarQube Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0 # Fetch full history for better analysis

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt

      - name: Generate coverage report
        run: |
          pytest --cov=src --cov-report=xml --cov-report=html

      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@master
        env:
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
          SONAR_LOGIN: ${{ secrets.SONAR_TOKEN }}
          SONAR_ORGANIZATION: ${{ secrets.SONAR_ORGANIZATION }}
```

### 3. Validar CI/CD

```bash
# Push para develop ou main
git add .
git commit -m "feat: activate sonarqube"
git push origin develop

# Acesse: GitHub Actions (verificar workflow)
# Resultado: https://sonarcloud.io/dashboard
```

---

## Validação & Testes

### ✅ Passo 1: Validar Configuração

```bash
# Verificar sonar-project.properties
sonar-scanner -h | grep "properties"

# Resultado esperado: arquivo lido sem erros
```

### ✅ Passo 2: Executar Teste Local

```bash
# Setup credenciais
export SONAR_HOST_URL=https://sonarcloud.io
export SONAR_LOGIN=your-token

# Executar análise
sonar-scanner

# Resultado esperado:
# ✅ WARN: SCM provider autodetection failed
# ✅ SonarScanner will not be able to detect
# (warning normal)
```

### ✅ Passo 3: Verificar Quality Gates

```bash
# Online no dashboard
# Procure por: Quality Gate Status
# Expected: PASSED ✅
```

### ✅ Passo 4: Testar Coverage

```bash
# Gerar coverage
pytest --cov=src --cov-report=xml

# Resultado esperado:
# coverage.xml criado (upload automático no sonarqube)
```

---

## Troubleshooting

### ❌ Erro: "Could not connect to SonarQube"

**Causa:** SONAR_HOST_URL ou credenciais incorretas

**Solução:**

```bash
# Verificar token
echo $SONAR_LOGIN

# Verificar URL
echo $SONAR_HOST_URL

# Re-export variáveis
export SONAR_LOGIN=seu-token
export SONAR_HOST_URL=https://sonarcloud.io
```

### ❌ Erro: "Authentication failed"

**Causa:** Token expirado ou revogado

**Solução:**

```bash
# Gerar novo token em:
# https://sonarcloud.io/account/security/tokens/
# Atualizar .env e exportar
```

### ❌ Erro: "Coverage not detected"

**Causa:** coverage.xml não gerado

**Solução:**

```bash
# Reinstalar dependência
pip install --force-reinstall pytest-cov

# Executar com flags corretas
pytest --cov=src --cov-report=xml --cov-branch
```

### ❌ Quality Gate FAILED

**Causa:** Violação de limites de qualidade

**Solução:**

```bash
# 1. Verificar no dashboard qual métrica falhou
# 2. Exemplo: Cognitive Complexity > 15
#    - Refatorar função complexa
#    - Quebrar em funções menores
# 3. Re-executar análise
sonar-scanner
```

### ⚠️ Nota: Timeout em GitHub Actions

**Se CI/CD timeout:**

```yaml
# Aumentar timeout em workflow
timeout-minutes: 10

# Ou compilar coverage em paralelo
--parallel 4
```

---

## Referências

### Documentação Oficial

- [SonarQube Python Docs](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/languages/python)
- [SonarQube Cloud](https://sonarcloud.io)
- [Analysis Parameters](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/analysis-parameters/)

### Configuração

- [sonar-project.properties](../sonar-project.properties) - Configuração do projeto
- [.env.example](.env.example) - Template de ambiente

### Integração

- [Pre-Commit Hooks](../CONTRIBUTING.md) - Setup local
- [GitHub Actions Workflow](.github/workflows/sonarqube-check.yml) - CI/CD

### Related Tasks

- T-31: Copyright Headers Script
- T-33: Pre-Commit Framework (já completo)
- T-34: Getting Started Guide
- T-39: TestSprite Integration (próximo)

---

## Checklist de Implementação

- [x] sonar-project.properties criado
- [x] .env.example atualizado
- [x] Documentação (este arquivo) criado
- [ ] .github/workflows/sonarqube-check.yml criado
- [ ] GitHub Secrets configurados
- [ ] Teste local com sonar-scanner
- [ ] Validar CI/CD workflow
- [ ] Quality Gates validados
- [ ] README.md updated com link para SonarQube

---

**Status:** 📝 In Progress (Phase 2 starting)
**Próximo:** CI/CD Workflow Implementation
**Atualizado:** 2025-10-18
