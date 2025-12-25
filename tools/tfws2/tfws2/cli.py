import argparse
from .validate import validate_json
from .hashwalk import hashwalk
from .minisign_verify import verify_minisign_detached
from .sim.rollback import simulate_rollback

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
    ms.add_argument("--pubkey", required=True, help="Path to minisign pubkey file")
    ms.add_argument("--message", required=True, help="Path to message file (e.g., sha256.json)")
    ms.add_argument("--sig", required=True, help="Path to .minisig file")

    sim = sub.add_parser("simulate-rollback", help="Simulate rollback/replay using two inventories")
    sim.add_argument("--current", required=True, help="Path to current sha256.json")
    sim.add_argument("--candidate", required=True, help="Path to candidate/older sha256.json")
    sim.add_argument("--mode", default="hard-fail", choices=["hard-fail", "quarantine"], help="Decision mode")

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

    if args.cmd == "simulate-rollback":
        decision = simulate_rollback(args.current, args.candidate, mode=args.mode)
        print(decision)
        return
