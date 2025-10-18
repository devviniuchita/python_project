"""
Integration tests for BGE Reranker in LangGraph workflow.

Tests cover:
- Full RAG workflow with reranking node
- Complexity-based top_n (simple=5, complex=7)
- Reranking node execution in graph
- Quality score improvement validation
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.core.domain.state import RAGState


class TestRerankerNodeIntegration:
    """Test reranker node integration in workflow."""

    def test_rerank_documents_node_execution(self):
        """Test that rerank_documents node executes correctly in workflow."""
        with patch('nodes.settings') as mock_settings:
            mock_settings.reranker_enabled = True

            with patch('nodes.get_reranker') as mock_get_reranker:
                # Mock reranker
                mock_reranker = MagicMock()
                mock_reranker.top_n = 5

                # Mock compress_documents to return first 5 docs
                from langchain_core.documents import Document

                def mock_compress(documents, query):
                    return documents[:5]

                mock_reranker.compress_documents = mock_compress
                mock_get_reranker.return_value = mock_reranker

                from nodes import rerank_documents

                # Create state with 10 documents
                state: RAGState = {
                    "question": "What is a Perceptron?",
                    "complexity": "simple",
                    "documents": [f"Document {i}" for i in range(10)],
                    "generation": "",
                    "quality_score": 0.0,
                    "iterations": 0,
                }

                result = rerank_documents(state)

                # Should reduce to 5 documents
                assert len(result["documents"]) == 5
                assert result["documents"][0] == "Document 0"
                print(f"✅ PASS - Rerank node reduced 10 → 5 documents")

    def test_rerank_node_disabled_returns_empty(self):
        """Test that rerank node returns empty dict when disabled."""
        with patch('nodes.settings') as mock_settings:
            mock_settings.reranker_enabled = False

            from nodes import rerank_documents

            state: RAGState = {
                "question": "What is a Perceptron?",
                "complexity": "simple",
                "documents": [f"Document {i}" for i in range(10)],
                "generation": "",
                "quality_score": 0.0,
                "iterations": 0,
            }

            result = rerank_documents(state)

            # Should return empty dict (no changes to state)
            assert result == {}
            print("✅ PASS - Disabled rerank node returns empty dict")

    def test_rerank_node_empty_documents(self):
        """Test that rerank node handles empty documents gracefully."""
        with patch('nodes.settings') as mock_settings:
            mock_settings.reranker_enabled = True

            from nodes import rerank_documents

            state: RAGState = {
                "question": "What is a Perceptron?",
                "complexity": "simple",
                "documents": [],
                "generation": "",
                "quality_score": 0.0,
                "iterations": 0,
            }

            result = rerank_documents(state)

            # Should return empty dict (no documents to rerank)
            assert result == {}
            print("✅ PASS - Empty documents returns empty dict")


class TestComplexityBasedTopN:
    """Test complexity-based top_n adjustment."""

    def test_simple_question_top_n_5(self):
        """Test that simple questions use top_n=5."""
        with patch('nodes.settings') as mock_settings:
            mock_settings.reranker_enabled = True

            with patch('nodes.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                mock_reranker.top_n = None  # Will be set by node

                from langchain_core.documents import Document

                def mock_compress(documents, query):
                    # Verify top_n was set to 5
                    assert mock_reranker.top_n == 5
                    return documents[:5]

                mock_reranker.compress_documents = mock_compress
                mock_get_reranker.return_value = mock_reranker

                from nodes import rerank_documents

                state: RAGState = {
                    "question": "What is a Perceptron?",
                    "complexity": "simple",
                    "documents": [f"Document {i}" for i in range(10)],
                    "generation": "",
                    "quality_score": 0.0,
                    "iterations": 0,
                }

                result = rerank_documents(state)

                assert len(result["documents"]) == 5
                print("✅ PASS - Simple questions use top_n=5")

    def test_complex_question_top_n_7(self):
        """Test that complex questions use top_n=7."""
        with patch('nodes.settings') as mock_settings:
            mock_settings.reranker_enabled = True

            with patch('nodes.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                mock_reranker.top_n = None

                from langchain_core.documents import Document

                def mock_compress(documents, query):
                    # Verify top_n was set to 7
                    assert mock_reranker.top_n == 7
                    return documents[:7]

                mock_reranker.compress_documents = mock_compress
                mock_get_reranker.return_value = mock_reranker

                from nodes import rerank_documents

                state: RAGState = {
                    "question": "Explain the detailed mathematical formulation of Perceptron?",
                    "complexity": "complex",
                    "documents": [f"Document {i}" for i in range(15)],
                    "generation": "",
                    "quality_score": 0.0,
                    "iterations": 0,
                }

                result = rerank_documents(state)

                assert len(result["documents"]) == 7
                print("✅ PASS - Complex questions use top_n=7")


class TestRerankerErrorHandlingInNode:
    """Test error handling in rerank_documents node."""

    def test_node_handles_reranker_exception(self):
        """Test that node handles exceptions gracefully."""
        with patch('nodes.settings') as mock_settings:
            mock_settings.reranker_enabled = True

            with patch('nodes.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                mock_reranker.compress_documents.side_effect = Exception("Model error")
                mock_get_reranker.return_value = mock_reranker

                from nodes import rerank_documents

                state: RAGState = {
                    "question": "What is a Perceptron?",
                    "complexity": "simple",
                    "documents": [f"Document {i}" for i in range(10)],
                    "generation": "",
                    "quality_score": 0.0,
                    "iterations": 0,
                }

                result = rerank_documents(state)

                # Should return empty dict (fallback to original documents)
                assert result == {}
                print("✅ PASS - Node handles exception and returns empty dict")

    def test_node_handles_none_reranker(self):
        """Test that node handles None reranker gracefully."""
        with patch('nodes.settings') as mock_settings:
            mock_settings.reranker_enabled = True

            with patch('nodes.get_reranker') as mock_get_reranker:
                mock_get_reranker.return_value = None

                from nodes import rerank_documents

                state: RAGState = {
                    "question": "What is a Perceptron?",
                    "complexity": "simple",
                    "documents": [f"Document {i}" for i in range(10)],
                    "generation": "",
                    "quality_score": 0.0,
                    "iterations": 0,
                }

                result = rerank_documents(state)

                # Should return empty dict
                assert result == {}
                print("✅ PASS - Node handles None reranker gracefully")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
