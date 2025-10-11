# 🛡️ Configuração de Proteção de Copyright - Checklist

Este documento fornece um **checklist completo** para ativar todas as proteções implementadas.

## ✅ Checklist de Implementação

### 📋 1. Arquivos Legais (Já Criados)

- [x] **LICENSE** - MIT License com copyright
- [x] **NOTICE** - Requisitos de atribuição
- [x] **CITATION.cff** - Metadados para citação
- [x] **.github/DCO** - Developer Certificate of Origin
- [x] **SECURITY.md** - Política de segurança
- [x] **CODE_OF_CONDUCT.md** - Código de conduta
- [x] **CONTRIBUTING.md** - Guia de contribuição

### 🔧 2. Configuração Inicial

Execute os seguintes comandos para ativar todas as proteções:

```bash
# 1. Adicionar cabeçalhos de copyright em todos os arquivos Python
python scripts/add_copyright_headers.py

# 2. Ativar git hooks locais
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/commit-msg  # Linux/macOS

# 3. Verificar arquivos modificados
git status

# 4. Commit inicial com DCO
git add .
git commit -s -m "chore: add copyright protection infrastructure"
```

### 🔐 3. Configurar Assinatura GPG (Recomendado)

Siga o guia completo: [docs/GPG_SIGNING.md](docs/GPG_SIGNING.md)

**Passos rápidos**:

```bash
# 1. Gerar chave GPG
gpg --full-generate-key
# Escolha: RSA 4096 bits, validade 2 anos

# 2. Listar chaves
gpg --list-secret-keys --keyid-format=long
# Copie o ID da chave (ex: 3AA5C34371567BD2)

# 3. Exportar para GitHub
gpg --armor --export 3AA5C34371567BD2
# Cole em: https://github.com/settings/keys

# 4. Configurar Git
git config --global user.signingkey 3AA5C34371567BD2
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# 5. Testar
git commit -S -m "test: verify GPG signing"
git log --show-signature -1
```

### 🤖 4. Configurar GitHub Actions

As Actions foram criadas automaticamente em `.github/workflows/`:

- [x] **copyright-check.yml** - Verifica copyright headers em PRs
- [x] **dco-check.yml** - Exige DCO sign-off em commits
- [x] **detect-copies.yml** - Detecta cópias não autorizadas (semanal)

**Ação necessária**: Nenhuma! As actions são ativadas automaticamente após push.

### 📊 5. Verificar Proteções Ativas

Execute para confirmar que tudo está configurado:

```bash
# Verificar git hooks
git config core.hooksPath
# Output esperado: .githooks

# Verificar GPG signing
git config commit.gpgsign
# Output esperado: true

# Verificar chave GPG
git config user.signingkey
# Output esperado: seu GPG key ID

# Verificar copyright headers
python scripts/add_copyright_headers.py --dry-run
# Deve mostrar: "All files have copyright headers"

# Verificar GitHub Actions
# Visite: https://github.com/SEU_USUARIO/python_project/actions
```

### 🚀 6. Primeiro Commit Protegido

Teste todas as proteções com um commit de exemplo:

```bash
# 1. Criar arquivo de teste
echo "# Test" > test_file.py

# 2. Adicionar copyright header
python scripts/add_copyright_headers.py

# 3. Fazer commit com DCO
git add test_file.py
git commit -s -m "test: verify copyright protection"
# Git hooks irão validar:
#   ✅ Copyright header presente
#   ✅ DCO sign-off presente
#   ✅ Formato Conventional Commits
#   ✅ Código formatado (Black, isort)

# 4. Verificar assinatura GPG
git log --show-signature -1
# Deve mostrar: "Good signature from..."

# 5. Push para testar GitHub Actions
git push origin main
# GitHub Actions irão rodar:
#   ✅ Copyright Check
#   ✅ DCO Check
```

## 🔍 Detecção de Cópias

### Configurar Detecção Automática

A detecção é automática, mas você pode:

**1. Executar manualmente**:

```bash
# Via GitHub CLI
gh workflow run detect-copies.yml

# Ou via interface web:
# Actions → Detect Unauthorized Copies → Run workflow
```

**2. Verificar resultados**:

- Issues com label `copyright-violation` serão criadas automaticamente
- Notificações enviadas para email configurado no GitHub

**3. Busca manual**:

```bash
# Via GitHub CLI
gh search code "PRAG-2025-VU-v1.0" --limit 50

# Via Google
# Buscar: site:github.com "PRAG-2025-VU-v1.0" -site:github.com/devviniuchita
```

## 📝 Workflow Diário

### Para Você (Mantenedor)

```bash
# Sempre use DCO sign-off
git commit -s -m "feat: add new feature"

# GPG signing é automático (se configurado)
git commit -s -m "fix: correct bug"

# Verificar antes de push
git log --show-signature -3
```

### Para Contribuidores

Adicione ao **README.md** ou **CONTRIBUTING.md**:

