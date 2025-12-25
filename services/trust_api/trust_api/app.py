from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]  # repo root
SCHEMA_TRUST_STATE = ROOT / "schemas" / "trust-state.schema.json"

app = FastAPI(
    title="TFWS v2 Trust API (reference)",
    version="0.1.0",
    description="Reference API layer on top of TFWS v2 schemas. Returns schema-valid trust-state payloads.",
)

def _now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def _valid_until_z(days: int = 7) -> str:
    t = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(days=days)
    return t.isoformat().replace("+00:00", "Z")

def _load_schema(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def _validate(schema: Dict[str, Any], payload: Dict[str, Any]) -> None:
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(payload), key=lambda e: list(e.path))
    if errors:
        msg = "; ".join([f"{list(e.path)}: {e.message}" for e in errors[:10]])
        raise HTTPException(status_code=500, detail=f"Generated payload failed schema validation: {msg}")

def _basic_signals(domain: str) -> List[Dict[str, Any]]:
    # Minimal, deterministic, safe defaults. Real checks (DNS/.well-known fetch) come later.
    return [
        {"code": "schema_valid", "weight": 10, "result": "pass", "evidence": ["schemas/trust-state.schema.json"]},
        {"code": "well_known_present", "weight": 10, "result": "unknown", "evidence": ["/.well-known/ai-trust-hub.json"]},
        {"code": "inventory_signed", "weight": 15, "result": "unknown", "evidence": ["sha256.json.minisig (optional)"]},
        {"code": "key_epoch_valid", "weight": 10, "result": "unknown", "evidence": ["key-history.json (optional)"]},
    ]

def build_trust_state_for_domain(domain: str) -> Dict[str, Any]:
    schema = _load_schema(SCHEMA_TRUST_STATE)

    payload: Dict[str, Any] = {
        "schema_version": "2.0",
        "subject": {"type": "domain", "id": domain},
        "computed_at": _now_z(),
        "valid_until": _valid_until_z(7),
        "score": {"value": 50.0, "confidence": 0.30, "grade": "UNKNOWN"},
        "signals": _basic_signals(domain),
    }

    _validate(schema, payload)
    return payload

@app.get("/api/v1/trust/domain/{domain}")
def get_trust_domain(domain: str):
    # Basic sanity: avoid obviously invalid strings
    if len(domain) < 3 or "." not in domain:
        raise HTTPException(status_code=400, detail="Invalid domain format")

    payload = build_trust_state_for_domain(domain)

    # Signature hook (future): compute detached signature or header signature.
    # For now we return unsigned payload. Later we can add:
    # - X-Trust-Signature
    # - X-Trust-KeyId
    # - X-Trust-Inventory
    return JSONResponse(content=payload)

def main():
    import uvicorn
    uvicorn.run("trust_api.app:app", host="127.0.0.1", port=8787, reload=True)

if __name__ == "__main__":
    main()
