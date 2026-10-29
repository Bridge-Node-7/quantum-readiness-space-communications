#!/usr/bin/env python3
"""Fail closed when declared source versions diverge. Does not publish releases."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def check(root: Path) -> list[str]:
    issues: list[str] = []

    def read(path: str) -> str:
        try:
            return (root / path).read_text(encoding="utf-8")
        except OSError:
            issues.append(f"missing source-version file: {path}")
            return ""

    version = read("VERSION").strip()
    if not SEMVER.fullmatch(version):
        issues.append("VERSION is not an unprefixed semantic version")
        return issues

    citation = read("CITATION.cff")
    match = re.search(r"(?m)^version:\s*[\"']?([0-9]+\.[0-9]+\.[0-9]+)[\"']?\s*$", citation)
    if not match or match.group(1) != version:
        issues.append("CITATION.cff version disagrees with VERSION")

    for path in ("release/release-metadata.json", "REPO_MANIFEST.json"):
        try:
            reported = json.loads(read(path)).get("version")
        except (ValueError, AttributeError):
            reported = None
        if reported != version:
            issues.append(f"{path} version disagrees with VERSION")

    checks = (
        ("CHANGELOG.md", rf"(?m)^##\s+{re.escape(version)}\b"),
        ("RELEASE_NOTES.md", rf"(?m)^#\s+.*\bv{re.escape(version)}\s*$"),
        ("RELEASE_REVIEW.md", rf"\*\*Version:\*\*\s+{re.escape(version)}\b"),
        ("release/release-status.md", rf"Current source version:\s+\*\*{re.escape(version)}\*\*"),
        ("tools/build_release.py", rf"default=\"quantum-readiness-space-communications-v{re.escape(version)}\""),
        ("tools/validate_repo.py", rf"VERSION must be {re.escape(version)}"),
    )
    for path, pattern in checks:
        if not re.search(pattern, read(path)):
            issues.append(f"{path} does not reflect VERSION")

    return issues


def main() -> int:
    issues = check(ROOT)
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1
    print("PASS: controlled source-version declarations agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
