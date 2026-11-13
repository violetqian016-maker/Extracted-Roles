# Extracted Roles

Character-centered dialogue resources from **16 television and animation series**, organized into dialogue lines, prompt–response pairs, character profiles, and vocabulary lists.

[中文说明](README.zh-CN.md) · [Data reference](docs/DATASET.md) · [Known issues](docs/KNOWN_ISSUES.md) · [File inventory](docs/catalog.json)

## Dataset at a glance

| Resource | Files | Records |
| --- | ---: | ---: |
| Character dialogue text | 96 | One nonempty line per utterance |
| Prompt–response pairs | 96 | 174,000 pairs |
| Character profiles | 97 | 97 profile objects |
| Character vocabulary | 96 | 186,109 entries |

These are file and record counts, not a verified count of distinct identities across every layer. In particular, the extra profile has a known identity mismatch. Vocabulary counts include entries as stored, without global deduplication.

This repository is a **dataset with inspection tools**. It does not currently include the original extraction pipeline, model training code, a deployed chatbot, or evaluation results.

## Quick start

Requirements: Git and Python 3.10 or later. The tools use only the Python standard library; no package installation or API key is required.

```bash
git clone https://github.com/violetqian016-maker/Extracted-Roles.git
cd Extracted-Roles
python3 scripts/dataset.py validate
python3 scripts/dataset.py catalog --check
python3 -m unittest discover -s tests -v
```

Read a character's pairs from the repository root:

```python
import json
from pathlib import Path

path = Path("data/latest_single_pair_seed_v3/Avatar/AANG.json")
pairs = json.loads(path.read_text(encoding="utf-8"))
print("Pairs:", len(pairs))
print("Target:", pairs[0]["target_char"])
print("Turn keys:", [list(turn) for turn in pairs[0]["dialogue"]])
```

## Repository layout

```text
Extracted-Roles/                 Original character dialogue text
data/latest_single_pair_seed_v3/ Prompt–response JSON arrays by series/character
profiles/                       Character profile JSON objects
vocab_by_character_clean_v1/     Character vocabulary JSON arrays
scripts/dataset.py              Validation and deterministic file inventory
tests/                          Validator regression tests
docs/                           Schema, limitations, and generated inventory
.github/                        CI and contribution templates
```

Original paths and contents are retained so existing downstream references continue to work. Names differ between layers (for example, `HIMYM` versus `How I Met Your Mother`); there is currently no authoritative cross-layer identity map.

## Covered series

Avatar, Big Bang Theory, Bones, Friends, Futurama, Game of Thrones, House, How I Met Your Mother, My Little Pony, Parks and Recreation, Seinfeld, Sex and the City, The Simpsons, South Park, SpongeBob SquarePants, and The Office.

## Data quality and provenance

All stored JSON files are structurally validated. Pair identifiers are checked for uniqueness across the pair layer. The generated [catalog](docs/catalog.json) records each file's relative path, record count, byte size, and SHA-256 digest; CI checks that it stays synchronized with the data.

Structural validation does not establish factual accuracy, correct speaker attribution, conversation adjacency, or permission to reuse the source material. Some retained pairs have short-turn flags or recovery metadata. Upstream script paths appear in source references but those scripts and extraction procedures are not included. Read the [data reference](docs/DATASET.md) and [known issues](docs/KNOWN_ISSUES.md) before interpreting results.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For data corrections, provide a file path, pair ID or field, and supporting evidence. Regenerate the catalog after changing data:

```bash
python3 scripts/dataset.py catalog
python3 scripts/dataset.py catalog --check
```

## Licensing and attribution

This repository currently has no declared license. No blanket license is applied to the included television dialogue or other third-party content. Source URLs, extraction dates, and rights information remain to be documented by the maintainer. See [RIGHTS.md](RIGHTS.md) for the current status.
