#!/usr/bin/env python3
"""
Script para adicionar cabeçalhos de copyright em arquivos Python.

Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
"""

import os
import sys

from pathlib import Path
from typing import List


# Copyright header template
COPYRIGHT_HEADER = '''"""
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

SHEBANG_HEADER = '''#!/usr/bin/env python3
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


def has_copyright(content: str) -> bool:
    """Verifica se o arquivo já tem cabeçalho de copyright."""
    return "Copyright (c)" in content or "SPDX-License-Identifier" in content


def has_shebang(content: str) -> bool:
    """Verifica se o arquivo tem shebang."""
    return content.startswith("#!")


def extract_existing_docstring(content: str) -> str:
    """Extrai docstring existente do arquivo."""
    lines = content.strip().split('\n')

    # Skip shebang if present
    start_idx = 1 if lines and lines[0].startswith("#!") else 0

    # Skip encoding declaration
    if start_idx < len(lines) and lines[start_idx].startswith("# -*- coding:"):
        start_idx += 1

    # Check for docstring
    if start_idx < len(lines):
        line = lines[start_idx].strip()
        if line.startswith('"""') or line.startswith("'''"):
            # Multi-line docstring
            quote = '"""' if line.startswith('"""') else "'''"
            docstring_lines = []

            # Check if it's a one-liner
            if line.endswith(quote) and len(line) > 6:
                return line[3:-3].strip()

            # Multi-line docstring
            for i in range(start_idx + 1, len(lines)):
                if quote in lines[i]:
                    return '\n'.join(docstring_lines).strip()
                docstring_lines.append(lines[i])

    return "Module docstring."


def add_copyright_header(file_path: Path, dry_run: bool = False) -> bool:
    """
    Adiciona cabeçalho de copyright a um arquivo Python.

    Args:
        file_path: Caminho do arquivo
        dry_run: Se True, apenas simula (não modifica arquivo)

    Returns:
        True se o arquivo foi modificado, False caso contrário
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"⚠️  Skipping {file_path} (encoding issue)")
        return False

    # Skip if already has copyright
    if has_copyright(content):
        print(f"✅ {file_path} - Already has copyright header")
        return False

    # Extract existing docstring
    docstring = extract_existing_docstring(content)

    # Determine header type
    needs_shebang = has_shebang(content)
    header = SHEBANG_HEADER if needs_shebang else COPYRIGHT_HEADER
    header = header.format(docstring=docstring)

    # Remove old shebang and docstring if present
    lines = content.split('\n')
    start_idx = 0

    # Skip shebang
    if lines and lines[0].startswith("#!"):
        start_idx = 1

    # Skip encoding
    if start_idx < len(lines) and lines[start_idx].startswith("# -*- coding:"):
        start_idx += 1

    # Skip old docstring
    if start_idx < len(lines):
        line = lines[start_idx].strip()
        if line.startswith('"""') or line.startswith("'''"):
            quote = '"""' if line.startswith('"""') else "'''"

            # One-liner
            if line.endswith(quote) and len(line) > 6:
                start_idx += 1
            else:
                # Multi-line
                for i in range(start_idx + 1, len(lines)):
                    if quote in lines[i]:
                        start_idx = i + 1
                        break

    # Skip blank lines after docstring
    while start_idx < len(lines) and not lines[start_idx].strip():
        start_idx += 1

    # Reconstruct content
    new_content = header + '\n'.join(lines[start_idx:])

    if dry_run:
        print(f"🔄 {file_path} - Would add copyright header")
        return True

    # Write new content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ {file_path} - Added copyright header")
    return True


def process_directory(
    directory: Path, exclude_patterns: List[str] = None, dry_run: bool = False
) -> tuple[int, int]:
    """
    Processa todos os arquivos Python em um diretório.

    Args:
        directory: Diretório raiz
        exclude_patterns: Padrões de arquivos/diretórios para excluir
        dry_run: Se True, apenas simula

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

    total = 0
    modified = 0

    for py_file in directory.rglob('*.py'):
        # Check exclusions
        should_exclude = False
        for pattern in exclude_patterns:
            if pattern in str(py_file):
                should_exclude = True
                break

        if should_exclude:
            continue

        total += 1
        if add_copyright_header(py_file, dry_run=dry_run):
            modified += 1

    return total, modified


def main():
    """Função principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Adicionar cabeçalhos de copyright em arquivos Python'
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
    parser.add_argument('--exclude', nargs='+', help='Padrões adicionais para excluir')

    args = parser.parse_args()

    directory = Path(args.directory).resolve()

    if not directory.exists():
        print(f"❌ Diretório não encontrado: {directory}")
        sys.exit(1)

    print(f"🔍 Processando: {directory}")
    print(f"{'🔄 DRY RUN MODE' if args.dry_run else '✍️  MODIFICANDO ARQUIVOS'}")
    print()

    exclude = args.exclude if args.exclude else None
    total, modified = process_directory(
        directory, exclude_patterns=exclude, dry_run=args.dry_run
    )

    print()
    print(f"📊 Resumo:")
    print(f"   Total de arquivos: {total}")
    print(f"   Arquivos {'que seriam ' if args.dry_run else ''}modificados: {modified}")

    if args.dry_run and modified > 0:
        print()
        print("💡 Execute sem --dry-run para aplicar as mudanças")


if __name__ == '__main__':
    main()
