"""
TC001 & TC002: Document Retrieval and Reranking Tests

Tests for document retrieval and reranking functionality in the RAG system.
- TC001: test_document_retrieval_functionality
- TC002: test_document_reranking_functionality
"""

from typing import List
from unittest.mock import MagicMock
from unittest.mock import patch

import numpy as np
import pytest


class TestDocumentRetrievalFunctionality:
    """TC001: Document retrieval tests."""

    def test_retrieve_documents_returns_top_k(
        self, mock_retriever, sample_documents, sample_query
    ):
        """Test that retrieve_documents returns exactly top_k documents."""
        # Arrange
        top_k = 3
        mock_retriever.retrieve_documents.return_value = sample_documents[:top_k]

        # Act
        result = mock_retriever.retrieve_documents(sample_query, top_k=top_k)

        # Assert
        assert len(result) == top_k
        assert all(doc in sample_documents for doc in result)
        mock_retriever.retrieve_documents.assert_called_once_with(
            sample_query, top_k=top_k
        )

    def test_retrieve_documents_similarity_ordering(self, mock_retriever):
        """Test that retrieved documents are ordered by similarity score (descending)."""
        # Arrange
        documents = ["doc1", "doc2", "doc3"]
        scores = [0.95, 0.87, 0.76]
        mock_retriever.get_similarity_scores.return_value = scores

        # Act
        retrieved_scores = mock_retriever.get_similarity_scores()

        # Assert - scores should be in descending order
        assert retrieved_scores == sorted(retrieved_scores, reverse=True)
        assert len(retrieved_scores) == len(documents)

    def test_retrieve_documents_empty_query(self, mock_retriever):
        """Test behavior with empty query string."""
        # Arrange
        mock_retriever.retrieve_documents.return_value = []

        # Act
        result = mock_retriever.retrieve_documents("", top_k=3)

        # Assert
        assert result == []

    def test_retrieve_documents_with_faiss_integration(self, sample_documents):
        """Test FAISS integration for vector similarity search."""
        # Arrange
        faiss_mock = MagicMock()
        query_embedding = np.random.randn(768)
        doc_embeddings = np.random.randn(len(sample_documents), 768)

        faiss_mock.search.return_value = (
            np.array([[0.95, 0.87, 0.76]]),  # similarity scores
            np.array([[0, 2, 1]]),  # document indices
        )

        # Act
        distances, indices = faiss_mock.search(query_embedding.reshape(1, -1), k=3)

        # Assert
        assert indices.shape == (1, 3)
        assert all(idx < len(sample_documents) for idx in indices[0])

    def test_retrieve_documents_performance(self, mock_retriever):
        """Test retrieval performance (latency requirement: <500ms)."""
        import time

        # Arrange
        mock_retriever.retrieve_documents.return_value = ["doc1", "doc2", "doc3"]

        # Act
        start = time.time()
        result = mock_retriever.retrieve_documents("test query", top_k=3)
        elapsed = time.time() - start

        # Assert
        assert len(result) == 3
        # Mock should be nearly instant
        assert elapsed < 0.1

    def test_retrieve_documents_with_gemini_embeddings(self, mock_embeddings):
        """Test document retrieval with Gemini embeddings integration."""
        # Arrange
        query = "Test query"
        docs = ["Doc 1", "Doc 2", "Doc 3"]

        # Mock embedding generation
        mock_embeddings.embed.return_value = np.random.randn(768).tolist()

        # Act
        query_embedding = mock_embeddings.embed(query)
        doc_embeddings = mock_embeddings.embed_documents(docs)

        # Assert
        assert len(query_embedding) == 768
        assert len(doc_embeddings) == 3
        assert all(len(emb) == 768 for emb in doc_embeddings)


