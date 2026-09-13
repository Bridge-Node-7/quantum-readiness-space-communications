#!/usr/bin/env python3
from __future__ import annotations

import argparse
import stat
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 8, 4, 0, 0, 0)
EXCLUDE_PARTS = {".git", "__pycache__", ".venv", "build", "dist"}


def files(output: Path) -> list[Path]:
    output = output.resolve()
    return sorted(
        [
            p
            for p in ROOT.rglob("*")
            if p.is_file()
            and p.resolve() != output
            and not any(part in EXCLUDE_PARTS for part in p.parts)
            and p.suffix not in {".pyc", ".pyo"}
        ],
        key=lambda p: p.relative_to(ROOT).as_posix(),
    )


def archive_mode(data: bytes) -> int:
    # Content-derived modes make builds consistent across Linux and Windows.
    return 0o755 if data.startswith(b"#!") else 0o644


def build(output: Path, prefix: str) -> None:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files(output):
            rel = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo(f"{prefix.rstrip('/')}/{rel}", FIXED_TIME)
            info.external_attr = (stat.S_IFREG | archive_mode(data)) << 16
            info.create_system = 3
            zf.writestr(info, data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--prefix", default="quantum-readiness-space-communications-v0.2.4")
    args = parser.parse_args()
    build(args.output, args.prefix)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
