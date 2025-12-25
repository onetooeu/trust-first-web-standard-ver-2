import hashlib, json, os

def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def hashwalk(root: str, out_json: str) -> None:
    items = []
    for dirpath, _, filenames in os.walk(root):
        if "/.git" in dirpath.replace("\\", "/"):
            continue
        for name in filenames:
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, root).replace("\\", "/")
            if rel.startswith(".git/"):
                continue
            items.append((rel, _sha256_file(p)))

    items.sort(key=lambda x: x[0])
    doc = {
        "schema_version": "2.0",
        "root": ".",
        "algo": "sha256",
        "count": len(items),
        "files": [{"path": p, "sha256": s} for p, s in items]
    }
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
