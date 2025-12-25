from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Tuple

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]  # repo root
SCHEMA_TRUST_STATE = ROOT / "schemas" / "trust-state.schema.json"

app = FastAPI(
    title="TFWS v2 Trust API (reference)",
    version="0.2.0",
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

def probe_ai_trust_hub(domain: str) -> Tuple[str, List[str]]:
    """
    Best-effort probe for: https://<domain>/.well-known/ai-trust-hub.json

    Returns: (result, evidence[])
      result in {pass, fail, warn, unknown}
    """
    url = f"https://{domain}/.well-known/ai-trust-hub.json"
    timeout = 2.5
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            r = client.head(url)
            status = r.status_code
            # Some servers don't support HEAD; fallback to GET.
            if status in (405, 501):
                r = client.get(url)
                status = r.status_code
    except Exception:
        return "unknown", [url]

    if status == 200:
        return "pass", [url]
    if status == 404:
        return "fail", [url]
    # other statuses (3xx/4xx/5xx) treated as warn
    return "warn", [f"{url} (http:{status})"]

def score_from_signals(signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Deterministic reference scoring model.

    - Start at 50
    - pass: +abs(weight)
    - fail: -abs(weight)
    - warn/unknown: 0
    Confidence increases with count of pass/fail (deterministic) signals.
    """
    total = 50.0
    known = 0

    for s in signals:
        w = float(s.get("weight", 0))
        res = s.get("result")
        if res == "pass":
            total += abs(w); known += 1
        elif res == "fail":
            total -= abs(w); known += 1

    total = max(0.0, min(100.0, total))
    confidence = min(1.0, 0.25 + 0.15 * known)

    if total >= 90:
        grade = "A"
    elif total >= 80:
        grade = "B"
    elif total >= 70:
        grade = "C"
    elif total >= 60:
        grade = "D"
    elif total >= 50:
        grade = "E"
    else:
        grade = "F"

    return {"value": total, "confidence": confidence, "grade": grade}

def _basic_signals(domain: str) -> List[Dict[str, Any]]:
    """
    Minimal baseline signals. Real probes can overwrite / add signals.
    """
    return [
        {"code": "schema_valid", "weight": 10, "result": "pass", "evidence": ["schemas/trust-state.schema.json"]},
        {"code": "well_known_present", "weight": 15, "result": "unknown", "evidence": ["/.well-known/ai-trust-hub.json"]},
        {"code": "inventory_signed", "weight": 15, "result": "unknown", "evidence": ["sha256.json.minisig (optional)"]},
        {"code": "key_epoch_valid", "weight": 10, "result": "unknown", "evidence": ["key-history.json (optional)"]},
    ]

def build_trust_state_for_domain(domain: str) -> Dict[str, Any]:
    schema = _load_schema(SCHEMA_TRUST_STATE)

    signals = _basic_signals(domain)

    # Replace well_known_present using real probe
    wk_result, wk_evidence = probe_ai_trust_hub(domain)
    for s in signals:
        if s.get("code") == "well_known_present":
            s["result"] = wk_result
            s["evidence"] = wk_evidence

    score = score_from_signals(signals)

    payload: Dict[str, Any] = {
        "schema_version": "2.0",
        "subject": {"type": "domain", "id": domain},
        "computed_at": _now_z(),
        "valid_until": _valid_until_z(7),
        "score": score,
        "signals": signals,
    }

    _validate(schema, payload)
    return payload

@app.get("/api/v1/trust/domain/{domain}")
def get_trust_domain(domain: str):
    if len(domain) < 3 or "." not in domain:
        raise HTTPException(status_code=400, detail="Invalid domain format")

    payload = build_trust_state_for_domain(domain)
    return JSONResponse(content=payload)

def main():
    import uvicorn
    uvicorn.run("trust_api.app:app", host="127.0.0.1", port=8787, reload=True)

if __name__ == "__main__":
    main()