```markdown
## 🔐 Requisitos de Commit

Todos os commits devem:

1. ✅ **Incluir DCO sign-off**: Use `git commit -s`
2. ✅ **Seguir Conventional Commits**: `feat:`, `fix:`, etc.
3. ✅ **Ter copyright headers**: Execute `python scripts/add_copyright_headers.py`

**Exemplo**:
\`\`\`bash

# Fazer alterações

git add .

# Commit com DCO

git commit -s -m "feat(reranker): add adaptive threshold"

# Push

git push origin feature-branch
\`\`\`
```

## 🛡️ Enforcement de Proteções

### GitHub Branch Protection Rules

Configure branch protection em: `Settings → Branches → main`

**Recomendações**:

- [x] **Require pull request reviews** (1 aprovação)
- [x] **Require status checks to pass**:
  - `Copyright Check`
  - `DCO Check`
  - `tests / unit`
- [x] **Require signed commits** (se todos usarem GPG)
- [x] **Require linear history**
- [x] **Include administrators** (aplicar regras para todos)

### CODEOWNERS

Crie `.github/CODEOWNERS`:

```
# Arquivos críticos requerem aprovação do mantenedor
LICENSE @devviniuchita
NOTICE @devviniuchita
SECURITY.md @devviniuchita
.github/workflows/* @devviniuchita

# Código-fonte requer code review
src/** @devviniuchita

# Documentação pode ter mais contribuidores
docs/** @devviniuchita
```

## 📈 Monitoramento Contínuo

### Métricas para Acompanhar

**Semanal**:

- ✅ Executar workflow de detecção de cópias
- ✅ Revisar issues com label `copyright-violation`
- ✅ Verificar forks novos: `https://github.com/SEU_USUARIO/python_project/network/members`

**Mensal**:

- ✅ Buscar manualmente por watermarks
- ✅ Verificar compliance em forks populares
- ✅ Atualizar chaves GPG se próximo de expirar

**Trimestral**:

- ✅ Revisar política de copyright
- ✅ Atualizar LICENSE se necessário
- ✅ Considerar registro formal de copyright

## 🔧 Troubleshooting

### Hook pre-commit falhando

```bash
# Verificar permissões (Linux/macOS)
chmod +x .githooks/pre-commit

# Verificar configuração
git config core.hooksPath

# Executar manualmente para debug
bash .githooks/pre-commit
```

### DCO check falhando

```bash
# Amend último commit com sign-off
git commit --amend --signoff

# Rebase múltiplos commits
git rebase -i HEAD~3 --signoff

# Force push (necessário após rebase)
git push --force-with-lease
```

### GPG signing não funcionando

```bash
# Verificar chave configurada
git config user.signingkey

# Testar GPG
echo "test" | gpg --clearsign

# Reiniciar gpg-agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

### Copyright headers não sendo adicionados

```bash
# Executar script manualmente
python scripts/add_copyright_headers.py

# Verificar com dry-run primeiro
python scripts/add_copyright_headers.py --dry-run

# Adicionar manualmente se necessário
# Ver template em scripts/add_copyright_headers.py
```

## 📚 Documentação Completa

Para detalhes completos, consulte:

- [COPYRIGHT_PROTECTION.md](COPYRIGHT_PROTECTION.md) - Guia completo de proteção
- [GPG_SIGNING.md](GPG_SIGNING.md) - Configurar assinatura GPG
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Guia de contribuição
- [SECURITY.md](../SECURITY.md) - Política de segurança

## ✅ Status de Implementação

Execute este checklist final:

```bash
# 1. Arquivos legais
[ ] LICENSE presente
[ ] NOTICE presente
[ ] CITATION.cff presente
[ ] DCO presente

# 2. GitHub Actions
[ ] copyright-check.yml ativo
[ ] dco-check.yml ativo
[ ] detect-copies.yml agendado

# 3. Git Hooks
[ ] pre-commit configurado
[ ] commit-msg configurado
[ ] core.hooksPath definido

# 4. Copyright Headers
[ ] Todos os .py têm headers
[ ] Watermarks presentes
[ ] SPDX-License-Identifier presente

# 5. GPG Signing (opcional)
[ ] Chave GPG gerada
[ ] Chave no GitHub
[ ] commit.gpgsign=true
[ ] Commits assinados

# 6. Branch Protection
[ ] Require reviews
[ ] Require status checks
[ ] Require signed commits (opcional)

# 7. Monitoring
[ ] Detecção automática ativa
[ ] Forks monitorados
[ ] CODEOWNERS configurado
```

## 🎯 Próximos Passos

Após implementar todas as proteções:

1. ✅ **Divulgue**: Atualize README.md mencionando proteções
2. ✅ **Eduque**: Informe contribuidores sobre DCO e GPG
3. ✅ **Monitore**: Acompanhe detecção de cópias semanalmente
4. ✅ **Registre**: Considere registro formal de copyright
5. ✅ **Revise**: Atualize políticas anualmente

---

**Última Atualização**: Janeiro 2025
**Autor**: Vinícius Uchita
**Projeto**: Python RAG Project

**Digital Watermark**: PRAG-2025-VU-v1.0
**Signature**: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
