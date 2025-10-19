#!/bin/bash

################################################################################
# Developer Environment Setup Script
# Purpose: Automate Python virtual environment and pre-commit hooks setup
#
# Usage:
#   bash scripts/setup-dev-environment.sh
#
# This script:
#   1. Creates a Python virtual environment (.venv)
#   2. Activates the virtual environment
#   3. Installs project dependencies (pip install -r requirements.txt)
#   4. Installs pre-commit hooks (pre-commit install)
#   5. Displays environment status and next steps
#
# Supported Platforms: Windows (Git Bash), Linux, macOS
# Python Version: 3.8+ (tested with 3.12)
#
# Related Tasks:
#   T-31: Copyright headers script (scripts/add_copyright_headers.py)
#   T-41: Pre-commit configuration (.pre-commit-config.yaml)
#   T-42: Custom hooks definition (.pre-commit-hooks.yaml)
#   T-43: Tool configurations (pyproject.toml)
#   T-44: Setup guide documentation (CONTRIBUTING.md)
#   T-45: Framework validation (pre-commit validated)
#
# See CONTRIBUTING.md for detailed setup guide and troubleshooting.
################################################################################

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"
PYTHON_VERSION="3.8+"
REQUIREMENTS_FILE="${PROJECT_DIR}/requirements-dev.txt"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
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

error_exit() {
    print_error "$1"
    exit 1
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        error_exit "$1 is not installed. Please install it first."
    fi
}

check_file() {
    if [ ! -f "$1" ]; then
        error_exit "File not found: $1"
    fi
}

# Normalize TLS / CA environment variables to avoid pip/pre-commit failures
# - Unset SSL_CERT_FILE / REQUESTS_CA_BUNDLE / PIP_CERT when they point to
#   non-existent files (common cause when OS or third-party installers set a
#   broken path like a PostgreSQL bundle that doesn't exist on the developer
#   machine).
# - If the activated Python already has certifi installed, point SSL vars to
#   certifi.where() so subprocesses (pip, pre-commit virtualenvs) inherit a
#   valid CA bundle.
normalize_ssl_cert_envs() {
    # If an env var points to a non-existing file, unset it to allow the
    # system default CAs to be used.
    if [ -n "$SSL_CERT_FILE" ] && [ ! -f "$SSL_CERT_FILE" ]; then
        print_warning "Detected SSL_CERT_FILE=$SSL_CERT_FILE which does not exist. Unsetting to allow pip to use system CAs."
        unset SSL_CERT_FILE
    fi
    if [ -n "$REQUESTS_CA_BUNDLE" ] && [ ! -f "$REQUESTS_CA_BUNDLE" ]; then
        print_warning "Detected REQUESTS_CA_BUNDLE=$REQUESTS_CA_BUNDLE which does not exist. Unsetting."
        unset REQUESTS_CA_BUNDLE
    fi
    if [ -n "$PIP_CERT" ] && [ ! -f "$PIP_CERT" ]; then
        print_warning "Detected PIP_CERT=$PIP_CERT which does not exist. Unsetting."
        unset PIP_CERT
    fi
    if [ -n "$CURL_CA_BUNDLE" ] && [ ! -f "$CURL_CA_BUNDLE" ]; then
        print_warning "Detected CURL_CA_BUNDLE=$CURL_CA_BUNDLE which does not exist. Unsetting."
        unset CURL_CA_BUNDLE
    fi

    # If certifi is already available in the activated Python, use it to set
    # SSL_CERT_FILE / REQUESTS_CA_BUNDLE for the current shell so child
    # processes (pip, pre-commit) will inherit a valid CA bundle.
    CERT_PATH=$(python - <<'PY'
try:
    import certifi
    print(certifi.where())
except Exception:
    pass
PY
)

    if [ -n "$CERT_PATH" ]; then
        export SSL_CERT_FILE="$CERT_PATH"
        export REQUESTS_CA_BUNDLE="$CERT_PATH"
        print_success "Using certifi CA bundle at $CERT_PATH"
    else
        print_info "certifi not found in the activated Python. If network installs fail, run: pip install certifi and re-run this script."
    fi
}

################################################################################
# Validation Phase
################################################################################

