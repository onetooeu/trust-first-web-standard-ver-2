import argparse
from .validate import validate_json
from .hashwalk import hashwalk

def main():
    ap = argparse.ArgumentParser(prog="tfws2")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate JSON against a schema")
    v.add_argument("--schema", required=True)
    v.add_argument("--json", required=True)

    h = sub.add_parser("hashwalk", help="Compute sha256 inventory for a folder")
    h.add_argument("--root", default=".")
    h.add_argument("--out", default="sha256.json")

    args = ap.parse_args()

    if args.cmd == "validate":
        validate_json(args.schema, args.json)
        print("OK")
    elif args.cmd == "hashwalk":
        hashwalk(args.root, args.out)
        print(f"Wrote {args.out}")
