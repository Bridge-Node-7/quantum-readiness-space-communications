from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.check_version_consistency import check


class VersionConsistencyTests(unittest.TestCase):
    def fixture(self, root: Path) -> None:
        records = {
            "VERSION": "0.2.4\n",
            "CITATION.cff": 'version: "0.2.4"\n',
            "release/release-metadata.json": '{"version": "0.2.4"}\n',
            "REPO_MANIFEST.json": '{"version": "0.2.4"}\n',
            "CHANGELOG.md": "## 0.2.4 - Unreleased source\n",
            "RELEASE_NOTES.md": "# Example v0.2.4\n",
            "RELEASE_REVIEW.md": "**Version:** 0.2.4\n",
            "release/release-status.md": "Current source version: **0.2.4**\n",
            "tools/build_release.py": 'default="quantum-readiness-space-communications-v0.2.4"\n',
            "tools/validate_repo.py": 'errors.append("VERSION must be 0.2.4")\n',
        }
        for name, content in records.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def test_matching_version_declarations_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.assertEqual(check(root), [])

    def test_citation_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "CITATION.cff").write_text('version: "0.2.5"\n', encoding="utf-8")
            self.assertTrue(any("CITATION.cff" in issue for issue in check(root)))

    def test_release_metadata_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "release/release-metadata.json").write_text('{"version": "0.2.5"}\n', encoding="utf-8")
            self.assertTrue(any("release/release-metadata.json" in issue for issue in check(root)))

    def test_builder_prefix_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "tools/build_release.py").write_text('default="quantum-readiness-space-communications-v0.2.5"\n', encoding="utf-8")
            self.assertTrue(any("tools/build_release.py" in issue for issue in check(root)))


if __name__ == "__main__":
    unittest.main()
