# 🛡️ Copyright Protection Setup - Quick Reference

## 🚀 Quick Start (5 minutos)

```bash
# 1. Adicionar copyright headers
python scripts/add_copyright_headers.py

# 2. Ativar git hooks
git config core.hooksPath .githooks
chmod +x .githooks/*  # Linux/macOS

# 3. Commit com DCO
git add .
git commit -s -m "chore: add copyright protection"

# 4. Push (ativa GitHub Actions)
git push origin main
```

## 📋 Arquivos Criados

| Arquivo                                   | Propósito                             | Status    |
| ----------------------------------------- | ------------------------------------- | --------- |
| **LICENSE**                               | MIT License com copyright             | ✅ Criado |
| **NOTICE**                                | Requisitos de atribuição Apache-style | ✅ Criado |
| **CITATION.cff**                          | Metadados para citação                | ✅ Criado |
| **.github/DCO**                           | Developer Certificate of Origin       | ✅ Criado |
| **.github/workflows/copyright-check.yml** | Verifica headers em PRs               | ✅ Criado |
| **.github/workflows/dco-check.yml**       | Exige DCO sign-off                    | ✅ Criado |
| **.github/workflows/detect-copies.yml**   | Detecta cópias (semanal)              | ✅ Criado |
| **.githooks/pre-commit**                  | Validação local de copyright          | ✅ Criado |
| **.githooks/commit-msg**                  | Valida DCO e Conventional Commits     | ✅ Criado |
| **scripts/add_copyright_headers.py**      | Adiciona headers automaticamente      | ✅ Criado |
| **docs/COPYRIGHT_PROTECTION.md**          | Guia completo                         | ✅ Criado |
| **docs/GPG_SIGNING.md**                   | Guia de assinatura GPG                | ✅ Criado |
| **docs/SETUP_CHECKLIST.md**               | Checklist de implementação            | ✅ Criado |

## 🔐 Proteções Implementadas

### 1. **Cabeçalhos de Copyright**

Todos os arquivos Python incluem:

```python
"""
Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

Project Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
"""
```

### 2. **Watermarks Digitais**

Identificadores únicos para detecção:

- `PRAG-2025-VU-v1.0` (Project ID)
- `8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d` (Signature)

### 3. **GitHub Actions**

- ✅ Verifica copyright em PRs
- ✅ Exige DCO sign-off
- ✅ Detecta cópias semanalmente

### 4. **Git Hooks**

- ✅ Pre-commit: Valida headers, formata código
- ✅ Commit-msg: Exige DCO, valida formato

### 5. **DCO (Developer Certificate of Origin)**

Todos os commits requerem:

```bash
git commit -s -m "feat: add feature"
```

### 6. **GPG Signing (Opcional mas Recomendado)**

Commits assinados com GPG garantem autenticidade.

## ⚡ Comandos Essenciais

### Adicionar Copyright Headers

```bash
# Dry run (apenas simular)
python scripts/add_copyright_headers.py --dry-run

# Aplicar em todo o projeto
python scripts/add_copyright_headers.py

# Aplicar em diretório específico
python scripts/add_copyright_headers.py src/
```

### Commits com Proteção

```bash
# Commit com DCO
git commit -s -m "feat(reranker): add threshold"

# Commit com GPG (se configurado)
git commit -S -s -m "fix: correct bug"

# Amend com DCO
git commit --amend --signoff
```

### Verificar Proteções

```bash
# Verificar git hooks
git config core.hooksPath

# Verificar GPG
git config commit.gpgsign
git log --show-signature -1

# Executar hook manualmente
bash .githooks/pre-commit
```

### Detectar Cópias

```bash
# Via GitHub CLI
gh workflow run detect-copies.yml

# Busca manual
gh search code "PRAG-2025-VU-v1.0"
```

## 🎯 Checklist de Ativação

- [ ] **1. Copyright Headers**: `python scripts/add_copyright_headers.py`
- [ ] **2. Git Hooks**: `git config core.hooksPath .githooks`
- [ ] **3. GitHub Actions**: Push para ativar workflows
- [ ] **4. GPG (opcional)**: Configurar assinatura (ver GPG_SIGNING.md)
- [ ] **5. Branch Protection**: Configurar em Settings → Branches
- [ ] **6. CODEOWNERS**: Criar `.github/CODEOWNERS`

## 📊 Monitoramento

### Semanal

- ✅ Revisar issues `copyright-violation`
- ✅ Verificar novos forks

### Mensal

- ✅ Buscar watermarks manualmente
- ✅ Verificar compliance em forks

## 📚 Documentação Completa

- **[COPYRIGHT_PROTECTION.md](COPYRIGHT_PROTECTION.md)** - Guia completo
- **[GPG_SIGNING.md](GPG_SIGNING.md)** - Assinatura GPG
- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Checklist detalhado

## 🆘 Suporte

**Problemas comuns**:

1. Hook não executa → `chmod +x .githooks/*`
2. DCO falhando → `git commit --amend --signoff`
3. GPG não funciona → `gpgconf --kill gpg-agent`

**Contato**: viniciusuchita@gmail.com

---

**Digital Watermark**: PRAG-2025-VU-v1.0
**Signature**: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
