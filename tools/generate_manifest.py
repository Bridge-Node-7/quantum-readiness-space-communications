#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "REPO_MANIFEST.json"
SUMS = ROOT / "SHA256SUMS"
EXCLUDED = {"REPO_MANIFEST.json", "SHA256SUMS"}
CACHE_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def controlled_files() -> list[Path]:
    result: list[Path] = []
    for p in ROOT.rglob("*"):
        if (
            not p.is_file()
            or any(part in CACHE_DIRS for part in p.parts)
            or p.suffix in {".pyc", ".pyo"}
        ):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in EXCLUDED or rel.startswith(("build/", "dist/")):
            continue
        result.append(p)
    return sorted(result, key=lambda p: p.relative_to(ROOT).as_posix())


def build_manifest() -> dict:
    metadata = json.loads(
        (ROOT / "release/release-metadata.json").read_text(encoding="utf-8")
    )
    records = [
        {
            "path": p.relative_to(ROOT).as_posix(),
            "bytes": p.stat().st_size,
            "sha256": sha256(p),
        }
        for p in controlled_files()
    ]
    return {
        "schema_version": "1.1",
        "repository": "Bridge-Node-7/quantum-readiness-space-communications",
        "title": metadata["title"],
        "version": metadata["version"],
        "release_date": metadata["release_date"],
        "methodology_scope": (
            "documentation-first; no automated assessment engine or workbook "
            "decision calculator"
        ),
        "controlled_file_count": len(records),
        "integrity_note": (
            "REPO_MANIFEST.json and SHA256SUMS are excluded from controlled files. "
            "SHA256SUMS includes REPO_MANIFEST.json but excludes itself."
        ),
        "files": records,
    }


def sums_text(manifest: dict) -> str:
    rows = [f"{e['sha256']}  {e['path']}" for e in manifest["files"]]
    rows.append(f"{sha256(MANIFEST)}  REPO_MANIFEST.json")
    return "\n".join(sorted(rows)) + "\n"


def write_files() -> None:
    manifest = build_manifest()
    MANIFEST.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    SUMS.write_text(sums_text(manifest), encoding="utf-8", newline="\n")


def _record_map(manifest: dict) -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for item in manifest.get("files", []):
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            result[item["path"]] = (
                int(item.get("bytes", -1)),
                str(item.get("sha256", "")),
            )
    return result


def _print_manifest_drift(actual: dict, expected: dict) -> None:
    actual_map = _record_map(actual)
    expected_map = _record_map(expected)
    for path in sorted(expected_map.keys() - actual_map.keys()):
        print(f"ADDED: {path}")
    for path in sorted(actual_map.keys() - expected_map.keys()):
        print(f"REMOVED: {path}")
    for path in sorted(actual_map.keys() & expected_map.keys()):
        if actual_map[path] != expected_map[path]:
            print(f"CHANGED: {path}")
    metadata_fields = (
        "schema_version",
        "repository",
        "title",
        "version",
        "release_date",
        "methodology_scope",
    )
    for field in metadata_fields:
        if actual.get(field) != expected.get(field):
            print(f"METADATA CHANGED: {field}")


def _parse_sums(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        digest, separator, path = line.partition("  ")
        if separator and path:
            result[path] = digest
    return result


def _print_checksum_drift(observed: str, expected: str) -> None:
    observed_map = _parse_sums(observed)
    expected_map = _parse_sums(expected)
    for path in sorted(expected_map.keys() - observed_map.keys()):
        print(f"CHECKSUM ADDED: {path}")
    for path in sorted(observed_map.keys() - expected_map.keys()):
        print(f"CHECKSUM REMOVED: {path}")
    for path in sorted(observed_map.keys() & expected_map.keys()):
        if observed_map[path] != expected_map[path]:
            print(f"CHECKSUM CHANGED: {path}")


def check() -> int:
    if not MANIFEST.exists() or not SUMS.exists():
        print("FAIL: manifest or checksum file missing")
        return 1

    expected = build_manifest()
    try:
        actual = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read REPO_MANIFEST.json: {exc}")
        return 1

    if actual != expected:
        print("FAIL: manifest drift")
        _print_manifest_drift(actual, expected)
        return 1

    expected_sums = sums_text(actual)
    observed_sums = SUMS.read_text(encoding="utf-8")
    if observed_sums != expected_sums:
        print("FAIL: checksum drift")
        _print_checksum_drift(observed_sums, expected_sums)
        return 1

    print(f"PASS: manifest and {len(actual['files']) + 1} hashes verify")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    write_files()
    print("PASS: generated manifest and checksums")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
