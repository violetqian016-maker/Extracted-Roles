# Extracted Roles

**A text analytics project that turns TV scripts into structured data for character-specific language modeling.**

[中文](README.zh-CN.md) · [Research notes](docs/RESEARCH.md) · [Data guide](docs/DATASET.md) · [Quality review](docs/PIPELINE_REVIEW.md)

I built this dataset for my undergraduate thesis at Fudan University. The starting question was simple: what data helps a language model sound like a particular character? A character biography provides background; dialogue provides evidence of word choice, recurring phrases, and responses to other people.

The project brings together **16 shows, 96 target roles, over 550,000 dialogue lines, and 174,000 prompt–response pairs**, with character vocabulary lists and supporting profiles.

## What I worked on

I developed the data construction and validation workflow, from heterogeneous text and CSV scripts to character-level datasets:

- **Prepared the data:** parsed different script formats, standardized speaker names, and removed stage directions, markup, and encoding artifacts.
- **Designed two useful outputs:** utterance collections for vocabulary analysis, and prompt–response pairs for role-playing fine-tuning. I balanced the training samples by character to reduce dominance by roles with more dialogue.
- **Assessed quality and usefulness:** audited completeness, speaker metadata, source references, and vocabulary coverage, then compared baseline and dynamic-vocabulary-enhanced generation.

The analytical work runs through the whole project: deciding which records to retain, how to balance coverage across characters, which quality measures to use, and what the evaluation results actually support.

## How the data fits together

```text
TV and animation scripts
    → parsing, cleaning, speaker normalization
        → character utterances → character vocabulary
        → prompt–response pairs → balanced training seeds

Wikipedia character information → supporting profiles
```

Separating the two dialogue outputs lets the same source material support both lexical analysis and response-generation experiments. Profiles add descriptive context; the original dialogue supplies the language evidence.

| Resource | Location | Current release |
| --- | --- | ---: |
| Character utterances | `Extracted-Roles/` | 96 files; 550,628 nonempty lines |
| Prompt–response pairs | `data/latest_single_pair_seed_v3/` | 174,000 pairs |
| Character vocabulary | `vocab_by_character_clean_v1/` | 186,109 entries |
| Supporting profiles | `profiles/` | 97 files; one known identity error |

The [data guide](docs/DATASET.md) explains the fields. [Research notes](docs/RESEARCH.md) distinguish the current files from the thesis statistics and describe the original methods.

## What the evaluation showed

In the thesis, **82.92% of target responses** matched at least one phrase from the corresponding character vocabulary. This measures lexical coverage, rather than overall response quality.

The downstream study compared generation with and without a character-specific dynamic vocabulary (DVA):

| Measure | Baseline | With DVA |
| --- | ---: | ---: |
| ROUGE-L | 6.097 | 8.734 |
| Pairwise wins, out of 479 valid comparisons | 155 (32.36%) | 309 (64.51%) |
| Diversity | 0.8787 | 0.7648 |

There were 15 ties. The results suggest better lexical alignment and a preference for DVA outputs in this setting, alongside lower diversity. Contextual relevance and role consistency did not improve consistently. These are preliminary results reported in the thesis; the original evaluation code and judgments are not included in this release.

## Try the dataset

Clone the repository and use Python 3.10+. No additional packages or API keys are needed for these examples.

```bash
git clone https://github.com/violetqian016-maker/Extracted-Roles.git
cd Extracted-Roles
python3 scripts/dataset.py validate
```

Read a character's dialogue pairs:

```python
import json
from pathlib import Path

path = Path("data/latest_single_pair_seed_v3/Big Bang Theory/SHELDON.json")
pairs = json.loads(path.read_text(encoding="utf-8"))

print(f"{len(pairs):,} pairs for Sheldon")
for turn in pairs[0]["dialogue"]:
    name = turn.get("speaker") or turn.get("interlocutor")
    print(f"{name}: {turn['text']}")
```

To inspect quality signals or verify the file inventory:

```bash
python3 scripts/audit_dataset.py
python3 scripts/dataset.py catalog --check
```

## Next steps

The next improvements focus on consistent character identifiers, reviewing repeated pairs and recovered examples, and preparing evaluation splits with source boundaries. The [quality review](docs/PIPELINE_REVIEW.md) documents the findings and priorities; [known issues](docs/KNOWN_ISSUES.md) tracks release discrepancies. Original data files have been preserved.

## About this work

**Ruiyi (Violet) Qian** · Fudan University · May 2026

Undergraduate thesis: *High-Quality English Role-Playing Datasets Facilitating Dynamic Role Vocabulary Construction*

Supervisor: **Ji Tao**

[Source references](docs/SOURCES.md) · [Contributing](CONTRIBUTING.md) · [Rights and licensing status](RIGHTS.md)

The corpus contains third-party script material and currently has no declared license. The repository documentation, inventory, and inspection tools were added after the thesis with Codex assistance.
