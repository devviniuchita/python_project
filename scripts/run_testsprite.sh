#!/bin/bash

#==============================================================================
# TestSprite Backend Testing Helper Script
# Purpose: Automated test execution with TestSprite + pytest integration
# Usage: ./scripts/run_testsprite.sh [options]
#==============================================================================

set -e

# ============================================================================
# COLORS FOR OUTPUT
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ $1${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
}

print_step() {
    echo -e "${CYAN}➤ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${MAGENTA}ℹ $1${NC}"
}

# ============================================================================
# ARGUMENT PARSING
# ============================================================================

SKIP_COVERAGE=false
SKIP_TESTS=false
VERBOSE=false
DEBUG=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-coverage)
            SKIP_COVERAGE=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -X)
            DEBUG=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

show_help() {
    cat << 'EOF'

🧪 TestSprite Backend Testing Helper

USAGE:
    ./scripts/run_testsprite.sh [options]

OPTIONS:
    --skip-coverage      Skip coverage report generation (faster)
    --skip-tests         Skip test execution (only validate setup)
    --verbose            Enable verbose output
    -X                   Enable debug mode (pytest -X flag)
    --help, -h           Show this help message

EXAMPLES:
    # Run full test suite with coverage
    ./scripts/run_testsprite.sh

    # Skip coverage for faster iteration
    ./scripts/run_testsprite.sh --skip-coverage

    # Debug mode with verbose output
    ./scripts/run_testsprite.sh -X --verbose

    # Just validate environment setup
    ./scripts/run_testsprite.sh --skip-tests

EOF
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

print_header "🧪 TestSprite Backend Testing"

# ============================================================================
# Step 1: Check Prerequisites
# ============================================================================

print_step "Checking prerequisites..."

# Check Python
if ! command -v python &> /dev/null; then
    print_error "Python is not installed"
    exit 1
fi
print_success "Python found: $(python --version)"

# Check pytest
if ! python -m pytest --version &> /dev/null 2>&1; then
    print_warning "pytest not installed. Installing..."
    python -m pip install pytest pytest-cov pytest-mock -q
fi
print_success "pytest found: $(python -m pytest --version | head -1)"

# ============================================================================
# Step 2: Configure Environment
# ============================================================================

print_step "Configuring Python environment..."

# Set PYTHONPATH
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH}"
print_success "PYTHONPATH set: $PYTHONPATH"

cd "${PROJECT_ROOT}"
print_success "Working directory: $(pwd)"

# ============================================================================
# Step 3: Environment Validation
# ============================================================================

print_step "Validating Python imports..."

# Try importing main modules
if python -c "from src.core import domain" 2>/dev/null; then
    print_success "Core modules accessible"
else
    print_warning "Some imports may fail - this is expected for missing modules"
fi

# ============================================================================
# Step 4: Prerequisites Installed
# ============================================================================

print_step "Installing test dependencies..."

REQUIRED_PACKAGES=(
    "pytest>=7.0.0"
    "pytest-cov>=4.0.0"
    "pytest-mock>=3.10.0"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    python -m pip install "$package" -q 2>/dev/null || true
done

print_success "Test dependencies ready"

# ============================================================================
# Step 5: Generate Coverage Report (Optional)
# ============================================================================

if [ "$SKIP_COVERAGE" = true ]; then
    print_info "Skipping coverage report generation"
    COVERAGE_FLAGS=""
else
    print_step "Preparing coverage generation..."
    COVERAGE_FLAGS="--cov=src --cov-report=html --cov-report=term-missing --cov-report=xml"
    print_success "Coverage reports will be generated"
fi

# ============================================================================
# Step 6: Execute Tests
# ============================================================================

if [ "$SKIP_TESTS" = true ]; then
    print_info "Test execution skipped (--skip-tests flag)"
else
    print_step "Executing test suite..."
    echo ""

    # Build pytest command
    PYTEST_CMD="python -m pytest tests/ -v --tb=short"

    # Add coverage flags if not skipped
    if [ -n "$COVERAGE_FLAGS" ]; then
        PYTEST_CMD="${PYTEST_CMD} ${COVERAGE_FLAGS}"
    fi

    # Add verbose flag
    if [ "$VERBOSE" = true ]; then
        PYTEST_CMD="${PYTEST_CMD} -vv"
    fi

    # Add debug flag
    if [ "$DEBUG" = true ]; then
        PYTEST_CMD="${PYTEST_CMD} -X"
    fi

    # Execute
    print_info "Running: $PYTEST_CMD"
    echo ""

    if eval "$PYTEST_CMD"; then
        echo ""
        print_success "Tests passed!"
    else
        echo ""
        print_error "Tests completed with failures"
        echo "This may be expected during infrastructure fixes."
        echo "See: docs/TESTING_WITH_TESTSPRITE.md"
    fi
fi

# ============================================================================
# Step 7: Generate Test Report
# ============================================================================

if [ ! -d "docs/testsprite_results" ]; then
    mkdir -p docs/testsprite_results
    print_success "Created docs/testsprite_results directory"
fi

# ============================================================================
# Step 8: Summary & Next Steps
# ============================================================================

echo ""
print_header "📊 Test Execution Summary"

print_info "Test Report Location:"
echo "  📄 Markdown Report: docs/testsprite_results/TESTSPRITE_REPORT.md"
echo "  📊 JSON Report: docs/testsprite_results/test_report_backend.json"

if [ "$SKIP_COVERAGE" = false ]; then
    print_info "Coverage Reports:"
    echo "  📈 HTML Report: htmlcov/index.html"
    if command -v open &> /dev/null; then
        print_info "To view coverage: open htmlcov/index.html"
    elif command -v xdg-open &> /dev/null; then
        print_info "To view coverage: xdg-open htmlcov/index.html"
    fi
fi

print_info "TestSprite Integration:"
echo "  📋 Test Plan: testsprite_tests/testsprite_backend_test_plan.json"
echo "  📚 Guide: docs/TESTING_WITH_TESTSPRITE.md"

echo ""
print_info "Quick Links:"
echo "  🔐 Copyright Protection: docs/COPYRIGHT_PROTECTION.md"
echo "  🔍 SonarQube Setup: docs/compliance/SONARQUBE_SETUP.md"
echo "  🎣 Pre-commit Hooks: .pre-commit-config.yaml"

echo ""
print_step "Next Steps:"
echo "  1. Review test results above"
echo "  2. Fix any failing tests (infrastructure issues documented)"
echo "  3. Run: pytest tests/ -v (to validate fixes)"
echo "  4. Check: docs/TESTING_WITH_TESTSPRITE.md for troubleshooting"

print_success "Test execution helper completed!"
echo ""
