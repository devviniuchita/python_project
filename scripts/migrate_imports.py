#!/usr/bin/env python3
"""
Migration script to update import statements after project reorganization.

This script automatically updates import statements to use the new modular structure:
- config/ → src.infrastructure.config
- utils/ → src.infrastructure.logging
- models/ → src.core.domain
- memory_manager → src.core.services.memory_manager
- monitoring → src.core.services.monitoring
- state → src.core.domain.state
- conversation → src.features.conversation.conversation
- conversation_graph → src.features.conversation.conversation_graph
- nodes → src.features.rag.nodes
- graph_rag → src.features.rag.graph_rag
- reranker → src.features.reranking.reranker
"""

import os
import re

# Import mapping for the migration
IMPORT_MAPPINGS = {
    # Core modules
    r"from state import": "from src.core.domain.state import",
    r"from models\.session import": "from src.core.domain.session import",
    r"from memory_manager import": "from src.core.services.memory_manager import",
    r"from monitoring import": "from src.core.services.monitoring import",
    # Infrastructure modules
    r"from config\.settings import": "from src.infrastructure.config.settings import",
    r"from config import": "from src.infrastructure.config import",
    r"from utils\.logger import": "from src.infrastructure.logging.logger import",
    r"from utils import": "from src.infrastructure.logging import",
    # Feature modules
    r"from conversation import": "from src.features.conversation.conversation import",
    r"from conversation_graph import": "from src.features.conversation.conversation_graph import",
    r"from nodes import": "from src.features.rag.nodes import",
    r"from graph_rag import": "from src.features.rag.graph_rag import",
    r"from reranker import": "from src.features.reranking.reranker import",
    # Also handle relative imports within the same feature
    r"from \.conversation import": "from .conversation import",
    r"from \.nodes import": "from .nodes import",
    r"from \.reranker import": "from .reranker import",
}


def migrate_file(file_path):
    """Migrate import statements in a single file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Apply all import mappings
        for pattern, replacement in IMPORT_MAPPINGS.items():
            content = re.sub(pattern, replacement, content)

        # Only write if content changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Migrated: {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error migrating {file_path}: {e}")
        return False


def find_python_files(directory):
    """Find all Python files in a directory recursively."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def main():
    """Main migration function."""
    print("🚀 Starting Import Migration")
    print("=" * 50)

    # Find all Python files in src, tests, and scripts
    directories_to_migrate = ["src", "tests", "scripts"]
    all_files = []

    for directory in directories_to_migrate:
        if os.path.exists(directory):
            files = find_python_files(directory)
            all_files.extend(files)
            print(f"📁 Found {len(files)} Python files in {directory}")

    print(f"\n📊 Total files to process: {len(all_files)}")

    # Migrate each file
    migrated_count = 0
    for file_path in all_files:
        if migrate_file(file_path):
            migrated_count += 1

    print("\n📊 Migration Summary")
    print("=" * 50)
    print(f"✅ Files migrated: {migrated_count}")
    print(f"⏭️  Files unchanged: {len(all_files) - migrated_count}")
    print(f"📁 Total files processed: {len(all_files)}")

    if migrated_count > 0:
        print("\n🎉 Migration completed successfully!")
        print("💡 Don't forget to run tests to verify all imports work correctly")
    else:
        print("\nℹ️  No files needed migration - structure may already be up to date")


if __name__ == "__main__":
    main()
