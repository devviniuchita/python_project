#!/usr/bin/env python3
"""precommit_wrapper.py

Normalize TLS/CA environment variables and forward execution to the project's
pre-commit runner. This prevents pip from failing to install hook venvs when
system-wide env vars point to invalid CA bundles (common on Windows when
third-party installers set broken SSL_CERT_FILE values).

Usage:
    python scripts/precommit_wrapper.py [pre-commit args...]

Example:
    python scripts/precommit_wrapper.py run --all-files

Behavior:
  - If `certifi` is available in the active Python, sets SSL_CERT_FILE and
    REQUESTS_CA_BUNDLE to certifi.where().
  - If an existing env var points to a non-existent file, it will be unset.
  - Executes `python -m pre_commit` with the normalized environment.
"""
from __future__ import annotations

import os
import shutil
import sys
from typing import List


def _is_valid_file(path: str) -> bool:
    try:
        return bool(path) and os.path.isfile(path)
    except Exception:
        return False


def normalize_ssl_env() -> None:
    """Normalize SSL-related environment variables for child processes.

    Strategy:
    - If certifi is available, set SSL_CERT_FILE and REQUESTS_CA_BUNDLE to
      certifi.where() so child processes (pip, pre-commit) use a reliable
      CA bundle.
    - If any SSL env var points to a non-existent file, unset it.
    """
    candidates = ["SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "PIP_CERT", "CURL_CA_BUNDLE"]

    # Unset invalid file paths first (helps fallback behavior)
    for name in candidates:
        val = os.environ.get(name)
        if val and not _is_valid_file(val):
            # Clear noisy/invalid values to allow system defaults or certifi
            # to be used instead.
            print(
                f"[precommit-wrapper] Unsetting {name} (invalid path: {val})",
                file=sys.stderr,
            )
            os.environ.pop(name, None)

    # If certifi is available, explicitly point SSL vars to it so pip/requests
    # will use the bundled CA set.
    try:
        import certifi

        cert_path = certifi.where()
        if _is_valid_file(cert_path):
            os.environ["SSL_CERT_FILE"] = cert_path
            os.environ["REQUESTS_CA_BUNDLE"] = cert_path
            # Also hint pip (PIP_CERT) in case some pip versions consult it
            os.environ["PIP_CERT"] = cert_path
            print(
                f"[precommit-wrapper] Using certifi CA bundle at: {cert_path}",
                file=sys.stderr,
            )
            return
    except Exception:
        # certifi not available or failed to import — leave env as-is or
        # already-unset values removed above.
        pass


def _find_python_executable() -> str:
    # Use the current Python interpreter (best option inside activated venv).
    return sys.executable


def main(argv: List[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    normalize_ssl_env()

    python = _find_python_executable()
    # Build command: python -m pre_commit <args...>
    cmd = [python, "-m", "pre_commit"] + list(argv)

    # Prefer exec so the OS replaces the wrapper process with pre-commit
    # and the normalized env is inherited by any sub-processes.
    try:
        print(f"[precommit-wrapper] Executing: {' '.join(cmd)}", file=sys.stderr)
        os.execv(python, cmd)
    except OSError as exc:
        print(f"[precommit-wrapper] Failed to exec pre-commit: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
