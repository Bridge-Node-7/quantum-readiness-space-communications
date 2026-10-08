# 05. Evidence Confidence and Coverage

## Summary

```text
Evidence Coverage: NOT_ESTABLISHED
Total In-Scope Items: NOT_ESTABLISHED
Evidence-Complete Items: NOT_ESTABLISHED
Critical Unknowns: NOT_ESTABLISHED; unresolved conditions remain visible below
Stale Evidence Items: 1
Conflicting Evidence Items: 1
Withdrawn or Superseded Items: 0
Unassessed Critical-Scope Items: at least 1; payload is explicitly unassessed
Approved Exclusions: 0
```

The former 7/11 calculation is not supported by the pack. Seven evidence records
are not seven evidence-complete scope items, and no approved eleven-item
denominator or claim-specific support floors are supplied. The arithmetic rounds
to 64 percent, but it does not establish evidence coverage. No replacement
percentage is justified by the current fictional records.

Stale, conflicting and withdrawn/superseded counts above count distinct ledger
IDs: E-04, E-03 and none, respectively. They are not counts of affected scope
items. Payload is one explicitly unassessed scope object; an overall count of
critical unknowns or unassessed critical scope requires the owner's scope and
criticality review. The earlier review's two retained unknowns are not an
enumerated register and do not establish an exhaustive current count.

## Ledger

| ID | Title | Level | Status | Supports | Limitation |
|---|---|---:|---|---|---|
| E-01 | Fictional architecture and crypto inventory | E2 | Current | C-01 through C-04 | Configuration verification incomplete |
| E-02 | Fictional data-lifetime record | E2 | Current | X-02 | Business retention assumption requires approval |
| E-03 | Fictional command-path laboratory notes | E3 | Conflicting | X-01, readiness testing | End-to-end result disagrees with vendor statement |
| E-04 | Fictional recovery procedure | E2 | Stale | Monitoring and recovery | Last exercised over one year ago |
| E-05 | Fictional migration options memo | E2 | Current | Migration strategy | No approved architecture |
| E-06 | Fictional vendor questionnaires | E1 | Current | Vendor readiness | One vendor response incomplete |
| E-07 | Fictional governance minutes | E2 | Current | Funding and ownership | Funding not authorized |

## Scope and dependency trace register

These entries trace the objects identified in the [scope](01-scope-and-link-map.md),
[inventory](02-cryptographic-inventory.md),
[exposure](03-quantum-exposure-severity.md) and
[override](06-critical-risk-overrides.md) records. They are provisional review
entries, not an approved coverage denominator or evidence-completeness finding.
Crypto dependencies and related critical conditions remain attached to their
scope objects so they cannot disappear from the review.

| Scope object | Related claims or dependencies | Evidence and status | Completeness limitation |
|---|---|---|---|
| SC-01 spacecraft avionics and secure boot | CR-03 key recovery; CR-04 safety applicability | E-01 Current | Configuration verification and governed recovery are incomplete; the fictional safety-owner determination is declared, not independently reproduced |
| LINK-01 primary command uplink | C-01, X-01; CR-01, CR-09, CR-12 | E-01 Current; E-03 Conflicting | End-to-end command authentication is incomplete and the material contradiction is unresolved |
| LINK-02 telemetry and mission-data downlink | C-02, X-02; CR-11 | E-01, E-02 Current | The fifteen-year horizon is documented, but retention approval and a migration decision remain pending |
| GS-01 ground station and mission network | C-04; CR-06 | E-01 Current; E-04 Stale | Operator identity is documented; current authenticated-recovery evidence is absent |
| UPDATE-01 firmware and software update path | C-03, X-03; CR-02, CR-05 | E-01 Current | Bootloader migration, secure-update and rollback evidence are incomplete |
| VENDOR-01 radio supplier | Algorithm roadmap and interoperability claim | E-06 Current, E1 | A preliminary self-attested roadmap does not establish interoperability or a complete commitment |
| VENDOR-02 ground-network service | Support/end-of-life dependency; CR-07 | E-06 Current, E1 | Support and end-of-life commitment is incomplete |
| Payload processing, pending scope decision | X-04; CR-09 | No evidence provided | Explicitly Unknown / Not Assessed; no approved exclusion, applicability determination or scope evidence |

## Readiness-domain claim trace register

Each canonical domain remains visible independently of the scope objects it
affects. Stage meanings and constraints are recorded in the
[readiness profile](04-migration-readiness-profile.md); the entries below assess
traceability limitations rather than assigning another stage or aggregate score.

