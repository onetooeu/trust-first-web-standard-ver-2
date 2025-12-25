# Compliance & Regulatory Mapping (TFWS v2)

TFWS v2 is a technical trust standard. It is not a legal framework, certification scheme, or regulatory authority.
This document explains how TFWS v2 can SUPPORT compliance and audit processes without replacing them.

---

## Compliance philosophy

TFWS v2 follows a **trust-by-evidence** approach:
- publish verifiable facts
- make integrity and continuity machine-checkable
- let auditors, agents, and regulators draw conclusions

TFWS v2 does NOT:
- issue certifications
- assert legal compliance
- replace human or organizational accountability

---

## Supported compliance dimensions

TFWS v2 provides technical primitives that help satisfy common compliance needs:

### Integrity
- Cryptographic signatures (Ed25519 / minisign)
- Tamper-evident inventories (`sha256.json`)
- Detects unauthorized modification of published artifacts

### Traceability
- Versioned artifacts
- Time-scoped key validity (`key-history.json`)
- Auditable change history

### Transparency
- Machine-readable trust state
- Explicit incident disclosure artifacts
- Publicly verifiable evidence

### Non-repudiation (technical)
- Signed artifacts tied to published keys
- Clear separation between data, signatures, and keys

---

## Mapping to common frameworks (non-exhaustive)

### ISO/IEC 27001 / 27002
TFWS v2 supports:
- A.8 Asset management (inventory + integrity)
- A.12 Operations security (change detection)
- A.16 Incident management (incident artifacts)

TFWS does not replace an ISMS.

### SOC 2 (Trust Services Criteria)
TFWS v2 supports evidence for:
- Security (integrity of artifacts)
- Availability (rollback detection)
- Processing integrity (validated structures)

TFWS does not perform audits or attestations.

### EU AI governance / AI Act (supportive role)
TFWS v2 can support:
- Transparency obligations (published trust state)
- Traceability of model/service metadata
- Machine-readable signals for AI-to-AI interaction

TFWS v2 does not classify AI systems or assign risk levels.

### Supply chain security
TFWS v2 supports:
- Signed metadata publication
- Detection of rollback/replay attacks
- Verification of upstream artifacts

---

## Incident handling & disclosure

TFWS v2 defines a **standardized incident artifact**:
- schema-valid incident records
- clear lifecycle (investigating › resolved)
- explicit impact declaration

This supports:
- internal incident response
- external transparency
- audit evidence

TFWS does not mandate disclosure thresholds or timelines.

---

## Audit usage model

An auditor or automated agent may:
1) Fetch published artifacts
2) Validate schemas
3) Verify signatures and inventories
4) Check key validity at relevant times
5) Compare versions over time

TFWS v2 provides **verifiable inputs**, not audit conclusions.

---

## Limitations & disclaimers

- TFWS v2 does not guarantee correctness of published claims
- TFWS v2 does not detect malicious intent by itself
- Trust decisions remain the responsibility of relying parties
- Legal interpretation is jurisdiction-specific

---

## Summary

TFWS v2 is best understood as:
- a **compliance-enabling infrastructure**
- a way to publish and verify evidence
- a bridge between technical systems and governance processes

It complements existing regulatory and audit frameworks without competing with them.
