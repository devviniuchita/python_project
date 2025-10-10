"""
BGE Reranker module for semantic document reranking.

This module provides direct access to sentence_transformers CrossEncoder models
for BAAI/bge-reranker. It implements lazy loading to avoid unnecessary model loading,
singleton pattern for efficient resource usage, and threshold-based filtering.

Example:
    >>> from reranker import get_reranker, rerank_documents
    >>> reranker = get_reranker()
    >>> reranked = rerank_documents(query="What is AI?", documents=docs, top_n=5)
"""

import time

from typing import List
from typing import Optional
from typing import Tuple

import langsmith
import numpy as np
import torch

from config.settings import settings
from langchain_core.documents import Document
from langsmith import traceable
from sentence_transformers import CrossEncoder
from structlog.contextvars import bind_contextvars
from utils.logger import get_logger


# Module logger
logger = get_logger(__name__)


# Global singleton to avoid reloading model multiple times
_reranker_instance: Optional[CrossEncoder] = None


@traceable(run_type="tool", name="Load BGE Reranker Model")
def get_reranker() -> Optional[CrossEncoder]:
    """
    Get or create the BGE reranker instance (singleton pattern).

    This function implements lazy loading - the model is only loaded when first needed
    and reused for all subsequent calls. If reranking is disabled in settings,
    returns None.

    Uses sentence_transformers.CrossEncoder directly for score access and threshold filtering.
    Activation function set to Sigmoid for 0-1 score range (threshold compatible).

    Returns:
        Optional[CrossEncoder]: The reranker instance, or None if disabled.

    Example:
        >>> reranker = get_reranker()
        >>> if reranker:
        ...     scores = reranker.predict([(query, doc1), (query, doc2)])
    """
    global _reranker_instance

    if not settings.reranker_enabled:
        return None

    if _reranker_instance is None:
        start_time = time.time()
        logger.info(
            "model_loading_started",
            model=settings.reranker_model,
            threshold=settings.reranker_score_threshold,
        )
        _reranker_instance = CrossEncoder(
            settings.reranker_model,
            activation_fn=torch.nn.Sigmoid(),  # 0-1 scores for threshold filtering
        )
        load_time_ms = (time.time() - start_time) * 1000
        logger.info(
            "model_loaded_successfully",
            model=settings.reranker_model,
            threshold=settings.reranker_score_threshold,
            load_time_ms=load_time_ms,
        )

    return _reranker_instance


@traceable(
    run_type="chain",
    name="BGE Semantic Reranking with Threshold",
    metadata={"component": "reranker", "model": "BAAI/bge-reranker-base"},
)
def rerank_documents(
    query: str, documents: List[str], top_n: Optional[int] = None
) -> List[str]:
    """
    Rerank documents by relevance to query using BGE cross-encoder with threshold filtering.

    This function uses sentence_transformers.CrossEncoder directly to:
    1. Calculate individual relevance scores for each document
    2. Apply threshold filtering (if configured)
    3. Sort by score descending
    4. Return top-N most relevant documents

    Args:
        query: The search query to rank documents against.
        documents: List of document texts to rerank.
        top_n: Number of top documents to return (overrides settings if provided).

    Returns:
        List[str]: Top-N reranked documents as strings, sorted by relevance.

    Example:
        >>> docs = ["AI is great", "ML is cool", "Python is fun"]
        >>> reranked = rerank_documents("machine learning", docs, top_n=2)
        >>> print(reranked)
        ['ML is cool', 'AI is great']
    """
    reranker = get_reranker()

    if reranker is None or not documents:
        # Reranking disabled or no documents - return original
        return documents

    # Use settings default if top_n not specified
    effective_top_n = top_n if top_n is not None else settings.reranker_top_n

    # Bind context variables for this reranking operation
    bind_contextvars(
        query_preview=query[:50] + "..." if len(query) > 50 else query,
        num_documents=len(documents),
        threshold=settings.reranker_score_threshold,
        top_n=effective_top_n,
    )

    try:
        # Batch predict scores for all (query, document) pairs (timed)
        scoring_start = time.time()
        pairs = [(query, doc) for doc in documents]
        scores = reranker.predict(pairs)  # Returns numpy.ndarray of float scores
        scoring_time_ms = (time.time() - scoring_start) * 1000

        # Preserve scores before threshold for metadata
        scores_before_threshold = scores.copy()

        # Apply threshold filtering if configured
        threshold = settings.reranker_score_threshold
        if threshold > 0.0:
            # Filter documents below threshold
            mask = scores >= threshold
            filtered_docs = [doc for doc, keep in zip(documents, mask) if keep]
            filtered_scores = scores[mask]

            # Edge case: All documents filtered out
            if len(filtered_docs) == 0:
                logger.warning(
                    "all_documents_below_threshold",
                    num_documents=len(documents),
                    threshold=threshold,
                    max_score=float(np.max(scores)),
                    action="returning_top_1_anyway",
                )
                # Return highest scoring document even if below threshold
                best_idx = int(np.argmax(scores))
                return [documents[best_idx]]

            logger.info(
                "threshold_filtering_applied",
                threshold=threshold,
                filtered_count=len(documents) - len(filtered_docs),
                total_documents=len(documents),
                kept_documents=len(filtered_docs),
            )
        else:
            # No threshold filtering
            filtered_docs = documents
            filtered_scores = scores

        # Sort by score descending (highest scores first)
        sorted_indices = np.argsort(filtered_scores)[::-1]

        # Apply top_n limit
        top_n_indices = sorted_indices[:effective_top_n]

        # Extract reranked documents
        reranked_docs = [filtered_docs[i] for i in top_n_indices]
        reranked_scores = [filtered_scores[i] for i in top_n_indices]

        # Attach custom metadata to LangSmith trace
        run_tree = langsmith.get_current_run_tree()
        if run_tree:
            run_tree.extra = {
                "scores_before_threshold": scores_before_threshold.tolist(),
                "scores_after_threshold": [float(s) for s in reranked_scores],
                "num_filtered": len(documents) - len(filtered_docs),
                "threshold_value": threshold,
                "scoring_time_ms": scoring_time_ms,
                "score_distribution": {
                    "max": float(np.max(scores_before_threshold)),
                    "min": float(np.min(scores_before_threshold)),
                    "mean": float(np.mean(scores_before_threshold)),
                    "median": float(np.median(scores_before_threshold)),
                    "p50": float(np.percentile(scores_before_threshold, 50)),
                    "p95": float(np.percentile(scores_before_threshold, 95)),
                },
            }

        # Log scoring details
        logger.info(
            "reranking_completed",
            original_count=len(documents),
            reranked_count=len(reranked_docs),
            score_max=float(reranked_scores[0]),
            score_min=float(reranked_scores[-1]),
            score_mean=float(np.mean(reranked_scores)),
            scoring_time_ms=scoring_time_ms,
        )

        return reranked_docs

    except Exception as e:
        # Graceful fallback on error
        logger.error(
            "reranking_error",
            error_type=type(e).__name__,
            error_message=str(e),
            num_documents=len(documents),
            exc_info=True,
        )
        return documents[:effective_top_n]


def reset_reranker() -> None:
    """
    Reset the reranker singleton (useful for testing or config changes).

    This forces the next call to get_reranker() to reload the model with
    current settings.

    Example:
        >>> reset_reranker()  # Force reload on next use
        >>> reranker = get_reranker()  # Loads fresh model
    """
    global _reranker_instance
    _reranker_instance = None
    logger.debug("reranker_instance_reset", action="will_reload_on_next_use")
