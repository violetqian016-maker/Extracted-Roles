# Research context and contribution evidence

## Thesis

**Title:** *High-Quality English Role-Playing Datasets Facilitating Dynamic Role Vocabulary Construction*

**Chinese title:** 促进动态角色词表构建的高质量英文角色扮演数据集

**Author:** Ruiyi Qian (钱睿怡)

**Institution:** College of Foreign Languages and Literature, Fudan University

**Supervisor:** Ji Tao (纪焘)

**Completion date:** May 25, 2026

This summary is grounded in the author's supplied undergraduate thesis. Section and table references below refer to that thesis. The full Word document is not bundled with this release.

## Research questions and significance

The thesis asks how to construct reliable character utterance data for dynamic vocabulary extraction, and how to construct and balance role-playing training seeds without extreme character-level data polarization.

Its contribution is a data infrastructure for lexical-stylistic modeling. Character utterances supply observable vocabulary and phrase-level evidence; prompt–response seeds supply examples of how a character responds to an interlocutor. These two outputs serve different purposes and therefore receive different selection and balancing treatment. Profiles provide auxiliary role information rather than replacing script-derived linguistic evidence.

The thesis positions this framework as support for the Dynamic Vocabulary Approach (DVA). It does not claim a new DVA algorithm. Its downstream experiment provides preliminary evidence for vocabulary-conditioned generation, rather than a comprehensive benchmark or proof of generalization.

## Construction methodology

### Script collection and preprocessing

The corpus covers 16 television and animation sources and 96 target roles. Scripts were collected mainly from Kaggle, using text and CSV inputs. Appendix A's source list is reproduced in [SOURCES.md](SOURCES.md).

In §4.2.2, a parsing audit compares strict and robust parsing over 587,222 raw lines. Strict parsing extracts 314,643 dialogue lines; robust parsing extracts 415,968 by accepting variants such as quoted speaker labels, bracketed speakers, and parenthetical speaker descriptions. These are parsing-audit counts, not the size of the complete final corpus.

Cleaning includes HTML unescaping, BOM and zero-width character removal, stage-direction removal, whitespace normalization, and residual encoding/markup cleanup. Speaker normalization and explicit alias mappings merge surface variants and remove non-dialogue labels. Appendix B supplies representative rules and examples.

### Dual-output framework

Sections 4.2.3–4.2.4 distinguish two primary outputs:

- **Character utterance files:** speaker-attributed dialogue for lexical and phrase-level analysis and subsequent dynamic vocabulary extraction.
- **Single-turn seeds:** a valid interlocutor prompt followed by a target-character response, prepared as supervision for role-playing fine-tuning. Recovery metadata may retain additional context outside the main two-turn dialogue field in the current release.

The seed construction process applies quality filters, deduplication, response-side cleanup, metadata collection, balancing, and final validation. The thesis includes pseudocode (Table 2), but the original executable pipeline is not in the repository.

### Auxiliary profiles

Section 4.2.5 describes Wikipedia-based profile construction using Qwen2.5-72B-Instruct. The retained introductory source passage is limited to 8,000 characters; temperature is set to 0.1. A fixed JSON schema covers identity, background, world setting, personality, style, and relationships. Relationship extraction is constrained to explicit links with other roles in the selected pool.

This documents the intended construction method, not a guarantee that every released profile is correct. The namesake error in `profiles/Bones_Jack.json` remains a known release issue.

### Role-level balancing

Section 4.2.6 separates lexical-evidence preservation in the utterance corpus from quality-aware softcap balancing in the seed corpus. Table 5 reports 174,000 pairs, with 1,025–2,000 seeds per role and a median of 1,900. The upper softcap is 2,000; roles are not forced to identical sample counts.

## Dataset audits reported in the thesis

