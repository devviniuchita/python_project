#!/usr/bin/env python3
"""
Gerador de Árvore de Arquitetura do Projeto
Gera visualização completa da estrutura de pastas e arquivos
"""

import os

from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple


# Pastas e arquivos a ignorar
IGNORE_DIRS = {
    '.git',
    '__pycache__',
    '.venv',
    'venv',
    'node_modules',
    '.pytest_cache',
    '.egg-info',
    'dist',
    'build',
    '.mypy_cache',
    '.tox',
    'htmlcov',
    '.coverage',
}

IGNORE_FILES = {'.DS_Store', 'Thumbs.db', '*.pyc', '.env'}


def is_ignored(path: Path, is_dir: bool) -> bool:
    """Verifica se um arquivo/pasta deve ser ignorado"""
    name = path.name

    if is_dir and name in IGNORE_DIRS:
        return True

    if not is_dir:
        if name in IGNORE_FILES or name.endswith('.pyc'):
            return True

    return False


def get_file_icon(path: Path) -> str:
    """Retorna um ícone apropriado para o arquivo/pasta"""
    if path.is_dir():
        if path.name.startswith('.'):
            return '⚙️'
        if path.name == 'src':
            return '💻'
        if path.name == 'tests':
            return '🧪'
        if path.name == 'docs':
            return '📚'
        if path.name == 'scripts':
            return '🔧'
        return '📁'

    suffix = path.suffix.lower()
    icons = {
        '.py': '🐍',
        '.md': '📝',
        '.txt': '📄',
        '.yml': '⚙️',
        '.yaml': '⚙️',
        '.json': '🔧',
        '.toml': '🔧',
        '.env': '🔐',
        '.gitignore': '🚫',
        '.cff': '📖',
        '.sh': '🔨',
        '.sql': '🗄️',
    }
    return icons.get(suffix, '📄')


def generate_tree(
    path: Path,
    prefix: str = '',
    is_last: bool = True,
    lines: Optional[List[str]] = None,
) -> List[str]:
    """Gera árvore de diretórios recursivamente"""
    if lines is None:
        lines = []

    try:
        # Obter items (diretórios primeiro, depois arquivos)
        items = sorted(
            [item for item in path.iterdir() if not is_ignored(item, item.is_dir())],
            key=lambda x: (not x.is_dir(), x.name.lower()),
        )

        for index, item in enumerate(items):
            is_last_item = index == len(items) - 1

            # Símbolos da árvore
            current = '└── ' if is_last_item else '├── '
            extension = '    ' if is_last_item else '│   '

            # Montar a linha
            icon = get_file_icon(item)
            line = f'{prefix}{current}{icon} {item.name}'

            # Adicionar tamanho se for arquivo
            if item.is_file():
                size = item.stat().st_size
                if size < 1024:
                    line += f' ({size}B)'
                elif size < 1024 * 1024:
                    line += f' ({size / 1024:.1f}KB)'
                else:
                    line += f' ({size / (1024 * 1024):.1f}MB)'

            lines.append(line)

            # Recursão se for diretório
            if item.is_dir():
                generate_tree(item, prefix + extension, is_last_item, lines)

        return lines

    except PermissionError:
        return lines


def generate_markdown(root_path: Path) -> str:
    """Gera arquivo Markdown com a árvore"""
    lines = ['# 📁 Project Structure\n']
    lines.append('```')

    # Gerar árvore
    tree_lines = generate_tree(root_path)
    lines.extend(tree_lines)

    lines.append('```\n')

    # Adicionar legenda
    lines.append('## 📋 Legenda\n')
    lines.append('- 💻 `src/` - Código-fonte principal')
    lines.append('- 🧪 `tests/` - Testes unitários e de integração')
    lines.append('- 📚 `docs/` - Documentação')
    lines.append('- 🔧 `scripts/` - Scripts utilitários')
    lines.append('- ⚙️ `.github/` - Configurações GitHub (workflows, etc)')
    lines.append('- 🔐 Arquivos com 🔐 contêm configurações sensíveis')
    lines.append('- 📝 `*.md` - Arquivos Markdown')
    lines.append('- 🐍 `*.py` - Arquivos Python')

    return '\n'.join(lines)


def main():
    """Função principal"""
    project_root = Path.cwd()

    print('🌳 Gerando árvore do projeto...')
    print(f'📍 Raiz: {project_root}\n')

    # Gerar Markdown
    markdown_content = generate_markdown(project_root)

    # Salvar arquivo
    output_file = project_root / 'PROJECT_STRUCTURE.md'
    output_file.write_text(markdown_content, encoding='utf-8')

    print(f'✅ Arquivo criado: {output_file}')
    print(f'📊 Total de linhas geradas: {len(markdown_content.splitlines())}')

    # Também printar na tela
    print('\n' + '=' * 60)
    print(markdown_content)
    print('=' * 60)


if __name__ == '__main__':
    main()
