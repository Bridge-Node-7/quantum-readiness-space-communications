#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "access token": re.compile(r"\b(?:ghp_|github_pat_|glpat-|xox[baprs]-)[-A-Za-z0-9_]{20,}\b"),
    "AWS key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "personal email": re.compile(r"\b[A-Za-z0-9._%+-]+@(?!example\.com\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "local path": re.compile(r"[A-Z]:\\Users\\|/Users/|/home/[^/]+/"),
}
ALLOW = {"SECURITY.md"}
SELF_SCAN_EXCLUSIONS = {"tools/scan_public_boundary.py", "tests/test_validator_mutations.py"}
LOCAL_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}

def main() -> int:
    findings = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in LOCAL_DIRS for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in {"SHA256SUMS", "REPO_MANIFEST.json"} or rel in SELF_SCAN_EXCLUSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if rel == "tools/validate_repo.py" and "re.search(r" in line and "/Users/" in line and "/home/" in line:
                continue
            for label, pattern in PATTERNS.items():
                if pattern.search(line) and not (label == "personal email" and rel in ALLOW):
                    findings.append(f"{rel}:{line_no}: {label}")
    if findings:
        for item in findings:
            print(f"FAIL: public-boundary finding: {item}")
        return 1
    print("PASS: no obvious keys, tokens, personal emails, or local user paths")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
