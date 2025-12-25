import json
from pathlib import Path

def _load_sha256_json(path: str) -> dict:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def _index_files(doc: dict) -> dict:
    files = doc.get("files", [])
    out = {}
    for it in files:
        if isinstance(it, dict) and "path" in it and "sha256" in it:
            out[it["path"]] = it["sha256"]
    return out

def simulate_rollback(current_path: str, candidate_path: str, mode: str = "hard-fail") -> str:
    """
    Detect rollback/replay indicators between two inventories.
    Returns a machine-friendly decision string.
    """
    cur = _load_sha256_json(current_path)
    cand = _load_sha256_json(candidate_path)

    cur_idx = _index_files(cur)
    cand_idx = _index_files(cand)

    cur_n = len(cur_idx)
    cand_n = len(cand_idx)

    missing = [p for p in cur_idx.keys() if p not in cand_idx]
    changed = [p for p in cur_idx.keys() if p in cand_idx and cand_idx[p] != cur_idx[p]]

    score = 0
    if cand_n < cur_n:
        score += 2
    if len(missing) > 0:
        score += 2
    if len(changed) > max(3, cur_n // 20):
        score += 1

    if score >= 3:
        return f"ROLLBACK_SUSPECT mode={mode} cur={cur_n} cand={cand_n} missing={len(missing)} changed={len(changed)}"
    if score >= 1:
        return f"ROLLBACK_POSSIBLE mode={mode} cur={cur_n} cand={cand_n} missing={len(missing)} changed={len(changed)}"
    return f"OK mode={mode} cur={cur_n} cand={cand_n} missing={len(missing)} changed={len(changed)}"
