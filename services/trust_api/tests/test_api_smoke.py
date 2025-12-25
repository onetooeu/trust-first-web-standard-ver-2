import json
from pathlib import Path
from jsonschema import Draft202012Validator

from trust_api.app import build_trust_state_for_domain

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads((ROOT / "schemas" / "trust-state.schema.json").read_text(encoding="utf-8"))

def test_generated_trust_state_is_schema_valid():
    payload = build_trust_state_for_domain("example.com")
    v = Draft202012Validator(SCHEMA)
    errors = list(v.iter_errors(payload))
    assert not errors, errors
