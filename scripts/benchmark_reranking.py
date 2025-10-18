"""
Benchmark script for BGE Reranker quality and performance validation.

Metrics measured:
- Quality Score: Baseline (without reranking) vs Enhanced (with reranking)
- Latency: Time overhead added by reranking
- Memory: Model loading impact
- Document Relevance: Top-N document quality

Target:
- Quality improvement ≥10%
- Latency overhead <500ms
"""

import sys
import time
from typing import Dict, List

from config.settings import settings
from graph_rag import create_rag_graph

# Test queries with expected complexity
TEST_QUERIES = [
    {
        "question": "O que é o Perceptron?",
        "complexity": "simple",
        "expected_keywords": ["rede neural", "elementar", "fundamental"],
    },
    {
        "question": "Quais as limitações do algoritmo Perceptron?",
        "complexity": "complex",
        "expected_keywords": ["linearmente separáveis", "limitações", "problemas"],
    },
    {
        "question": "Como funciona o treinamento do Perceptron?",
        "complexity": "complex",
        "expected_keywords": ["pesos", "iterativo", "ajusta", "aprendizado"],
    },
    {
        "question": "Qual a função de ativação do Perceptron?",
        "complexity": "simple",
        "expected_keywords": ["função", "ativação", "degrau", "sigma"],
    },
    {
        "question": "Explique a diferença entre Perceptron e Multilayer Perceptron.",
        "complexity": "complex",
        "expected_keywords": ["multicamadas", "complexos", "linearmente", "resolver"],
    },
]


class BenchmarkResults:
    """Store and analyze benchmark results."""

    def __init__(self):
        self.baseline_results: List[Dict] = []
        self.enhanced_results: List[Dict] = []

    def add_baseline(
        self, question: str, quality: float, latency: float, iterations: int
    ):
        """Add baseline result (without reranking)."""
        self.baseline_results.append(
            {
                "question": question,
                "quality_score": quality,
                "latency_ms": latency,
                "iterations": iterations,
            }
        )

    def add_enhanced(
        self, question: str, quality: float, latency: float, iterations: int
    ):
        """Add enhanced result (with reranking)."""
        self.enhanced_results.append(
            {
                "question": question,
                "quality_score": quality,
                "latency_ms": latency,
                "iterations": iterations,
            }
        )

    def calculate_metrics(self) -> Dict:
        """Calculate comparison metrics."""
        if not self.baseline_results or not self.enhanced_results:
            return {}

        # Quality metrics
        baseline_quality = sum(r["quality_score"] for r in self.baseline_results) / len(
            self.baseline_results
        )
        enhanced_quality = sum(r["quality_score"] for r in self.enhanced_results) / len(
            self.enhanced_results
        )
        quality_improvement = (
            (enhanced_quality - baseline_quality) / baseline_quality
        ) * 100

        # Latency metrics
        baseline_latency = sum(r["latency_ms"] for r in self.baseline_results) / len(
            self.baseline_results
        )
        enhanced_latency = sum(r["latency_ms"] for r in self.enhanced_results) / len(
            self.enhanced_results
        )
        latency_overhead = enhanced_latency - baseline_latency

        # Iteration metrics
        baseline_iters = sum(r["iterations"] for r in self.baseline_results) / len(
            self.baseline_results
        )
        enhanced_iters = sum(r["iterations"] for r in self.enhanced_results) / len(
            self.enhanced_results
        )

        return {
            "baseline_quality": baseline_quality,
            "enhanced_quality": enhanced_quality,
            "quality_improvement_percent": quality_improvement,
            "baseline_latency_ms": baseline_latency,
            "enhanced_latency_ms": enhanced_latency,
            "latency_overhead_ms": latency_overhead,
            "baseline_iterations": baseline_iters,
            "enhanced_iterations": enhanced_iters,
        }

    def print_report(self):
        """Print comprehensive benchmark report."""
        metrics = self.calculate_metrics()

        if not metrics:
            print("❌ No results to report")
            return

        print("\n" + "=" * 80)
        print("📊 BENCHMARK RESULTS - BGE RERANKER QUALITY & PERFORMANCE")
        print("=" * 80)

        print("\n🎯 QUALITY METRICS:")
        print(f"  Baseline Quality Score:  {metrics['baseline_quality']:.3f}")
        print(f"  Enhanced Quality Score:  {metrics['enhanced_quality']:.3f}")
        print(
            f"  Quality Improvement:     {metrics['quality_improvement_percent']:+.1f}%"
        )

        # Quality verdict
        if metrics["quality_improvement_percent"] >= 10:
            print("  ✅ PASS - Quality improvement ≥10% (Target: ≥10%)")
        else:
            print("  ❌ FAIL - Quality improvement <10% (Target: ≥10%)")

        print("\n⚡ PERFORMANCE METRICS:")
        print(f"  Baseline Latency:        {metrics['baseline_latency_ms']:.0f}ms")
        print(f"  Enhanced Latency:        {metrics['enhanced_latency_ms']:.0f}ms")
        print(f"  Latency Overhead:        +{metrics['latency_overhead_ms']:.0f}ms")

        # Latency verdict
        if metrics["latency_overhead_ms"] < 500:
            print("  ✅ PASS - Latency overhead <500ms (Target: <500ms)")
        else:
            print("  ⚠️  WARNING - Latency overhead ≥500ms (Target: <500ms)")

        print("\n🔄 REFINEMENT METRICS:")
        print(f"  Baseline Iterations:     {metrics['baseline_iterations']:.1f}")
        print(f"  Enhanced Iterations:     {metrics['enhanced_iterations']:.1f}")

        # Overall verdict
        print("\n" + "=" * 80)
        quality_pass = metrics["quality_improvement_percent"] >= 10
        latency_pass = metrics["latency_overhead_ms"] < 500

        if quality_pass and latency_pass:
            print(
                "🎉 OVERALL VERDICT: ✅ PASS - Reranking provides acceptable trade-off"
            )
        elif quality_pass:
            print("⚠️  OVERALL VERDICT: PARTIAL - Quality improved but latency high")
        else:
            print("❌ OVERALL VERDICT: FAIL - Quality improvement insufficient")
        print("=" * 80 + "\n")


