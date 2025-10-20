#!/usr/bin/env python3
"""
Script to add inline chunk markers to documentation files for RAG optimization.

Usage:
    python scripts/add_chunk_markers.py

Adds HTML comment markers for semantic chunking:
<!-- CHUNK: id | Lines: X-Y | Keywords: k1, k2, k3 | Tokens: ~N -->
[Content]
<!-- END CHUNK: id -->
"""

from pathlib import Path
from typing import List, Tuple

# Chunk definitions for project-rules.md
RULES_CHUNKS: List[Tuple[str, int, int, List[str], int]] = [
    (
        "rules-metadata",
        1,
        76,
        ["metadata", "quick-navigation-index", "search-shortcuts"],
        600,
    ),
    (
        "rules-clean-arch",
        77,
        95,
        ["clean-architecture", "4-layers", "dependency-boundaries"],
        200,
    ),
    (
        "rules-solid-overview",
        96,
        123,
        ["solid-principles", "srp", "ocp", "lsp", "isp", "dip"],
        300,
    ),
    (
        "rules-abstraction",
        124,
        171,
        ["typeddict", "ragstate", "literal", "pep-589"],
        500,
    ),
    (
        "rules-encapsulation",
        172,
        218,
        ["pydantic", "basesettings", "field", "computed-field"],
        500,
    ),
    (
        "rules-inheritance",
        219,
        254,
        ["sessionconfig", "settings", "pydantic-inheritance"],
        400,
    ),
    (
        "rules-polymorphism",
        255,
        311,
        ["callable", "strategy-pattern", "adaptive-retrieval"],
        600,
    ),
    (
        "rules-abc-part1",
        312,
        380,
        ["abstractmethod", "metricscollector", "abc-protocol"],
        700,
    ),
    ("rules-abc-part2", 381, 443, ["embeddingprovider", "protocol-enforcement"], 650),
    (
        "rules-composition-part1",
        444,
        520,
        ["dependency-injection", "aggregation", "composition"],
        800,
    ),
    ("rules-composition-part2", 521, 594, ["decision-matrix", "trade-offs"], 750),
    (
        "rules-compliance-immutable",
        595,
        632,
        ["immutable-rules", "approval-criteria", "quality-gates"],
        400,
    ),
    (
        "rules-compliance-tools",
        633,
        682,
        ["validation-tools", "pre-commit", "sonarqube"],
        500,
    ),
    (
        "rules-compliance-git",
        683,
        738,
        ["git-commit-hooks", "github-actions", "ci-cd"],
        600,
    ),
    (
        "rules-compliance-checklist",
        739,
        773,
        ["compliance-checklist", "verification-steps"],
        350,
    ),
    (
        "rules-cross-reference",
        774,
        811,
        ["cross-reference-table", "bidirectional-links"],
        400,
    ),
]

