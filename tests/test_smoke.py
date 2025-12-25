import json
from pathlib import Path

from jsonschema import Draft202012Validator


BASE = Path(__file__).resolve().parent.parent

CASES = [
    ("schemas/trust-state.schema.json", "examples/schemas/trust-state.example.json"),
    ("schemas/incident.schema.json", "examples/schemas/incident.example.json"),
    ("schemas/key-history.schema.json", "examples/schemas/key-history.example.json"),
]


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def test_examples_validate_against_schemas():
    for schema_rel, example_rel in CASES:
        schema_path = BASE / schema_rel
        example_path = BASE / example_rel

        schema = load_json(schema_path)
        example = load_json(example_path)

        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(example), key=lambda e: list(e.path))

        assert not errors, f"{example_rel} failed validation: {errors}"
