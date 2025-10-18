<!--
Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita
Watermark: PRAG-2025-VU-v1.0

COPYRIGHT HEADERS GUIDE - Documentation for add_copyright_headers.py script
-->

# COPYRIGHT HEADERS GUIDE

## Overview

O script `scripts/add_copyright_headers.py` é uma ferramenta robusta para adicionar e validar cabeçalhos de copyright em múltiplos tipos de arquivo. Suporta automática detecção de tipo de arquivo, modo de verificação read-only, e integração com REUSE Tool.

## Supported File Types

| Type         | Extension       | Header Style         | Example                                 |
| ------------ | --------------- | -------------------- | --------------------------------------- |
| Python       | `.py`           | Docstring (""")      | Triple quotes at top                    |
| Shell Script | `.sh`           | Comments (#)         | `# SPDX-License-Identifier: MIT`        |
| YAML         | `.yml`, `.yaml` | Comments (#)         | `# SPDX-License-Identifier: MIT`        |
| Markdown     | `.md`           | HTML Comments (<!--) | `<!-- SPDX-License-Identifier: MIT -->` |
| JSON         | `.json`         | `.json.license`      | Separate file (REUSE spec)              |

## Quick Start

### Basic Usage

```bash
# Adicionar headers a todos os arquivos suportados
python scripts/add_copyright_headers.py .

# Apenas verificar conformidade (read-only)
python scripts/add_copyright_headers.py . --verify

# Simular sem modificar
python scripts/add_copyright_headers.py . --dry-run
```

### Common Patterns

```bash
# Processar apenas arquivos Python e Shell
python scripts/add_copyright_headers.py . --file-types .py .sh

# Excluir diretórios específicos
python scripts/add_copyright_headers.py . --exclude tests build dist

# Modo completo: Verify + Dry-run + Exclude + File-types
python scripts/add_copyright_headers.py . \
  --verify \
  --exclude tests build dist .venv venv __pycache__ .git \
  --file-types .py .sh .md

# Com validação REUSE Tool (requer: pip install reuse)
python scripts/add_copyright_headers.py . --reuse-check
```

## Command Line Options

```
positional arguments:
  directory              Diretório para processar (padrão: diretório atual)

optional arguments:
  -h, --help            Mostrar esta mensagem de ajuda
  --dry-run             Simular sem modificar arquivos
  --verify              Apenas verificar conformidade (nunca modifica)
  --file-types TYPES    Extensões a processar (ex: .py .sh .yml .md)
  --exclude PATTERNS    Padrões adicionais para excluir (ex: tests docs)
  --verbose             Modo verboso com mais detalhes
  --reuse-check         Validar com REUSE Tool após processar
```

## Output Format

### Verify Mode Output

```
[*] Processando: C:\project
[MODE] VERIFICAÇÃO (conformidade read-only)

[FAIL] project/app.py - Non-compliant (missing copyright)
[OK] project/main.py - Compliant (has copyright)
[FAIL] docs/README.md - Non-compliant (missing copyright)

[SUMMARY] Resumo:
   Total de arquivos: 3
   Arquivos não-conformes: 2
```

### Modify Mode Output

```
[*] Processando: C:\project
[MODE] MODIFICAÇÃO (aplicando mudanças)

[DONE] project/app.py - Added PYTHON copyright header
[DONE] project/script.sh - Added SHELL copyright header
[SKIP] project/binary.bin - Skipped (no header template for type)

[SUMMARY] Resumo:
   Total de arquivos: 3
   Arquivos modificados: 2
```

### Dry-Run Mode Output

```
[*] Processando: C:\project
[MODE] DRY-RUN (simulando)

[DRY-RUN] project/app.py - Would add PYTHON copyright header
[DRY-RUN] project/script.sh - Would add SHELL copyright header

[SUMMARY] Resumo:
   Total de arquivos: 2
   Arquivos que seriam modificados: 2

[TIP] Execute sem --dry-run para aplicar as mudanças
```

## Examples by File Type

### Python Files

**Input:**

```python
"""
Main application module.
"""

def main():
    pass
```

**Output:**

```python
"""
Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Team

Watermark: PRAG-2025-VU-v1.0

Main application module.
"""

def main():
    pass
```

### Shell Scripts

**Input:**

```bash
#!/bin/bash
# Deployment script

set -e
```

**Output:**

```bash
#!/bin/bash
# Copyright (c) 2025 Python RAG Project Team
# SPDX-License-Identifier: MIT
# Author: Team
#
# Deployment script

set -e
```

### YAML Configuration

**Input:**

```yaml
# Application configuration
version: 1.0

settings:
  debug: true
```

**Output:**

```yaml
# Copyright (c) 2025 Python RAG Project Team
# SPDX-License-Identifier: MIT
# Author: Team
#
# Application configuration
version: 1.0

settings:
  debug: true
```

### Markdown Documents

**Input:**

```markdown
# Project Documentation

This is the main documentation.
```

**Output:**

```markdown
<!--
Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Team

Project Documentation
-->

# Project Documentation

This is the main documentation.
```

## Advanced Features

### Verify Mode

Use `--verify` to check compliance without modifying any files:

```bash
python scripts/add_copyright_headers.py . --verify
```

**Output:**

- `[OK]`: File has copyright header
- `[FAIL]`: File missing copyright header
- `[SKIP]`: File type not supported

**Perfect for CI/CD pipelines** - Exits with count of non-compliant files.

### Dry-Run Mode

Preview changes before applying:

```bash
python scripts/add_copyright_headers.py . --dry-run
```

Shows exactly which files would be modified and what headers would be added.

### File Type Filtering

Process only specific file types:

```bash
# Only Python and Shell files
python scripts/add_copyright_headers.py . --file-types .py .sh

# Only Markdown files
python scripts/add_copyright_headers.py . --file-types .md
```

### Pattern Exclusion

Exclude directories and file patterns:

```bash
python scripts/add_copyright_headers.py . \
  --exclude tests build dist .venv __pycache__ .git .pytest_cache
```

**Common exclusions:**

- `tests` - Test files
- `build dist` - Build artifacts
- `.venv venv` - Virtual environments
- `__pycache__` - Python cache
- `.git .github` - Git files
- `.pytest_cache` - Test cache

### REUSE Tool Integration

Validate copyright compliance with REUSE specification:

```bash
# Install REUSE Tool first
pip install reuse

# Run compliance check
python scripts/add_copyright_headers.py . --reuse-check
```

**Output:**

```
[*] Validando com REUSE Tool...
[OK] REUSE Tool validation: PASSED
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Copyright Compliance

on: [pull_request]

jobs:
  copyright:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Check copyright headers
        run: |
          python scripts/add_copyright_headers.py . --verify
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: copyright-headers
      name: Copyright Headers
      entry: python scripts/add_copyright_headers.py
      language: python
      types: [python, shell, yaml, markdown]
      pass_filenames: false
      always_run: true
      stages: [commit]
```

## Troubleshooting

### Issue: "File encoding issue" warnings

**Solution:** Ensure all source files use UTF-8 encoding.

```bash
# Check file encoding
file -i your_file.py

# Convert to UTF-8 if needed
iconv -f ISO-8859-1 -t UTF-8 your_file.py > your_file_utf8.py
```

### Issue: REUSE Tool not found

**Solution:** Install the REUSE package:

```bash
pip install reuse
```

### Issue: Scripts have inconsistent shebang handling

**Solution:** The script automatically preserves shebangs:

```bash
#!/bin/bash
# Copyright header inserted here (after shebang)
```

### Issue: JSON files not being processed

**Solution:** JSON files require `.json.license` companion files per REUSE spec:

```
myconfig.json        -> Create myconfig.json.license
myconfig.json.license contents:
  Copyright (c) 2025 Team
  SPDX-License-Identifier: MIT
```

## Copyright Header Templates

### PYTHON_HEADER

```python
"""
{docstring}
Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
"""
```

### SHEBANG_HEADER

```bash
#!/bin/bash
# Copyright (c) 2025 Python RAG Project Team
# SPDX-License-Identifier: MIT
# Author: Vinícius Uchita
```

### SHELL_HEADER

```bash
# Copyright (c) 2025 Python RAG Project Team
# SPDX-License-Identifier: MIT
# Author: Vinícius Uchita
```

### YAML_HEADER

```yaml
# Copyright (c) 2025 Python RAG Project Team
# SPDX-License-Identifier: MIT
# Author: Vinícius Uchita
```

### MARKDOWN_HEADER

```markdown
<!--
Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita
-->
```

### JSON_LICENSE_HEADER

```
Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita
```

## Performance Notes

- **Execution Time:** ~100-500ms for typical projects
- **Memory Usage:** Minimal (processes files sequentially)
- **Safe:** No files modified in verify or dry-run modes
- **Idempotent:** Safe to run multiple times

## Related Tasks

- **T-31.1:** Code Review ✅
- **T-31.2:** Multi-Extension Support ✅
- **T-31.3:** --verify Mode ✅
- **T-31.4:** REUSE Tool Integration ✅
- **T-31.5:** Unit Tests ✅
- **T-31.6:** Documentation ✅
- **T-33:** Pre-commit Framework Integration (depends on T-31)

## License

Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT

## See Also

- [REUSE Specification](https://reuse.software/)
- [SPDX License List](https://spdx.org/licenses/)
- [Pre-commit Framework](https://pre-commit.com/)
