"""Protect identity boundaries in the non-destructive duplicate review."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("audit_dataset", Path(__file__).resolve().parents[1] / "scripts/audit_dataset.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AuditTests(unittest.TestCase):
    def test_text_duplicates_keep_role_and_show_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for show, target, prompts in [("ShowA", "ALICE", ["Hello", "  HELLO  "]),
                                           ("ShowA", "BOB", ["Hello"]),
                                           ("ShowB", "ALICE", ["Hello"])]:
                path = root / "data/latest_single_pair_seed_v3" / show / f"{target}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                rows = [{"canonical_pair_id": f"{show}-{target}-{i}", "target_char": target,
                         "dialogue": [{"text": prompt}, {"text": "Good morning"}],
                         "prompt_word_count": 1, "response_word_count": 2,
                         "quality_flags": [], "source_type": "fixture"}
                        for i, prompt in enumerate(prompts)]
                path.write_text(json.dumps(rows), encoding="utf-8")
            before = {p: p.read_bytes() for p in root.rglob("*.json")}
            report = module.audit(root)
            self.assertEqual(report["duplicate_groups"], 1)
            self.assertEqual(report["duplicate_excess_records"], 1)
            self.assertEqual(report["pair_count"], 4)
            self.assertEqual({p: p.read_bytes() for p in root.rglob("*.json")}, before)

    def test_missing_corpus_is_not_a_clean_report(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "No pair files"):
                module.audit(Path(directory))


if __name__ == "__main__":
    unittest.main()
