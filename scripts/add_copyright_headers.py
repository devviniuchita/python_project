#!/usr/bin/env python3
"""
Script para adicionar cabeçalhos de copyright em arquivos de múltiplos tipos.

Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d

SUPORTADO:
- Python (.py): Docstring triple-quotes
- Shell (.sh): # comentários
- YAML (.yml, .yaml): # comentários
- Markdown (.md): <!-- comments -->
- JSON: .json.license file ou skip
"""

import enum
import json
import os
import subprocess
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


class FileType(enum.Enum):
    """Tipos de arquivo suportados."""

    PYTHON = "python"
    SHELL = "shell"
    YAML = "yaml"
    MARKDOWN = "markdown"
    JSON = "json"
    UNKNOWN = "unknown"


@dataclass
class HeaderTemplates:
    """Templates de copyright para cada tipo de arquivo."""

    # Python
    PYTHON_HEADER = '''"""
{docstring}

Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

This file is part of Python RAG Project.
See LICENSE file for full license details.

Project Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
"""
'''

    PYTHON_SHEBANG_HEADER = '''#!/usr/bin/env python3
"""
{docstring}

Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

This file is part of Python RAG Project.
See LICENSE file for full license details.

Project Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
"""
'''

    # Shell
    SHELL_HEADER = '''#!/bin/bash
# {docstring}
#
# Copyright (c) 2025 Python RAG Project Team
# SPDX-License-Identifier: MIT
# Author: Vinícius Uchita <viniciusuchita@gmail.com>
#
# This file is part of Python RAG Project.
# See LICENSE file for full license details.
#
# Project Watermark: PRAG-2025-VU-v1.0
# Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
'''

    SHELL_NOSHEBANG_HEADER = '''# {docstring}
#
# Copyright (c) 2025 Python RAG Project Team
# SPDX-License-Identifier: MIT
# Author: Vinícius Uchita <viniciusuchita@gmail.com>
#
# This file is part of Python RAG Project.
# See LICENSE file for full license details.
#
# Project Watermark: PRAG-2025-VU-v1.0
# Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
'''

    # YAML
    YAML_HEADER = '''# {docstring}
#
# Copyright (c) 2025 Python RAG Project Team
# SPDX-License-Identifier: MIT
# Author: Vinícius Uchita <viniciusuchita@gmail.com>
#
# This file is part of Python RAG Project.
# See LICENSE file for full license details.
#
# Project Watermark: PRAG-2025-VU-v1.0
# Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
'''

    # Markdown
    MARKDOWN_HEADER = '''<!-- {docstring}

Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

This file is part of Python RAG Project.
See LICENSE file for full license details.

Project Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
-->
'''

    # JSON
    JSON_LICENSE_HEADER = '''{
  "copyright": "Copyright (c) 2025 Python RAG Project Team",
  "license": "MIT",
  "spdx": "SPDX-License-Identifier: MIT",
  "author": "Vinícius Uchita <viniciusuchita@gmail.com>",
  "project": "Python RAG Project",
  "watermark": "PRAG-2025-VU-v1.0",
  "signature": "8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d",
  "note": "{docstring}"
}
'''


# Copyright header template - DEPRECATED (mantido para compatibilidade)
COPYRIGHT_HEADER = HeaderTemplates.PYTHON_HEADER
SHEBANG_HEADER = HeaderTemplates.PYTHON_SHEBANG_HEADER


def detect_file_type(file_path: Path) -> FileType:
    """Detecta o tipo de arquivo baseado na extensão."""
    suffix = file_path.suffix.lower()

    if suffix == ".py":
        return FileType.PYTHON
    elif suffix == ".sh":
        return FileType.SHELL
    elif suffix in [".yml", ".yaml"]:
        return FileType.YAML
    elif suffix == ".md":
        return FileType.MARKDOWN
    elif suffix == ".json":
        return FileType.JSON
    else:
        return FileType.UNKNOWN


def has_copyright(content: str) -> bool:
    """Verifica se o arquivo já tem cabeçalho de copyright."""
    return "Copyright (c)" in content or "SPDX-License-Identifier" in content


def has_shebang(content: str) -> bool:
    """Verifica se o arquivo tem shebang."""
    return content.startswith("#!")


def extract_docstring_from_content(content: str, file_type: FileType) -> str:
    """Extrai docstring existente do arquivo conforme tipo."""
    lines = content.strip().split('\n')

    if not lines:
        return f"{file_type.value} file"

    if file_type == FileType.PYTHON:
        return _extract_python_docstring(lines)
    elif file_type == FileType.SHELL:
        return _extract_shell_docstring(lines)
    elif file_type == FileType.YAML:
        return _extract_yaml_description(lines)
    elif file_type == FileType.MARKDOWN:
        return _extract_markdown_title(lines)
    else:
        return f"{file_type.value} file"


