"""Regression checks for malformed data and cross-file duplicate detection."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("dataset", Path(__file__).resolve().parents[1] / "scripts/dataset.py")
dataset = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dataset)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "AANG.json"
        self.row = {"canonical_pair_id": "test::1", "target_char": "AANG",
                    "dialogue": [{"text": "Hello"}, {"text": "Hello again"}],
                    "prompt_word_count": 1, "response_word_count": 2,
                    "total_word_count": 3, "quality_flags": [],
                    "source_refs": [{"prompt_source_path": "unbundled.txt"}]}

    def inspect(self, seen=None):
        self.path.write_text(json.dumps([self.row]), encoding="utf-8")
        return dataset.inspect_file(self.path, "pairs", set() if seen is None else seen)

    def test_valid_pair(self):
        self.assertEqual(self.inspect(), 1)

    def test_cross_file_duplicate(self):
        with self.assertRaisesRegex(ValueError, "duplicate pair ID"):
            self.inspect({"test::1"})

    def test_bad_turn_and_word_counts(self):
        self.row["dialogue"][0]["text"] = " "
        with self.assertRaisesRegex(ValueError, "invalid turn text"):
            self.inspect()
        self.row["dialogue"][0]["text"] = "Hello"
        self.row["total_word_count"] = 9
        with self.assertRaisesRegex(ValueError, "inconsistent word counts"):
            self.inspect()

    def test_target_mismatch(self):
        self.row["target_char"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "target differs"):
            self.inspect()


if __name__ == "__main__":
    unittest.main()