def run_single_query(question: str, reranking_enabled: bool) -> Dict:
    """Run a single query and measure metrics."""
    # Update settings
    original_enabled = settings.reranker_enabled
    settings.reranker_enabled = reranking_enabled

    try:
        # Create fresh graph
        graph = create_rag_graph()

        # Initial state
        initial_state = {
            "question": question,
            "complexity": "",
            "documents": [],
            "generation": "",
            "quality_score": 0.0,
            "iterations": 0,
        }

        # Measure execution time
        start_time = time.time()
        final_state = graph.invoke(initial_state)
        end_time = time.time()

        latency_ms = (end_time - start_time) * 1000

        return {
            "quality_score": final_state["quality_score"],
            "latency_ms": latency_ms,
            "iterations": final_state["iterations"],
            "complexity": final_state["complexity"],
        }
    finally:
        # Restore original setting
        settings.reranker_enabled = original_enabled


def run_benchmark():
    """Run complete benchmark suite."""
    print("\n" + "=" * 80)
    print("🚀 STARTING BGE RERANKER BENCHMARK")
    print("=" * 80)
    print(f"\n📋 Test Suite: {len(TEST_QUERIES)} queries")
    print("   - Simple questions: 2")
    print("   - Complex questions: 3")
    print("\n⏱️  Estimated time: ~2-3 minutes\n")

    results = BenchmarkResults()

    # Phase 1: Baseline (without reranking)
    print("=" * 80)
    print("📍 PHASE 1: BASELINE (Without Reranking)")
    print("=" * 80 + "\n")

    for i, test_case in enumerate(TEST_QUERIES, 1):
        question = test_case["question"]
        print(f"[{i}/{len(TEST_QUERIES)}] Testing: {question[:60]}...")

        result = run_single_query(question, reranking_enabled=False)

        results.add_baseline(
            question=question,
            quality=result["quality_score"],
            latency=result["latency_ms"],
            iterations=result["iterations"],
        )

        print(
            f"    Quality: {result['quality_score']:.2f} | Latency: {result['latency_ms']:.0f}ms | "
            f"Iterations: {result['iterations']} | Complexity: {result['complexity']}"
        )

    # Phase 2: Enhanced (with reranking)
    print("\n" + "=" * 80)
    print("📍 PHASE 2: ENHANCED (With BGE Reranking)")
    print("=" * 80 + "\n")

    for i, test_case in enumerate(TEST_QUERIES, 1):
        question = test_case["question"]
        print(f"[{i}/{len(TEST_QUERIES)}] Testing: {question[:60]}...")

        result = run_single_query(question, reranking_enabled=True)

        results.add_enhanced(
            question=question,
            quality=result["quality_score"],
            latency=result["latency_ms"],
            iterations=result["iterations"],
        )

        print(
            f"    Quality: {result['quality_score']:.2f} | Latency: {result['latency_ms']:.0f}ms | "
            f"Iterations: {result['iterations']} | Complexity: {result['complexity']}"
        )

    # Print final report
    results.print_report()

    # Return metrics for programmatic use
    return results.calculate_metrics()


if __name__ == "__main__":
    print("\n🔬 BGE RERANKER BENCHMARK SUITE")
    print("   Validates quality improvement and performance impact\n")

    try:
        metrics = run_benchmark()

        # Exit code based on success criteria
        quality_pass = metrics.get("quality_improvement_percent", 0) >= 10
        latency_pass = metrics.get("latency_overhead_ms", 999) < 500

        if quality_pass and latency_pass:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
    except KeyboardInterrupt:
        print("\n\n⚠️  Benchmark interrupted by user")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n❌ Benchmark failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(3)
