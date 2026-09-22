# Quantum Readiness for Space Communications

Evidence-based assessment and migration-planning framework for post-quantum cryptography across spacecraft, satellite links, ground systems, mission operations, and supporting vendors.

This repository helps teams identify cryptographic dependencies, document quantum-era exposure, plan migration, and assemble a human-reviewed **Quantum Readiness Decision Pack**.

It is documentation-first. It provides methods, templates, examples, and validation tools. It does not connect to live systems, implement cryptography, or issue certification or operational authorization.

## Bridge Node 7 system role

Quantum Readiness for Space Communications is the **post-quantum cryptographic-transition domain implementation** within [Bridge Node 7's Frontier Assurance Architecture](https://github.com/Bridge-Node-7/Bridge-Node-7/blob/main/docs/FRONTIER_ASSURANCE_ARCHITECTURE.md). Its Quantum Readiness Decision Pack is a domain-specific review artifact; it does not create a separate enterprise decision authority or automatic compliance determination.

## Start Here

| Goal | Start with | Continue with |
|---|---|---|
| Understand the completed workflow | [Fictional Decision Pack](examples/sample-small-satellite-decision-pack/README.md) | [Documentation Index](docs/README.md) |
| Begin an assessment | [Assessment Overview](assessment/quantum-readiness-space-communications-assessment.md) | [Assessor Guide](docs/assessor-guide.md) |
| Build the final deliverable | [Decision Pack Guide](decision-pack/README.md) | [Decision Summary Template](decision-pack/decision-summary-template.md) |
| Review technical context | [Quantum-Cryptography Foundations](docs/quantum-cryptography-foundations.md) | [Standards Register](docs/standards-register.md) |
| Validate a repository change | [Validation](#validate-the-repository) | [Methodology Integrity](docs/methodology-integrity.md) |

For a first review, open the fictional Decision Pack before filling in a blank template. It shows the expected structure, evidence links, unknowns, critical conditions, actions, limitations, and decision record.

## What You Need Before Starting

Use the framework only after defining:

- the authorized systems, links, data, vendors, and lifecycle stages in scope;
- an accountable scope owner and the intended decision;
- information-handling rules for mission, customer, vendor, security, and controlled data;
- available architecture, configuration, certificate, firmware, software, test, and vendor evidence;
- known exclusions, assumptions, review dates, and reassessment triggers.

Do not treat missing information as favorable evidence.

## Core Workflow

1. [Define scope, boundaries, owners, and exclusions](assessment/quantum-readiness-space-communications-assessment.md).
2. [Map spacecraft, ground, cloud, vendor, update, recovery, and communications paths](assessment/link-map-template.md).
3. [Inventory algorithms, protocols, certificates, libraries, firmware, keys, trust anchors, and vendor dependencies](assessment/crypto-inventory-template.md).
4. [Record Quantum Exposure Severity for each material scope item](assessment/quantum-exposure-severity.md).
5. [Profile migration readiness across ten separate domains](assessment/migration-readiness-profile.md).
6. [Record evidence confidence, provenance, currency, conflicts, and coverage](assessment/evidence-confidence-ledger.md).
7. [Evaluate all twelve Critical Risk Overrides](assessment/critical-risk-overrides.md).
8. [Assign accountable owners, actions, resources, due dates, and escalation paths](assessment/ownership-matrix-template.md).
9. [Build the migration and recovery roadmap](frameworks/pqc-migration-roadmap.md).
10. [Assemble and review the Quantum Readiness Decision Pack](decision-pack/README.md).

Start with inventory. Do not make a favorable exposure or readiness statement before the relevant systems, cryptography, owners, and evidence are in scope.

## Current Federal PQC Policy Context

Federal policy now provides explicit transition milestones that may affect Federal systems and covered contractors:

- Executive Order 14412 directs Federal migration to NIST-approved PQC standards, requires high-value assets and high-impact systems to use PQC for key establishment by **December 31, 2030** and digital signatures by **December 31, 2031**, and directs a proposed FAR rule requiring covered contractors to comply by **December 31, 2030** with applicable NIST FIPS incorporating PQC algorithms.
- OMB Memorandum M-26-15 phases Federal agency migration through **2035**, including prioritized key-establishment migration during 2028–2030, signature migration in 2031, and full migration of remaining covered systems by 2035. The memorandum states that it does not apply to National Security Systems.

These dates are policy context, not an automatic compliance determination for every spacecraft, operator, supplier, contract, or mission. Establish the governing authority and contract requirements before treating a date as applicable. See the [Standards and Guidance Register](docs/standards-register.md).

## What the Decision Pack Contains

The framework keeps four decision inputs separate:

1. **Quantum Exposure Severity** records concern for each asset, link, protocol, trust function, update path, vendor dependency, or protected data set.
2. **Migration Readiness Profile** records demonstrated capability across ten non-compensating domains.
3. **Evidence Confidence and Coverage** records support strength, provenance, currency, conflicts, exclusions, and unassessed critical scope.
4. **Critical Risk Overrides** preserve conditions that cannot be canceled by progress elsewhere.

The completed package also records scope, ownership, actions, vendor and standards applicability, migration and recovery planning, decisions, approvals, limitations, dissent, review history, and reassessment triggers.

## How to Interpret Results

- Higher exposure severity means greater concern.
- Higher readiness stages mean stronger demonstrated migration capability.
- Evidence strength is separate from exposure and readiness.
- Critical conditions cannot be averaged away.
- `Unknown / Not Assessed` remains visible until supported evidence is available.
- `Not Applicable` requires sufficient evidence, a written rationale, an accountable decision owner, and a reassessment trigger.
- Do not combine the four decision inputs into one aggregate readiness number.

These human-governed postures support planning only:

- **Assessment Incomplete**
- **Evidence Required**
- **Critical Action Required**
- **Executive Decision Required**
- **Ready for Governed Migration**

The postures are not certification, compliance determination, deployment approval, flight qualification, operational authorization, or proof that a system is quantum-safe.

## Who It Helps

The framework is useful for:

- spacecraft, satellite, payload, ground-station, and mission-operations teams;
- cybersecurity, cryptography, mission-assurance, and systems-engineering reviewers;
- program, procurement, supply-chain, vendor-management, and governance teams;
- commercial, civil, defense, national-security, international, and research programs applying their own authorized requirements;
- analysts and reviewers preparing evidence-linked planning artifacts for human review.

Use the [Role-Based Reading Paths](docs/role-based-reading-paths.md) for a shorter route through the repository.

## Repository Map

| Location | Purpose |
|---|---|
| `assessment/` | Scope, link map, cryptographic inventory, exposure, readiness, evidence, critical-condition, ownership, vendor, and executive templates |
| `briefings/` | Action-planning templates |
| `decision-pack/` | Final deliverable assembly, decision summary, and review record |
| `docs/` | Methodology, evidence, standards, technical context, limitations, and reading paths |
| `examples/` | Complete fictional worked example |
| `frameworks/` | Migration and recovery roadmap |
| `release/` | Release metadata and reproducibility records |
| `tests/` | Positive and adversarial methodology tests |
| `tools/` | Repository, link, public-boundary, manifest, and packaging validators |

## Validate the Repository

Git Bash or another Bash environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-validation.txt
bash scripts/validate.sh
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-validation.txt
powershell -ExecutionPolicy Bypass -File scripts/validate.ps1
```

The repository validators intentionally ignore local virtualenv/cache directories such as `.venv` while continuing to validate governed source files.

Hosted continuous integration also runs network-aware link checks. To enable those checks locally:

```bash
VALIDATE_NETWORK=1 bash scripts/validate.sh
```

The validators check repository integrity and methodology boundaries. They do not calculate an assessment result.

## Release status

`main` is the current reviewed source. GitHub Releases are stable distribution milestones and may intentionally lag reviewed maintenance on `main`. A source version ahead of the latest GitHub Release is unreleased until a release is published.

## Publicly Distributable Use

Use only information approved for unrestricted publication. Keep scope, evidence, limitations, and decision authority explicit.

Before publishing a completed artifact, apply the review and authorization requirements appropriate to the environment.

## Limits and Responsible Use

Read [Known Limitations](KNOWN_LIMITATIONS.md), [Public Claim Boundaries](docs/public-claim-boundaries.md), and [SECURITY.md](SECURITY.md).

This framework supports evidence-based planning. It does not replace cryptographic engineering, mission engineering, safety review, legal analysis, contracting decisions, standards applicability determinations, or formal authorization processes.

## License and Citation

MIT License. See [LICENSE](LICENSE).

Use [CITATION.cff](CITATION.cff) and cite the exact tagged release used for an assessment or derivative work.