| Measure | Thesis result | Location |
| --- | ---: | --- |
| Cleaned utterances | 550,601 | Table 4 |
| Shows / target roles | 16 / 96 | Tables 4–5 |
| Prompt–response pairs | 174,000 | Table 5 |
| Responses with at least one character-vocabulary phrase hit | 82.92% | Table 6 |
| Average phrase hits per response | 2.38 | Table 6 |
| Total phrase hits | 413,435 | Table 6 |
| Missing prompts / missing responses | 0 / 0 | Table 7 |
| Response speaker mismatches / missing source references | 0 / 0 | Table 7 |
| Duplicate canonical IDs / strict response-start speaker-label residues | 0 / 0 | Table 7 |

The phrase audit normalizes case, punctuation, and whitespace, and uses longest matching to avoid counting overlapping shorter phrases repeatedly. It measures overlap with the corresponding character vocabulary; it does not establish that a phrase is unique to that character or that the response is contextually correct. Zero-hit responses are not automatically invalid.

Table 7 reports the thesis's rule-based audit results. The later repository validator checks a subset of structural invariants; it does not independently reproduce all original audits or manually verify speaker attribution.

## Downstream experiment

Section 5.6 compares baseline and DVA-enhanced generation with the same base model and configuration; the enhanced setting adds a character-specific dynamic vocabulary list. The thesis does not provide sufficient executable configuration and raw outputs in this repository for independent reproduction.

| Metric | Baseline | DVA-enhanced |
| --- | ---: | ---: |
| ROUGE-L | 6.097 | 8.734 |
| Rep-2 | 0.0776 | 0.0790 |
| Rep-3 | 0.0301 | 0.0742 |
| Rep-4 | 0.0187 | 0.1030 |
| Diversity | 0.8787 | 0.7648 |
| Bytes per token | 1.167 | 2.665 |

Table 9 reports these values. Higher ROUGE-L indicates greater surface overlap with reference responses in the reported evaluation. Higher repeated-phrase metrics and lower diversity reveal a tradeoff alongside increased lexical alignment.

Table 10 reports 480 attempted samples, 479 complete comparisons, 309 DVA wins (64.51%), 155 baseline wins (32.36%), and 15 ties (3.13%). Excluding ties, the DVA win rate is 66.59%; the README uses the all-valid-comparisons denominator of 479.

The thesis uses automatic metrics and LLM-based pairwise evaluation and calls the experiment preliminary. Contextual relevance and role consistency do not improve consistently. These findings should not be generalized across models or interpreted as a controlled demonstration that fine-tuning on the seed corpus caused the improvement. Raw judgments, precise model/judge configuration, evaluation prompts, and split definitions are needed for a reproducible account.

## Thesis statistics and current release

The current catalog counts **550,628 nonempty text lines**, while thesis Table 4 reports **550,601 cleaned utterances**. The difference of 27 has not been reconciled; the README reports both with their respective definitions. The thesis's 174,000 seed count matches the current JSON arrays. Current per-file seed counts have a **minimum of 1,083**, versus **1,025 in thesis Table 5**; both report a maximum of 2,000 and a median of 1,900. The cause of the minimum-count difference is unresolved.

The release contains 97 profile files against 96 dialogue, pair, and vocabulary files per layer. The thesis describes aligned resources; current names and the extra erroneous profile require review before an authoritative cross-layer mapping can be claimed.

## Original research and later maintenance

The undergraduate contribution is the dual-output framework, role-level balancing, and rule-based validation and auditing, together with the reported downstream study. Bilingual repository documentation, the deterministic SHA-256 catalog, the present Python validator and its regression tests, and GitHub Actions were added later with Codex assistance. These maintenance additions are distinct from the original thesis implementation.

## Reference

Qian, Ruiyi. (2026). *High-Quality English Role-Playing Datasets Facilitating Dynamic Role Vocabulary Construction*. Undergraduate thesis, College of Foreign Languages and Literature, Fudan University. Supervisor: Ji Tao. Completed May 25, 2026.
