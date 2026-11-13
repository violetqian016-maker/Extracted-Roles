# Extracted Roles — Undergraduate Research Dataset

A character-centered dialogue dataset developed by **Ruiyi (Violet) Qian** as part of her undergraduate research at **Fudan University**, supporting the study of character language and LLM role-playing.

The project turns television and animation dialogue into structured research resources: **550,628 dialogue lines** across **16 series and 96 character files**, **174,000 prompt–response pairs**, and accompanying character profiles and vocabulary lists.

[中文说明](README.zh-CN.md) · [Data reference](docs/DATASET.md) · [Known issues](docs/KNOWN_ISSUES.md) · [File inventory](docs/catalog.json)

## My research contribution

My undergraduate work centered on constructing the dataset and evaluating its use for character-conditioned generation:

- **Dialogue cleaning and standardization.** Cleaned more than 550,000 dialogue lines through text normalization, speaker-name mapping, and removal of non-dialogue content and encoding artifacts.
- **Prompt–response dataset construction.** Built 174,000 pairs from adjacent dialogue turns, using deduplication, quality filtering, and character-level balancing to prepare structured inputs and target-character responses.
- **Data quality checks.** Checked completeness, speaker consistency, and source traceability during dataset construction. The released pair records retain identifiers, speaker metadata, source references, and quality annotations for inspection.
- **Role-playing evaluation.** Compared baseline LLM outputs with a dynamic-vocabulary-enhanced setting using automated metrics and LLM-based pairwise comparisons. My project summary reports a **64.5% win rate across 479 valid comparisons** for the enhanced setting.

The construction methods and evaluation result above are documented in my project summary. The corpus counts can also be checked directly from this release. The full thesis, evaluation outputs, and original pipeline are not included here, so this repository does not yet independently reproduce the reported win rate. See [Research context](docs/RESEARCH.md) for the evidence boundary.

## Why this dataset matters

Character role-playing experiments need evidence of how a character speaks as well as descriptive information about who the character is. This dataset provides several complementary resources for studying that relationship:

| Resource | Research value |
| --- | --- |
| Character-specific dialogue | Supports analysis of recurring expressions, lexical preferences, and differences between characters |
| Prompt–response pairs | Provides interlocutor prompts and target-character replies for character-conditioned generation experiments |
| Character vocabulary | Provides candidate words and phrases for studying vocabulary-based conditioning, including the dynamic-vocabulary approach explored in the undergraduate project |
| Character profiles | Provides descriptive context that can be compared with dialogue-derived language evidence, subject to factual review |
| Pair-level source and quality metadata | Allows researchers to inspect retained examples and apply their own filtering decisions |

Coverage across 16 series makes it possible to compare characters within a series and explore differences across series. The current release supplies the data for such experiments; it does not establish cross-series generalization or a validated benchmark. Cross-layer identity alignment and leakage-aware evaluation splits still require explicit preparation.

## Dataset at a glance

| Resource | Files | Records |
| --- | ---: | ---: |
| Character dialogue text | 96 | One nonempty line per utterance |
| Prompt–response pairs | 96 | 174,000 pairs |
| Character profiles | 97 | 97 profile objects |
| Character vocabulary | 96 | 186,109 entries |

These are file and record counts, not a verified count of distinct identities across every layer. In particular, the extra profile has a known identity mismatch. Vocabulary counts include entries as stored, without global deduplication.

This release contains the **research dataset and inspection tools**. The original extraction pipeline, model training code, deployed applications, and raw evaluation outputs are not included.

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
