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

---

## Trust-First Web Standard (TFWS v2)

ONETOO.eu je praktickou referenčnou implementáciou
**Trust-First Web Standard (TFWS v2)** — otvoreného, decentralizovaného
štandardu pre publikovanie **overiteľných signálov dôvery** na úrovni domény.

TFWS nevytvára nové autority, registry ani povolenia.
Nepotrebuje účty, onboarding ani runtime služby.
Je navrhnutý ako **čisto publikačný a overiteľný mechanizmus**,
ktorý funguje výhradne nad existujúcim webom.

---

## Prečo Trust-First

Moderný web je postavený na nepriamych a často implicitných formách dôvery:
certifikačné autority, identity provideri, uzavreté API ekosystémy,
reputačné databázy a platformové signály.

Tieto systémy majú spoločné vlastnosti:
- centralizované rozhodovanie
- netransparentné procesy
- nemožnosť nezávislého overenia
- dlhodobú krehkosť

TFWS vychádza z opačného predpokladu:

> **Dôvera nie je niečo, čo sa udeľuje.  
> Dôvera je niečo, čo sa publikuje.  
> Overenie a interpretácia patria pozorovateľovi.**

---

## Čo TFWS robí (a nerobí)

TFWS rieši **len jednu vec** — publikovanie tvrdení spôsobom,
ktorý je technicky overiteľný a dlhodobo stabilný.

### TFWS umožňuje:
- publikovať strojovo čitateľné vyhlásenia o doméne
- pripojiť kryptografický podpis k týmto vyhláseniam
- umožniť komukoľvek ich overiť offline
- vytvoriť konzistentný „trust surface“ pre ľudí aj AI

### TFWS zámerne nerobí:
- hodnotenie dôvery
- prideľovanie reputácie
- autorizáciu prístupu
- centralizované rozhodovanie

TFWS je **formát a proces**, nie arbitrážny mechanizmus.

---

## Architektonický model

TFWS je navrhnutý ako **web-native, statický systém**.

Základný tok je vždy rovnaký:

1. Doména publikuje súbory v `/.well-known/`
2. Súbory sú jednoznačne identifikovateľné (URL, hash)
3. Súbory sú kryptograficky podpísané (Ed25519 / minisign)
4. Overenie prebieha bez potreby tretej strany

Typické artefakty:
- `ai-trust-hub.json`
- `llms.txt`
- `minisign.pub`
- podpisy (`*.minisig`)
- hash inventory (`dumps/sha256.json`)

Všetko je:
- statické
- auditovateľné
- archivovateľné
- CDN-friendly

---

## Machine-first, human-verifiable

TFWS je navrhnutý primárne pre **stroje**:
AI agentov, crawlerov, autonómne systémy, validačné nástroje.

Zároveň však:
- každý súbor má stabilnú URL
- každý podpis je overiteľný bežným nástrojom
- každý artefakt je čitateľný aj bez špecializovaného softvéru

To umožňuje:
- nezávislý audit
- dlhodobé uchovanie
- manuálnu kontrolu v krízových situáciách

---

## ONETOO.eu ako referenčný trust hub

ONETOO.eu slúži ako **tichý referenčný bod** pre TFWS v2.

Nie je to:
- certifikačná autorita
- registrátor
- trust provider

Je to:
- konzistentná, stabilná implementácia
- ukážka kompletného trust pipeline
- dlhodobo nemenný publikačný bod

ONETOO.eu nikoho neschvaľuje.
Len **publikuje vlastné overiteľné vyhlásenia**.

---

## Dlhodobý dizajn a stabilita

TFWS v2 je navrhnutý s cieľom:
- minimálnych zmien
- maximálnej spätnej kompatibility
- odolnosti voči technologickým trendom

Štandard je vhodný na:
- archiváciu
- „cold storage“
- dlhodobé referencovanie

Ak sa okolo TFWS prestane rozvíjať ekosystém,
samotné artefakty **zostanú čitateľné a overiteľné**.

---

## Licencia a použitie

TFWS aj ONETOO.eu sú publikované ako **verejné dobro**.

- žiadne poplatky
- žiadne licenčné obmedzenia
- žiadne povolenia
- žiadne závislosti

Používaj.
Forkuj.
Archivuj.
Overuj.

---

## Záverečný princíp

TFWS nikoho nenúti veriť.
TFWS nikoho nepresviedča.
TFWS nikoho nehodnotí.

TFWS len hovorí:

> „Toto je tvrdenie.  
> Toto je podpis.  
> Rozhodnutie je na tebe.“