def _extract_python_docstring(lines: List[str]) -> str:
    """Extrai docstring de arquivo Python."""
    # Skip shebang if present
    start_idx = 1 if lines and lines[0].startswith("#!") else 0

    # Skip encoding declaration
    if start_idx < len(lines) and lines[start_idx].startswith("# -*- coding:"):
        start_idx += 1

    # Check for docstring
    if start_idx < len(lines):
        line = lines[start_idx].strip()
        if line.startswith('"""') or line.startswith("'''"):
            quote = '"""' if line.startswith('"""') else "'''"

            # One-liner
            if line.endswith(quote) and len(line) > 6:
                return line[3:-3].strip()

            # Multi-line docstring
            docstring_lines = []
            for i in range(start_idx + 1, len(lines)):
                if quote in lines[i]:
                    return '\n'.join(docstring_lines).strip()
                docstring_lines.append(lines[i])

    return "Python module"


def _extract_shell_docstring(lines: List[str]) -> str:
    """Extrai descrição de script Shell."""
    start_idx = 1 if lines and lines[0].startswith("#!") else 0
    docstring_lines = []

    for i in range(start_idx, min(start_idx + 5, len(lines))):
        line = lines[i].strip()
        if line.startswith("#"):
            docstring_lines.append(line[1:].strip())
        elif line:
            break

    return ' '.join(docstring_lines) if docstring_lines else "Shell script"


def _extract_yaml_description(lines: List[str]) -> str:
    """Extrai descrição de arquivo YAML."""
    for line in lines[:5]:
        if "description:" in line.lower():
            return line.split(":", 1)[1].strip()
        elif line.startswith("#"):
            return line[1:].strip()
    return "YAML configuration file"


def _extract_markdown_title(lines: List[str]) -> str:
    """Extrai título de arquivo Markdown."""
    for line in lines[:5]:
        if line.startswith("# "):
            return line[2:].strip()
        elif line.startswith("---"):
            continue
    return "Markdown documentation"


def extract_existing_docstring(content: str) -> str:
    """Extrai docstring existente (wrapper compatibilidade)."""
    return extract_docstring_from_content(content, FileType.PYTHON)


def add_copyright_header(
    file_path: Path, dry_run: bool = False, verify_mode: bool = False
) -> bool:
    """
    Adiciona cabeçalho de copyright a um arquivo.

    Args:
        file_path: Caminho do arquivo
        dry_run: Se True, apenas simula (não modifica arquivo)
        verify_mode: Se True, apenas verifica conformidade (nunca modifica)

    Returns:
        True se o arquivo foi modificado/está OK, False caso contrário
    """
    file_type = detect_file_type(file_path)

    if file_type == FileType.UNKNOWN:
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"[SKIP] {file_path} (encoding issue)")
        return False

    # Skip if already has copyright
    if has_copyright(content):
        if verify_mode:
            print(f"[OK] {file_path} - Compliant (has copyright)")
        return False

    # Extract appropriate docstring
    docstring = extract_docstring_from_content(content, file_type)

    # Determine header based on file type
    header = _get_header_for_type(file_type, content, docstring)

    if header is None:
        print(f"[SKIP] {file_path} - Skipped (no header template for type)")
        return False

    # Remove old headers
    new_content = _remove_old_header(content, file_type)

    # Construct final content
    final_content = header + '\n' + new_content.lstrip('\n')

    # In verify mode, just report non-compliance
    if verify_mode:
        print(f"[FAIL] {file_path} - Non-compliant (missing copyright)")
        return True

    if dry_run:
        print(f"[DRY-RUN] {file_path} - Would add {file_type.value} copyright header")
        return True

    # Write new content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"[DONE] {file_path} - Added {file_type.value} copyright header")
    return True


