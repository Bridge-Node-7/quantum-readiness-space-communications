#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Run: python -m pip install -r requirements-validation.txt") from exc

TITLE = "Quantum Readiness for Space Communications"
SLUG = "quantum-readiness-space-communications"
DECISION_PACK = "Quantum Readiness Decision Pack"
OLD_PATTERN = re.compile(r"quantum[ -]safe space communications|quantum-safe-space-communications", re.I)
OLD_ALLOWED = {
    "CHANGELOG.md", "METHODOLOGY_CHANGELOG.md", "ERRATA_v0.1.5.md",
    "docs/compatibility-and-supersession.md", "assessment/readiness-index.md",
    "assessment/space-link-risk-matrix.md", "assessment/quantum-safe-space-communications-assessment.md",
    "release/release-status.md",
    "release/changed-files-allowlist.txt", "tools/validate_repo.py", "tests/test_validator_mutations.py",
    "REPO_MANIFEST.json",
}
REQUIRED = {
    "README.md", "VERSION", "STATUS.md", "CHANGELOG.md", "METHODOLOGY_CHANGELOG.md",
    "ERRATA_v0.1.5.md", "KNOWN_LIMITATIONS.md", "CITATION.cff", "GOVERNANCE.md",
    "MAINTAINERS.md", "RELEASE_NOTES.md", "RELEASE_REVIEW.md", "REPO_MANIFEST.json",
    "SHA256SUMS", "requirements-validation.txt", "assessment/quantum-readiness-space-communications-assessment.md",
    "assessment/quantum-exposure-severity.md", "assessment/migration-readiness-profile.md",
    "assessment/evidence-confidence-ledger.md", "assessment/critical-risk-overrides.md",
    "decision-pack/README.md", "docs/README.md", "docs/assessor-guide.md", "docs/evidence-model.md",
    "docs/change-control.md", "docs/quantum-cryptography-foundations.md", "docs/standards-register.md",
    "examples/sample-small-satellite-decision-pack/README.md", "release/release-status.md",
    "release/release-metadata.json", "release/external-link-exceptions.json", ".gitattributes", "docs/accessibility-and-mobile-use.md",
    "tools/build_release.py", "tools/check_external_links.py", "tools/check_staged_whitespace.py",
    "tools/scan_public_boundary.py", "tests/test_methodology.py", "tests/test_validator_mutations.py", "tests/test_external_links.py",
    ".github/workflows/methodology-integrity.yml", ".github/dependabot.yml", "tests/test_release_tools.py",
}
TEXT_SUFFIXES = {".md", ".txt", ".cff", ".json", ".yml", ".yaml", ".py", ".sh", ".ps1", ".toml", ".ini", ".cfg", ".xml", ".js", ".ts", ".rb", ".go", ".rs", ".java", ".c", ".h", ".cpp", ".cs"}
FORBIDDEN_DIRS = {"src", "schema"}
FORBIDDEN_SUFFIXES = {".xlsx", ".xlsm", ".exe", ".dll", ".so", ".dylib"}
PROHIBITED_ACTIVE = [
    re.compile(r"weighted\s+(?:readiness|migration)", re.I),
    re.compile(r"composite\s+(?:readiness|migration)\s+(?:score|index)", re.I),
    re.compile(r"\bCONDITIONAL_GO\b|\bAUTOMATED_GO\b", re.I),
    re.compile(r"automated\s+(?:assessment\s+)?(?:decision|disposition)", re.I),
]
HISTORICAL_CONTEXT = re.compile(
    r"\b(?:retir(?:e|ed|es|ing)|supersed(?:e|ed|es|ing)|historical|invalid|defect|"
    r"does not|do not|must not|no weighted|without weighted|prohibit(?:ed|s)?|defective|"
    r"removed|withdrawn|replaced|unsupported|not certification|not authorization)\b",
    re.I,
)
PROHIBITED_ASSURANCE = [
    re.compile(r"\bcertif(?:y|ies|ied|ication)\b.{0,100}\bunbreakable\b", re.I),
    re.compile(r"\bcertif(?:y|ies|ied|ication)\b.{0,100}\bquantum[- ]resistant\b", re.I),
    re.compile(r"\bunbreakable\b.{0,100}\bquantum(?:-resistant|-safe)?\b", re.I),
    re.compile(r"\bquantum[- ]proof\b", re.I),
    re.compile(r"\bflight[- ]ready\b", re.I),
    re.compile(r"\bmission[- ]assured\b", re.I),
    re.compile(r"\bauthoritative\s+operational\s+approval\b", re.I),
    re.compile(r"\bpostures?\s+(?:are|is)\s+authoritative\b", re.I),
    re.compile(r"\bapproved\s+for\s+deployment\b", re.I),
    re.compile(r"\bguarantee(?:s|d)?\b.{0,100}\bquantum(?:-resistant|-safe)?\b", re.I),
    re.compile(r"\bproduction[- ]ready\b.{0,100}\boperational deployment\b", re.I),
    re.compile(r"\bcertif(?:y|ies|ied|ication)\b.{0,100}\bmission readiness\b", re.I),
    re.compile(r"\bvalidated for operations\b", re.I),
    re.compile(r"\bproves?\b.{0,100}\bquantum[- ]secure communications\b", re.I),
    re.compile(r"\bcertified for deployment\b", re.I),
    re.compile(r"\bmission[- ]ready\b", re.I),
    re.compile(r"\bcompliance certification\b", re.I),
]
SEMANTIC_SOURCE_EXCLUSIONS = {"tools/validate_repo.py", "tests/test_validator_mutations.py"}
CODE_SUFFIXES = {".py", ".sh", ".ps1", ".js", ".ts", ".rb", ".go", ".rs", ".java", ".c", ".h", ".cpp", ".cs"}
LOCAL_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}


