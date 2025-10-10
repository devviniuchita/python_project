"""
Unit tests for threshold filtering in reranker.py.

Tests cover:
- Threshold filtering with different values (0.0, 0.3, 0.5, 0.8, 1.0)
- Score calculation and ordering
- Edge cases (all filtered, empty input, threshold boundaries)
- Logging and error handling
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import numpy as np
import pytest


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        "Perceptron is a fundamental neural network unit",
        "Deep learning uses multiple layers of neurons",
        "Machine learning algorithms learn from data",
        "Python is a programming language",
        "The weather is sunny today",
    ]


@pytest.fixture
def sample_query():
    """Sample query for testing."""
    return "What is Perceptron and neural networks?"


class TestThresholdFiltering:
    """Test threshold-based document filtering."""

    def test_threshold_zero_no_filtering(self, sample_documents, sample_query):
        """Test that threshold=0.0 does not filter any documents."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True
            mock_settings.reranker_score_threshold = 0.0
            mock_settings.reranker_top_n = 3

            with patch('reranker.get_reranker') as mock_get_reranker:
                # Mock reranker with scores
                mock_reranker = MagicMock()
                mock_scores = np.array([0.95, 0.72, 0.31, 0.12, 0.05])
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                from reranker import rerank_documents

                result = rerank_documents(sample_query, sample_documents)

                # Should return top 3 (no filtering, just sorting + top_n)
                assert len(result) == 3
                # Verify order (highest scores first)
                assert result[0] == sample_documents[0]  # score 0.95
                assert result[1] == sample_documents[1]  # score 0.72
                assert result[2] == sample_documents[2]  # score 0.31
                print("✅ PASS - Threshold=0.0 returns top_n without filtering")

    def test_threshold_medium_filters_low_scores(self, sample_documents, sample_query):
        """Test that threshold=0.5 filters documents with scores < 0.5."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True
            mock_settings.reranker_score_threshold = 0.5
            mock_settings.reranker_top_n = 5

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                # Scores: 0.95, 0.72, 0.31, 0.12, 0.05
                # Threshold 0.5 should keep only first 2
                mock_scores = np.array([0.95, 0.72, 0.31, 0.12, 0.05])
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                from reranker import rerank_documents

                result = rerank_documents(sample_query, sample_documents)

                # Only 2 documents above threshold
                assert len(result) == 2
                assert result[0] == sample_documents[0]  # score 0.95
                assert result[1] == sample_documents[1]  # score 0.72
                print("✅ PASS - Threshold=0.5 correctly filters low-scoring docs")

    def test_threshold_high_returns_at_least_one(self, sample_documents, sample_query):
        """Test that threshold=1.0 returns at least 1 document (fallback)."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True
            mock_settings.reranker_score_threshold = 1.0
            mock_settings.reranker_top_n = 5

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                # All scores below threshold
                mock_scores = np.array([0.95, 0.72, 0.31, 0.12, 0.05])
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                from reranker import rerank_documents

                result = rerank_documents(sample_query, sample_documents)

                # Should return best document even if below threshold
                assert len(result) == 1
                assert result[0] == sample_documents[0]  # highest score 0.95
                print(
                    "✅ PASS - Threshold=1.0 returns top 1 when all docs below threshold"
                )

    def test_threshold_boundary_exact_match(self, sample_documents, sample_query):
        """Test that documents with score == threshold are kept."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True
            mock_settings.reranker_score_threshold = 0.72
            mock_settings.reranker_top_n = 5

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                # Score 0.72 exactly matches threshold
                mock_scores = np.array([0.95, 0.72, 0.31, 0.12, 0.05])
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                from reranker import rerank_documents

                result = rerank_documents(sample_query, sample_documents)

                # Should keep 0.95 and 0.72 (>= threshold)
                assert len(result) == 2
                assert result[0] == sample_documents[0]  # score 0.95
                assert result[1] == sample_documents[1]  # score 0.72
                print("✅ PASS - Documents with score == threshold are kept")


class TestScoreOrdering:
    """Test score-based document ordering."""

    def test_documents_sorted_by_score_descending(self, sample_documents, sample_query):
        """Test that documents are sorted by score (highest first)."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True
            mock_settings.reranker_score_threshold = 0.0
            mock_settings.reranker_top_n = 5

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                # Scores in random order
                mock_scores = np.array([0.31, 0.95, 0.12, 0.72, 0.05])
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                from reranker import rerank_documents

                result = rerank_documents(sample_query, sample_documents)

                # Should be reordered by score: 0.95, 0.72, 0.31, 0.12, 0.05
                assert result[0] == sample_documents[1]  # score 0.95
                assert result[1] == sample_documents[3]  # score 0.72
                assert result[2] == sample_documents[0]  # score 0.31
                assert result[3] == sample_documents[2]  # score 0.12
                assert result[4] == sample_documents[4]  # score 0.05
                print("✅ PASS - Documents correctly sorted by score descending")


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_document_list_returns_empty(self, sample_query):
        """Test that empty document list returns empty result."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True

            from reranker import rerank_documents

            result = rerank_documents(sample_query, [])

            assert result == []
            print("✅ PASS - Empty input returns empty output")

    def test_reranker_disabled_returns_original(self, sample_documents, sample_query):
        """Test that disabled reranker returns original documents."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = False

            from reranker import rerank_documents

            result = rerank_documents(sample_query, sample_documents, top_n=3)

            # Should return original documents unchanged
            assert result == sample_documents
            print("✅ PASS - Disabled reranker returns original documents")

    def test_exception_during_scoring_returns_originals(
        self, sample_documents, sample_query
    ):
        """Test graceful fallback when scoring fails."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True
            mock_settings.reranker_top_n = 3

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                # Simulate error during prediction
                mock_reranker.predict.side_effect = Exception("Model error")
                mock_get_reranker.return_value = mock_reranker

                from reranker import rerank_documents

                # Should catch exception and return originals (limited to top_n)
                result = rerank_documents(sample_query, sample_documents, top_n=3)

                assert len(result) == 3
                assert result == sample_documents[:3]
                print(
                    "✅ PASS - Exception returns original documents (graceful fallback)"
                )


class TestThresholdLogging:
    """Test logging behavior with threshold filtering."""

    def test_threshold_filtering_logged(self, sample_documents, sample_query, capsys):
        """Test that threshold filtering is logged."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True
            mock_settings.reranker_score_threshold = 0.5
            mock_settings.reranker_top_n = 5

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                # 2 above threshold, 3 below
                mock_scores = np.array([0.95, 0.72, 0.31, 0.12, 0.05])
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                from reranker import rerank_documents

                rerank_documents(sample_query, sample_documents)

                captured = capsys.readouterr()
                assert "Threshold 0.50 filtered 3/5 documents" in captured.out
                print("✅ PASS - Threshold filtering logged correctly")

    def test_all_filtered_warning_logged(self, sample_documents, sample_query, capsys):
        """Test that warning is logged when all documents are filtered."""
        with patch('reranker.settings') as mock_settings:
            mock_settings.reranker_enabled = True
            mock_settings.reranker_score_threshold = 1.0
            mock_settings.reranker_top_n = 5

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                mock_scores = np.array([0.95, 0.72, 0.31, 0.12, 0.05])
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                from reranker import rerank_documents

                rerank_documents(sample_query, sample_documents)

                captured = capsys.readouterr()
                assert "WARNING: All 5 documents below threshold 1.00" in captured.out
                assert "Returning top 1 anyway" in captured.out
                print("✅ PASS - All-filtered warning logged correctly")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
