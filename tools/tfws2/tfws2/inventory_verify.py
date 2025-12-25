from __future__ import annotations

from pathlib import Path
from .minisign_verify import verify_minisign_detached

def pick_signature_for_inventory(inventory_path: str, sigdir: str | None = None) -> Path:
    inv = Path(inventory_path)
    base = inv.name
    d = Path(sigdir) if sigdir else inv.parent

    cand1 = d / f"{base}.k1-provider.minisig"
    cand2 = d / f"{base}.minisig"

    if cand1.exists():
        return cand1
    if cand2.exists():
        return cand2
    raise FileNotFoundError(f"no_signature_found for {base} in {d}")

def verify_inventory(pubkey_path: str, inventory_path: str, sigdir: str | None = None):
    sig = pick_signature_for_inventory(inventory_path, sigdir=sigdir)
    ok, info = verify_minisign_detached(pubkey_path, inventory_path, str(sig))
    return ok, info, str(sig)