RUNTIME_DISPOSITION = re.compile(
    r"(?:print|console\.log|return|write-host|printf)\s*\(?\s*[\"']"
    r"(?:GO|HOLD|CONDITIONAL_GO|AUTOMATED_GO)\b",
    re.I,
)



def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return re.sub(r"[ _]+", "-", text).strip("-")


def headings(text: str) -> set[str]:
    return {slugify(m.group(1)) for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.M)}


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def table_errors(rel: str, text: str) -> list[str]:
    errors: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if not lines[i].lstrip().startswith("|"):
            i += 1
            continue
        block = []
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            block.append((i + 1, lines[i]))
            i += 1
        if len(block) < 2:
            continue
        counts = [len(re.split(r"(?<!\\)\|", row.strip().strip("|"))) for _, row in block]
        if len(set(counts)) != 1:
            errors.append(f"malformed Markdown table in {rel}: lines {[n for n,_ in block]} have cell counts {counts}")
    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for rel in sorted(REQUIRED):
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    if (root / "VERSION").read_text(encoding="utf-8").strip() != "0.2.4":
        errors.append("VERSION must be 0.2.4")

    attributes = (root / ".gitattributes").read_text(encoding="utf-8")
    if "* text=auto eol=lf" not in attributes:
        errors.append(".gitattributes must enforce LF line endings for cross-platform hash stability")

    files = [p for p in root.rglob("*") if p.is_file() and not any(part in LOCAL_DIRS for part in p.parts)]
    for path in root.rglob("*"):
        if any(part in LOCAL_DIRS for part in path.parts):
            continue
        if path.is_dir() and path.name in FORBIDDEN_DIRS:
            errors.append(f"forbidden public software directory: {path.relative_to(root)}")
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden executable or workbook artifact: {rel}")
        if path.suffix == ".py" and not rel.startswith(("tools/", "tests/")):
            errors.append(f"Python file outside lightweight validation/test scope: {rel}")
        if path.suffix.lower() in CODE_SUFFIXES:
            allowed = (
                (path.suffix.lower() == ".py" and rel.startswith(("tools/", "tests/")))
                or (path.suffix.lower() in {".sh", ".ps1"} and rel.startswith("scripts/"))
            )
            if not allowed:
                errors.append(f"unexpected executable-code artifact outside approved validation scope: {rel}")

    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE", ".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), 1):
            if re.search(r"[ \t]+$", line):
                errors.append(f"trailing whitespace in {rel}:{line_no}")
        if text.endswith("\n\n"):
            errors.append(f"extra blank line at EOF in {rel}")
        if rel not in OLD_ALLOWED and OLD_PATTERN.search(text):
            errors.append(f"retired identity outside compatibility allowlist: {rel}")
        if rel not in {"tools/validate_repo.py", "tools/scan_public_boundary.py"} and re.search(r"[A-Z]:\\|/Users/|/home/[^/]+/", text):
            errors.append(f"local path found: {rel}")
        if rel not in SEMANTIC_SOURCE_EXCLUSIONS:
            semantic_lines = text.splitlines()
            for line_no, line in enumerate(semantic_lines, 1):
                context = " ".join(semantic_lines[max(0, line_no-3):min(len(semantic_lines), line_no+2)])
                for pattern in PROHIBITED_ACTIVE:
                    if pattern.search(line) and not HISTORICAL_CONTEXT.search(context):
                        errors.append(
                            f"prohibited active methodology or automated-disposition language in {rel}:{line_no}: {pattern.pattern}"
                        )
            for line_no, line in enumerate(text.splitlines(), 1):
                context = " ".join(text.splitlines()[max(0, line_no-3):min(len(text.splitlines()), line_no+2)])
                for pattern in PROHIBITED_ASSURANCE:
                    if pattern.search(line) and not HISTORICAL_CONTEXT.search(context):
                        errors.append(f"unsupported assurance or operational-approval claim in {rel}:{line_no}: {pattern.pattern}")
            if path.suffix.lower() in CODE_SUFFIXES and RUNTIME_DISPOSITION.search(text):
                errors.append(f"runtime operational disposition found in executable code: {rel}")
        if path.suffix == ".md":
            errors.extend(table_errors(rel, text))

    key = "\n".join((root / p).read_text(encoding="utf-8") for p in ["README.md", "CITATION.cff", "RELEASE_NOTES.md", "release/release-metadata.json"])
    for token in [TITLE, SLUG, DECISION_PACK]:
        if token not in key:
            errors.append(f"required public identity token missing from key files: {token}")

    allowlist = {
        line.strip()
        for line in (root / "release/changed-files-allowlist.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    for rel in {"REPO_MANIFEST.json", "SHA256SUMS", ".gitattributes"}:
        if rel not in allowlist:
            errors.append(f"release changed-file allowlist is missing required generated/control file: {rel}")

    exposure = (root / "assessment/quantum-exposure-severity.md").read_text(encoding="utf-8")
    for phrase in ["Unknown / Not Assessed", "Higher severity means greater concern", "sufficient evidence", "accountable applicability", "Do not average"]:
        if phrase.lower() not in exposure.lower():
            errors.append(f"exposure invariant missing: {phrase}")
    if not re.search(r"\|\s*0\s*\|\s*Not Applicable\s*\|", exposure):
        errors.append("exposure level 0 must be Not Applicable")
    exposure_contradictions = [
        r"higher exposure severity (?:also )?means lower concern",
        r"lower exposure severity (?:also )?means greater concern",
        r"missing or inconclusive information (?:may|can|should) be (?:recorded as )?`?Not Applicable`?",
    ]
    for pattern in exposure_contradictions:
        if re.search(pattern, exposure, re.I):
            errors.append(f"contradictory exposure or applicability statement: {pattern}")

    readiness = (root / "assessment/migration-readiness-profile.md").read_text(encoding="utf-8")
    if len(re.findall(r"^### Domain \d+\. ", readiness, re.M)) != 10:
        errors.append("migration readiness profile must contain exactly ten domains")
    if "Sustained and Reassessed" not in readiness:
        errors.append("highest readiness stage must be Sustained and Reassessed")
    if "Higher stages mean stronger demonstrated migration capability." not in readiness:
        errors.append("readiness orientation must state that higher stages mean stronger demonstrated migration capability")
    readiness_contradictions = [
        r"higher readiness stages (?:also )?mean weaker capability",
        r"higher stages (?:also )?mean weaker demonstrated migration capability",
        r"stage 0 (?:is|means) (?:fully ready|complete|deployed|sustained)",
    ]
    for pattern in readiness_contradictions:
        if re.search(pattern, readiness, re.I):
            errors.append(f"contradictory readiness statement: {pattern}")
    expected_stages = {
        0: ("Not Assessed", ("insufficient", "characterize")),
        1: ("Initiated", ("initial activity", "incomplete", "self-attested")),
        2: ("Defined", ("Documented process", "accountable ownership")),
        3: ("Piloted", ("representative environment", "evidence")),
        4: ("Deployed", ("implemented", "approved scope", "governed operations")),
        5: ("Sustained and Reassessed", ("monitored", "tested", "recovered", "reviewed", "updated")),
    }
    stage_rows = {}
    for line in readiness.splitlines():
        match = re.match(r"\|\s*([0-5])\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", line)
        if match:
            stage_rows[int(match.group(1))] = (match.group(2).strip(), match.group(3).strip())
    for stage, (label, tokens) in expected_stages.items():
        if stage not in stage_rows:
            errors.append(f"readiness stage {stage} row is missing")
            continue
        actual_label, standard = stage_rows[stage]
        if actual_label != label:
            errors.append(f"readiness stage {stage} label must be {label}")
        for token in tokens:
            if token.lower() not in standard.lower():
                errors.append(f"readiness stage {stage} meaning is missing: {token}")
    if re.search(r"\b\d+(?:\.\d+)?%", readiness) or re.search(r"\|\s*(?:weight|weighted|percentage)\s*\|", readiness, re.I):
        errors.append("readiness profile must not contain numeric weights or percentage-scoring tables")
    if "not a weighted index" not in readiness.lower():
        errors.append("readiness profile must explicitly reject weighted aggregation")

    evidence = (root / "assessment/evidence-confidence-ledger.md").read_text(encoding="utf-8")
    required_evidence = ["Evidence Confidence and Coverage", "Evidence Coverage (%)", "Critical Unknowns", "Stale Evidence Items", "Conflicting Evidence Items", "Unassessed Critical-Scope Items", "Approved Exclusions"]
    for phrase in required_evidence:
        if phrase not in evidence:
            errors.append(f"evidence model invariant missing: {phrase}")
    for level in ["E0", "E1", "E2", "E3", "E4"]:
        if level not in evidence:
            errors.append(f"evidence level missing: {level}")
    coverage_formula = re.compile(
        r"Evidence Coverage \(\%\)\s*=\s*Evidence-complete in-scope items\s*/\s*Total in-scope items\s*[×x]\s*100",
        re.I,
    )
    if not coverage_formula.search(evidence):
        errors.append("evidence coverage formula must use evidence-complete in-scope items divided by total in-scope items")
    evidence_contradictions = [
        r"Evidence Coverage.*Total in-scope items\s*/\s*Evidence-complete in-scope items",
        r"evidence coverage uses the reverse numerator and denominator",
    ]
    for pattern in evidence_contradictions:
        if re.search(pattern, evidence, re.I):
            errors.append(f"contradictory evidence-coverage statement: {pattern}")
    for phrase in [
        "Weak or incomplete evidence does not reduce exposure",
        "Only current, applicable evidence may support a current statement",
        "Conflicting evidence must be reconciled or escalated under CR-12",
    ]:
        if phrase.lower() not in evidence.lower():
            errors.append(f"evidence directionality invariant missing: {phrase}")

    overrides = (root / "assessment/critical-risk-overrides.md").read_text(encoding="utf-8")
    override_semantics = {
        "CR-01": ("Command authentication", "not demonstrated", "critical control path"),
        "CR-02": ("Secure update", "rollback verification", "failed or is absent", "critical component"),
        "CR-03": ("Critical key material", "trust anchors", "custody", "revocation", "recovery"),
        "CR-04": ("safety-critical function", "unacceptable residual exposure"),
        "CR-05": ("unpatchable", "unsupported critical component", "no approved migration", "compensating-control path"),
        "CR-06": ("Authenticated recovery", "rollback", "not demonstrated", "critical service"),
        "CR-07": ("critical vendor", "supply-chain dependency", "unresolved or unsupported"),
        "CR-08": ("critical exposure", "no accountable owner", "due date"),
        "CR-09": ("Evidence coverage is insufficient", "critical item remains unassessed"),
        "CR-10": ("assessment-specific mission-loss condition", "accountable authority"),
        "CR-11": ("Long-lived sensitive information", "quantum-vulnerable key establishment", "harvest-now-decrypt-later"),
        "CR-12": ("critical path", "materially contradictory", "unreliable", "unreconciled"),
    }
    override_lines = {}
    for line in overrides.splitlines():
        match = re.match(r"\|\s*(CR-\d{2})\s*\|\s*(.*?)\s*\|$", line)
        if match:
            override_lines[match.group(1)] = match.group(2)
    for code, tokens in override_semantics.items():
        line = override_lines.get(code, "")
        if not line:
            errors.append(f"critical condition missing: {code}")
            continue
        for token in tokens:
            if token.lower() not in line.lower():
                errors.append(f"critical condition semantic invariant missing: {code} / {token}")
    weakening_pattern = re.compile(
        r"\b(?:but (?:this|it) is not critical|may be ignored|can be ignored|"
        r"optional(?: and)? non[- ]?critical|never critical|non[- ]?critical|"
        r"low priority|not a priority|may be deferred without review)\b",
        re.I,
    )
    for code, line in override_lines.items():
        if weakening_pattern.search(line):
            errors.append(f"critical condition directionality is weakened or negated: {code}")

    applicability_sentence = "Missing or inconclusive information is `Unknown / Not Assessed`, never `Not Applicable`."
    if applicability_sentence.lower() not in exposure.lower():
        errors.append("applicability invariant must prohibit missing evidence from becoming Not Applicable")

    readme = (root / "README.md").read_text(encoding="utf-8")
    for phrase in [
        "These human-governed postures support planning only",
        "The postures are not certification, compliance determination, deployment approval, flight qualification, operational authorization",
    ]:
        if phrase.lower() not in readme.lower():
            errors.append(f"README decision-boundary invariant missing: {phrase}")

    limitations = (root / "KNOWN_LIMITATIONS.md").read_text(encoding="utf-8")
    required_limitations = [
        "documentation-first planning framework",
        "does not",
        "implement cryptography",
        "calculate an authoritative score or decision",
        "predict when a cryptographically relevant quantum computer will exist",
        "Assessment quality depends on scope completeness",
        "not operational authorization",
    ]
    if len(limitations.split()) < 100:
        errors.append("KNOWN_LIMITATIONS.md is too short to preserve the required limitations record")
    for phrase in required_limitations:
        if phrase.lower() not in limitations.lower():
            errors.append(f"known-limitations invariant missing: {phrase}")

    dp = (root / "decision-pack/README.md").read_text(encoding="utf-8")
    for heading in ["Purpose", "Required artifacts", "Assembly order", "Minimum quality gates", "Approval and review", "Retention"]:
        if f"## {heading}" not in dp:
            errors.append(f"Decision Pack section missing: {heading}")
    if len(dp.split()) < 180:
        errors.append("Decision Pack guide is too short to be operationally useful")

    example_dir = root / "examples/sample-small-satellite-decision-pack"
    expected_example = {"README.md"} | {f"{i:02d}-{name}.md" for i, name in [
        (1,"scope-and-link-map"),(2,"cryptographic-inventory"),(3,"quantum-exposure-severity"),(4,"migration-readiness-profile"),(5,"evidence-confidence-and-coverage"),(6,"critical-risk-overrides"),(7,"ownership-and-actions"),(8,"vendor-and-standards"),(9,"migration-and-recovery-roadmap"),(10,"decision-record-and-review")
    ]}
    if example_dir.is_dir():
        actual = {p.name for p in example_dir.glob("*.md")}
        for missing in sorted(expected_example - actual):
            errors.append(f"complete fictional Decision Pack artifact missing: {missing}")
    else:
        errors.append("complete fictional Decision Pack directory missing")

    # Parse all structured files.
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix in {".yml", ".yaml", ".cff"}:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                if data is None:
                    raise ValueError("empty YAML document")
                if rel.startswith(".github/ISSUE_TEMPLATE/") and not isinstance(data.get("body"), list):
                    raise ValueError("issue form body must be a list")
        except Exception as exc:
            errors.append(f"invalid structured file {rel}: {exc}")

    cff = yaml.safe_load((root / "CITATION.cff").read_text(encoding="utf-8"))
    for field in ["cff-version", "message", "title", "authors", "version", "repository-code"]:
        if not cff.get(field):
            errors.append(f"CITATION.cff required field missing: {field}")

    metadata = json.loads((root / "release/release-metadata.json").read_text(encoding="utf-8"))
    for field, expected in [("name", SLUG), ("title", TITLE), ("version", "0.2.4"), ("decision_pack_name", DECISION_PACK)]:
        if metadata.get(field) != expected:
            errors.append(f"release metadata mismatch: {field}")
    release_date = metadata.get("release_date")
    if release_date != "{{RELEASE_DATE}}":
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(release_date)):
            errors.append("release_date must be {{RELEASE_DATE}} in candidate source or a real ISO date in stamped source")
        else:
            try:
                dt.date.fromisoformat(str(release_date))
            except ValueError:
                errors.append("release_date must be a real calendar date")

    # Relative links and fragments.
    heading_cache: dict[Path, set[str]] = {}
    for path in root.rglob("*.md"):
        if any(part in LOCAL_DIRS for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for target in markdown_links(text):
            target = unquote(target.strip())
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, fragment = target.partition("#")
            resolved = path if not file_part else (path.parent / file_part).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"link escapes repository: {rel} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken relative link: {rel} -> {target}")
                continue
            if fragment and resolved.is_file() and resolved.suffix == ".md":
                if resolved not in heading_cache:
                    heading_cache[resolved] = headings(resolved.read_text(encoding="utf-8"))
                if slugify(fragment) not in heading_cache[resolved]:
                    errors.append(f"broken Markdown anchor: {rel} -> {target}")

    dependabot_path = root / ".github/dependabot.yml"
    dependabot = yaml.safe_load(dependabot_path.read_text(encoding="utf-8"))
    updates = dependabot.get("updates") if isinstance(dependabot, dict) else None
    if not isinstance(updates, list):
        errors.append("Dependabot configuration must contain an updates list")
    else:
        ecosystems = {row.get("package-ecosystem"): row for row in updates if isinstance(row, dict)}
        for ecosystem in ("pip", "github-actions"):
            row = ecosystems.get(ecosystem)
            if not row:
                errors.append(f"Dependabot must review {ecosystem} dependencies")
                continue
            if ((row.get("schedule") or {}).get("interval")) != "weekly":
                errors.append(f"Dependabot {ecosystem} review must run weekly")

    workflow = yaml.safe_load((root / ".github/workflows/methodology-integrity.yml").read_text(encoding="utf-8"))
    workflow_text = (root / ".github/workflows/methodology-integrity.yml").read_text(encoding="utf-8")
    if "ubuntu-24.04" not in workflow_text or "windows-2022" not in workflow_text:
        errors.append("workflow must validate on pinned Linux and Windows runner labels")
    for token in ["timeout-minutes", "concurrency", "persist-credentials: false", "permissions:\n  contents: read", "python -m pip check"]:
        if token not in workflow_text:
            errors.append(f"workflow hardening token missing: {token}")
    for match in re.findall(r"uses:\s*([^\s#]+)", workflow_text):
        if "@" not in match or not re.search(r"@[0-9a-f]{40}$", match):
            errors.append(f"workflow action is not pinned to full SHA: {match}")

    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"STOP: {len(errors)} repository validation finding(s)")
        return 1
    print("PASS: identity, methodology semantics, structured files, tables, links, examples, metadata, and workflow controls validate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