| Canonical domain claim | Evidence and status | Completeness limitation |
|---|---|---|
| Governance and accountability | E-07 Current | Owners and actions are documented; funding and the payload scope decision are pending |
| Cryptographic inventory and visibility | E-01 Current | C-01 through C-04 are documented; configuration and dependency verification are incomplete |
| Exposure characterization | E-01, E-02 Current; E-03 Conflicting | Retention assumptions require approval; command-path evidence is unresolved and payload exposure is unassessed |
| Critical-link protection | E-01 Current; E-03 Conflicting | Identified critical paths do not establish demonstrated command, secure-update or rollback protection |
| Migration strategy and sequencing | E-05 Current | An options memo and initial roadmap do not establish an approved architecture or exit criteria |
| Crypto-agility architecture | E-05 Current, options only | No applicable architecture or controlled-change demonstration is provided; the domain remains Not Assessed |
| Implementation and interoperability | E-07 Current; E-03 Conflicting | Owned testing actions do not establish a representative end-to-end or interoperability result |
| Key and trust management | E-01 Current | Custody evidence is not provided; rotation and recovery design remain pending |
| Vendor and supply-chain readiness | E-06 Current, E1 | Self-attestation and incomplete commitments do not establish supported migration or interoperability |
| Monitoring, recovery, and reassessment | E-04 Stale | Historical recovery procedure cannot support a current capability claim; reassessment is required |

## Critical-condition traceability

The [override register](06-critical-risk-overrides.md) retains the conditions
below. Its Open, Closed and Not Applicable declarations are not evidence-
completeness decisions. In particular, a closure or applicability determination
must meet the [canonical override requirements](../../assessment/critical-risk-overrides.md).

| Condition | Existing declaration | Evidence linkage and remaining limitation |
|---|---|---|
| CR-01 | Open | LINK-01: E-01 Current, E-03 Conflicting; command demonstration incomplete |
| CR-02 | Open | UPDATE-01: E-01 Current; secure-update and rollback evidence incomplete |
| CR-03 | Open | SC-01: E-01 Current; governed key recovery pending |
| CR-04 | Not Applicable | Safety functions: E-01 Current; fictional applicability determination declared, supporting review not reproduced |
| CR-05 | Open | Bootloader/UPDATE-01: E-01 Current; no established migration or compensating path |
| CR-06 | Open | GS-01: E-01 Current, E-04 Stale; authenticated recovery not demonstrated |
| CR-07 | Open | VENDOR-02: E-06 Current, E1; support commitment incomplete |
| CR-08 | Closed | E-07 Current records owners and dates; full closure authority and verification details are not supplied in this public pack |
| CR-09 | Open | Payload and LINK-01: no payload evidence; E-03 Conflicting; scope and critical evidence gaps remain |
| CR-10 | Not Applicable | No additional mission-loss condition declared; no evidence ID is supplied for the applicability determination |
| CR-11 | Open | LINK-02: E-01, E-02 Current; long-lived confidentiality treatment remains pending |
| CR-12 | Open | LINK-01: E-03 Conflicting; contradiction requires reconciliation or escalation |

## Counting rule and pending decisions

Before calculating coverage, the accountable scope owner must approve the
complete item register and counting unit, including assets, links, crypto and
vendor dependencies, critical conditions and readiness-domain claims. The three
trace registers overlap and must not be summed into a denominator. For example,
LINK-01, C-01, CR-01, CR-12 and the critical-link domain describe related claims;
the owner must state which are distinct items and which are material claims of
the same item. Payload cannot be removed while its exclusion remains unapproved.

The assessor and reviewer must then record the material claims and support floor
for each approved item, confirm evidence currency and applicability, and identify
all critical unknowns. No item is counted complete merely because an E-ID exists
or a planning stage has an owner. The referenced fictional records do not supply
all source-owner, collection/verification-date, integrity and review details
required by the [evidence model](../../assessment/evidence-confidence-ledger.md).

Count each approved in-scope item once in the denominator. Count it once in the
numerator only when every material claim has current, applicable evidence meeting
its stated support floor. Stale, conflicting, unavailable or unassessed support
cannot satisfy that test; conflicts require reconciliation or escalation under
CR-12. A single item may have several gaps, and an E-ID may support several items;
neither overlap increases the numerator or licenses repeated subtraction from
the denominator. Keep the distinct critical-unknown, stale, conflicting and
unassessed categories visible instead of adding them into one gap total.

After approval and evidence review, calculate evidence-complete in-scope items
divided by total in-scope items, multiplied by 100, and state the rounding rule.
Until then, coverage remains NOT_ESTABLISHED. This traceability correction adds
no evidence, closes no critical condition and does not authorize the requested
pilot or operational deployment.
