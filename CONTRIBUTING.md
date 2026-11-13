# Contributing

Use Python 3.10+ and work on a branch. No third-party dependencies are needed for repository checks.

For data corrections, include the exact file path, `canonical_pair_id` (for pairs) or field name, the proposed correction, and supporting source evidence. Preserve source metadata. Avoid bulk renaming or identity merges without a documented mapping.

Do not commit credentials, local environments, or unreviewed generated artifacts. Keep source data changes separate from tooling changes where practical.

Before submitting:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/dataset.py catalog
python3 scripts/dataset.py catalog --check
git diff --check
```

The catalog update should accompany data changes. Explain any changed counts and update the dataset documentation. Passing checks verifies structure and inventory consistency; provide evidence separately for factual corrections.
