# Research context and contribution evidence

## Undergraduate project

Extracted Roles is part of Ruiyi (Violet) Qian's undergraduate research at Fudan University. Her project summary identifies the work as **LLM Role-Playing Dataset Construction & Evaluation**. This is the project description available for this release, not a verified formal thesis title.

The research contribution described in that summary covers dialogue cleaning and speaker-name normalization; adjacent-turn pair construction with deduplication, filtering, and role-level balancing; completeness, speaker-consistency, and source-traceability checks; and evaluation of baseline versus dynamic-vocabulary-enhanced generation.

## What can be verified from this release

| Claim | Available evidence |
| --- | --- |
| 550,628 nonempty dialogue lines | Original text files and generated catalog |
| 16 series and 96 character dialogue files | Directory structure and catalog; these are file counts, not a cross-layer identity audit |
| 174,000 prompt–response pairs | JSON arrays, globally unique pair IDs, and catalog |
| Character vocabulary and profiles | Released JSON files; profile facts require review |
| Pair provenance and selection metadata are retained | Fields such as `source_refs`, `quality_flags`, `source_type`, and optional balancing/recovery metadata |
| Cleaning, pair construction, and evaluation were part of the author's work | Author's project summary; original implementation and thesis are not bundled |
| 64.5% enhanced-setting win rate over 479 valid comparisons | Author's project summary; raw judgments and evaluation setup are not bundled |

The reported win rate describes that project's comparison setting. It should not be generalized to all characters, models, judges, or deployment scenarios. The available summary does not establish model versions, judge instructions, tie handling, sampling, uncertainty, or statistical significance, so no such claims are made here.

## Research significance

The dataset's practical contribution is its character-centered organization of dialogue and accompanying resources. Utterance collections support descriptive language analysis; paired turns provide inputs and target replies for generation experiments; vocabulary lists provide candidate lexical cues; profiles provide descriptive conditioning information. Together these resources support experiments on how different forms of character information affect generated responses.

Pair-level metadata allows downstream users to inspect selection and recovery labels rather than treating every retained pair as equally reliable. A deterministic inventory makes the released snapshot auditable. These properties support further research, while the missing original pipeline and evaluation materials limit full experimental reproduction.

## Original research and later repository maintenance

The README's research contribution refers to the undergraduate work. The bilingual documentation, deterministic catalog, Python structural validator, validator tests, and GitHub Actions were added during later repository maintenance with Codex assistance. They are not presented as original thesis methods or experimental findings.

## Materials needed for a complete research record

The formal thesis title and date, thesis or public abstract, original construction scripts, source attribution, experimental configuration, evaluation outputs, and collaborator/advisor credits should be added when available. These materials would allow the research narrative and reported results to be checked against the full thesis.
