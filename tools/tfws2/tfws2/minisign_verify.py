import subprocess
from pathlib import Path

def verify_minisign_detached(pubkey_path: str, message_path: str, sig_path: str):
    """
    Verifies a detached minisign signature using the minisign CLI.
    Returns (ok: bool, info: str).
    """
    pubkey = Path(pubkey_path)
    msg = Path(message_path)
    sig = Path(sig_path)

    if not pubkey.exists():
        return False, "pubkey_not_found"
    if not msg.exists():
        return False, "message_not_found"
    if not sig.exists():
        return False, "sig_not_found"

    cmd = ["minisign", "-V", "-p", str(pubkey), "-m", str(msg), "-x", str(sig)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        return False, "minisign_not_in_path"

    if r.returncode == 0:
        return True, "ok"
    detail = (r.stderr or r.stdout or "").strip()
    return False, detail[:400] if detail else "verify_failed"
