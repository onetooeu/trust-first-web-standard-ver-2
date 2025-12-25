import json
from jsonschema import Draft202012Validator

def validate_json(schema_path: str, json_path: str) -> None:
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(data), key=lambda e: e.path)
    if errors:
        msg = "\n".join([f"- {list(e.path)}: {e.message}" for e in errors[:50]])
        raise SystemExit(f"Validation failed:\n{msg}")
