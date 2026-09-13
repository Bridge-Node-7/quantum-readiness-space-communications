from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


class ReleaseToolTests(unittest.TestCase):
    def test_invalid_calendar_release_date_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "tools").mkdir()
            shutil.copy2(
                Path(__file__).parents[1] / "tools/stamp_release.py",
                root / "tools/stamp_release.py",
            )
            for rel in ["CHANGELOG.md", "CITATION.cff", "RELEASE_REVIEW.md"]:
                (root / rel).write_text("{{RELEASE_DATE}}\n", encoding="utf-8")
            (root / "release").mkdir()
            (root / "release/release-metadata.json").write_text(
                '{"release_date":"{{RELEASE_DATE}}"}\n', encoding="utf-8"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(root / "tools/stamp_release.py"),
                    "--date",
                    "2026-02-31",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("real calendar date", result.stderr + result.stdout)

    def test_build_output_inside_repository_is_not_embedded(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "tools").mkdir()
            shutil.copy2(
                Path(__file__).parents[1] / "tools/build_release.py",
                root / "tools/build_release.py",
            )
            (root / "README.md").write_text("# Example\n", encoding="utf-8")
            output = root / "output.zip"
            subprocess.run(
                [
                    sys.executable,
                    str(root / "tools/build_release.py"),
                    "--output",
                    str(output),
                ],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
            with zipfile.ZipFile(output) as zf:
                self.assertFalse(
                    any(name.endswith("/output.zip") for name in zf.namelist())
                )

    def test_archive_modes_are_content_derived(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "tools").mkdir()
            shutil.copy2(
                Path(__file__).parents[1] / "tools/build_release.py",
                root / "tools/build_release.py",
            )
            (root / "scripts").mkdir()
            script = root / "scripts/run.sh"
            script.write_text("#!/usr/bin/env bash\necho ok\n", encoding="utf-8")
            script.chmod(0o644)
            (root / "notes.txt").write_text("notes\n", encoding="utf-8")
            output = Path(td).parent / f"{root.name}-modes.zip"
            try:
                subprocess.run(
                    [
                        sys.executable,
                        str(root / "tools/build_release.py"),
                        "--output",
                        str(output),
                    ],
                    cwd=root,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                with zipfile.ZipFile(output) as zf:
                    modes = {
                        i.filename: (i.external_attr >> 16) & 0o777
                        for i in zf.infolist()
                    }
                self.assertEqual(
                    next(v for k, v in modes.items() if k.endswith("/scripts/run.sh")),
                    0o755,
                )
                self.assertEqual(
                    next(v for k, v in modes.items() if k.endswith("/notes.txt")),
                    0o644,
                )
            finally:
                output.unlink(missing_ok=True)

    def _manifest_fixture(self, root: Path) -> Path:
        (root / "tools").mkdir(parents=True, exist_ok=True)
        generator = root / "tools/generate_manifest.py"
        shutil.copy2(
            Path(__file__).parents[1] / "tools/generate_manifest.py", generator
        )
        (root / "release").mkdir()
        (root / "release/release-metadata.json").write_text(
            '{"title":"Synthetic","version":"0.0.0","release_date":"2026-09-12"}\n',
            encoding="utf-8",
        )
        (root / "notes.txt").write_text("stable\n", encoding="utf-8")
        return generator

    def test_manifest_ignores_ephemeral_pytest_cache(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            generator = self._manifest_fixture(root)
            cache = root / ".pytest_cache/v/cache/nodeids"
            cache.parent.mkdir(parents=True)
            cache.write_text("[]\n", encoding="utf-8")

            subprocess.run(
                [sys.executable, str(generator)],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
            manifest = (root / "REPO_MANIFEST.json").read_text(encoding="utf-8")
            self.assertNotIn(".pytest_cache", manifest)

            checked = subprocess.run(
                [sys.executable, str(generator), "--check"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_manifest_drift_names_changed_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            generator = self._manifest_fixture(root)
            subprocess.run(
                [sys.executable, str(generator)],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
            (root / "notes.txt").write_text("changed\n", encoding="utf-8")

            checked = subprocess.run(
                [sys.executable, str(generator), "--check"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("FAIL: manifest drift", checked.stdout)
            self.assertIn("CHANGED: notes.txt", checked.stdout)


if __name__ == "__main__":
    unittest.main()
