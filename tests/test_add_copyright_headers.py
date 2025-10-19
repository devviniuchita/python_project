"""
Tests for copyright headers script.

Copyright (c) 2025 Python RAG Project Team
SPDX-License-Identifier: MIT
Author: Vinícius Uchita <viniciusuchita@gmail.com>

Project Watermark: PRAG-2025-VU-v1.0
Digital Signature: 8f3c9d2e1a4b7f6c5e9d8a3b2c1f4e7d
"""

import sys
import tempfile

from pathlib import Path

import pytest


# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from add_copyright_headers import FileType
from add_copyright_headers import add_copyright_header
from add_copyright_headers import detect_file_type
from add_copyright_headers import extract_docstring_from_content
from add_copyright_headers import has_copyright
from add_copyright_headers import has_shebang
from add_copyright_headers import process_directory


class TestFileTypeDetection:
    """Testes para detecção de tipo de arquivo."""

    def test_detect_python_file(self):
        """Detecta arquivos Python."""
        assert detect_file_type(Path("test.py")) == FileType.PYTHON

    def test_detect_shell_file(self):
        """Detecta scripts Shell."""
        assert detect_file_type(Path("test.sh")) == FileType.SHELL

    def test_detect_yaml_file(self):
        """Detecta arquivos YAML."""
        assert detect_file_type(Path("config.yml")) == FileType.YAML
        assert detect_file_type(Path("config.yaml")) == FileType.YAML

    def test_detect_markdown_file(self):
        """Detecta arquivos Markdown."""
        assert detect_file_type(Path("README.md")) == FileType.MARKDOWN

    def test_detect_json_file(self):
        """Detecta arquivos JSON."""
        assert detect_file_type(Path("config.json")) == FileType.JSON

    def test_detect_unknown_file(self):
        """Detecta arquivo desconhecido."""
        assert detect_file_type(Path("file.unknown")) == FileType.UNKNOWN


class TestCopyrightDetection:
    """Testes para detecção de copyright existente."""

    def test_has_copyright_with_copyright_marker(self):
        """Detecta copyright existente."""
        content = "Copyright (c) 2025 Test"
        assert has_copyright(content)

    def test_has_copyright_with_spdx(self):
        """Detecta SPDX-License-Identifier."""
        content = "SPDX-License-Identifier: MIT"
        assert has_copyright(content)

    def test_no_copyright(self):
        """Detecta falta de copyright."""
        content = 'print("Hello World")'
        assert not has_copyright(content)


class TestShebangDetection:
    """Testes para detecção de shebang."""

    def test_has_python_shebang(self):
        """Detecta shebang Python."""
        content = '#!/usr/bin/env python3\nprint("test")'
        assert has_shebang(content)

    def test_has_bash_shebang(self):
        """Detecta shebang Bash."""
        content = '#!/bin/bash\necho "test"'
        assert has_shebang(content)

    def test_no_shebang(self):
        """Detecta falta de shebang."""
        content = 'print("test")'
        assert not has_shebang(content)


class TestDocstringExtraction:
    """Testes para extração de docstrings."""

    def test_extract_python_docstring_triple_quote(self):
        """Extrai docstring Python com triple quotes."""
        content = '''"""
        Test module description.
        With multiple lines.
        """
        print("code")'''
        result = extract_docstring_from_content(content, FileType.PYTHON)
        assert "Test module description" in result

    def test_extract_python_docstring_single_line(self):
        """Extrai docstring Python de uma linha."""
        content = '"""Test module."""\nprint("code")'
        result = extract_docstring_from_content(content, FileType.PYTHON)
        assert "Test module" in result

    def test_extract_shell_docstring(self):
        """Extrai descrição de script Shell."""
        content = '''#!/bin/bash
        # My script description
        echo "test"'''
        result = extract_docstring_from_content(content, FileType.SHELL)
        assert len(result) > 0

    def test_extract_yaml_description(self):
        """Extrai descrição de YAML."""
        content = "description: Test configuration\nkey: value"
        result = extract_docstring_from_content(content, FileType.YAML)
        assert len(result) > 0

    def test_extract_markdown_title(self):
        """Extrai título de Markdown."""
        content = "# Test Documentation\n\nContent here"
        result = extract_docstring_from_content(content, FileType.MARKDOWN)
        assert "Test Documentation" in result


