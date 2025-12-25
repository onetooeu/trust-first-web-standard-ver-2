# TFWS v2 Architecture

TFWS v2 is a **domain-first trust publishing and verification standard**.
It defines a small set of machine-readable artifacts (JSON) and a verification workflow that agents can run without a central authority.

This repository provides:
- Normative JSON Schemas (`/schemas`)
- Reference tooling (`/tools/tfws2`)
- Optional reference services (`/services/trust_api`)
- Optional playground (`/playground`)

---

## 1) Layered view

### Layer 0 — Publishing surface (Domain)
A TFWS-enabled domain MAY publish trust artifacts at stable URLs, typically under `/.well-known/` and optionally under a public dumps path.

Typical endpoints:
- `/.well-known/ai-trust-hub.json` (entry point / manifest)
- `/.well-known/minisign.pub` (public verification key)
- `/.well-known/key-history.json` (key epochs, rotations, revocations)
- `/dumps/sha256.json` and `/dumps/sha256.json.minisig` (optional signed inventory)

### Layer 1 — Schemas (Normative contract)
All artifacts MUST validate against the JSON Schemas in:
- `schemas/` (canonical)

Schemas define:
- required fields
- allowed values / enums
- date-time formats
- additionalProperties rules (hardening)

### Layer 2 — Tooling (Verifier/Validator)
Reference tooling in `tools/tfws2` provides:
- schema validation (`tfws2 validate`)
- inventory computation (`tfws2 hashwalk`)
- minisign detached signature verification (`tfws2 verify-minisign`)
- inventory verification helper (`tfws2 verify-inventory`)
- key epoch checks (`tfws2 check-key-epoch`)
- rollback simulation (`tfws2 simulate-rollback`)

### Layer 3 — Policy & decision (Agent side)
TFWS does not enforce a single global policy.
Instead, agents apply local policy using the validated signals:
- allow / warn / quarantine / block
- thresholds (grade, confidence)
- hard rules (block_on / quarantine_on lists)

The repo includes a minimal reference policy and a CLI playground.

### Layer 4 — Optional API layer (Service)
A Trust API can exist as a convenience layer:
- fetches/probes well-known endpoints
- (optionally) verifies signatures / inventories
- outputs a schema-valid `trust-state` payload
- makes integration easier for applications and agents

This repo includes `services/trust_api` as a reference implementation.

---

## 2) Data flow (end-to-end)

### A) Operator / domain owner (Publish mode)
1. Generate or rotate signing keys (minisign/Ed25519).
2. Publish public key: `/.well-known/minisign.pub`.
3. Publish manifest/entry point: `/.well-known/ai-trust-hub.json`.
4. Optionally publish:
   - `/.well-known/key-history.json` (key epoch governance)
   - `/dumps/sha256.json` + `/dumps/sha256.json.minisig` (signed inventory)

### B) Agent / verifier (Verify mode)
1. Fetch artifacts from the domain.
2. Validate each artifact against TFWS schemas.
3. Verify integrity (when available):
   - minisign detached signatures
   - inventory integrity
   - key epoch validity (not_before / not_after / status)
4. Convert observations into signals and score (implementation-defined).
5. Apply local policy to decide: allow / warn / quarantine / block.
6. Cache results until `valid_until` or local TTL.

---

## 3) Trust-State output model (reference)

The reference output `trust-state` contains:
- subject (domain/org/service/endpoint)
- computed_at + valid_until
- score (value/confidence/grade)
- signals[] (code, weight, result, evidence)

The **meaning** of signals is stable; the **policy** interpretation is local.

---

## 4) Threat model notes

TFWS v2 is designed around practical threats:
- spoofed payloads (mitigated by signatures + schema validation)
- rollback/replay of older inventories (mitigated by key epochs + rollback simulation)
- partial publication / missing endpoints (handled as warn/unknown and policy decisions)
- redirections / transport differences (handled by follow_redirects rules in clients)

---

## 5) Repository map

- `docs/` — documentation set (getting started, schemas, governance, compliance, use cases)
- `schemas/` — canonical JSON Schemas
- `examples/` — schema-valid example artifacts
- `tools/tfws2/` — reference CLI + utilities
- `services/trust_api/` — optional reference API
- `playground/` — optional agent decision playground