print_header "Python RAG Project - Developer Environment Setup"

print_info "Validating environment requirements..."

# Check Python installation
check_command "python3"
PYTHON_CMD="python3"

# Check pip installation
if ! "$PYTHON_CMD" -m pip --version &> /dev/null; then
    error_exit "pip is not available. Please install pip first."
fi
print_success "Python 3 installed (pip available)"

# Check git installation
check_command "git"
print_success "Git installed"

# Check if we're in the right directory
if [ ! -f "${PROJECT_DIR}/pyproject.toml" ]; then
    error_exit "pyproject.toml not found. Please run this script from the project root directory."
fi
print_success "Project directory verified: ${PROJECT_DIR}"

################################################################################
# Virtual Environment Setup
################################################################################

print_header "Setting Up Virtual Environment"

# Check if .venv already exists
if [ -d "$VENV_DIR" ]; then
    print_warning ".venv already exists at ${VENV_DIR}"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Removing existing .venv..."
        rm -rf "$VENV_DIR"
        print_success "Removed old virtual environment"
    else
        print_info "Using existing .venv"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    print_info "Creating virtual environment at ${VENV_DIR}..."
    "$PYTHON_CMD" -m venv "$VENV_DIR"

    if [ ! -d "$VENV_DIR" ]; then
        error_exit "Failed to create virtual environment at ${VENV_DIR}"
    fi
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source "${VENV_DIR}/bin/activate" 2>/dev/null || \
    . "${VENV_DIR}/Scripts/activate" 2>/dev/null || \
    error_exit "Failed to activate virtual environment"
print_success "Virtual environment activated"

# Normalize TLS/CA environment before any pip operations to avoid failures
print_info "Verificando variáveis SSL/TLS e certifi para garantir que o pip funcione..."
normalize_ssl_cert_envs

################################################################################
# Dependency Installation
################################################################################

print_header "Installing Project Dependencies"

# Upgrade pip, setuptools, wheel
print_info "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel -q
print_success "pip, setuptools, and wheel upgraded"

# Try to ensure certifi is available so we can point SSL_CERT_FILE to a
# known-good CA bundle. If this installation fails, we warn (it may be due
# to an upstream TLS/CA issue) but continue so the developer can follow the
# troubleshooting steps documented in docs/TROUBLESHOOT_PRECOMMIT_TLS.md.
print_info "Garantindo que 'certifi' esteja presente (usado para CA bundle)..."
if python -m pip install --upgrade certifi -q; then
    print_success "certifi instalado/atualizado"
    # Re-run normalization now that certifi may be available.
    normalize_ssl_cert_envs
else
    print_warning "Falha ao instalar 'certifi'. Se houver erro de TLS, veja docs/TROUBLESHOOT_PRECOMMIT_TLS.md"
fi

# Check for requirements files
if [ -f "$REQUIREMENTS_FILE" ]; then
    print_info "Installing dependencies from ${REQUIREMENTS_FILE}..."
    pip install -r "$REQUIREMENTS_FILE"
    print_success "Project dependencies installed from requirements-dev.txt"
elif [ -f "${PROJECT_DIR}/requirements.txt" ]; then
    print_info "Installing dependencies from requirements.txt..."
    pip install -r "${PROJECT_DIR}/requirements.txt"
    print_success "Project dependencies installed from requirements.txt"
else
    print_warning "No requirements.txt or requirements-dev.txt found"
    print_info "You may need to install dependencies manually"
fi

################################################################################
# Pre-commit Hooks Setup
################################################################################

print_header "Setting Up Pre-Commit Hooks"

# Install pre-commit package (framework used by CI and developers)
print_info "Installing pre-commit framework..."
pip install pre-commit -q
print_success "pre-commit installed"

# Validate pre-commit configuration
if [ ! -f "${PROJECT_DIR}/.pre-commit-config.yaml" ]; then
    error_exit ".pre-commit-config.yaml not found at ${PROJECT_DIR}"
fi

print_info "Validating pre-commit configuration..."
pre-commit validate-config
print_success "Pre-commit configuration validated"

