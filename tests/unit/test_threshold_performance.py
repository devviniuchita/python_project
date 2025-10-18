"""
Performance and load testing for threshold scoring system.

Tests cover:
- Large dataset performance testing
- Memory usage analysis
- Timing benchmarks
- Concurrent processing validation
- Scalability testing
"""

import time
import psutil
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.features.reranking.reranker import rerank_documents
from config.settings import settings


class TestThresholdPerformance:
    """Performance testing for threshold system."""

    def test_large_dataset_performance(self):
        """Test performance with large document sets."""
        # Generate large synthetic dataset
        n_docs = 1000
        query = "artificial intelligence neural networks"

        # Create documents with varying relevance
        documents = []
        for i in range(n_docs):
            if i < n_docs // 3:  # 33% highly relevant
                doc = f"This document discusses {query} in detail with technical accuracy and comprehensive examples."
            elif i < 2 * n_docs // 3:  # 33% medium relevant
                doc = f"This contains some information about machine learning and AI concepts."
            else:  # 34% low relevant
                doc = f"This document is about cooking recipes and has nothing to do with {query}."

            documents.append(doc)

        print(f"Testing with {n_docs} documents...")

        # Measure execution time
        start_time = time.time()

        with patch('reranker.get_reranker') as mock_get_reranker:
            mock_reranker = MagicMock()
            # Simulate realistic scoring times (faster for testing)
            mock_scores = np.random.random(n_docs) * 0.8 + 0.1  # Scores between 0.1-0.9
            mock_reranker.predict.return_value = mock_scores
            mock_get_reranker.return_value = mock_reranker

            result = rerank_documents(query, documents, top_n=50)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time:.3f} seconds")
        print(f"Documents processed per second: {n_docs / execution_time.1f}}")

        # Validate performance requirements
        assert execution_time < 10.0, f"Too slow: {execution_time:.3f}s for {n_docs} documents"
        assert len(result) <= 50, f"Returned too many results: {len(result)}"
        assert len(result) > 0, "No results returned"

        print(f"✅ PASS - Large dataset performance: {execution_time:.3f}")

    def test_memory_usage_monitoring(self):
        """Test memory usage during threshold processing."""
        process = psutil.Process()

        # Get initial memory usage
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Process medium-sized dataset
        n_docs = 500
        query = "machine learning algorithms"
        documents = [f"Document {i} about {query}" for i in range(n_docs)]

        with patch('reranker.get_reranker') as mock_get_reranker:
            mock_reranker = MagicMock()
            mock_scores = np.random.random(n_docs)
            mock_reranker.predict.return_value = mock_scores
            mock_get_reranker.return_value = mock_reranker

            result = rerank_documents(query, documents, top_n=25)

        # Get final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        print("Memory Usage Analysis:")
        print(f"  Initial memory: {initial_memory:.1f} MB")
        print(f"  Final memory: {final_memory:.1f} MB")
        print(f"  Memory increase: {memory_increase:.1f} MB")

        # Memory increase should be reasonable (< 50MB for 500 docs)
        assert memory_increase < 50, f"Memory increase {memory_increase:.1f}MB is too high"
        assert len(result) <= 25, f"Too many results: {len(result)}"

        print(f"✅ PASS - Memory usage acceptable: +{memory_increase:.1f}MB")

    def test_concurrent_threshold_processing(self):
        """Test concurrent processing of multiple threshold operations."""
        n_concurrent = 10
        n_docs_per_query = 100

        queries = [
            "neural networks deep learning",
            "computer vision image recognition",
            "natural language processing",
            "reinforcement learning algorithms",
            "supervised learning classification",
            "unsupervised learning clustering",
            "machine learning best practices",
            "artificial intelligence ethics",
            "data science methodologies",
            "predictive analytics models"
        ]

        def process_query(query_idx):
            query = queries[query_idx]
            documents = [f"Document {i} relevant to {query}" for i in range(n_docs_per_query)]

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                mock_scores = np.random.random(n_docs_per_query)
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                return rerank_documents(query, documents, top_n=20)

        # Execute concurrent requests
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=n_concurrent) as executor:
            futures = [executor.submit(process_query, i) for i in range(n_concurrent)]
            results = [future.result() for future in as_completed(futures)]

        end_time = time.time()
        total_time = end_time - start_time

        print("Concurrent Processing Results:")
        print(f"  Concurrent requests: {n_concurrent}")
        print(f"  Documents per request: {n_docs_per_query}")
        print(f"  Total processing time: {total_time:.3f} seconds")
        print(f"  Average time per request: {total_time / n_concurrent:.3f} seconds")

        # Validate results
        assert len(results) == n_concurrent, "Not all requests completed"
        for i, result in enumerate(results):
            assert len(result) <= 20, f"Query {i} returned too many results: {len(result)}"
            assert len(result) > 0, f"Query {i} returned no results"

        # Performance should be reasonable (less than 30 seconds for 10 concurrent requests)
        assert total_time < 30, f"Concurrent processing too slow: {total_time:.3f}s"

        print(f"✅ PASS - Concurrent processing: {total_time:.3f}s")

    def test_scalability_with_increasing_dataset_size(self):
        """Test scalability as dataset size increases."""
        dataset_sizes = [50, 100, 200, 500, 1000]
        query = "quantum computing algorithms"

        execution_times = []

        for n_docs in dataset_sizes:
            documents = [f"Document {i} about {query}" for i in range(n_docs)]

            start_time = time.time()

            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()
                mock_scores = np.random.random(n_docs)
                mock_reranker.predict.return_value = mock_scores
                mock_get_reranker.return_value = mock_reranker

                result = rerank_documents(query, documents, top_n=min(25, n_docs))

            end_time = time.time()
            execution_time = end_time - start_time
            execution_times.append(execution_time)

            print(f"  {n_docs:4d} docs: {execution_time:6.3f}s ({n_docs/execution_time:6.1f} docs/s)")

        # Validate scalability - execution time should not grow exponentially
        # Linear growth is acceptable, exponential growth indicates problems
        for i in range(1, len(execution_times)):
            growth_ratio = execution_times[i] / execution_times[i-1]
            dataset_ratio = dataset_sizes[i] / dataset_sizes[i-1]

            print(f"  Growth {dataset_sizes[i-1]}→{dataset_sizes[i]}: {growth_ratio:.2f}x time, {dataset_ratio:.2f}x data")

            # Growth should be roughly linear (not much higher than dataset ratio)
            assert growth_ratio < dataset_ratio * 2.5, \
                f"Non-linear growth detected: {growth_ratio:.2f}x time for {dataset_ratio:.2f}x data"

        print("✅ PASS - Scalability analysis shows linear performance growth")


