# Release automation readiness

## Current boundary

`VERSION` identifies reviewed source; [GitHub Releases](https://github.com/Bridge-Node-7/quantum-readiness-space-communications/releases/latest) record published distribution identity. A source version ahead of the latest release is not published until its tag and GitHub Release exist, and does not by itself require immediate publication.

This repository's existing release process requires human review, deterministic package generation, an integrity manifest, checksums, and traceable assets. Do not replace that process with a bare tag and empty GitHub Release.

## Preflight gate

The required `release-integrity` job runs `tools/check_version_consistency.py`. It checks the controlled source-version declarations, including citation metadata, release metadata, README-independent changelog and review records, source manifest, and version-specific validation and package settings. The existing manifest and checksum validator remains authoritative for file integrity.

This gate deliberately blocks a release-please version PR if it changes only `VERSION` but leaves related source and packaging identities stale.

## Conditions before enabling release-please

1. Define which operation owns the tag, draft release, package validation, asset upload, and publication.
2. Preserve explicit human approval and the existing release-artifact contract.
3. Convert hard-coded version checks and package defaults to controlled, version-derived values, with regression tests.
4. Account for the release-specific notes, review record, status document, release metadata, repository manifest, and checksums. A generated release PR must include every required update or be rejected by CI.
5. Establish a tested baseline between the latest published release and current source; do not silently jump versions or rewrite old releases.
6. Verify that bot-generated pull requests run required CI and that the chosen authentication and event chain work as designed.
7. Validate a draft release candidate and compare resulting assets to the previous release contract before permitting automatic publication.

Until these gates pass, no release-please publishing workflow should be enabled. Existing source and GitHub Releases remain unchanged.

## Pilot evidence

For each acceptance gate, record the exact commit, CI run, generated PR diff, tag verification, package hashes, release assets, and authorization decision. Changes are accepted only when the existing controls are preserved or improved.
