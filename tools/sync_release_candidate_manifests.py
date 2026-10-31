#!/usr/bin/env python3
"""Align version-bearing files to release-please manifest, strip compare URL, refresh manifest hashes."""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
COMPARE_HEADING_RE = re.compile(
    r"(^## \[\d+\.\d+\.\d+\])\(https://github\.com/[^\s)]+/compare/[^\s)]+\)( \(\d{4}-\d{2}-\d{2}\))",
    re.MULTILINE,
)
def main() -> int:
    root = Path(".").resolve()
    version = str(json.loads((root / ".release-please-manifest.json").read_text(encoding="utf-8")).get(".", "")).strip()
    if not VERSION_RE.fullmatch(version):
        print(f"FAIL: invalid manifest version {version!r}", file=sys.stderr); return 1
    # Discover previous declared version from release-metadata if present
    meta_path = root / "release/release-metadata.json"
    prev = None
    if meta_path.exists():
        try:
            prev = json.loads(meta_path.read_text(encoding="utf-8")).get("version")
        except json.JSONDecodeError:
            prev = None
    if not prev or prev == version:
        # try REPO_MANIFEST
        try:
            prev = json.loads((root / "REPO_MANIFEST.json").read_text(encoding="utf-8")).get("version")
        except Exception:
            prev = None
    vp = root / "VERSION"
    if vp.read_text(encoding="utf-8").strip() != version:
        vp.write_text(version + "\n", encoding="utf-8", newline="\n")
        print(f"PASS: aligned VERSION to {version}")
    else:
        print(f"PASS: VERSION already {version}")
    cl = root / "CHANGELOG.md"
    text = cl.read_text(encoding="utf-8")
    rewritten, n = COMPARE_HEADING_RE.subn(r"\1\2", text, count=1)
    if n:
        cl.write_text(rewritten, encoding="utf-8", newline="\n")
        print("PASS: stripped pre-tag CHANGELOG compare URL")
    if prev and prev != version:
        # surgical replacements for known version authorities
        for rel in ("release/release-metadata.json", "REPO_MANIFEST.json"):
            path = root / rel
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("version") != version:
                data["version"] = version
                path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
                print(f"PASS: {rel} -> {version}")
        # text files with precise patterns (same as check_version_consistency)
        notes = (root / "RELEASE_NOTES.md").read_text(encoding="utf-8")
        notes2, n = re.subn(rf"(?m)^(#\s+.*\bv){re.escape(prev)}(\s*)$", rf"\g<1>{version}\2", notes, count=1)
        notes2 = re.sub(rf"(?m)^(Version ){re.escape(prev)}( is )", rf"\g<1>{version}\2", notes2, count=1)
        if notes2 != notes:
            (root / "RELEASE_NOTES.md").write_text(notes2, encoding="utf-8", newline="\n")
            print("PASS: RELEASE_NOTES.md")
        rev = (root / "RELEASE_REVIEW.md").read_text(encoding="utf-8")
        rev2 = re.sub(rf"(\*\*Version:\*\*\s+){re.escape(prev)}\b", rf"\g<1>{version}", rev, count=1)
        if rev2 != rev:
            (root / "RELEASE_REVIEW.md").write_text(rev2, encoding="utf-8", newline="\n")
            print("PASS: RELEASE_REVIEW.md")
        st = (root / "release/release-status.md").read_text(encoding="utf-8")
        st2 = re.sub(rf"(Current source version:\s+\*\*){re.escape(prev)}(\*\*)", rf"\g<1>{version}\2", st, count=1)
        if st2 != st:
            (root / "release/release-status.md").write_text(st2, encoding="utf-8", newline="\n")
            print("PASS: release-status.md")
        for rel, a, b in (
            ("tools/build_release.py", f"quantum-readiness-space-communications-v{prev}", f"quantum-readiness-space-communications-v{version}"),
            ("tools/validate_repo.py", f"VERSION must be {prev}", f"VERSION must be {version}"),
            ("tools/validate_repo.py", f'("version", "{prev}")', f'("version", "{version}")'),
            ("tools/validate_repo.py", f'.strip() != "{prev}"', f'.strip() != "{version}"'),
        ):
            path = root / rel
            text = path.read_text(encoding="utf-8")
            if a in text:
                path.write_text(text.replace(a, b), encoding="utf-8", newline="\n")
                print(f"PASS: {rel}")
    r = subprocess.run([sys.executable, "tools/generate_manifest.py"], cwd=root)
    if r.returncode != 0:
        return r.returncode
    print("PASS: refreshed SHA256 inventory")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
