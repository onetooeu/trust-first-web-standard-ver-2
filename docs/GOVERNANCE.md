# Governance (TFWS v2)

This document defines how TFWS v2 evolves: versioning rules, decision rights, and release process.
TFWS is designed to be stable for decades: changes are intentional, reviewable, and verifiable.

## Scope
Governance covers:
- Schema evolution (`schemas/*.schema.json`)
- Tooling behavior contracts (`tools/tfws2` CLI semantics)
- Documentation and normative requirements

Governance does NOT cover:
- Any single website/product implementation
- Central registries or authorities (TFWS is domain-first and decentralized)

---

## Roles
### Maintainers
Maintainers are the people with commit access to the canonical repository.
Responsibilities:
- Review and merge changes
- Cut releases and publish changelogs
- Maintain backward compatibility rules

### Contributors
Anyone can propose changes via pull requests/issues.
Contributors must follow the change process below.

---

## Decision policy
- **Security fixes**: prioritized, may be released out-of-band.
- **Breaking changes**: require an explicit major version bump and a migration note.
- **Normative schema changes**: must include updated examples and tests in the same PR.

When in doubt: choose stability over novelty.

---

## Versioning
TFWS v2 follows semantic versioning with a strict interpretation:

- **MAJOR** (X.0): breaking changes to schemas or verification semantics
- **MINOR** (2.Y): backward-compatible additions (new optional fields, new schemas, additive CLI flags)
- **PATCH** (2.Y.Z): clarifications, bug fixes, doc fixes; no schema breakage

### Pre-releases
Examples: `2.0.0-beta.1`, `2.0.0-rc.1`

Pre-release rules:
- Intended for testing and early adopters
- Backward compatibility is best-effort
- Breaking changes are allowed between pre-release builds
- Once `2.0.0` is released, compatibility expectations become strict

---

## Backward compatibility rules (schemas)
Allowed in MINOR/PATCH:
- Add new **optional** properties
- Add new schema files (new artifact types)
- Tighten descriptions, examples, and documentation (without changing validation result for valid instances)

Breaking (requires MAJOR):
- Remove a required field
- Change the type/meaning of an existing field
- Make an optional field required
- Tighten constraints such that previously valid payloads become invalid

Deprecation strategy:
- Mark fields as deprecated in docs first
- Keep them valid for at least one MINOR cycle unless security requires removal sooner
- Provide migration guidance and examples

---

## Compatibility rules (tools / CLI)
The `tfws2` CLI is part of the public surface area.

Allowed in MINOR/PATCH:
- Add new subcommands
- Add new flags with safe defaults
- Improve error messages
- Performance improvements that preserve outputs and exit codes

Breaking (requires MAJOR):
- Rename/remove subcommands
- Change default output formats in a way that breaks scripts
- Change exit code meanings
- Change verification semantics

---

## Required artifacts per change (quality gates)
Any PR that modifies schemas MUST include:
1) Updated schema file(s) in `schemas/`
2) Updated example JSON in `examples/schemas/`
3) A validation proof (CI or smoke test) that examples validate with `tfws2 validate`

Any PR that modifies CLI behavior MUST include:
1) Updated `tools/tfws2/README.md`
2) A smoke test or reproducible command showing expected output

---

## Release process
1) Merge changes to `main`
2) Update CHANGELOG (or release notes)
3) Tag release (e.g., `v2.0.1`)
4) Publish signed release artifacts if applicable (inventory + signatures)
5) Announce compatibility notes (especially for MINOR/MAJOR)

---

## Security & incident handling
If a security issue affects TFWS itself (schemas/tools):
- Create an `incident` entry describing impact and mitigation
- Release a patch or minor version depending on scope
- Document whether any artifacts or keys need rotation

If a signing key is compromised in a TFWS deployment:
- Update `key-history.json` (set compromised key to `revoked`)
- Publish an incident record
- Rotate keys and publish new signatures/inventory

---

## Repository policy
- `main` is the canonical line.
- Documentation is treated as part of the product surface area.
- Releases may be cryptographically sealed (signed inventories) to make history auditable.

