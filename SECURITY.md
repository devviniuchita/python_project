# 🔒 Política de Segurança

Segurança é prioridade neste projeto. Incentivamos pesquisadores, desenvolvedores e colaboradores a **reportar vulnerabilidades de forma responsável**.

## 🎯 Versões Suportadas

Atualmente oferecemos suporte de segurança para as seguintes versões:

| Versão  | Suporte          | Status                    |
| ------- | ---------------- | ------------------------- |
| main    | ✅ Suporte Ativo | Branch de produção        |
| develop | ⚠️ Parcial       | Branch de desenvolvimento |
| < 1.0   | ❌ Sem Suporte   | Versões legadas           |

## 📩 Como Reportar Vulnerabilidades

### Canais de Comunicação

1. **Email Direto** (Recomendado para questões críticas):
   - 📧 **viniciusuchita@gmail.com**
   - Assunto: `[SECURITY] Descrição breve da vulnerabilidade`

2. **GitHub Security Advisory** (Preferencial):
   - Acesse: [Security Advisories](../../security/advisories)
   - Clique em "Report a vulnerability"

3. **Issue Privada** (Se disponível):
   - Use a tag `security` e marque como privada
   - Inclua todos os detalhes necessários

### ⚠️ Importante: NÃO Divulgue Publicamente

**NUNCA** divulgue detalhes de vulnerabilidades em:

- ❌ Issues públicas
- ❌ Pull Requests
- ❌ Discussions públicas
- ❌ Redes sociais
- ❌ Fóruns públicos

## ✅ O Que Incluir no Relatório

Para facilitar a análise e correção, inclua:

1. **Descrição Clara**:
   - Tipo de vulnerabilidade (ex.: XSS, SQL Injection, RCE)
   - Componentes afetados

2. **Passos para Reproduzir**:

   ```
   1. Configurar ambiente X
   2. Executar comando Y
   3. Observar comportamento Z
   ```

3. **Impacto Estimado**:
   - 🔴 Crítico: Execução remota de código, vazamento de dados sensíveis
   - 🟡 Alto: Bypass de autenticação, escalada de privilégios
   - 🟢 Médio: DoS, exposição de informações não-críticas
   - ⚪ Baixo: Problemas de configuração, warnings

4. **Prova de Conceito** (PoC):
   - Código ou script demonstrando a vulnerabilidade
   - Screenshots ou logs relevantes

5. **Sugestões de Correção** (Opcional):
   - Patches propostos
   - Mitigações temporárias

## ⏱ SLA de Resposta

Nosso compromisso com segurança:

| Etapa                  | Prazo      | Descrição                                       |
| ---------------------- | ---------- | ----------------------------------------------- |
| **Reconhecimento**     | 72 horas   | Confirmação de recebimento do relatório         |
| **Análise Preliminar** | 7 dias     | Validação e priorização da vulnerabilidade      |
| **Plano de Ação**      | 14 dias    | Estratégia de correção e cronograma             |
| **Correção**           | 30-60 dias | Desenvolvimento, teste e release do patch       |
| **Divulgação Pública** | Pós-patch  | Coordenada com o pesquisador (CVE se aplicável) |

**Nota**: Vulnerabilidades críticas podem ter SLA acelerado.

## 🔒 Boas Práticas de Segurança

### Para Contribuidores

- ✅ **Revise Dependências**: Use `pip-audit` ou `safety` regularmente
- ✅ **Secrets Management**: NUNCA commite credenciais, use `.env` e `.gitignore`
- ✅ **Code Review**: Revise PRs com olhar crítico para segurança
- ✅ **Input Validation**: Sempre valide e sanitize inputs de usuário
- ✅ **Least Privilege**: Execute com permissões mínimas necessárias

### Para Usuários

- ✅ **Mantenha Atualizado**: Use sempre a versão mais recente
- ✅ **Variáveis de Ambiente**: Proteja `.env` com permissões adequadas (600)
- ✅ **Logs Seguros**: Não logue informações sensíveis
- ✅ **HTTPS/TLS**: Use conexões seguras para APIs externas
- ✅ **Auditoria Regular**: Revise logs e métricas de segurança

## 🛡️ Vulnerabilidades Conhecidas

| CVE ID | Severidade | Componente | Status | Versão Corrigida |
| ------ | ---------- | ---------- | ------ | ---------------- |
| -      | -          | -          | -      | -                |

_Nenhuma vulnerabilidade crítica conhecida no momento._

## 🏆 Reconhecimento (Hall of Fame)

Agradecemos aos pesquisadores que reportaram vulnerabilidades responsavelmente:

| Pesquisador | Vulnerabilidade | Data | Severidade |
| ----------- | --------------- | ---- | ---------- |
| -           | -               | -    | -          |

