# Changelog

## 0.2.4 - 2026-09-12

- Exclude ephemeral test/tool caches from the controlled release manifest without weakening tracked source integrity.
- Report exact added, removed, and changed paths when manifest or checksum drift is detected.
- Add regression tests proving `.pytest_cache` does not create false drift while real controlled-file changes fail with actionable diagnostics.
- Publish expected integrity evidence from pull-request CI so manifest updates remain reviewable and machine-generated.
- Exclude common in-tree virtualenv and local tool-cache directories from controlled-source scans without weakening governed source checks.
- Document an isolated virtualenv validation path for clean adopters.
- Preserve the v0.2.3 methodology and assessment semantics without modification.

## 0.2.3 - 2026-08-07

- Aligned security and public contribution guidance with restricted issue creation.
- Directed public-safe corrections to focused pull requests while preserving private vulnerability reporting.
- Reconciled current citation, review, notes, release metadata, package prefix, manifest, and SHA-256 records.
- Preserved the v0.2.2 assessment methodology without modification.

## 0.2.2 - 2026-08-05

- Rewrote the README around practical use and removed release-history content from the repository landing page.
- Added audience-neutral, zero-context navigation and clearer reading paths.
- Simplified the repository scope statement for first-time readers.
- Aligned version, citation, release metadata, source review, package prefix, manifest, and SHA-256 records.
- Preserved the v0.2.1 assessment methodology without modification.

## 0.2.1 - 2026-08-05

- Updated the pinned `actions/checkout` dependency from v4.2.2 to v7.0.1.
- Updated the pinned `actions/setup-python` dependency from v5.6.0 to v7.0.0.
- Grouped future GitHub Actions version updates into one Dependabot pull request.
- Regenerated the repository manifest and SHA-256 records.
- Clarified release status and final-seal treatment of documented maintenance pull requests.
- Preserved the v0.2.0 methodology without modification.

## 0.2.0 - 2026-08-05

- Corrected Windows validation portability by enforcing UTF-8 and making the evidence-coverage mutation test verify that its mutation was applied.
- Added repository-local release identity controls and fresh-run checkpoint binding.
- Added real calendar-date validation, cross-platform archive modes, output self-exclusion, and release-tool regression tests.
- Added weekly Dependabot review for validation and GitHub Actions dependencies.

### Changed

- Renamed the public framework to **Quantum Readiness for Space Communications**.
- Retired the invalid v0.1.5 weighted readiness aggregate and compensating average risk model.
- Added `Unknown / Not Assessed` outside the exposure scale.
- Separated Quantum Exposure Severity, Migration Readiness Profile, Evidence Confidence and Coverage, and Critical Risk Overrides.
- Added twelve explicit critical conditions, including long-lived confidentiality exposure and contradictory critical evidence.
- Restored ten non-compensating readiness domains and the highest stage **Sustained and Reassessed**.
- Added a complete fictional Quantum Readiness Decision Pack.
- Added an assessor guide, evidence model, change-control guide, known limitations, foundations page, and consolidated v0.1.5 errata.
- Added stronger semantic validation, mutation tests, Windows CI, secret scanning, link checks, and deterministic packaging.
- Replaced the monolithic controller with staged, non-destructive, exact-SHA release controls.
- Added normalized YAML, JSON, and Markdown external-link parsing with quoted-URL regression tests.
- Added semantic mutation gates for evidence-coverage direction, CR-11 and CR-12 directionality, applicability, unsupported assurance claims, README decision boundaries, and the complete limitations record.
- Added a documentation index for assessment, technical, standards, governance, and example materials.
- Added repository-wide whitespace enforcement, exact readiness-stage semantics, all-condition critical-override semantics, and broader unsupported-assurance mutation guards.
- Corrected owner-only required-check guidance to match the hosted `release-integrity` and `windows-validation` jobs.

### Public scope decision

The experimental engine and workbook candidates were evaluated and withdrawn from the public v0.2.0 scope. They remain internal experimental material and are not part of this release.

## 0.1.5 - 2026-06-19

Historical initial release under the former identity. See [Consolidated Errata](ERRATA_v0.1.5.md) and [Compatibility and Supersession](docs/compatibility-and-supersession.md).
