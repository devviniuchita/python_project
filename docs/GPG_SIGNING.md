# 🔐 Guia de Assinatura GPG para Commits

Este guia ensina como configurar assinatura GPG para seus commits, garantindo autenticidade e integridade.

## 🎯 Por que assinar commits?

- ✅ **Prova de Autoria**: Verifica que você é o autor real do commit
- ✅ **Integridade**: Garante que o código não foi alterado após o commit
- ✅ **Confiança**: Badges "Verified" no GitHub aumentam credibilidade
- ✅ **Proteção Legal**: Fortalece reivindicações de copyright

## 📋 Pré-requisitos

- Git 2.0+
- GPG instalado no sistema

### Instalar GPG

**Windows**:

```bash
# Via Chocolatey
choco install gpg4win

# Ou baixar: https://gpg4win.org/
```

**macOS**:

```bash
brew install gnupg
```

**Linux**:

```bash
# Debian/Ubuntu
sudo apt-get install gnupg

# Fedora
sudo dnf install gnupg
```

## 🔑 Passo 1: Gerar Chave GPG

```bash
# Gerar nova chave GPG
gpg --full-generate-key

# Seleções recomendadas:
# 1. Tipo: RSA and RSA (default)
# 2. Tamanho: 4096 bits
# 3. Validade: 2 anos (pode renovar depois)
# 4. Nome: Seu nome completo
# 5. Email: mesmo email do GitHub
# 6. Senha: escolha uma senha forte
```

### Exemplo de Interação:

```
gpg (GnuPG) 2.4.0; Copyright (C) 2024 Free Software Foundation, Inc.

Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
Your selection? 1

RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096

Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 2y

Real name: Vinícius Uchita
Email address: viniciusuchita@gmail.com
Comment: Python RAG Project
```

## 🔍 Passo 2: Listar e Exportar Chave

```bash
# Listar chaves GPG
gpg --list-secret-keys --keyid-format=long

# Output exemplo:
# sec   rsa4096/3AA5C34371567BD2 2024-01-10 [SC] [expires: 2026-01-10]
#       4E9B7F8D2A1C6E5B3AA5C34371567BD2
# uid                 [ultimate] Vinícius Uchita <viniciusuchita@gmail.com>
# ssb   rsa4096/4BB6DD4D4D11B09E 2024-01-10 [E] [expires: 2026-01-10]

# Copie o ID da chave: 3AA5C34371567BD2

# Exportar chave pública (para GitHub)
gpg --armor --export 3AA5C34371567BD2

# Copie todo o output (de -----BEGIN PGP PUBLIC KEY BLOCK----- até -----END PGP PUBLIC KEY BLOCK-----)
```

## 🐙 Passo 3: Adicionar Chave ao GitHub

1. Acesse: https://github.com/settings/keys
2. Clique em **New GPG key**
3. Cole a chave pública exportada
4. Clique em **Add GPG key**

## ⚙️ Passo 4: Configurar Git

```bash
# Configurar chave GPG no Git (use o ID da sua chave)
git config --global user.signingkey 3AA5C34371567BD2

# Configurar email (DEVE ser o mesmo da chave GPG)
git config --global user.email "viniciusuchita@gmail.com"

# Habilitar assinatura automática de commits
git config --global commit.gpgsign true

# Habilitar assinatura de tags
git config --global tag.gpgsign true

# Configurar programa GPG (se necessário)
git config --global gpg.program gpg
```

### Windows: Configuração Adicional

Se estiver usando Git Bash no Windows:

```bash
# Adicionar ao ~/.bashrc ou ~/.bash_profile
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
source ~/.bashrc
```

## ✍️ Passo 5: Assinar Commits

### Commit Assinado Automaticamente

```bash
# Se configurou commit.gpgsign=true, todos os commits serão assinados
git commit -m "feat: adicionar nova funcionalidade"
```

### Commit Assinado Manualmente

```bash
# Usar flag -S para assinar commit individual
git commit -S -m "feat: adicionar nova funcionalidade"
```

### Assinar Tag

```bash
# Criar tag assinada
git tag -s v1.0.0 -m "Release v1.0.0"

# Verificar assinatura da tag
git tag -v v1.0.0
```

## ✅ Passo 6: Verificar Assinatura

