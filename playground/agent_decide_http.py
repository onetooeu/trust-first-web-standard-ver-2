from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import httpx

GRADE_ORDER = ["A", "B", "C", "D", "E", "F", "UNKNOWN"]


def load_json(p: Path) -> Dict[str, Any]:
    return json.loads(p.read_text(encoding="utf-8"))


def grade_ge(a: str, b: str) -> bool:
    # True if grade a is >= grade b (A best)
    try:
        ia = GRADE_ORDER.index(a)
    except ValueError:
        ia = len(GRADE_ORDER) - 1
    try:
        ib = GRADE_ORDER.index(b)
    except ValueError:
        ib = len(GRADE_ORDER) - 1
    return ia <= ib


def decide(trust_state: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    score = trust_state.get("score") or {}
    grade = score.get("grade", "UNKNOWN")
    confidence = float(score.get("confidence", 0.0))

    signals = trust_state.get("signals") or []
    observed = [f"{s.get('code')}:{s.get('result')}" for s in signals if s.get("code")]

    block_on = set(policy.get("block_on") or [])
    quarantine_on = set(policy.get("quarantine_on") or [])
    warn_on = set(policy.get("warn_on") or [])

    signal_results = {s.get("code"): s.get("result") for s in signals if s.get("code")}

    for code in block_on:
        if signal_results.get(code) in ("fail", "warn"):
            return {
                "decision": "block",
                "reason": f"policy:block_on:{code}",
                "observed": observed,
                "grade": grade,
                "confidence": confidence,
            }

    for code in quarantine_on:
        if signal_results.get(code) in ("fail", "warn", "unknown"):
            return {
                "decision": "quarantine",
                "reason": f"policy:quarantine_on:{code}",
                "observed": observed,
                "grade": grade,
                "confidence": confidence,
            }

    min_grade = policy.get("min_grade_allow", "B")
    min_conf = float(policy.get("min_confidence_allow", 0.6))

    if not grade_ge(grade, min_grade):
        return {
            "decision": "block",
            "reason": "policy:grade_too_low",
            "observed": observed,
            "grade": grade,
            "confidence": confidence,
        }

    if confidence < min_conf:
        return {
            "decision": "warn",
            "reason": "policy:low_confidence",
            "observed": observed,
            "grade": grade,
            "confidence": confidence,
        }

    for code in warn_on:
        if signal_results.get(code) in ("fail", "warn", "unknown"):
            return {
                "decision": "warn",
                "reason": f"policy:warn_on:{code}",
                "observed": observed,
                "grade": grade,
                "confidence": confidence,
            }

    return {
        "decision": "allow",
        "reason": "policy:pass",
        "observed": observed,
        "grade": grade,
        "confidence": confidence,
    }


def fetch_trust_state(api_base: str, domain: str) -> Dict[str, Any]:
    url = api_base.rstrip("/") + f"/api/v1/trust/domain/{domain}"
    with httpx.Client(timeout=5.0) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.json()


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit("Usage: python playground/agent_decide_http.py <api_base> <domain> <policy.json>")

    api_base = sys.argv[1]
    domain = sys.argv[2]
    policy_path = Path(sys.argv[3])

    policy = load_json(policy_path)
    trust_state = fetch_trust_state(api_base, domain)

    result = decide(trust_state, policy)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
