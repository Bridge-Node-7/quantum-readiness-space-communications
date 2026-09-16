# Contributing

Contributions are welcome when they preserve the repository's publicly distributable, evidence-first scope.

## Before opening a pull request

1. Read [GOVERNANCE.md](GOVERNANCE.md).
2. Confirm the change does not introduce an automated assurance engine or cryptographic implementation.
3. Update affected methodology and compatibility records.
4. Add or update tests for methodology invariants.
5. Run the complete validation suite.

```bash
bash scripts/validate.sh
```

## Methodology changes

A methodology change must state:

- the objective or condition being advanced;
- the affected files and outputs;
- whether the change is breaking;
- how non-compensation, evidence separation, and critical overrides remain intact;
- what tests prove the change;
- any standards-status or applicability effect.

## Publicly distributable requirements

Do not submit real secrets, credentials, mission data, controlled technical data, sensitive architecture, customer information, or proprietary vendor evidence.

## Claim boundaries

Do not describe the framework or its outputs as certification, authorization, compliance determination, operational validation, flight qualification, or proof that a system is quantum-safe.
