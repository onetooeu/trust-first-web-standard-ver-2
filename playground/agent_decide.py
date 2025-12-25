from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

GRADE_ORDER = ["A", "B", "C", "D", "E", "F", "UNKNOWN"]

def load_json(p: Path) -> Dict[str, Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def grade_ge(a: str, b: str) -> bool:
    # return True if grade a is >= grade b (A best)
    try:
        ia = GRADE_ORDER.index(a)
    except ValueError:
        ia = len(GRADE_ORDER) - 1
    try:
        ib = GRADE_ORDER.index(b)
    except ValueError:
        ib = len(GRADE_ORDER) - 1
    return ia <= ib  # smaller index = better grade

def signal_codes(payload: Dict[str, Any]) -> List[str]:
    out = []
    for s in payload.get("signals", []) or []:
        code = s.get("code")
        res = s.get("result")
        if code and res:
            out.append(f"{code}:{res}")
    return out

def decide(trust_state: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    score = trust_state.get("score") or {}
    grade = score.get("grade", "UNKNOWN")
    confidence = float(score.get("confidence", 0.0))

    codes = signal_codes(trust_state)

    def has(prefix: str) -> bool:
        # prefix like "rollback_suspected" matches any "rollback_suspected:fail|warn|pass|unknown"
        for c in codes:
            if c.startswith(prefix + ":"):
                return True
        return False

    # Hard blocks
    for c in policy.get("block_on", []) or []:
        if has(c):
            return {"decision": "block", "reason": f"policy:block_on:{c}", "observed": codes}

    # Quarantine
    for c in policy.get("quarantine_on", []) or []:
        if has(c):
            return {"decision": "quarantine", "reason": f"policy:quarantine_on:{c}", "observed": codes}

    # Grade/Confidence gates
    min_grade = policy.get("min_grade_allow", "B")
    min_conf = float(policy.get("min_confidence_allow", 0.6))

    if not grade_ge(grade, min_grade) or confidence < min_conf:
        # maybe warn instead of block
        return {"decision": "warn", "reason": "policy:grade_or_confidence_low", "observed": codes, "grade": grade, "confidence": confidence}

    # Warn signals
    for c in policy.get("warn_on", []) or []:
        if has(c):
            return {"decision": "warn", "reason": f"policy:warn_on:{c}", "observed": codes}

    return {"decision": "allow", "reason": "policy:pass", "observed": codes, "grade": grade, "confidence": confidence}

def main():
    if len(sys.argv) < 3:
        print("Usage: python playground/agent_decide.py <trust_state.json> <policy.json>", file=sys.stderr)
        raise SystemExit(2)

    trust_path = Path(sys.argv[1])
    policy_path = Path(sys.argv[2])

    trust = load_json(trust_path)
    policy = load_json(policy_path)

    out = decide(trust, policy)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
