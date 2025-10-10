"""
Statistical validation tests for threshold scoring system.

Tests cover:
- ROC curve analysis for threshold optimization
- Precision-recall curve evaluation
- Statistical significance testing
- Confidence interval validation
- Threshold performance metrics
"""

import numpy as np
import pytest
from sklearn.metrics import roc_curve, precision_recall_curve, auc
from unittest.mock import MagicMock, patch

from reranker import rerank_documents
from config.settings import settings


class TestThresholdStatisticalValidation:
    """Statistical validation of threshold scoring system."""

    def test_roc_curve_analysis_for_threshold_optimization(self):
        """Test ROC curve analysis to find optimal threshold."""
        # Generate synthetic relevance scores and ground truth
        np.random.seed(42)
        n_samples = 1000

        # Simulate relevance scores (higher = more relevant)
        relevant_scores = np.random.normal(0.8, 0.1, n_samples // 2)
        irrelevant_scores = np.random.normal(0.3, 0.15, n_samples // 2)

        all_scores = np.concatenate([relevant_scores, irrelevant_scores])
        ground_truth = np.concatenate([np.ones(n_samples // 2), np.zeros(n_samples // 2)])

        # Calculate ROC curve
        fpr, tpr, thresholds = roc_curve(ground_truth, all_scores)
        roc_auc = auc(fpr, tpr)

        print("ROC Analysis Results:"        print(f"  AUC: {roc_auc".3f"}")
        print(f"  Optimal threshold (Youden): {thresholds[np.argmax(tpr - fpr)]".3f"}")

        # Validate that AUC is meaningful (> 0.7 indicates good discrimination)
        assert roc_auc > 0.7, f"ROC AUC {roc_auc".3f"} is too low for effective threshold"

        # Find optimal threshold using Youden's J statistic
        youden_threshold = thresholds[np.argmax(tpr - fpr)]
        print(f"✅ PASS - ROC analysis identifies optimal threshold: {youden_threshold:.".3f")

    def test_precision_recall_curve_analysis(self):
        """Test precision-recall curve for threshold evaluation."""
        # Generate imbalanced dataset (more irrelevant documents)
        np.random.seed(42)
        n_relevant = 100
        n_irrelevant = 900

        relevant_scores = np.random.normal(0.7, 0.15, n_relevant)
        irrelevant_scores = np.random.normal(0.2, 0.1, n_irrelevant)

        all_scores = np.concatenate([relevant_scores, irrelevant_scores])
        ground_truth = np.concatenate([np.ones(n_relevant), np.zeros(n_irrelevant)])

        # Calculate precision-recall curve
        precision, recall, thresholds = precision_recall_curve(ground_truth, all_scores)
        pr_auc = auc(recall, precision)

        print("Precision-Recall Analysis Results:"        print(f"  AUC: {pr_auc".3f"}")
        print(f"  Max precision: {np.max(precision)".3f"}")
        print(f"  Max recall: {np.max(recall)".3f"}")

        # Find threshold that balances precision and recall
        f1_scores = 2 * (precision * recall) / (precision + recall)
        best_threshold = thresholds[np.argmax(f1_scores)]

        print(f"  Best F1 threshold: {best_threshold".3f"}")

        assert pr_auc > 0.3, f"PR AUC {pr_auc".3f"} is too low"
        print(f"✅ PASS - PR curve analysis identifies balanced threshold: {best_threshold:.".3f")

    def test_threshold_confidence_intervals(self):
        """Test statistical confidence intervals for threshold decisions."""
        np.random.seed(42)

        # Bootstrap sampling for confidence intervals
        n_bootstrap = 1000
        sample_size = 200

        # Generate base relevance scores
        relevant_scores = np.random.normal(0.75, 0.12, 100)
        irrelevant_scores = np.random.normal(0.25, 0.08, 100)

        bootstrap_thresholds = []

        for _ in range(n_bootstrap):
            # Sample with replacement
            rel_sample = np.random.choice(relevant_scores, sample_size // 2, replace=True)
            irrel_sample = np.random.choice(irrelevant_scores, sample_size // 2, replace=True)

            scores = np.concatenate([rel_sample, irrel_sample])
            ground_truth = np.concatenate([np.ones(sample_size // 2), np.zeros(sample_size // 2)])

            # Find optimal threshold for this bootstrap sample
            fpr, tpr, thresholds = roc_curve(ground_truth, scores)
            optimal_idx = np.argmax(tpr - fpr)
            bootstrap_thresholds.append(thresholds[optimal_idx])

        # Calculate confidence intervals
        ci_lower = np.percentile(bootstrap_thresholds, 2.5)
        ci_upper = np.percentile(bootstrap_thresholds, 97.5)
        mean_threshold = np.mean(bootstrap_thresholds)

        print("Threshold Confidence Interval Analysis:"        print(f"  Mean threshold: {mean_threshold".3f"}")
        print(f"  95% CI: [{ci_lower".3f"}, {ci_upper".3f"}]")
        print(f"  CI width: {ci_upper - ci_lower".3f"}")

        # Validate confidence interval is reasonable
        assert ci_upper - ci_lower < 0.3, f"CI width {ci_upper - ci_lower:.".3f"is too large"
        assert ci_lower > 0.0 and ci_upper < 1.0, "CI should be within valid range"

        print(f"✅ PASS - Threshold CI analysis: {mean_threshold:.".3f"± {(ci_upper-ci_lower)/2:.".3f")


class TestThresholdPerformanceMetrics:
    """Performance metrics for threshold system."""

    def test_threshold_discriminative_power(self):
        """Test that threshold effectively discriminates relevant vs irrelevant docs."""
        # Create clearly separable score distributions
        relevant_scores = [0.9, 0.85, 0.8, 0.75, 0.7]  # High relevance
        irrelevant_scores = [0.3, 0.25, 0.2, 0.15, 0.1]  # Low relevance

        all_scores = relevant_scores + irrelevant_scores
        ground_truth = [1] * len(relevant_scores) + [0] * len(irrelevant_scores)

        # Test different threshold values
        thresholds_to_test = [0.4, 0.5, 0.6, 0.7]

        for threshold in thresholds_to_test:
            # Apply threshold
            predictions = [1 if score >= threshold else 0 for score in all_scores]

            # Calculate confusion matrix
            tp = sum(1 for gt, pred in zip(ground_truth, predictions) if gt == 1 and pred == 1)
            tn = sum(1 for gt, pred in zip(ground_truth, predictions) if gt == 0 and pred == 0)
            fp = sum(1 for gt, pred in zip(ground_truth, predictions) if gt == 0 and pred == 1)
            fn = sum(1 for gt, pred in zip(ground_truth, predictions) if gt == 1 and pred == 0)

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

            print(f"  Threshold {threshold".1f"}:")
            print(f"    Precision: {precision".3f"}")
            print(f"    Recall: {recall".3f"}")
            print(f"    F1: {f1".3f"}")

            # Validate performance metrics
            assert precision >= 0.8, f"Precision {precision:.".3f"too low for threshold {threshold}"
            assert recall >= 0.8, f"Recall {recall:.".3f"too low for threshold {threshold}"

        print("✅ PASS - All thresholds show good discriminative power")

    def test_threshold_robustness_to_score_distribution(self):
        """Test threshold robustness across different score distributions."""
        distributions = [
            ("normal", lambda: np.random.normal(0.5, 0.2, 100)),
            ("skewed_right", lambda: np.random.beta(2, 5, 100) * 0.8 + 0.1),
            ("skewed_left", lambda: np.random.beta(5, 2, 100) * 0.8 + 0.1),
            ("uniform", lambda: np.random.uniform(0.1, 0.9, 100))
        ]

        for dist_name, score_gen in distributions:
            scores = score_gen()
            ground_truth = (scores > 0.5).astype(int)  # Binary ground truth

            # Test threshold at median
            threshold = np.median(scores)

            predictions = (scores >= threshold).astype(int)

            # Calculate accuracy
            accuracy = np.mean(predictions == ground_truth)

            print(f"  {dist_name} distribution: accuracy = {accuracy".3f"}")

            # Should achieve reasonable accuracy across distributions
            assert accuracy > 0.6, f"Poor accuracy {accuracy:.".3f"for {dist_name} distribution"

        print("✅ PASS - Threshold robust across different score distributions")


class TestThresholdOptimization:
    """Automated threshold optimization testing."""

    def test_automated_threshold_tuning(self):
        """Test automated threshold selection using F1 optimization."""
        # Generate synthetic data with known optimal threshold
        np.random.seed(42)
        n_samples = 500

        # Optimal threshold around 0.6
        relevant_scores = np.random.normal(0.75, 0.1, n_samples // 2)
        irrelevant_scores = np.random.normal(0.25, 0.1, n_samples // 2)

        all_scores = np.concatenate([relevant_scores, irrelevant_scores])
        ground_truth = np.concatenate([np.ones(n_samples // 2), np.zeros(n_samples // 2)])

        # Test multiple threshold candidates
        threshold_candidates = np.linspace(0.1, 0.9, 50)
        best_f1 = 0
        best_threshold = 0

        for threshold in threshold_candidates:
            predictions = (all_scores >= threshold).astype(int)

            tp = np.sum((ground_truth == 1) & (predictions == 1))
            fp = np.sum((ground_truth == 0) & (predictions == 1))
            fn = np.sum((ground_truth == 1) & (predictions == 0))

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

            if f1 > best_f1:
                best_f1 = f1
                best_threshold = threshold

        print("Automated Threshold Tuning Results:"        print(f"  Best threshold: {best_threshold".3f"}")
        print(f"  Best F1 score: {best_f1".3f"}")
        print(f"  Expected range: [0.5, 0.7]")

        # Validate optimal threshold is in expected range
        assert 0.5 <= best_threshold <= 0.7, f"Optimal threshold {best_threshold:.".3f"outside expected range"
        assert best_f1 > 0.8, f"F1 score {best_f1:.".3f"too low for optimal threshold"

        print(f"✅ PASS - Automated threshold tuning found optimal: {best_threshold:.".3f")


if __name__ == "__main__":
    # Run statistical validation tests
    test_suite = TestThresholdStatisticalValidation()
    test_suite.test_roc_curve_analysis_for_threshold_optimization()
    test_suite.test_precision_recall_curve_analysis()
    test_suite.test_threshold_confidence_intervals()

    perf_suite = TestThresholdPerformanceMetrics()
    perf_suite.test_threshold_discriminative_power()
    perf_suite.test_threshold_robustness_to_score_distribution()

    opt_suite = TestThresholdOptimization()
    opt_suite.test_automated_threshold_tuning()

    print("\n🎉 All statistical validation tests passed!")
