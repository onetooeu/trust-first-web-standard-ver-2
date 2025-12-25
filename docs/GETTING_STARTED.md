# Getting Started (TFWS v2)

TFWS v2 is usable in two modes:
- Publish mode (operators): publish signed artifacts for a domain
- Verify mode (agents/tools): validate artifacts and enforce local policy

This repository ships:
- TFWS v2 JSON Schemas (schemas/)
- Python tools (tools/tfws2) via the tfws2 CLI
- Valid examples (examples/schemas/)
- Documentation (docs/)

---

## Install the TFWS v2 tools (tfws2)

From repository root:

python -m pip install -e tools/tfws2

Verify:

tfws2 --help

---

## Validate examples against schemas

tfws2 validate --schema schemas/trust-state.schema.json --json examples/schemas/trust-state.example.json
tfws2 validate --schema schemas/incident.schema.json --json examples/schemas/incident.example.json
tfws2 validate --schema schemas/key-history.schema.json --json examples/schemas/key-history.example.json

---

## Run smoke tests

python -m pip install -U pytest
python -m pytest -q

---

## Run the Trust API (reference implementation)

The repository includes a minimal FastAPI service that generates a schema-valid TFWS v2 trust-state payload.

Install:

python -m pip install -e services/trust_api

Run:

python -m trust_api.app

The API will start on http://127.0.0.1:8787

Example request:

curl http://127.0.0.1:8787/api/v1/trust/domain/example.com

---

## Run the Agent Decision Playground (CLI)

Run:

python playground/agent_decide.py examples/schemas/trust-state.example.json playground/policies/default-policy.json

Output:
- allow
- warn
- quarantine
- block