def _get_header_for_type(
    file_type: FileType, content: str, docstring: str
) -> Optional[str]:
    """Retorna o template de header apropriado para o tipo de arquivo."""
    if file_type == FileType.PYTHON:
        has_shebang_line = has_shebang(content)
        template = (
            HeaderTemplates.PYTHON_SHEBANG_HEADER
            if has_shebang_line
            else HeaderTemplates.PYTHON_HEADER
        )
        return template.format(docstring=docstring)

    elif file_type == FileType.SHELL:
        has_shebang_line = has_shebang(content)
        template = (
            HeaderTemplates.SHELL_HEADER
            if has_shebang_line
            else HeaderTemplates.SHELL_NOSHEBANG_HEADER
        )
        return template.format(docstring=docstring)

    elif file_type == FileType.YAML:
        return HeaderTemplates.YAML_HEADER.format(docstring=docstring)

    elif file_type == FileType.MARKDOWN:
        return HeaderTemplates.MARKDOWN_HEADER.format(docstring=docstring)

    elif file_type == FileType.JSON:
        return HeaderTemplates.JSON_LICENSE_HEADER.format(docstring=docstring)

    else:
        return None


def _remove_old_header(content: str, file_type: FileType) -> str:
    """Remove cabeçalho copyright antigo."""
    lines = content.split('\n')

    if file_type == FileType.PYTHON:
        return _remove_python_header(lines)
    elif file_type == FileType.SHELL:
        return _remove_shell_header(lines)
    elif file_type in [FileType.YAML, FileType.MARKDOWN]:
        return _remove_comment_header(
            lines, "#" if file_type == FileType.YAML else "<!--"
        )
    elif file_type == FileType.JSON:
        return content  # JSON pode ter .json.license separado
    else:
        return content


def _remove_python_header(lines: List[str]) -> str:
    """Remove cabeçalho Python (docstring + comments)."""
    start_idx = 0

    # Skip shebang
    if lines and lines[0].startswith("#!"):
        start_idx = 1

    # Skip encoding
    if start_idx < len(lines) and lines[start_idx].startswith("# -*- coding:"):
        start_idx += 1

    # Skip docstring
    if start_idx < len(lines):
        line = lines[start_idx].strip()
        if line.startswith('"""') or line.startswith("'''"):
            quote = '"""' if line.startswith('"""') else "'''"

            if line.endswith(quote) and len(line) > 6:
                start_idx += 1
            else:
                for i in range(start_idx + 1, len(lines)):
                    if quote in lines[i]:
                        start_idx = i + 1
                        break

    # Skip blank lines
    while start_idx < len(lines) and not lines[start_idx].strip():
        start_idx += 1

    return '\n'.join(lines[start_idx:])


def _remove_shell_header(lines: List[str]) -> str:
    """Remove cabeçalho Shell (#-comentários)."""
    start_idx = 0

    # Skip shebang
    if lines and lines[0].startswith("#!"):
        start_idx = 1

    # Skip copyright comments
    while start_idx < len(lines):
        line = lines[start_idx].strip()
        if line.startswith("#") and (
            "Copyright" in line or "SPDX" in line or "Watermark" in line
        ):
            start_idx += 1
        elif line.startswith("#") and line.strip() == "#":
            start_idx += 1
        elif line and not line.startswith("#"):
            break
        else:
            start_idx += 1

    return '\n'.join(lines[start_idx:])


def _remove_comment_header(lines: List[str], comment_char: str) -> str:
    """Remove cabeçalho genérico com comments."""
    start_idx = 0

    while start_idx < len(lines):
        line = lines[start_idx].strip()
        if (comment_char == "#" and line.startswith("#")) or (
            comment_char == "<!--" and "<!--" in line
        ):
            start_idx += 1
        elif not line:
            start_idx += 1
        else:
            break

    return '\n'.join(lines[start_idx:])


def process_directory(
    directory: Path,
    exclude_patterns: Optional[List[str]] = None,
    dry_run: bool = False,
    verify_mode: bool = False,
    file_types: Optional[List[str]] = None,
) -> Tuple[int, int]:
    """
    Processa arquivos em um diretório com suporte a múltiplos tipos.

    Args:
        directory: Diretório raiz
        exclude_patterns: Padrões de arquivos/diretórios para excluir
        dry_run: Se True, apenas simula
        verify_mode: Se True, apenas verifica conformidade
        file_types: Lista de extensões a processar (ex: ['.py', '.sh', '.yml'])

    Returns:
        Tupla (total de arquivos, arquivos modificados)
    """
    if exclude_patterns is None:
        exclude_patterns = [
            '__pycache__',
            '.git',
            '.venv',
            'venv',
            'env',
            '.pytest_cache',
            '.mypy_cache',
            'htmlcov',
            'dist',
            'build',
            '*.egg-info',
        ]

    # Padrões de arquivo padrão
    if file_types is None:
        file_types = ['.py', '.sh', '.yml', '.yaml', '.md']

    total = 0
    modified = 0

    for file_path in directory.rglob('*'):
        # Skip directories
        if file_path.is_dir():
            continue

        # Check if file extension matches
        if file_path.suffix.lower() not in file_types:
            continue

        # Check exclusions
        should_exclude = False
        for pattern in exclude_patterns:
            if pattern in str(file_path):
                should_exclude = True
                break

        if should_exclude:
            continue

        total += 1
        if add_copyright_header(file_path, dry_run=dry_run, verify_mode=verify_mode):
            modified += 1

    return total, modified