# Chunk definitions for project-codification.md
CODIFICATION_CHUNKS: List[Tuple[str, int, int, List[str], int]] = [
    (
        "codif-metadata",
        1,
        89,
        ["metadata", "quick-navigation-index", "search-shortcuts"],
        700,
    ),
    (
        "codif-layer1-part1",
        90,
        195,
        ["presentation-layer", "cli-interface", "command-pattern"],
        1100,
    ),
    (
        "codif-layer1-part2",
        196,
        303,
        ["traceable", "graph-invoke", "handler-pattern"],
        1100,
    ),
    ("codif-layer2-part1", 304, 450, ["orchestration", "stategraph", "add-node"], 1500),
    (
        "codif-layer2-part2",
        451,
        580,
        ["add-edge", "compile", "conditional-edges"],
        1350,
    ),
    ("codif-layer2-part3", 581, 655, ["graph-patterns", "routing-logic"], 780),
    (
        "codif-layer3-part1",
        656,
        740,
        ["business-logic", "retrieve-adaptive", "rag-nodes"],
        880,
    ),
    ("codif-layer3-part2", 741, 820, ["rerank-documents", "crossencoder"], 840),
    ("codif-layer3-part3", 821, 887, ["generate-answer", "llm-node"], 700),
    (
        "codif-layer4-part1",
        888,
        980,
        ["specialized-services", "infrastructure", "settings"],
        960,
    ),
    (
        "codif-layer4-part2",
        981,
        1087,
        ["faiss-integration", "langsmith-observability"],
        1100,
    ),
    ("codif-inventory", 1088, 1123, ["structured-inventory", "module-mapping"], 370),
    (
        "codif-communication",
        1124,
        1219,
        ["universal-language", "thread-safety", "validation"],
        1000,
    ),
    (
        "codif-strategy-pattern",
        1220,
        1293,
        ["strategy-pattern", "callable", "complexity-routing"],
        780,
    ),
    (
        "codif-dependency-injection",
        1294,
        1380,
        ["di-pattern", "sessionconfig", "lazy-load"],
        900,
    ),
    (
        "codif-exception-hierarchy",
        1381,
        1470,
        ["custom-exceptions", "error-handling", "retry-logic"],
        950,
    ),
    ("codif-immutable-rules", 1471, 1504, ["hierarchy-enforcement", "no-bypass"], 350),
    (
        "codif-validation",
        1505,
        1530,
        ["architectural-validation", "compliance-tests"],
        270,
    ),
    (
        "codif-cross-reference",
        1531,
        1597,
        ["cross-reference-table", "bidirectional-links"],
        700,
    ),
]


def add_chunk_markers(
    file_path: Path, chunks: List[Tuple[str, int, int, List[str], int]]
) -> str:
    """
    Add chunk markers to a file based on chunk definitions.

    Args:
        file_path: Path to the file to process
        chunks: List of (chunk_id, start_line, end_line, keywords, token_count)

    Returns:
        Modified file content with chunk markers
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Build new content with markers
    new_lines = []
    current_line = 1

    for chunk_id, start_line, end_line, keywords, token_count in chunks:
        # Add lines before chunk
        while current_line < start_line:
            new_lines.append(lines[current_line - 1])
            current_line += 1

        # Add chunk start marker
        keywords_str = ", ".join(keywords)
        start_marker = (
            f"<!-- CHUNK: {chunk_id} | Lines: {start_line}-{end_line} | "
            f"Keywords: {keywords_str} | Tokens: ~{token_count} -->\n"
        )
        new_lines.append(start_marker)

        # Add chunk content
        while current_line <= end_line:
            new_lines.append(lines[current_line - 1])
            current_line += 1

        # Add chunk end marker
        end_marker = f"<!-- END CHUNK: {chunk_id} -->\n"
        new_lines.append(end_marker)

    # Add remaining lines
    while current_line <= len(lines):
        new_lines.append(lines[current_line - 1])
        current_line += 1

    return "".join(new_lines)


def main():
    """Main execution function."""
    project_root = Path(__file__).parent.parent
    rules_file = project_root / ".github" / "copilot-rules" / "project-rules.md"
    codification_file = (
        project_root / ".github" / "copilot-rules" / "project-codification.md"
    )

    print("🔄 Adding chunk markers to documentation files...")

    # Process project-rules.md
    print(f"\n📝 Processing {rules_file.name}...")
    rules_content = add_chunk_markers(rules_file, RULES_CHUNKS)
    with open(rules_file, "w", encoding="utf-8") as f:
        f.write(rules_content)
    print(f"✅ Added {len(RULES_CHUNKS)} chunks to {rules_file.name}")

    # Process project-codification.md
    print(f"\n📝 Processing {codification_file.name}...")
    codification_content = add_chunk_markers(codification_file, CODIFICATION_CHUNKS)
    with open(codification_file, "w", encoding="utf-8") as f:
        f.write(codification_content)
    print(f"✅ Added {len(CODIFICATION_CHUNKS)} chunks to {codification_file.name}")

    print("\n✨ Chunk markers added successfully!")
    print(f"📊 Total chunks: {len(RULES_CHUNKS) + len(CODIFICATION_CHUNKS)}")
    print("\n💡 Markers are invisible HTML comments - verify with Markdown preview")


if __name__ == "__main__":
    main()
