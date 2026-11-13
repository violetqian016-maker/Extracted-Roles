#!/usr/bin/env python3
"""Validate the corpus and build a reproducible inventory (Python 3.10+)."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LAYERS = {
    "dialogues": ("Extracted-Roles", "*.txt"),
    "pairs": ("data/latest_single_pair_seed_v3", "*.json"),
    "profiles": ("profiles", "*.json"),
    "vocabulary": ("vocab_by_character_clean_v1", "*.json"),
}
PROFILE_FIELDS = (
    "character_name", "series_name", "identity", "background", "relationships",
    "personality", "world_setting", "style_guide",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect_file(path, layer, seen_ids):
    """Return record count after structural checks; never rewrite source files."""
    text = path.read_text(encoding="utf-8")
    require(bool(text.strip()), "empty file")
    if layer == "dialogues":
        return sum(bool(line.strip()) for line in text.splitlines())
    data = json.loads(text)
    if layer == "profiles":
        require(isinstance(data, dict), "profile must be an object")
        for field in PROFILE_FIELDS:
            require(field in data, f"missing profile field: {field}")
            expected = dict if field == "relationships" else str
            require(isinstance(data[field], expected), f"invalid profile field: {field}")
        return 1
    require(isinstance(data, list) and bool(data), "expected a nonempty array")
    if layer == "vocabulary":
        require(all(isinstance(item, str) and item.strip() for item in data),
                "vocabulary entries must be nonempty strings")
        return len(data)
    for index, row in enumerate(data):
        label = f"row {index}"
        require(isinstance(row, dict), f"{label}: expected an object")
        pair_id = row.get("canonical_pair_id")
        require(isinstance(pair_id, str) and bool(pair_id), f"{label}: missing pair ID")
        require(pair_id not in seen_ids, f"{label}: duplicate pair ID: {pair_id}")
        seen_ids.add(pair_id)
        require(row.get("target_char") == path.stem, f"{label}: target differs from filename")
        dialogue = row.get("dialogue")
        require(isinstance(dialogue, list) and len(dialogue) == 2,
                f"{label}: dialogue must contain two turns")
        for turn in dialogue:
            require(isinstance(turn, dict) and isinstance(turn.get("text"), str)
                    and bool(turn["text"].strip()), f"{label}: invalid turn text")
        for field in ("prompt_word_count", "response_word_count", "total_word_count"):
            require(type(row.get(field)) is int and row[field] >= 0,
                    f"{label}: invalid {field}")
        require(row["total_word_count"] == row["prompt_word_count"] + row["response_word_count"],
                f"{label}: inconsistent word counts")
        require(isinstance(row.get("quality_flags"), list), f"{label}: invalid quality flags")
        require(isinstance(row.get("source_refs"), list) and bool(row["source_refs"]),
                f"{label}: missing source references")
    return len(data)


def inventory(root):
    files, errors, seen_ids = [], [], set()
    for layer, (directory, pattern) in LAYERS.items():
        paths = sorted((root / directory).rglob(pattern))
        if not paths:
            errors.append(f"{directory}: no matching files")
        for path in paths:
            try:
                records = inspect_file(path, layer, seen_ids)
                files.append({
                    "path": path.relative_to(root).as_posix(), "layer": layer,
                    "records": records, "bytes": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                })
            except (ValueError, OSError, TypeError, KeyError) as exc:
                errors.append(f"{path.relative_to(root)}: {exc}")
    counts, records = Counter(), Counter()
    for entry in files:
        counts[entry["layer"]] += 1
        records[entry["layer"]] += entry["records"]
    return {"schema_version": 1, "file_counts": dict(counts),
            "record_counts": dict(records), "files": files}, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "catalog"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/catalog.json")
    parser.add_argument("--check", action="store_true", help="check the catalog without writing it")
    args = parser.parse_args()
    result, errors = inventory(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps({key: result[key] for key in ("file_counts", "record_counts")}, indent=2))
    print("NOTE: structural validation does not verify dialogue attribution or profile facts.")
    print("Known profile anomaly: profiles/Bones_Jack.json; see docs/KNOWN_ISSUES.md.")
    if args.command == "catalog":
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.check:
            if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
                print("ERROR: catalog is stale; run python3 scripts/dataset.py catalog", file=sys.stderr)
                return 1
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
