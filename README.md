# Extracted Roles — Undergraduate Research Dataset

A character-centered dialogue dataset developed by **Ruiyi (Violet) Qian** as part of her undergraduate research at **Fudan University**, for dynamic-vocabulary-enhanced English role-playing.

**Thesis:** *High-Quality English Role-Playing Datasets Facilitating Dynamic Role Vocabulary Construction* (May 2026), supervised by **Ji Tao**.

The project turns television and animation dialogue into structured research resources: **550,628 dialogue lines** across **16 series and 96 character files**, **174,000 prompt–response pairs**, and accompanying character profiles and vocabulary lists.

[中文说明](README.zh-CN.md) · [Data reference](docs/DATASET.md) · [Known issues](docs/KNOWN_ISSUES.md) · [File inventory](docs/catalog.json)

## My research contribution

My thesis develops a data construction and validation framework for the Dynamic Vocabulary Approach (DVA), with three main contributions:

1. **A dual-output construction framework.** I separate character utterances for dynamic vocabulary extraction from prompt–response seeds for supervised fine-tuning. The pipeline covers heterogeneous script parsing, cleaning, speaker normalization, utterance extraction, adjacent-turn pairing, and auxiliary profile construction. In the thesis parsing audit, robust parsing recovered 415,968 dialogue lines versus 314,643 with a strict parser from the same 587,222 raw lines (§4.2.2).
2. **A balancing strategy tailored to each data objective.** I preserve character-specific lexical evidence in the utterance corpus and apply quality-aware role-level softcap balancing to the seed corpus. The thesis reports **1,025–2,000 seeds per role**, reducing dominance by high-resource characters while retaining usable lower-resource roles (§4.2.6; Table 5).
3. **Rule-based validation and lexical auditing.** I audit sample completeness, speaker consistency, source references, duplicate IDs, and formatting residues. The thesis reports zero failures on its six final structural checks (Table 7). A phrase-matching audit found that **82.92% of target responses** matched at least one phrase in the corresponding character vocabulary, averaging **2.38 matches per response** (Table 6).

The contribution is the **DVA-oriented data framework and its validation**, rather than a new dynamic vocabulary algorithm. Profiles are auxiliary metadata; script-derived utterances supply the primary lexical evidence.

## Why this dataset matters

The thesis addresses a practical requirement for recognizable character voice: models need reliable evidence of a character's recurring words and phrases, as well as examples of how that character replies in conversation. The two core outputs serve those different needs:

| Resource | Intended research use |
| --- | --- |
| Character utterances | Extract recurrent expressions and lexical patterns for dynamic role vocabulary construction |
| Prompt–response seeds | Provide local conversational inputs and target-character responses for supervised fine-tuning |
| Character vocabulary lists | Supply lexical cues for character-conditioned generation and phrase-level analysis |
| Structured profiles | Supply auxiliary identity and background information for role conditioning |
| Source and quality metadata | Support sample inspection, filtering, and analysis of balancing/recovery decisions |

This design connects lexical analysis and conversational supervision using the same target-role pool. Role-level balancing reduces extreme training-data polarization, while retained metadata makes selection decisions inspectable. Coverage spans **16 shows and 96 target roles** in the thesis. The released profiles still require identity review; see [Known issues](docs/KNOWN_ISSUES.md).

## Results reported in the thesis

The downstream experiment compares a baseline with a DVA-enhanced generation setting using the same base model and configuration, with character-specific dynamic vocabulary added in the enhanced setting (§5.6).

| Measure | Baseline | DVA-enhanced |
| --- | ---: | ---: |
| ROUGE-L | 6.097 | 8.734 |
| Pairwise wins, out of 479 valid comparisons | 155 (32.36%) | **309 (64.51%)** |
| Diversity | 0.8787 | 0.7648 |

There were **15 ties (3.13%)**, and 479 of 480 attempted comparisons received complete scores. These results provide preliminary evidence of improved lexical alignment and pairwise preference in the tested setting. The thesis also reports increased repeated phrase patterns, lower diversity, and inconsistent gains in contextual relevance and role consistency. The experiment does not establish that seed fine-tuning alone caused the improvement.

The figures above are transcribed from thesis Tables 9–10, not reproduced by this repository's checks. See [Research context](docs/RESEARCH.md) for methods, interpretation, and the distinction between thesis statistics and the current release.

## Dataset at a glance

| Resource | Files | Records |
| --- | ---: | ---: |
| Character dialogue text | 96 | 550,628 nonempty lines |
| Prompt–response pairs | 96 | 174,000 pairs |
| Character profiles | 97 | 97 profile objects |
| Character vocabulary | 96 | 186,109 entries |

The thesis reports **550,601 cleaned utterances** (Table 4); the current release contains **550,628 nonempty text lines**, a difference of 27 that has not yet been reconciled. The current minimum seed count per role is 1,083, versus 1,025 in thesis Table 5; total pairs, maximum, and median agree.

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

Structural validation does not establish factual accuracy, correct speaker attribution, conversation adjacency, or permission to reuse the source material. Some retained pairs have short-turn flags or recovery metadata. Upstream script paths appear in source references but those scripts and the original executable pipeline are not included. The methodology is summarized in [Research context](docs/RESEARCH.md), and Appendix A source links are recorded in [Sources](docs/SOURCES.md). Read the [data reference](docs/DATASET.md) and [known issues](docs/KNOWN_ISSUES.md) before interpreting results.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For data corrections, provide a file path, pair ID or field, and supporting evidence. Regenerate the catalog after changing data:

```bash
python3 scripts/dataset.py catalog
python3 scripts/dataset.py catalog --check
```

## Licensing and attribution

This repository currently has no declared license. No blanket license is applied to the included television dialogue or other third-party content. Source URLs from the thesis are recorded in [Sources](docs/SOURCES.md); acquisition dates, source versions, and rights information remain to be documented. See [RIGHTS.md](RIGHTS.md) for the current status.

## Thesis reference

Qian, Ruiyi. (2026). *High-Quality English Role-Playing Datasets Facilitating Dynamic Role Vocabulary Construction*. Undergraduate thesis, College of Foreign Languages and Literature, Fudan University. Supervisor: Ji Tao. Completed May 25, 2026.
