#!/usr/bin/env python3
"""Profile the released pairs without changing data or judging semantic quality."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]


def normalize(text):
    """Ignore case and whitespace only; retain punctuation and wording."""
    return " ".join(text.casefold().split())


def audit(root):
    groups = defaultdict(list)
    flags, sources, counts = Counter(), Counter(), Counter()
    flag_sources = defaultdict(Counter)
    roles, examples = [], defaultdict(list)
    total = 0
    for path in sorted((root / "data/latest_single_pair_seed_v3").rglob("*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        roles.append({"path": path.relative_to(root).as_posix(), "pairs": len(rows)})
        for row in rows:
            total += 1
            prompt, response = (normalize(turn["text"]) for turn in row["dialogue"])
            # Target identity is part of the key: shared dialogue across roles
            # is not automatically a duplicate supervision target.
            key = (path.parent.name, row["target_char"], prompt, response)
            groups[key].append({"path": path.relative_to(root).as_posix(),
                                "pair_id": row["canonical_pair_id"]})
            sources[row["source_type"]] += 1
            flags.update(row["quality_flags"])
            for flag in row["quality_flags"]:
                flag_sources[flag][row["source_type"]] += 1
            checks = {
                "identical_prompt_response": prompt == response,
                "prompt_under_3_stored_words": row["prompt_word_count"] < 3,
                "response_under_3_stored_words": row["response_word_count"] < 3,
                "response_over_50_stored_words": row["response_word_count"] > 50,
            }
            for label, matched in checks.items():
                if matched:
                    counts[label] += 1
                    if len(examples[label]) < 5:
                        examples[label].append({"path": path.relative_to(root).as_posix(),
                                                "pair_id": row["canonical_pair_id"]})
    if not roles:
        raise ValueError("No pair files found")
    duplicates = [members for members in groups.values() if len(members) > 1]
    return {
        "schema_version": 1,
        "scope": "Released pairs; casefold and whitespace normalization; no data edits",
        "pair_count": total,
        "role_files": len(roles),
        "pairs_per_role": {"min": min(r["pairs"] for r in roles),
                           "max": max(r["pairs"] for r in roles),
                           "median": statistics.median(r["pairs"] for r in roles)},
        "duplicate_key": ["series_folder", "target_char", "normalized_prompt", "normalized_response"],
        "duplicate_groups": len(duplicates),
        "duplicate_excess_records": sum(len(members) - 1 for members in duplicates),
        "duplicate_members": duplicates,
        "review_counts": dict(sorted(counts.items())),
        "review_examples": dict(examples),
        "quality_flag_counts": dict(sorted(flags.items())),
        "quality_flags_by_source_type": {flag: dict(sorted(source_counts.items()))
                                         for flag, source_counts in sorted(flag_sources.items())},
        "source_type_counts": dict(sorted(sources.items())),
        "role_counts": roles,
        "interpretation": "Review signals are not errors. Repeated lines may be legitimate; "
                          "short or recovered samples must be assessed in context. "
                          "Unique IDs do not imply unique text. No episode/split leakage audit is performed.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="write the full JSON report to this path")
    args = parser.parse_args()
    report = audit(args.root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {key: value for key, value in report.items()
               if key not in ("duplicate_members", "role_counts", "review_examples", "quality_flags_by_source_type")}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