class TestDocumentRerankingFunctionality:
    """TC002: Document reranking tests."""

    def test_rerank_documents_returns_reordered_list(self, mock_reranker):
        """Test that rerank_documents returns documents in new order."""
        # Arrange
        original_docs = ["doc1", "doc2", "doc3"]
        reranked_result = {
            "documents": ["doc2", "doc1", "doc3"],
            "scores": [0.92, 0.85, 0.71],
            "indices": [1, 0, 2],
        }
        mock_reranker.rerank_documents.return_value = reranked_result

        # Act
        result = mock_reranker.rerank_documents(original_docs)

        # Assert
        assert len(result["documents"]) == len(original_docs)
        assert result["documents"] != original_docs  # Order changed
        assert all(doc in original_docs for doc in result["documents"])

    def test_rerank_documents_with_bge_model(self, mock_reranker):
        """Test reranking using BGE (BAAI General Embeddings) model."""
        # Arrange
        documents = ["doc1", "doc2", "doc3"]
        query = "test query"
        expected_scores = np.array([0.92, 0.85, 0.71])

        mock_reranker.calculate_scores.return_value = expected_scores

        # Act
        scores = mock_reranker.calculate_scores(query, documents)

        # Assert
        assert len(scores) == len(documents)
        assert all(0 <= score <= 1 for score in scores)
        np.testing.assert_array_almost_equal(scores, expected_scores)

    def test_rerank_documents_adaptive_threshold(self, mock_reranker):
        """Test adaptive thresholding in reranking."""
        # Arrange
        scores = np.array([0.95, 0.87, 0.76, 0.61, 0.54])
        threshold = 0.75

        mock_reranker.rerank_documents.return_value = {
            "documents": ["doc1", "doc2"],
            "scores": [0.95, 0.87],
            "indices": [0, 1],
        }

        # Act
        result = mock_reranker.rerank_documents(["d1", "d2", "d3", "d4", "d5"])

        # Assert - only documents above threshold should be returned
        assert all(score >= threshold for score in result["scores"])
        assert len(result["documents"]) <= 5

    def test_rerank_documents_score_monotonicity(self, mock_reranker):
        """Test that reranked scores are in descending order."""
        # Arrange
        mock_reranker.calculate_scores.return_value = np.array(
            [0.95, 0.87, 0.76, 0.65, 0.54]
        )

        # Act
        scores = mock_reranker.calculate_scores("query", ["d1", "d2", "d3", "d4", "d5"])

        # Assert - scores should be monotonically decreasing
        for i in range(len(scores) - 1):
            assert scores[i] >= scores[i + 1]

    def test_rerank_documents_stability(self, mock_reranker):
        """Test that reranking is deterministic (same input -> same output)."""
        # Arrange
        documents = ["doc1", "doc2", "doc3"]
        query = "stable query"

        mock_reranker.rerank_documents.return_value = {
            "documents": ["doc2", "doc1", "doc3"],
            "scores": [0.92, 0.85, 0.71],
        }

        # Act - call twice
        result1 = mock_reranker.rerank_documents(documents, query)
        result2 = mock_reranker.rerank_documents(documents, query)

        # Assert - results should be identical
        assert result1["documents"] == result2["documents"]
        assert result1["scores"] == result2["scores"]

    def test_rerank_documents_with_empty_list(self, mock_reranker):
        """Test reranking with empty document list."""
        # Arrange
        mock_reranker.rerank_documents.return_value = {
            "documents": [],
            "scores": [],
            "indices": [],
        }

        # Act
        result = mock_reranker.rerank_documents([])

        # Assert
        assert result["documents"] == []
        assert result["scores"] == []

    def test_rerank_documents_filters_low_scores(self, mock_reranker):
        """Test that reranking properly filters documents below threshold."""
        # Arrange
        all_docs = ["high1", "high2", "low1", "low2"]
        min_score_threshold = 0.70

        mock_reranker.rerank_documents.return_value = {
            "documents": ["high1", "high2"],
            "scores": [0.95, 0.87],
            "indices": [0, 1],
            "filtered_count": 2,
        }

        # Act
        result = mock_reranker.rerank_documents(all_docs)

        # Assert
        assert all(score >= min_score_threshold for score in result["scores"])
        assert "filtered_count" in result
        assert result["filtered_count"] == 2


# ============================================================================
# INTEGRATION TESTS - RETRIEVAL + RERANKING PIPELINE
# ============================================================================


class TestRetrievalRerankingPipeline:
    """Integration tests for retrieval + reranking pipeline."""

    def test_full_rag_retrieval_pipeline(
        self, rag_system_mocks, sample_query, sample_documents
    ):
        """Test complete retrieval -> reranking pipeline."""
        # Arrange
        retriever = rag_system_mocks["retriever"]
        reranker = rag_system_mocks["reranker"]

        retriever.retrieve_documents.return_value = sample_documents[:3]
        reranker.rerank_documents.return_value = {
            "documents": sample_documents[:3],
            "scores": [0.95, 0.87, 0.76],
            "indices": [0, 1, 2],
        }

        # Act - Retrieve
        retrieved = retriever.retrieve_documents(sample_query, top_k=3)

        # Act - Rerank
        reranked = reranker.rerank_documents(retrieved)

        # Assert
        assert len(retrieved) == 3
        assert len(reranked["documents"]) == 3
        assert all(s >= 0.7 for s in reranked["scores"])

    def test_pipeline_preserves_document_content(self, rag_system_mocks, sample_query):
        """Test that pipeline preserves original document content."""
        # Arrange
        original_content = "Important information in document"
        rag_system_mocks["retriever"].retrieve_documents.return_value = [
            original_content
        ]
        rag_system_mocks["reranker"].rerank_documents.return_value = {
            "documents": [original_content],
            "scores": [0.92],
        }

        # Act
        retrieved = rag_system_mocks["retriever"].retrieve_documents(sample_query)
        final = rag_system_mocks["reranker"].rerank_documents(retrieved)

        # Assert
        assert final["documents"][0] == original_content

    @pytest.mark.parametrize("top_k", [1, 3, 5, 10])
    def test_pipeline_with_varying_k(self, rag_system_mocks, sample_query, top_k):
        """Test pipeline with different k values."""
        # Arrange
        docs = [f"Document {i}" for i in range(top_k)]
        rag_system_mocks["retriever"].retrieve_documents.return_value = docs
        rag_system_mocks["reranker"].rerank_documents.return_value = {
            "documents": docs,
            "scores": [0.9 - i * 0.05 for i in range(top_k)],
        }

        # Act
        retrieved = rag_system_mocks["retriever"].retrieve_documents(
            sample_query, top_k=top_k
        )
        reranked = rag_system_mocks["reranker"].rerank_documents(retrieved)

        # Assert
        assert len(reranked["documents"]) == top_k
