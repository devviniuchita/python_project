# Resolução: Erro TLS/CA durante instalação de hooks do pre-commit

Problema: ao executar `git commit` o pre-commit tenta instalar ambientes para hooks remotos e o pip falha com erro:

```
ERROR: Could not install packages due to an OSError: Could not find a suitable TLS CA certificate bundle, invalid path: C:\Program Files\PostgreSQL\18\ssl\certs\ca-bundle.crt
```

Causa comum:

- Variáveis de ambiente como `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE` ou `PIP_CERT` apontam para um arquivo de certificado inexistente.

Soluções rápidas (temporárias)

1. Fazer commit imediatamente (bypass dos hooks):

   ```bash
   git add -A
   git commit --no-verify -m "<mensagem de commit>"
   ```

   Observação: utilizar `--no-verify` apenas em emergência — hooks são importantes.

2. Rodar o pre-commit manualmente numa sessão onde a variável esteja corrigida:

   ```bash
   # Git Bash / Linux / macOS (sessão temporária)
   unset SSL_CERT_FILE
   unset REQUESTS_CA_BUNDLE
   unset PIP_CERT
   pre-commit run --all-files
   ```

   ```powershell
   # PowerShell (temporário)
   Remove-Item Env:\SSL_CERT_FILE -ErrorAction SilentlyContinue
   Remove-Item Env:\REQUESTS_CA_BUNDLE -ErrorAction SilentlyContinue
   Remove-Item Env:\PIP_CERT -ErrorAction SilentlyContinue
   pre-commit run --all-files
   ```

Soluções permanentes recomendadas

- Identificar onde a variável foi definida (variáveis de sistema, .env do venv, perfil do shell) e corrigir o caminho para o bundle de CA correto.
  - Verificar valor atual:

    ```bash
    echo "$SSL_CERT_FILE"
    echo "$REQUESTS_CA_BUNDLE"
    python -c "import certifi; print(certifi.where())"
    ```

  - Usar o bundle fornecido pelo pacote `certifi` (recomendado):

    ```bash
    # Instale certifi no venv
    pip install certifi

    # Exporte certificado válido (sessão)
    export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")

    # No Windows (PowerShell) para persistir:
    # setx SSL_CERT_FILE "C:\\path\\to\\certifi\\cacert.pem"
    ```

- Alternativa: configurar Git para apontar um CA válido:

  ```bash
  git config --global http.sslCAinfo "C:/path/to/ca-bundle.crt"
  ```

Verificação

- Após ajustar a variável, reexecute:

  ```bash
  pre-commit run --all-files
  pre-commit install
  git commit -m "fix: reinstalar hooks pre-commit after cert fix"
  ```

Notas de segurança

- NÃO coloque certificados privados em repositório.
- Prefira usar `certifi` ou o CA do sistema.

Se quiser, eu tento:

- rodar os hooks localmente numa sessão com `SSL_CERT_FILE` sobrescrito e, se sucessso, reinstalar hooks, ou
- adicionar instruções automatizadas ao script de setup (`scripts/setup-dev-environment.sh`) para garantir que `certifi` está instalado e `SSL_CERT_FILE` definido corretamente.

Automação aplicada (atualização do repositório)

- O script `scripts/setup-dev-environment.sh` agora detecta e limpa variáveis TLS inválidas (por exemplo, caminhos que não existem) antes de executar quaisquer operações do pip. Se o pacote `certifi` estiver disponível no ambiente Python ativado, o script também exporta `SSL_CERT_FILE` e `REQUESTS_CA_BUNDLE` apontando para o bundle do `certifi` para garantir downloads HTTPS seguros.

- O hook local `.githooks/pre-commit` foi atualizado para validar as variáveis TLS no momento do commit: ele tenta localizar o Python do `.venv` e, se `certifi` estiver instalado, define as variáveis para o bundle do `certifi`; caso contrário, ele remove apenas as variáveis que apontam para arquivos inexistentes para evitar falhas de ferramentas (black/isort/flake8) durante o commit.

- Adicionado um executor seguro `scripts/precommit_wrapper.py` que normaliza as variáveis TLS/CA e repassa a execução para o `pre-commit` do ambiente atual.
  - Uso rápido (sessão):

    ```bash
    # Executa pre-commit com normalização TLS usando o python do venv ativado
    python scripts/precommit_wrapper.py run --all-files
    ```

  - O wrapper é cross-platform e assegura que o processo que cria venvs para hooks (p.ex. mirrors-mypy) herde um CA bundle válido (via certifi) ou não utilize variáveis inválidas.

Comandos rápidos para recuperar um ambiente quebrado:

```bash
# Ative o virtualenv do projeto (Git Bash)
source .venv/bin/activate || . .venv/Scripts/activate

# Atualize/instale certifi no venv
python -m pip install --upgrade certifi

# Re-execute o script de setup (irá normalizar variáveis e instalar hooks)
bash scripts/setup-dev-environment.sh

# Reinstale hooks e valide tudo
pre-commit install --install-hooks
pre-commit run --all-files
```