```bash
# Verificar assinatura do último commit
git log --show-signature -1

# Output esperado:
# commit abc123... (HEAD -> main)
# gpg: Signature made Thu 10 Jan 2025 10:00:00 AM -03
# gpg:                using RSA key 3AA5C34371567BD2
# gpg: Good signature from "Vinícius Uchita <viniciusuchita@gmail.com>"
# Author: Vinícius Uchita <viniciusuchita@gmail.com>
# Date:   Thu Jan 10 10:00:00 2025 -0300
#
#     feat: adicionar nova funcionalidade
```

## 🔄 Assinar Commits Antigos (Rebase)

```bash
# Assinar últimos 3 commits
git rebase --exec 'git commit --amend --no-edit -n -S' -i HEAD~3

# Assinar todos os commits de uma branch
git rebase --exec 'git commit --amend --no-edit -n -S' -i main

# Force push (necessário após rebase)
git push --force-with-lease
```

## 🛠️ Troubleshooting

### Erro: "gpg failed to sign the data"

**Solução 1**: Configurar GPG_TTY

```bash
export GPG_TTY=$(tty)
```

**Solução 2**: Testar GPG

```bash
echo "test" | gpg --clearsign
```

**Solução 3**: Reiniciar gpg-agent

```bash
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

### Erro: "No secret key"

```bash
# Verificar se a chave existe
gpg --list-secret-keys

# Reconfigurar chave no Git
git config --global user.signingkey SEU_KEY_ID
```

### Erro: Senha GPG não solicitada

**Windows (Git Bash)**:

```bash
# Instalar pinentry
choco install pinentry

# Configurar pinentry
echo "pinentry-program /c/Program Files (x86)/Gpg4win/bin/pinentry.exe" >> ~/.gnupg/gpg-agent.conf

# Reiniciar gpg-agent
gpgconf --kill gpg-agent
```

**macOS**:

```bash
# Instalar pinentry-mac
brew install pinentry-mac

# Configurar
echo "pinentry-program $(which pinentry-mac)" >> ~/.gnupg/gpg-agent.conf

# Reiniciar
gpgconf --kill gpg-agent
```

## 🔐 Backup da Chave GPG

**IMPORTANTE**: Faça backup da sua chave privada em local seguro!

```bash
# Exportar chave privada (MANTENHA SEGURO!)
gpg --export-secret-keys -a 3AA5C34371567BD2 > gpg-private-key-backup.asc

# Exportar chave pública
gpg --export -a 3AA5C34371567BD2 > gpg-public-key-backup.asc

# Exportar ownertrust
gpg --export-ownertrust > gpg-ownertrust-backup.txt
```

### Restaurar Chave de Backup

```bash
# Importar chave privada
gpg --import gpg-private-key-backup.asc

# Importar chave pública
gpg --import gpg-public-key-backup.asc

# Restaurar ownertrust
gpg --import-ownertrust gpg-ownertrust-backup.txt
```

## 📱 Renovar Chave Expirada

```bash
# Listar chaves
gpg --list-keys

# Editar chave
gpg --edit-key 3AA5C34371567BD2

# No prompt gpg>:
gpg> expire
# Escolha nova validade (ex.: 2y)

gpg> save

# Exportar chave atualizada para GitHub
gpg --armor --export 3AA5C34371567BD2
```

## 🎯 Boas Práticas

1. ✅ **Use senha forte** na chave GPG
2. ✅ **Faça backup** da chave privada em local seguro
3. ✅ **Renove a chave** antes de expirar
4. ✅ **Use o mesmo email** do GitHub
5. ✅ **Configure assinatura automática** (commit.gpgsign=true)
6. ✅ **Verifique badges "Verified"** no GitHub após push
7. ✅ **Nunca compartilhe** a chave privada

## 📊 Verificar Status no GitHub

Após configurar:

1. Faça um commit assinado e push
2. Acesse o commit no GitHub
3. Verifique o badge **"Verified"** verde

Exemplo:

```
✓ Verified
Vinícius Uchita committed 2 hours ago
commit abc123...
```

## 🔗 Links Úteis

- [GitHub: GPG Commit Signature Verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [GPG Documentation](https://gnupg.org/documentation/)
- [Git Tools - Signing Your Work](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)

---

**Última Atualização**: Janeiro 2025
**Autor**: Vinícius Uchita
**Projeto**: Python RAG Project