class TestAddCopyrightHeader:
    """Testes para adição de headers."""

    def test_add_copyright_to_python_file(self):
        """Adiciona copyright em arquivo Python."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write('"""Test module."""\nprint("hello")')
            f.flush()
            temp_path = Path(f.name)

        try:
            result = add_copyright_header(temp_path, dry_run=False)
            assert result

            # Verify copyright was added
            with open(temp_path, "r") as f:
                content = f.read()
            assert "Copyright (c) 2025" in content
            assert "SPDX-License-Identifier: MIT" in content
        finally:
            temp_path.unlink()

    def test_add_copyright_shell_script(self):
        """Adiciona copyright em script Shell."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".sh", delete=False, encoding="utf-8"
        ) as f:
            f.write('#!/bin/bash\necho "test"')
            f.flush()
            temp_path = Path(f.name)

        try:
            result = add_copyright_header(temp_path, dry_run=False)
            assert result

            with open(temp_path, "r") as f:
                content = f.read()
            assert "Copyright (c) 2025" in content
            assert content.startswith("#!/bin/bash")
        finally:
            temp_path.unlink()

    def test_add_copyright_yaml_file(self):
        """Adiciona copyright em arquivo YAML."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False, encoding="utf-8"
        ) as f:
            f.write("name: test\nversion: 1.0")
            f.flush()
            temp_path = Path(f.name)

        try:
            result = add_copyright_header(temp_path, dry_run=False)
            assert result

            with open(temp_path, "r") as f:
                content = f.read()
            assert "Copyright (c) 2025" in content
            assert "# SPDX-License-Identifier: MIT" in content
        finally:
            temp_path.unlink()

    def test_skip_file_with_existing_copyright(self):
        """Pula arquivo que já tem copyright."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write('"""Module."""\n# Copyright (c) 2025\nprint("test")')
            f.flush()
            temp_path = Path(f.name)

        try:
            result = add_copyright_header(temp_path, dry_run=False)
            assert not result  # Should return False (already has copyright)
        finally:
            temp_path.unlink()

    def test_verify_mode_no_modification(self):
        """Modo verify não modifica arquivo."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write('print("test")')
            f.flush()
            temp_path = Path(f.name)

        try:
            original_content = temp_path.read_text()
            result = add_copyright_header(temp_path, verify_mode=True)
            final_content = temp_path.read_text()

            # Verify mode reports non-compliance but doesn't modify
            assert result
            assert original_content == final_content
        finally:
            temp_path.unlink()

    def test_dry_run_no_modification(self):
        """Modo dry-run não modifica arquivo."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write('print("test")')
            f.flush()
            temp_path = Path(f.name)

        try:
            original_content = temp_path.read_text()
            result = add_copyright_header(temp_path, dry_run=True)
            final_content = temp_path.read_text()

            assert result
            assert original_content == final_content
        finally:
            temp_path.unlink()


class TestProcessDirectory:
    """Testes para processamento de diretórios."""

    def test_process_directory_multiple_types(self):
        """Processa múltiplos tipos de arquivo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test files
            (tmppath / "test.py").write_text('print("test")')
            (tmppath / "script.sh").write_text('#!/bin/bash\necho "test"')
            (tmppath / "config.yml").write_text("name: test")

            total, modified = process_directory(tmppath, dry_run=False)

            assert total == 3
            assert modified == 3

            # Verify all have copyright
            assert "Copyright" in (tmppath / "test.py").read_text()
            assert "Copyright" in (tmppath / "script.sh").read_text()
            assert "Copyright" in (tmppath / "config.yml").read_text()

    def test_respect_exclude_patterns(self):
        """Respeita padrões de exclusão."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test files
            (tmppath / "test.py").write_text('print("test")')
            venv_dir = tmppath / "venv"
            venv_dir.mkdir()
            (venv_dir / "module.py").write_text('print("test")')

            total, modified = process_directory(
                tmppath, exclude_patterns=["venv"], dry_run=False
            )

            assert total == 1  # Only main test.py, not venv/module.py
            assert modified == 1

    def test_filter_by_file_types(self):
        """Filtra por tipos de arquivo específicos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test files
            (tmppath / "test.py").write_text('print("test")')
            (tmppath / "script.sh").write_text('echo "test"')
            (tmppath / "config.yml").write_text("name: test")

            # Process only .py files
            total, modified = process_directory(
                tmppath, file_types=[".py"], dry_run=False
            )

            assert total == 1  # Only .py file
            assert modified == 1


class TestIntegration:
    """Testes de integração completa."""

    def test_end_to_end_workflow(self):
        """Testa fluxo completo: criação → verify → modify."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create files without copyright
            (tmppath / "app.py").write_text('"""Main app."""\nprint("run")')
            (tmppath / "run.sh").write_text('#!/bin/bash\necho "run"')

            # Step 1: Verify mode should report non-compliance
            total, non_compliant = process_directory(
                tmppath, verify_mode=True, dry_run=False
            )
            assert total == 2
            assert non_compliant == 2

            # Step 2: Add copyright
            total, modified = process_directory(tmppath, dry_run=False)
            assert total == 2
            assert modified == 2

            # Step 3: Verify again - should pass
            total, non_compliant = process_directory(
                tmppath, verify_mode=True, dry_run=False
            )
            assert total == 2
            assert non_compliant == 0  # All compliant now


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