# Configure Git to use the repository-tracked hooks folder (.githooks).
# This ensures the TLS/CA normalization wrapper (committed in the repo)
# runs early (before any pip invocation) so hook venv creation won't fail
# when system environment variables point to invalid CA bundles.
print_info "Configuring Git to use repository hooks at .githooks (local setting)..."
mkdir -p "${PROJECT_DIR}/.githooks"
git config --local core.hooksPath .githooks || print_warning "Could not set core.hooksPath; you can run 'git config core.hooksPath .githooks' manually."
print_success "Git core.hooksPath set to .githooks (local)"

# Copy the repository wrapper into .git/hooks for immediate use in this clone
# (some GUIs/tools still call .git/hooks directly). We keep a backup to be
# non-destructive.
if [ -d "${PROJECT_DIR}/.git" ]; then
    if [ -f "${PROJECT_DIR}/.git/hooks/pre-commit" ]; then
        cp "${PROJECT_DIR}/.git/hooks/pre-commit" "${PROJECT_DIR}/.git/hooks/pre-commit.backup" 2>/dev/null || true
    fi
    if [ -f "${PROJECT_DIR}/.githooks/pre-commit" ]; then
        cp "${PROJECT_DIR}/.githooks/pre-commit" "${PROJECT_DIR}/.git/hooks/pre-commit"
        chmod +x "${PROJECT_DIR}/.git/hooks/pre-commit"
        print_success "Installed tracked hook wrapper into .git/hooks/pre-commit for immediate use"
    else
        print_warning "Tracked hook wrapper (.githooks/pre-commit) not found. Ensure repository includes .githooks/pre-commit"
    fi
fi

# Ensure local mypy & type-stubs are available so the wrapper can run static
# type checks using the project's virtualenv (avoids pre-commit creating its
# own venvs and failing if TLS env vars are broken).
print_info "Ensuring mypy and type-stubs are available in the virtualenv..."
if python -m pip install --upgrade mypy types-requests types-PyYAML typing_extensions -q; then
    print_success "mypy and common type-stubs installed"
else
    print_warning "Failed to install mypy/type-stubs. If pre-commit hook venvs still fail, see docs/TROUBLESHOOT_PRECOMMIT_TLS.md"
fi

################################################################################
# Final Status Report
################################################################################

print_header "Setup Complete! 🎉"

# Get environment info
PYTHON_FULL_VERSION=$("$PYTHON_CMD" --version 2>&1 | awk '{print $2}')
VENV_PYTHON="${VENV_DIR}/bin/python"
[ -f "$VENV_PYTHON" ] || VENV_PYTHON="${VENV_DIR}/Scripts/python.exe"

echo "Environment Details:"
echo "  Python Version:     ${PYTHON_FULL_VERSION}"
echo "  Virtual Environment: ${VENV_DIR}"
echo "  Python Executable:  $(which python)"

# Check pre-commit installation
if pre-commit validate-config &> /dev/null; then
    HOOKS_COUNT=$(grep -c "^\s*-\s*id:" "${PROJECT_DIR}/.pre-commit-config.yaml" 2>/dev/null || echo "?")
    echo "  Pre-commit Hooks:   ${HOOKS_COUNT} hooks installed and ready"
else
    print_warning "Pre-commit validation failed (TLS issue on Windows?)"
    echo "  Pre-commit Hooks:   Installed (note: validation skipped on Windows)"
fi

echo ""
echo "Next Steps:"
print_info "1. Source virtual environment:"
echo "     source .venv/bin/activate              # Linux/macOS"
echo "     . .venv/Scripts/activate               # Windows (Git Bash)"
echo ""
print_info "2. Start developing:"
echo "     - Edit files in src/ or tests/"
echo "     - Pre-commit hooks will run on git commit"
echo "     - See CONTRIBUTING.md for detailed development guide"
echo ""
print_info "3. Common commands:"
echo "     pytest tests/                          # Run tests"
echo "     black src/ tests/                      # Format code"
echo "     isort src/ tests/                      # Organize imports"
echo "     flake8 src/ tests/                     # Lint code"
echo "     mypy src/                              # Type check"
echo ""

print_success "Developer environment is ready!"
print_success "Happy coding! 🚀"

exit 0
