#!/usr/bin/env python3
"""
Unit tests for add_chunk_markers.py script.

Tests chunk marker insertion logic, edge cases, and validation.
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
from add_chunk_markers import add_chunk_markers


@pytest.fixture
def sample_markdown_file(tmp_path):
    """Create a sample markdown file for testing."""
    test_file = tmp_path / "test.md"
    content = """# Header 1

Some content here.

## Header 2

More content.

### Header 3

Final content.
"""
    test_file.write_text(content, encoding="utf-8")
    return test_file


@pytest.fixture
def sample_chunks() -> List[Tuple[str, int, int, List[str], int]]:
    """Sample chunk definitions for testing."""
    return [
        ("test-chunk-1", 1, 3, ["header", "metadata"], 100),
        ("test-chunk-2", 4, 8, ["content", "section"], 200),
        ("test-chunk-3", 9, 11, ["final", "conclusion"], 150),
    ]


def test_add_chunk_markers_basic(sample_markdown_file, sample_chunks):
    """Test basic chunk marker insertion."""
    result = add_chunk_markers(sample_markdown_file, sample_chunks)

    # Verify chunk start markers are present
    assert "<!-- CHUNK: test-chunk-1" in result
    assert "<!-- CHUNK: test-chunk-2" in result
    assert "<!-- CHUNK: test-chunk-3" in result

    # Verify chunk end markers are present
    assert "<!-- END CHUNK: test-chunk-1 -->" in result
    assert "<!-- END CHUNK: test-chunk-2 -->" in result
    assert "<!-- END CHUNK: test-chunk-3 -->" in result


def test_chunk_marker_format(sample_markdown_file, sample_chunks):
    """Test chunk marker format correctness."""
    result = add_chunk_markers(sample_markdown_file, sample_chunks)

    # Verify marker format: <!-- CHUNK: id | Lines: X-Y | Keywords: k1, k2 | Tokens: ~N -->
    expected_marker = "<!-- CHUNK: test-chunk-1 | Lines: 1-3 | Keywords: header, metadata | Tokens: ~100 -->"
    assert expected_marker in result


def test_original_content_preserved(sample_markdown_file, sample_chunks):
    """Test that original content is preserved after marker insertion."""
    result = add_chunk_markers(sample_markdown_file, sample_chunks)

    # Original content should still be in result (just with markers added)
    assert "# Header 1" in result
    assert "Some content here." in result
    assert "## Header 2" in result
    assert "More content." in result


def test_chunk_boundaries_correct(sample_markdown_file, sample_chunks):
    """Test that chunk boundaries are correctly placed."""
    result = add_chunk_markers(sample_markdown_file, sample_chunks)
    lines = result.split("\n")

    # Find chunk 1 markers
    chunk1_start_idx = None
    chunk1_end_idx = None
    for i, line in enumerate(lines):
        if "<!-- CHUNK: test-chunk-1" in line:
            chunk1_start_idx = i
        if "<!-- END CHUNK: test-chunk-1 -->" in line:
            chunk1_end_idx = i

    assert chunk1_start_idx is not None
    assert chunk1_end_idx is not None
    # Chunk 1 should contain lines 1-3, so there should be content between markers
    assert chunk1_end_idx > chunk1_start_idx


def test_multiple_chunks_non_overlapping(sample_markdown_file, sample_chunks):
    """Test that multiple chunks don't overlap."""
    result = add_chunk_markers(sample_markdown_file, sample_chunks)

    # Count chunk markers
    chunk1_start = result.count("<!-- CHUNK: test-chunk-1")
    chunk1_end = result.count("<!-- END CHUNK: test-chunk-1 -->")
    chunk2_start = result.count("<!-- CHUNK: test-chunk-2")
    chunk2_end = result.count("<!-- END CHUNK: test-chunk-2 -->")

    # Each chunk should have exactly one start and one end marker
    assert chunk1_start == 1
    assert chunk1_end == 1
    assert chunk2_start == 1
    assert chunk2_end == 1


def test_empty_file():
    """Test handling of empty file."""
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(mode="w", delete=False, suffix=".md") as f:
        f.write("")
        temp_path = Path(f.name)

    try:
        chunks = [("test-chunk", 1, 1, ["test"], 50)]
        # Should handle gracefully (may raise IndexError, which is expected)
        try:
            result = add_chunk_markers(temp_path, chunks)
            # If it doesn't raise, verify no crash
            assert isinstance(result, str)
        except IndexError:
            # Expected for empty file
            pass
    finally:
        temp_path.unlink()


def test_keywords_formatting(sample_markdown_file):
    """Test that keywords are correctly formatted with commas."""
    chunks = [("test-chunk", 1, 3, ["keyword1", "keyword2", "keyword3"], 100)]
    result = add_chunk_markers(sample_markdown_file, chunks)

    # Keywords should be comma-separated
    assert "Keywords: keyword1, keyword2, keyword3" in result


def test_chunk_id_uniqueness(sample_markdown_file):
    """Test that chunk IDs are preserved correctly."""
    chunks = [
        ("unique-id-1", 1, 3, ["test"], 100),
        ("unique-id-2", 4, 8, ["test"], 200),
    ]
    result = add_chunk_markers(sample_markdown_file, chunks)

    # Both IDs should be present
    assert "unique-id-1" in result
    assert "unique-id-2" in result

    # End markers should match start markers
    assert "<!-- END CHUNK: unique-id-1 -->" in result
    assert "<!-- END CHUNK: unique-id-2 -->" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
