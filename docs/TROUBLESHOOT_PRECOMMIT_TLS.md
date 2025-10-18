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
