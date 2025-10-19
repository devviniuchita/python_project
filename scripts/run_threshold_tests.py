#!/usr/bin/env python3
"""
Script to run comprehensive threshold tests without pytest dependency.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_test_function(test_class, test_method_name):
    """Run a specific test method and return success status."""
    try:
        # Create test instance
        test_instance = test_class()

        # Get the test method
        test_method = getattr(test_instance, test_method_name)

        # Run the test
        print(f"\n🧪 Running {test_class.__name__}.{test_method_name}")
        test_method()
        print(f"✅ PASS - {test_class.__name__}.{test_method_name}")
        return True

    except Exception as e:
        print(f"❌ FAIL - {test_class.__name__}.{test_method_name}: {e}")
        return False


def main():
    """Run all threshold tests."""
    print("🚀 Running Comprehensive Threshold Tests")
    print("=" * 60)

    # Import test modules
    try:
        from tests.test_threshold_statistical_validation import (
            TestThresholdOptimization,
            TestThresholdStatisticalValidation,
        )

        print("✅ Statistical validation tests imported")
    except ImportError as e:
        print(f"❌ Failed to import statistical tests: {e}")
        return False

    try:
        from tests.test_threshold_performance import TestThresholdPerformance

        print("✅ Performance tests imported")
    except ImportError as e:
        print(f"❌ Failed to import performance tests: {e}")
        return False

    # Run statistical validation tests
    print("\n📊 STATISTICAL VALIDATION TESTS")
    print("-" * 40)

    stat_tests = [
        (
            TestThresholdStatisticalValidation,
            "test_roc_curve_analysis_for_threshold_optimization",
        ),
        (TestThresholdStatisticalValidation, "test_precision_recall_curve_analysis"),
        (TestThresholdStatisticalValidation, "test_threshold_confidence_intervals"),
    ]

    stat_results = []
    for test_class, test_method in stat_tests:
        stat_results.append(run_test_function(test_class, test_method))

    # Run performance tests
    print("\n⚡ PERFORMANCE TESTS")
    print("-" * 40)

    perf_tests = [
        (TestThresholdPerformance, "test_threshold_discriminative_power"),
        (TestThresholdPerformance, "test_threshold_robustness_to_score_distribution"),
        (TestThresholdOptimization, "test_automated_threshold_tuning"),
    ]

    perf_results = []
    for test_class, test_method in perf_tests:
        perf_results.append(run_test_function(test_class, test_method))

    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)

    total_stat_tests = len(stat_results)
    passed_stat_tests = sum(stat_results)
    total_perf_tests = len(perf_results)
    passed_perf_tests = sum(perf_results)

    print(f"Statistical Validation: {passed_stat_tests}/{total_stat_tests} passed")
    print(f"Performance Tests: {passed_perf_tests}/{total_perf_tests} passed")

    total_tests = total_stat_tests + total_perf_tests
    passed_tests = passed_stat_tests + passed_perf_tests

    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("⚠️  SOME TESTS FAILED")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
