# 04. Migration Readiness Profile

This fictional profile follows the ten domains and stage rubric in the
[canonical Migration Readiness Profile](../../assessment/migration-readiness-profile.md).
The records illustrate a planning assessment; no real system or cryptographic
implementation was tested.

| Domain | Demonstrated stage | Evidence | Constraint |
|---|---:|---|---|
| Governance and accountability | 2 | E-07 | Owners and actions are documented; funding and the payload scope decision remain pending |
| Cryptographic inventory and visibility | 2 | E-01 | Documented C-01 through C-04 inventory; configuration and firmware dependencies need verification |
| Exposure characterization | 2 | E-01, E-02 | Exposure rationale is documented; data-retention approval and command-path evidence remain incomplete |
| Critical-link protection | 1 | E-01 | Critical paths and owners are identified; E-03 is conflicting, and command authentication, update and rollback remain unproven |
| Migration strategy and sequencing | 1 | E-05 | Options and initial sequencing are identified; architecture and exit criteria are not approved |
| Crypto-agility architecture | 0 | E-05 identifies options only | No applicable architecture or demonstration of controlled algorithm, key or trust-anchor changes is provided |
| Implementation and interoperability | 1 | E-07 | Initial testing actions have owners; E-03 is conflicting and does not establish a representative interoperability demonstration |
| Key and trust management | 1 | E-01 | Rotation and recovery design pending |
| Vendor and supply-chain readiness | 1 | E-06 | One response incomplete |
| Monitoring, recovery, and reassessment | 0 | E-04 is historical only | Stale recovery evidence cannot establish current capability; a current assessment and exercise are required |

Implementation and interoperability remains at initial activity, rather than a
demonstrated pilot: E-03's conflict is unresolved. Software, firmware and secure
update constraints belong within critical-link protection, implementation and
interoperability, and key and trust management; they do not replace a canonical
domain. Scope and ownership are covered by governance and inventory.

Stage 0 means Not Assessed, not Not Applicable. The profile is not averaged.
Weak domains, unresolved critical conditions and evidence limitations remain
visible and do not authorize deployment.