_Seja o primeiro a contribuir para nossa segurança!_

## 🔐 Política de Divulgação Responsável

### Compromisso do Projeto

- ✅ Responderemos prontamente a todos os relatórios válidos
- ✅ Manteremos o pesquisador informado sobre o progresso
- ✅ Creditaremos publicamente após a correção (se desejado)
- ✅ Não tomaremos ações legais contra pesquisadores que seguirem esta política

### Expectativas do Pesquisador

- ✅ Dê-nos tempo razoável para correção antes da divulgação pública
- ✅ Não explore a vulnerabilidade além do necessário para demonstração
- ✅ Não acesse, modifique ou exfiltre dados de produção
- ✅ Não execute DoS ou teste de carga que possa impactar serviços

## 📧 Contato de Segurança

**Email**: viniciusuchita@gmail.com
**PGP Key**: (Disponível mediante solicitação)
**LinkedIn**: [Vinícius Uchita](https://www.linkedin.com/in/viniciusuchita/)

## 📜 Conformidade e Certificações

Este projeto segue os padrões de segurança reconhecidos pela indústria:

- ✅ **[OWASP Top 10](https://owasp.org/www-project-top-ten/)**: Seguimos as diretrizes de segurança de aplicações web da Open Web Application Security Project
- ✅ **[CWE/SANS Top 25](https://cwe.mitre.org/top25/)**: Aderimos às práticas para evitar as vulnerabilidades mais perigosas de software
- ✅ **[Secure SDLC](https://owasp.org/www-project-integration-standards/)**: Implementamos práticas de desenvolvimento seguro em todo o ciclo de vida
- ✅ **Dependency Scanning**: Realizamos varredura automatizada de dependências com ferramentas como `pip-audit` e `safety`

### 🔗 Recursos de Segurança

- **OWASP Foundation**: [owasp.org](https://owasp.org/)
- **CWE (Common Weakness Enumeration)**: [cwe.mitre.org](https://cwe.mitre.org/)
- **NIST Cybersecurity Framework**: [nist.gov/cyberframework](https://www.nist.gov/cyberframework)
- **GitHub Security Best Practices**: [docs.github.com/security](https://docs.github.com/en/code-security)

### 🛡️ Recursos de Copyright e Proteção Intelectual

Este projeto implementa um **sistema robusto de 4 camadas** para proteção de copyright e propriedade intelectual:

**Documentação de Proteção**:

- 📚 **[COPYRIGHT_PROTECTION.md](docs/COPYRIGHT_PROTECTION.md)** - Documentação completa do sistema de 4 camadas
- 🔐 **[GPG_SIGNING.md](docs/GPG_SIGNING.md)** - Guia de assinatura GPG para commits e tags
- ✅ **[SETUP_CHECKLIST.md](docs/SETUP_CHECKLIST.md)** - Checklist de configuração de proteção
- 📖 **[COPYRIGHT_QUICK_REFERENCE.md](docs/COPYRIGHT_QUICK_REFERENCE.md)** - Referência rápida para contribuidores

**Automação e Verificação**:

- 🤖 **[copyright-check.yml](.github/workflows/copyright-check.yml)** - Workflow que verifica headers de copyright em todos os arquivos
- ✍️ **[dco-check.yml](.github/workflows/dco-check.yml)** - Workflow que valida assinaturas DCO em commits
- 🔍 **[detect-copies.yml](.github/workflows/detect-copies.yml)** - Workflow que detecta duplicação não autorizada de código

**Proteção Local**:

- 🪝 **[.githooks/pre-commit](.githooks/pre-commit)** - Hook que adiciona headers de copyright antes de cada commit
- ✅ **[.githooks/commit-msg](.githooks/commit-msg)** - Hook que valida mensagens de commit e DCO sign-off

**Requisitos Legais**:

- 📜 **[NOTICE](NOTICE)** - Atribuição obrigatória de copyright (Apache-style)
- ✍️ **[DCO](.github/DCO)** - Developer Certificate of Origin v1.1
- 📖 **[CITATION.cff](CITATION.cff)** - Citação acadêmica padronizada (CFF 1.2.0)

**⚠️ Importante**: Todas as contribuições devem incluir:

1. **Headers de copyright** em arquivos de código
2. **DCO sign-off** em todos os commits (`git commit -s`)
3. **Conformidade** com os termos da [LICENSE](LICENSE) e [NOTICE](NOTICE)

Para mais detalhes, consulte [CONTRIBUTING.md](CONTRIBUTING.md) (seção "Developer Certificate of Origin").

---

**Última Atualização**: Janeiro 2025
**Versão da Política**: 1.0
**Próxima Revisão**: Julho 2025
