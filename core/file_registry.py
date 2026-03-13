import os
import json
import hashlib


def calc_file_hash(file_path: str) -> str:
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def load_registry(registry_path="metadata.json"):
    if not os.path.exists(registry_path):
        return {"files": {}}
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(registry, registry_path="metadata.json"):
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def is_file_duplicate(file_path: str, registry_path="metadata.json") -> bool:
    registry = load_registry(registry_path)
    file_hash = calc_file_hash(file_path)
    return file_hash in registry["files"]


def register_file(file_path: str, registry_path="metadata.json"):
    registry = load_registry(registry_path)
    file_hash = calc_file_hash(file_path)
    registry["files"][file_hash] = {
        "filename": os.path.basename(file_path),
        "path": file_path
    }
    save_registry(registry, registry_path)