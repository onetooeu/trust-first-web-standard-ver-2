from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def _parse_dt(s: str) -> datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s).astimezone(timezone.utc)


@dataclass
class KeyDecision:
    ok: bool
    reason: str
    kid: str | None = None


def check_key_epoch(key_history_path: str, kid: str, at_iso: str) -> KeyDecision:
    data = json.loads(Path(key_history_path).read_text(encoding="utf-8"))
    at = _parse_dt(at_iso)

    for k in data.get("keys", []):
        if k.get("kid") != kid:
            continue

        status = k.get("status")
        nb = _parse_dt(k["not_before"])
        na = _parse_dt(k["not_after"]) if k.get("not_after") else None

        if status == "revoked":
            return KeyDecision(False, "kid_revoked", kid=kid)
        if at < nb:
            return KeyDecision(False, "before_not_before", kid=kid)
        if na and at > na:
            return KeyDecision(False, "after_not_after", kid=kid)

        return KeyDecision(True, "ok", kid=kid)

    return KeyDecision(False, "kid_not_found", kid=kid)