def validate_with_reuse_tool(directory: Path) -> Tuple[bool, str]:
    """
    Valida a conformidade com REUSE Tool.

    Returns:
        Tuple[bool, str]: (sucesso, mensagem)
    """
    try:
        result = subprocess.run(
            ["reuse", "lint"],
            cwd=str(directory),
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return True, "REUSE Tool validation: PASSED"
        else:
            return False, f"REUSE Tool validation: FAILED\n{result.stdout}"

    except FileNotFoundError:
        return False, "REUSE Tool not found. Install with: pip install reuse"
    except subprocess.TimeoutExpired:
        return False, "REUSE Tool validation timed out"
    except Exception as e:
        return False, f"REUSE Tool error: {str(e)}"


def main():
    """Função principal com CLI melhorada."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Adicionar/verificar cabeçalhos de copyright em arquivos (suporta .py, .sh, .yml, .md)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:
  %(prog)s .                                    # Adiciona headers em todos os arquivos
  %(prog)s . --dry-run                          # Simula sem modificar
  %(prog)s . --verify                           # Apenas verifica conformidade
  %(prog)s . --file-types .py .sh .yml          # Apenas estes tipos
  %(prog)s . --exclude tests docs --dry-run     # Exclui diretórios
        ''',
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Diretório para processar (padrão: diretório atual)',
    )
    parser.add_argument(
        '--dry-run', action='store_true', help='Simular sem modificar arquivos'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Apenas verificar conformidade (nunca modifica)',
    )
    parser.add_argument(
        '--file-types',
        nargs='+',
        default=None,
        help='Extensões a processar (ex: .py .sh .yml .md) - padrão: .py .sh .yml .yaml .md',
    )
    parser.add_argument(
        '--exclude', nargs='+', help='Padrões adicionais para excluir (ex: tests docs)'
    )
    parser.add_argument(
        '--verbose', action='store_true', help='Modo verboso com mais detalhes'
    )
    parser.add_argument(
        '--reuse-check',
        action='store_true',
        help='Validar com REUSE Tool após processar (requer: pip install reuse)',
    )

    args = parser.parse_args()

    directory = Path(args.directory).resolve()

    if not directory.exists():
        print(f"[ERROR] Diretório não encontrado: {directory}")
        sys.exit(1)

    print(f"[*] Processando: {directory}")
    if args.verify:
        print(f"[MODE] VERIFICAÇÃO (conformidade read-only)")
    elif args.dry_run:
        print(f"[MODE] DRY-RUN (simulando)")
    else:
        print(f"[MODE] MODIFICAÇÃO (aplicando mudanças)")
    print()

    exclude = args.exclude if args.exclude else None
    file_types = args.file_types if args.file_types else None

    # Adicionar ponto às extensões se não tiver
    if file_types:
        file_types = [f".{ft}" if not ft.startswith(".") else ft for ft in file_types]

    total, modified = process_directory(
        directory,
        exclude_patterns=exclude,
        dry_run=args.dry_run,
        verify_mode=args.verify,
        file_types=file_types,
    )

    print()
    print(f"[SUMMARY] Resumo:")
    print(f"   Total de arquivos: {total}")
    if args.verify:
        print(f"   Arquivos não-conformes: {modified}")
    elif args.dry_run:
        print(
            f"   Arquivos que {' seriam ' if total > 0 else ''}modificados: {modified}"
        )
    else:
        print(f"   Arquivos modificados: {modified}")

    if args.dry_run and modified > 0:
        print()
        print("[TIP] Execute sem --dry-run para aplicar as mudanças")

    if args.verify and modified > 0:
        print()
        print(
            "[TIP] Execute sem --verify para adicionar headers aos arquivos não-conformes"
        )

    # Executar REUSE check se solicitado
    if args.reuse_check and not args.verify:
        print()
        print("[*] Validando com REUSE Tool...")
        success, message = validate_with_reuse_tool(directory)
        if success:
            print(f"[OK] {message}")
        else:
            print(f"[FAIL] {message}")


if __name__ == '__main__':
    main()
