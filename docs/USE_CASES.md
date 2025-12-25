# Use Cases (TFWS v2)

This document lists practical scenarios where TFWS v2 provides value.
Each use case is expressed as:
- Publisher (who publishes)
- Artifacts (what is published)
- Verifier (who verifies)
- Decision (what happens next)

TFWS v2 provides verifiable inputs. The final decision is always policy-driven.

---

## 1) Domain trust profile for agents (baseline)
**Publisher:** a domain operator (company, public institution, service owner)

**Artifacts:**
- `trust-state.json` (schema-valid)
- `key-history.json` (schema-valid)
- inventory `sha256.json` + detached signature(s)
- published public key (e.g., `/.well-known/minisign.pub`)

**Verifier:** crawler / AI agent / partner integration

**Checks:**
- `tfws2 validate` on `trust-state.json`
- `tfws2 verify-inventory` for published inventory
- `tfws2 check-key-epoch` at time-of-use

**Decision examples:**
- allow automated browsing/integration
- warn if signatures missing
- quarantine if rollback suspected

---

## 2) Signed release artifact distribution
**Publisher:** open-source project or vendor publishing releases

**Artifacts:**
- signed inventories for release bundles
- optional `trust-state` for the release endpoint
- optional `incident` if a release must be revoked

**Verifier:** CI system, package manager, enterprise downloader

**Checks:**
- verify inventory signature
- compare inventory across time to detect rollback
- validate incident disclosures

**Decision examples:**
- accept release only if signature and epoch checks pass
- block downloads if a key is revoked
- require manual review if downgrade detected

---

## 3) Incident disclosure & operational transparency
**Publisher:** service operator after a security or integrity event

**Artifacts:**
- `incident.json` (schema-valid)
- updated `trust-state.json` (score/signals reflect current posture)
- updated `key-history.json` if key rotation/revocation occurred

**Verifier:** partners, auditors, automated agents

**Checks:**
- schema validation for incident lifecycle
- verify that artifacts are signed and current

**Decision examples:**
- temporarily reduce trust score locally
- pause high-risk automations
- resume once status becomes `resolved`

---

## 4) Key rotation with continuity guarantees
**Publisher:** any operator rotating signing keys

**Artifacts:**
- updated `key-history.json` (new key active, old key retired/revoked)
- new signatures for inventories/artifacts
- optional incident for emergency rotation

**Verifier:** agents verifying at different points in time

**Checks:**
- `tfws2 check-key-epoch --at <time>`
- reject signatures outside valid epoch windows

**Decision examples:**
- accept old signatures for historical artifacts (when valid in that epoch)
- reject signatures by revoked keys regardless of time (policy-dependent)

---

## 5) API response integrity (product layer on top of TFWS)
**Publisher:** service exposing an API that returns trust-relevant claims

**Artifacts:**
- signed API responses or signed daily dumps
- schema-valid payloads where applicable
- published public key + key history

**Verifier:** another service, agent, integrator

**Checks:**
- validate response structure
- verify signature (detached or embedded)
- ensure the signing key is valid at time-of-response

**Decision examples:**
- accept responses into automated decision pipelines
- require fallback to cached/known-good if verification fails

Note: TFWS v2 provides the building blocks; the API layer is an implementation detail.

---

## 6) Anti-rollback protection for trust feeds
**Publisher:** a domain publishing a frequently updated trust feed/dump

**Artifacts:**
- periodic inventories (e.g., daily `sha256.json`)
- signatures for each inventory
- optional rollback simulation guidance

**Verifier:** agents comparing current vs candidate inventories

**Checks:**
- `tfws2 simulate-rollback --current A --candidate B`
- treat downgrade as suspicious

**Decision examples:**
- hard-fail and alert
- quarantine candidate state and request more evidence
- allow only if explicitly whitelisted by policy

---

## 7) Cross-organization partner onboarding
**Publisher:** a vendor or partner publishing machine-readable trust posture

**Artifacts:**
- trust state + key history + signed inventory
- incident disclosures (when needed)

**Verifier:** procurement automation, integration gateways

**Checks:**
- validate + verify as normal
- enforce local minimum requirements (e.g., signatures required)

**Decision examples:**
- auto-approve low-risk integration
- require human approval for missing signals
- block high-risk or compromised partners

---

## What to publish first (practical starter)
If you are adopting TFWS v2 today, start with:
1) a schema-valid `trust-state.json`
2) a schema-valid `key-history.json`
3) a signed inventory for your published trust artifacts

Then expand with incident disclosures and additional signals as needed.
