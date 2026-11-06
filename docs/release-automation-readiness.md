# Release automation

`VERSION` identifies reviewed source. [GitHub Releases](https://github.com/Bridge-Node-7/quantum-readiness-space-communications/releases/latest) identify published distributions; source maintenance does not itself publish a release.

Release-please prepares version and changelog changes. The required `release-integrity` check validates controlled version declarations, repository manifests, checksums and deterministic packaging before merge.

Publishing a distribution remains separate from preparing a version change. Existing release assets and historical tags retain their recorded identities.
