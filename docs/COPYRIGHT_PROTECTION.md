# 🛡️ Guia de Proteção de Copyright

Este documento descreve as medidas de proteção implementadas no Python RAG Project.

## 📋 Índice

- [Medidas Legais](#medidas-legais)
- [Medidas Técnicas](#medidas-técnicas)
- [Detecção de Cópias](#detecção-de-cópias)
- [Ações de Enforcement](#ações-de-enforcement)
- [FAQ](#faq)

## ⚖️ Medidas Legais

### 1. Licença MIT com Requisitos de Atribuição

O projeto usa **MIT License** que exige:

✅ Inclusão do arquivo LICENSE em todas as cópias
✅ Preservação de avisos de copyright
✅ Isenção de responsabilidade mantida

**Arquivo**: [LICENSE](../LICENSE)

### 2. Arquivo NOTICE

Requisitos adicionais de atribuição (inspirado em Apache 2.0):

✅ Atribuição obrigatória em redistribuições
✅ Listagem de componentes de terceiros
✅ Requisitos para uso em SaaS

**Arquivo**: [NOTICE](../NOTICE)

### 3. CITATION.cff

Formato padrão para citações acadêmicas e técnicas:

✅ Metadados estruturados para citação
✅ Compatível com GitHub, Zenodo, etc.
✅ Facilita atribuição automática

**Arquivo**: [CITATION.cff](../CITATION.cff)

### 4. Developer Certificate of Origin (DCO)

Certificado de autoria para contribuidores:

✅ Garante que contribuidores têm direito ao código
✅ Verificação automática via GitHub Actions
✅ Requer `Signed-off-by:` em commits

**Arquivo**: [.github/DCO](../.github/DCO)

## 🔒 Medidas Técnicas

### 1. Cabeçalhos de Copyright

Todos os arquivos Python contêm:

```python
"""
Module description.

Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

This file is part of Python RAG Project.
See LICENSE file for full license details.

Project Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
"""
```

**Adicionar automaticamente**:

```bash
python scripts/add_copyright_headers.py
```

### 2. Watermarking Digital

Identificadores únicos inseridos no código:

- **Project ID**: `PRAG-2025-VU-v1.0`
- **Digital Signature**: `8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d`

Estes watermarks permitem:
✅ Busca automatizada por cópias não autorizadas
✅ Prova de origem do código
✅ Detecção de remoção maliciosa

### 3. Assinatura GPG de Commits

Commits assinados garantem:

✅ Autenticidade do autor
✅ Integridade do código (não modificado)
✅ Badges "Verified" no GitHub

**Configurar**: Ver [GPG_SIGNING.md](GPG_SIGNING.md)

### 4. Git Hooks

Hooks locais para verificação automática:

**Pre-commit** (`.githooks/pre-commit`):

- ✅ Verifica cabeçalhos de copyright
- ✅ Executa formatadores (Black, isort)
- ✅ Roda linters (flake8)

**Commit-msg** (`.githooks/commit-msg`):

- ✅ Verifica formato Conventional Commits
- ✅ Exige DCO sign-off
- ✅ Detecta remoção de watermarks

**Ativar hooks**:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/*
```

## 🔍 Detecção de Cópias

### 1. GitHub Action de Detecção Automática

Workflow que roda semanalmente:

**Arquivo**: [.github/workflows/detect-copies.yml](../.github/workflows/detect-copies.yml)

**Funcionamento**:

1. Busca por watermarks únicos via GitHub Code Search
2. Identifica repositórios contendo nosso código
3. Cria issue automaticamente se cópias encontradas
4. Envia notificação para revisão

**Executar manualmente**:

```bash
# Via GitHub CLI
gh workflow run detect-copies.yml

# Ou via interface web
# Actions → Detect Unauthorized Copies → Run workflow
```

### 2. Busca Manual

**Via GitHub Code Search**:

```
"PRAG-2025-VU-v1.0"
"8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d"
"Python RAG Project Team"
```

**Via Google**:

```
site:github.com "PRAG-2025-VU-v1.0"
site:github.com "Python RAG Project Team" -site:github.com/devviniuchita
```

**Ferramentas Especializadas**:

- [Sourcegraph](https://sourcegraph.com/)
- [GitHub Code Search](https://github.com/search?type=code)
- [FOSSID](https://fossid.com/) (enterprise)

### 3. Monitoramento de Forks

Forks são visíveis no GitHub:

**Ver forks**:

```bash
# Via GitHub CLI
gh api repos/devviniuchita/python_project/forks

# Ou na interface
https://github.com/devviniuchita/python_project/network/members
```

**Verificar atribuição em forks**:

```bash
# Script para checar LICENSE em forks
for fork in $(gh api repos/devviniuchita/python_project/forks --jq '.[].full_name'); do
  echo "Checking $fork"
  gh api repos/$fork/contents/LICENSE 2>/dev/null || echo "❌ No LICENSE"
  gh api repos/$fork/contents/NOTICE 2>/dev/null || echo "⚠️  No NOTICE"
done
```

## ⚖️ Ações de Enforcement

### 1. Contato Amigável (Primeira Etapa)

Se detectar uso sem atribuição:

**Template de Email**:

```
Subject: Attribution Request for Python RAG Project

Hi [Nome],

I noticed your project [repo-link] appears to include code from
Python RAG Project (https://github.com/devviniuchita/python_project).

While we're happy you found our work useful, the MIT License requires:
1. Including the LICENSE file
2. Preserving copyright notices
3. Including the NOTICE file

Could you please add these files to comply with the license?

Thanks,
Vinícius Uchita
```

### 2. GitHub DMCA Takedown

Se copyright foi violado:

**Quando usar**:

- Código copiado sem LICENSE
- Copyright notices removidos
- Uso não autorizado após pedido de compliance

**Como fazer**:

1. Acesse: https://github.com/contact/dmca
2. Preencha formulário DMCA
3. Forneça:
   - Link do seu repositório original
   - Link do repositório infrator
   - Prova de autoria (commits assinados, histórico)
   - Descrição da violação

**Documentação**: https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy

### 3. Ação Legal

Para casos sérios:

**Quando considerar**:

- Uso comercial sem licença
- Recusa em compliance após contato
- Danos financeiros ou reputacionais

**Passos**:

1. Consultar advogado especializado em IP
2. Coletar evidências (commits, timestamps, GitHub insights)
3. Enviar cease and desist letter
4. Processar se necessário

**Evidências úteis**:

- Commits assinados com GPG
- GitHub commit history
- Copyright registration (se feito)
- Comunicações anteriores

## ❓ FAQ

### Por que MIT License se quero proteção?

MIT é permissiva mas **exige atribuição**. Isso significa:

- ✅ Permite uso comercial (aumenta adoção)
- ✅ Permite modificações
- ✅ **EXIGE** inclusão de LICENSE e copyright
- ✅ Base legal para ação se atribuição removida

### O que é watermark digital?

Identificadores únicos no código que permitem:

- Busca automatizada por cópias
- Prova de origem
- Detecção de remoção maliciosa

**Nossos watermarks**:

- `PRAG-2025-VU-v1.0` (Project ID)
- `8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d` (Digital Signature)

### Watermarks podem ser removidos?

Sim, mas:

- ❌ Remoção pode ser detectada via git hooks
- ❌ Busca ainda pode encontrar cópias antigas
- ❌ Remoção pode configurar má-fé (legal)

### Como provar autoria em caso de disputa?

**Evidências fortes**:

1. ✅ Commits assinados com GPG (timestamp verificável)
2. ✅ Histórico completo no GitHub (não force-pushed)
3. ✅ Copyright registration (US Copyright Office)
4. ✅ Comunicações e documentação

**Dica**: Mantenha histórico limpo e assine commits importantes.

### Preciso registrar copyright?

**Não obrigatório**, mas recomendado:

**Sem registro**:

- ✅ Copyright automático ao criar
- ✅ Pode processar por violação
- ❌ Danos limitados

**Com registro**:

- ✅ Prova prima facie de autoria
- ✅ Danos estatutários (até $150k por violação nos EUA)
- ✅ Custas legais recuperáveis

**Como registrar** (EUA):

- https://www.copyright.gov/registration/
- Custo: ~$65
- Processo online

### Como evitar que alguém clone meu repo?

**Repositório público**: Impossível tecnicamente.

**Opções**:

1. ⭐ **Tornar privado**: Controle total de acesso
2. ⭐ **Distribuir binários**: Código-fonte privado, só releases públicas
3. ⭐ **Acesso via API**: SaaS, código não exposto

**Para público com proteção**:

- Use licença forte (GPL/AGPL para reciprocidade)
- Implemente detecção automática
- Registre copyright
- Assine commits

### GitHub mostra quem clona meu repo?

**Não**. GitHub Traffic mostra:

- ✅ Número de clones (últimos 14 dias)
- ✅ Número de visitantes únicos
- ❌ **NÃO** identidade de quem clonou

**Visível**:

- ✅ Forks (com autor)
- ✅ Stars (com autor)
- ✅ Watches (com autor)

### Como detectar cópias não-forkadas?

**Métodos**:

1. ✅ Busca por watermarks (automatizada)
2. ✅ GitHub Code Search
3. ✅ Google Code Search
4. ✅ Ferramentas especializadas (Sourcegraph, FOSSID)
5. ✅ Monitoring de package registries (PyPI, NPM)

**Nosso workflow**: `.github/workflows/detect-copies.yml`

### O que fazer se encontrar cópia?

**Checklist**:

1. ✅ Verificar se LICENSE está incluído
2. ✅ Verificar se NOTICE está incluído
3. ✅ Verificar atribuição adequada
4. ✅ Verificar compliance com MIT

**Se não-conforme**:

1. 📧 Contato amigável (template acima)
2. ⏳ Aguardar 7-14 dias
3. 🔨 GitHub DMCA se não responder
4. ⚖️ Ação legal se necessário

### Posso mudar para licença mais restritiva?

**Sim**, mas:

- ✅ Futuras versões podem usar nova licença
- ❌ Versões antigas permanecem sob MIT
- ⚠️ Pode afetar adoção e contribuições

**Opções mais restritivas**:

- **GPLv3**: Derivados devem ser GPL (copyleft)
- **AGPLv3**: Como GPL, mas inclui uso via rede
- **Proprietária**: Proíbe redistribuição

### Watermarks afetam performance?

**Não**. São apenas strings/comentários:

- ✅ Zero overhead de runtime
- ✅ Apenas bytes extras no arquivo
- ✅ Removidos em minification (se aplicável)

### Como contribuidores adicionam copyright?

**Automático**:

```bash
# Script adiciona headers
python scripts/add_copyright_headers.py

# Ou pre-commit hook adiciona
git config core.hooksPath .githooks
```

**Manual**: Ver template em `scripts/add_copyright_headers.py`

## 📚 Recursos Adicionais

### Documentação

- [LICENSE](../LICENSE) - Licença MIT
- [NOTICE](../NOTICE) - Requisitos de atribuição
- [CITATION.cff](../CITATION.cff) - Como citar
- [GPG_SIGNING.md](GPG_SIGNING.md) - Assinar commits
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Guia de contribuição
- [SECURITY.md](../SECURITY.md) - Política de segurança

### Ferramentas

- [add_copyright_headers.py](../scripts/add_copyright_headers.py) - Adicionar headers
- [copyright-check.yml](../.github/workflows/copyright-check.yml) - CI check
- [detect-copies.yml](../.github/workflows/detect-copies.yml) - Detector automático
- [dco-check.yml](../.github/workflows/dco-check.yml) - DCO enforcement

### Links Externos

- [GitHub DMCA Guide](https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy)
- [US Copyright Office](https://www.copyright.gov/)
- [Developer Certificate of Origin](https://developercertificate.org/)
- [SPDX License List](https://spdx.org/licenses/)
- [Choose a License](https://choosealicense.com/)

---

**Última Atualização**: Janeiro 2025
**Autor**: Vinícius Uchita
**Projeto**: Python RAG Project

**Digital Watermark**: PRAG-2025-VU-v1.0
**Signature**: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
