#!/bin/bash

# ========================================
# SonarQube Local Testing Script
# ========================================
# Purpose: Automate local SonarQube testing
# Usage: ./scripts/run_sonarqube.sh [options]
#
# Requirements:
#   - Python 3.12+
#   - pytest-cov installed
#   - sonar-scanner installed
#   - .env file configured with SONAR_HOST_URL and SONAR_LOGIN

set -e

# ========================================
# Colors for output
# ========================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========================================
# Helper Functions
# ========================================

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $1"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ========================================
# Check Prerequisites
# ========================================

check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check Python
    if ! command -v python &> /dev/null; then
        print_error "Python not found. Please install Python 3.12+"
        exit 1
    fi
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"

    # Check pytest
    if ! python -c "import pytest" 2>/dev/null; then
        print_error "pytest not installed. Run: pip install pytest pytest-cov"
        exit 1
    fi
    print_success "pytest installed"

    # Check sonar-scanner
    if ! command -v sonar-scanner &> /dev/null; then
        print_warning "sonar-scanner not found in PATH"
        print_info "Install it using:"
        echo "  macOS: brew install sonar-scanner"
        echo "  Linux: sudo apt-get install sonarqube-scanner"
        echo "  Windows: Download from https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/scanners/sonarscanner/"
        exit 1
    fi
    print_success "sonar-scanner installed"

    # Check .env file
    if [ ! -f .env ]; then
        print_error ".env file not found"
        print_info "Create .env from .env.example:"
        echo "  cp .env.example .env"
        echo "  Edit .env with your SonarQube credentials"
        exit 1
    fi
    print_success ".env file found"
}

# ========================================
# Load Environment Variables
# ========================================

load_env() {
    print_header "Loading Environment Configuration"

    set -a
    source .env
    set +a

    if [ -z "$SONAR_LOGIN" ]; then
        print_error "SONAR_LOGIN not set in .env"
        exit 1
    fi

    if [ -z "$SONAR_HOST_URL" ]; then
        print_error "SONAR_HOST_URL not set in .env"
        exit 1
    fi

    print_success "SONAR_HOST_URL: $SONAR_HOST_URL"
    print_success "SONAR_PROJECT_KEY: ${SONAR_PROJECT_KEY:-python_project}"
    print_info "SONAR_LOGIN: ******* (token hidden for security)"
}

# ========================================
# Run Tests with Coverage
# ========================================

generate_coverage() {
    print_header "Generating Coverage Report"

    if [ ! -d "tests" ]; then
        print_warning "tests/ directory not found. Skipping coverage generation."
        return 0
    fi

    print_info "Running pytest with coverage..."
    python -m pytest \
        --cov=src \
        --cov-report=xml:coverage.xml \
        --cov-report=html:htmlcov \
        --cov-report=term-missing \
        --verbose \
        --tb=short \
        tests/ || {
        print_warning "Some tests failed, but continuing with SonarQube analysis..."
    }

    if [ -f "coverage.xml" ]; then
        print_success "Coverage report generated: coverage.xml"
    fi
}

# ========================================
# Run SonarQube Scan
# ========================================

run_sonar_scan() {
    print_header "Running SonarQube Analysis"

    print_info "Starting sonar-scanner..."

    sonar-scanner \
        -Dsonar.projectKey="${SONAR_PROJECT_KEY:-python_project}" \
        -Dsonar.sources=src,scripts \
        -Dsonar.tests=tests \
        -Dsonar.python.version=3.12 \
        -Dsonar.python.coverage.reportPath=coverage.xml \
        -Dsonar.exclusions="**/__pycache__/**,**/.venv/**,**/migrations/**" \
        -Dsonar.coverage.exclusions="tests/**,setup.py,**/__init__.py" \
        -Dsonar.host.url="$SONAR_HOST_URL" \
        -Dsonar.login="$SONAR_LOGIN" \
        -Dsonar.organization="${SONAR_ORGANIZATION}" \
        ${SONAR_EXTRA_ARGS} || {
        print_error "SonarQube analysis failed"
        exit 1
    }

    print_success "SonarQube analysis completed"
}

# ========================================
# Display Results
# ========================================

display_results() {
    print_header "Analysis Results"

    echo ""
    print_info "Coverage Report: htmlcov/index.html (open in browser)"
    print_info "SonarQube Dashboard: $SONAR_HOST_URL/dashboard?id=${SONAR_PROJECT_KEY:-python_project}"
    echo ""

    if [ -f "coverage.xml" ]; then
        print_success "Coverage data file created: coverage.xml"
    fi

    print_success "Analysis completed successfully!"
}

# ========================================
# Help Function
# ========================================

show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    --help              Show this help message
    --skip-coverage     Skip coverage generation (faster)
    --skip-tests        Skip running tests
    --verbose           Enable verbose output
    -X                  Pass -X flag to sonar-scanner (debug mode)

Examples:
    # Full analysis
    $0

    # Skip coverage generation for faster testing
    $0 --skip-coverage

    # Debug mode
    $0 -X

    # Skip tests, only analyze existing code
    $0 --skip-tests

Environment Variables (set in .env):
    SONAR_HOST_URL      SonarQube server URL (default: https://sonarcloud.io)
    SONAR_LOGIN         Authentication token
    SONAR_PROJECT_KEY   Project key (default: python_project)
    SONAR_ORGANIZATION  Organization key (for SonarQube Cloud)

EOF
}

# ========================================
# Parse Arguments
# ========================================

SKIP_COVERAGE=false
SKIP_TESTS=false
SONAR_DEBUG_MODE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            show_help
            exit 0
            ;;
        --skip-coverage)
            SKIP_COVERAGE=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --verbose)
            set -x
            shift
            ;;
        -X)
            SONAR_DEBUG_MODE="-X"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# ========================================
# Main Execution
# ========================================

main() {
    print_header "SonarQube Local Analysis - python_project"

    check_prerequisites
    load_env

    if [ "$SKIP_TESTS" = false ]; then
        if [ "$SKIP_COVERAGE" = false ]; then
            generate_coverage
        fi
    fi

    run_sonar_scan $SONAR_DEBUG_MODE
    display_results
}

# Execute main function
main "$@"