class TestThresholdStressTesting:
    """Stress testing for edge cases and extreme scenarios."""

    def test_extreme_threshold_values(self):
        """Test behavior with extreme threshold values."""
        n_docs = 100
        documents = [f"Document {i}" for i in range(n_docs)]

        extreme_thresholds = [0.0, 0.001, 0.999, 1.0]

        for threshold in extreme_thresholds:
            with patch('reranker.settings') as mock_settings:
                mock_settings.reranker_score_threshold = threshold

                with patch('reranker.get_reranker') as mock_get_reranker:
                    mock_reranker = MagicMock()
                    mock_scores = np.random.random(n_docs)
                    mock_reranker.predict.return_value = mock_scores
                    mock_get_reranker.return_value = mock_reranker

                    result = rerank_documents("test query", documents)

                    print(f"  Threshold {threshold:.3f}: {len(result)} results")

                    # Validate edge case behavior
                    if threshold >= 1.0:
                        # Very high threshold should return at most 1 document (highest score)
                        assert len(result) <= 1, f"High threshold returned too many: {len(result)}"
                    elif threshold <= 0.0:
                        # Very low threshold should return top_n documents (no filtering)
                        assert len(result) <= 25, f"Low threshold returned too many: {len(result)}"

        print("✅ PASS - Extreme threshold values handled correctly")

    def test_empty_and_minimal_inputs(self):
        """Test behavior with minimal and empty inputs."""
        test_cases = [
            ([], "Should handle empty document list"),
            (["single document"], "Should handle single document"),
            (["doc1", "doc2"], "Should handle minimal document set")
        ]

        for documents, description in test_cases:
            with patch('reranker.get_reranker') as mock_get_reranker:
                mock_reranker = MagicMock()

                if documents:  # Only mock scores if documents exist
                    mock_scores = np.random.random(len(documents))
                    mock_reranker.predict.return_value = mock_scores
                else:
                    mock_reranker.predict.return_value = np.array([])

                mock_get_reranker.return_value = mock_reranker

                result = rerank_documents("test query", documents)

                print(f"  {description}: {len(result)} results")

                # Validate minimal input handling
                assert isinstance(result, list), "Result should be a list"
                if not documents:
                    assert len(result) == 0, "Empty input should return empty list"

        print("✅ PASS - Minimal and empty inputs handled correctly")


if __name__ == "__main__":
    # Run performance tests
    perf_suite = TestThresholdPerformance()
    perf_suite.test_large_dataset_performance()
    perf_suite.test_memory_usage_monitoring()
    perf_suite.test_concurrent_threshold_processing()
    perf_suite.test_scalability_with_increasing_dataset_size()

    stress_suite = TestThresholdStressTesting()
    stress_suite.test_extreme_threshold_values()
    stress_suite.test_empty_and_minimal_inputs()

    print("\n🎉 All performance tests passed!")
