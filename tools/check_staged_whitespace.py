#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".md", ".txt", ".cff", ".json", ".yml", ".yaml", ".py", ".sh",
    ".ps1", ".toml", ".ini", ".cfg", ".xml", ".js", ".ts", ".rb",
    ".go", ".rs", ".java", ".c", ".h", ".cpp", ".cs",
}
SPECIAL_TEXT_NAMES = {"LICENSE", ".gitignore", ".gitattributes", "VERSION"}
LOCAL_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}


def main() -> int:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in LOCAL_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in SPECIAL_TEXT_NAMES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), 1):
            if re.search(r"[ \t]+$", line):
                errors.append(f"{rel}:{line_no}: trailing whitespace")
            if re.match(r"^(?:<<<<<<<|=======|>>>>>>>)", line):
                errors.append(f"{rel}:{line_no}: conflict marker")
        if text.endswith("\n\n"):
            errors.append(f"{rel}: extra blank line at EOF")
    if errors:
        for error in errors:
            print(error)
        return 2
    print("PASS: source whitespace and conflict-marker check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
