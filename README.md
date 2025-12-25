🧭 Trust-First Web Standard v2 — Beta Release

This is the first complete public release of Trust-First Web Standard (TFWS) v2.

TFWS v2 defines a domain-first, signature-based trust publishing model designed for both humans and autonomous agents — without central authorities.

✅ What’s included
📐 Normative core

Finalized TFWS v2 JSON Schemas

trust-state

incident

key-history

Schema-validated examples for all artifacts

Smoke tests validating schemas against examples

📚 Documentation set (complete)

Architecture overview

Governance & versioning policy

Compliance & regulatory mapping

Use cases

Getting Started guide

Schema reference map

🛠 Reference tooling

tfws2 CLI tools:

schema validation

hash inventory generation

minisign (Ed25519) verification

key epoch checks

rollback simulation

🌐 Reference Trust API (optional layer)

FastAPI-based Trust API

Deterministic scoring & grading

Probing of:

/.well-known/ai-trust-hub.json

/.well-known/minisign.pub

/.well-known/key-history.json

signed inventory (sha256.json + .minisig)

Always emits schema-valid trust-state

🤖 Agent Decision Playground

CLI-based agent decision engine

Policy-driven decisions:

allow / warn / quarantine / block

HTTP-based agent consuming Trust API

🧠 Design philosophy

Trust is published, not granted

Verification over authority

Schemas over prose

Local policy over global rules

Human-readable + machine-verifiable by default

TFWS v2 is intentionally minimal, composable, and future-proof.

⚠️ Release status

Status: Beta

Compatibility: TFWS v2 only (no backward compatibility with v1)

API stability: Schemas considered stable; tooling & API may evolve

Security: Reference implementations are not hardened for production

🚀 Next steps

Community feedback

Independent implementations

Optional future v2.x iterations

No mandatory roadmap is imposed.

🖤 Trust-First Web Standard is released to live its own life.
