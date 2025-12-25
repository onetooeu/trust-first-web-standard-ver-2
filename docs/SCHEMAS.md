# TFWS v2 Schemas

TFWS v2 uses JSON Schema as the normative contract.
Artifacts MUST validate against the relevant schema before trust decisions.

## Canonical schema location
This repository currently contains schemas in two locations:
- `schemas/` ? canonical for current tooling and docs
- `v2/schemas/` (compat/history copy)

If there is a mismatch, treat `schemas/` as authoritative unless a release note explicitly states otherwise.

## How to validate
Install tools (from repo root):

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -e tools/tfws2

