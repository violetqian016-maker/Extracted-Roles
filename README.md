# Extracted Roles

**A structured English dialogue dataset for character-level text analysis and dynamic-vocabulary-enhanced language generation.**

[中文](README.zh-CN.md) · [Research notes](docs/RESEARCH.md) · [Data guide](docs/DATASET.md) · [Quality review](docs/PIPELINE_REVIEW.md)

Extracted Roles organizes television and animation scripts into character-attributed dialogue, prompt–response pairs, vocabulary lists, and supporting profiles. The dataset supports analysis of lexical patterns and the evaluation of character-specific response generation.

The project brings together **16 shows, 96 target roles, over 550,000 dialogue lines, and 174,000 prompt–response pairs**, with character vocabulary lists and supporting profiles.

## Methodology and contributions

The construction framework converts heterogeneous TXT and CSV scripts into complementary resources for lexical analysis and dialogue modeling.

- **Text preparation and speaker normalization:** standardizes script formats and speaker aliases, and removes stage directions, markup, and encoding artifacts.
- **Dual-output dataset construction:** separates character utterances for vocabulary extraction from prompt–response seeds for supervised fine-tuning. Role-level balancing reduces the concentration of training samples among high-resource characters.
- **Quality assessment and comparative evaluation:** examines structural completeness, speaker metadata, source traceability, and lexical coverage, followed by a comparison of baseline and dynamic-vocabulary-enhanced generation.

This workflow connects unstructured data preparation with sampling design, quality measurement, and evaluation. It provides a basis for studying how data selection and lexical conditioning affect generated language.

## Data structure

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
| Supporting profiles | `profiles/` | 97 files |

Field definitions and metadata are documented in the [data guide](docs/DATASET.md). Construction methods and statistical definitions are described in the [research notes](docs/RESEARCH.md).

## Evaluation results

The reported phrase-level audit found that **82.92% of target responses** matched at least one phrase from the corresponding character vocabulary. This measures coverage of vocabulary-derived lexical cues.

The downstream study compared generation with and without a character-specific dynamic vocabulary (DVA):

| Measure | Baseline | With DVA |
| --- | ---: | ---: |
| ROUGE-L | 6.097 | 8.734 |
| Pairwise wins, out of 479 valid comparisons | 155 (32.36%) | 309 (64.51%) |
| Diversity | 0.8787 | 0.7648 |

The comparison included 15 ties. In the evaluated setting, DVA achieved higher reference overlap and more pairwise wins, with lower diversity. Improvements in contextual relevance and role consistency varied across evaluation dimensions. Detailed methods and result interpretation are provided in the [research notes](docs/RESEARCH.md).

## Usage

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

## Documentation

- [Data reference](docs/DATASET.md): schema and field definitions.
- [Research notes](docs/RESEARCH.md): construction methods, statistical definitions, and evaluation.
- [Quality review](docs/PIPELINE_REVIEW.md): release audit and pipeline improvement priorities.
- [Source references](docs/SOURCES.md): source corpus information.
- [Contributing](CONTRIBUTING.md) and [rights information](RIGHTS.md).
