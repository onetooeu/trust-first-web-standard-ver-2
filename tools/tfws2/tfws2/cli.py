import argparse
from .validate import validate_json
from .hashwalk import hashwalk
from .minisign_verify import verify_minisign_detached
from .sim.rollback import simulate_rollback
from .inventory_verify import verify_inventory
from .key_epoch import check_key_epoch


def main():
    ap = argparse.ArgumentParser(prog="tfws2")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate JSON against a schema")
    v.add_argument("--schema", required=True)
    v.add_argument("--json", required=True)

    h = sub.add_parser("hashwalk", help="Compute sha256 inventory for a folder")
    h.add_argument("--root", default=".")
    h.add_argument("--out", default="sha256.json")

    ms = sub.add_parser("verify-minisign", help="Verify minisign detached signature")
    ms.add_argument("--pubkey", required=True)
    ms.add_argument("--message", required=True)
    ms.add_argument("--sig", required=True)

    vi = sub.add_parser("verify-inventory", help="Verify an inventory and auto-pick the correct signature file")
    vi.add_argument("--pubkey", required=True)
    vi.add_argument("--inventory", required=True)
    vi.add_argument("--sigdir", default=None)

    ke = sub.add_parser("check-key-epoch", help="Check key epoch validity from key-history.json")
    ke.add_argument("--key-history", required=True)
    ke.add_argument("--kid", required=True)
    ke.add_argument("--at", required=True, help="ISO8601 time (e.g. 2025-12-25T00:00:00Z)")

    sim = sub.add_parser("simulate-rollback", help="Simulate rollback/replay using two inventories")
    sim.add_argument("--current", required=True)
    sim.add_argument("--candidate", required=True)
    sim.add_argument("--mode", default="hard-fail", choices=["hard-fail", "quarantine"])

    args = ap.parse_args()

    if args.cmd == "validate":
        validate_json(args.schema, args.json)
        print("OK")
        return

    if args.cmd == "hashwalk":
        hashwalk(args.root, args.out)
        print(f"Wrote {args.out}")
        return

    if args.cmd == "verify-minisign":
        ok, info = verify_minisign_detached(args.pubkey, args.message, args.sig)
        if not ok:
            raise SystemExit(f"FAIL: minisign verification failed ({info})")
        print("OK: minisign verification passed")
        return

    if args.cmd == "verify-inventory":
        ok, info, sig_used = verify_inventory(args.pubkey, args.inventory, sigdir=args.sigdir)
        if not ok:
            raise SystemExit(f"FAIL: inventory verification failed ({info}) sig={sig_used}")
        print(f"OK: inventory verification passed sig={sig_used}")
        return

    if args.cmd == "check-key-epoch":
        d = check_key_epoch(args.key_history, args.kid, args.at)
        if not d.ok:
            raise SystemExit(f"FAIL: {d.reason} kid={d.kid}")
        print(f"OK: {d.reason} kid={d.kid}")
        return

    if args.cmd == "simulate-rollback":
        decision = simulate_rollback(args.current, args.candidate, mode=args.mode)
        print(decision)
        return
