# Data reference

## Dialogue text

`Extracted-Roles/<series>/<character>.txt` contains UTF-8 text, with one nonempty line counted as one utterance. These files do not preserve complete speaker-to-speaker conversation structure or explicit episode boundaries.

## Prompt–response pairs

`data/latest_single_pair_seed_v3/<series>/<CHARACTER>.json` is an array of objects. The current snapshot has 174,000 objects across 96 files.

| Field | Stored meaning / structure |
| --- | --- |
| `canonical_pair_id` | Unique string across this pair layer |
| `target_char` | Target character identifier; matches the JSON filename stem |
| `interlocutor`, `interlocutor_type` | Prompt speaker identifier and category |
| `dialogue` | Two objects with `text`; speaker labels use `interlocutor` and/or `speaker` |
| `prompt_speaker_in_roster`, `response_speaker_in_roster` | Boolean roster membership metadata |
| `prompt_word_count`, `response_word_count`, `total_word_count` | Stored counts; total must equal prompt plus response |
| `quality_flags` | Array of quality annotations; retained records may still carry drop/short flags |
| `single_turn_quality_score`, `quality_decision` | Stored quality metadata; scoring procedure is not bundled |
| `source_type`, `dedup_status` | Extraction/recovery and deduplication labels |
| `source_refs`, `source_count` | Source-reference objects and stored source count |
| `softcap_*`, `sample_weight`, `recovery_reason` | Optional selection/recovery metadata |
| `input_turns`, `context_window`, `context_candidate_id` | Optional context-recovery metadata |

Additional fields are preserved. This table describes observed data rather than an independently verified extraction specification. The validator checks core structural invariants, not every optional metadata field or the original tokenizer. All current `quality_decision` values are `keep`; this is an upstream decision, not an independent quality certification.

Observed `source_type` values and counts:

| Source type | Pairs |
| --- | ---: |
| `single_turn_raw_txt_robust_roster_prompt` | 59,209 |
| `single_turn_csv_roster_prompt` | 49,938 |
| `single_turn_csv_external_prompt` | 33,190 |
| `single_turn_raw_txt_robust_external_prompt` | 24,148 |
| `low_resource_raw_rescan_same_speaker_merged` | 4,156 |
| `borderline_real_recovered` | 2,841 |
| `context_window_recovered` | 518 |

Source references contain paths such as `Full Scripts_stageclean_all_v1/...` and line/row locations. These refer to upstream material that is absent from this repository; the validator does not treat those paths as local files.

## Profiles

`profiles/*.json` contains one object per file, with string fields `character_name`, `series_name`, `identity`, `background`, `personality`, `world_setting`, and `style_guide`, plus a `relationships` object. The generation method and supporting sources are not bundled. Profile facts and quoted catchphrases require review.

## Vocabulary

`vocab_by_character_clean_v1/*.json` contains arrays of nonempty strings. Entries include words, names, phrases, and fragments. They are not frequency tables, nor necessarily unique across characters. The extraction and cleaning procedures are not bundled.

## Reproducible inventory

Run `python3 scripts/dataset.py catalog` after changing any corpus files. The inventory is sorted by layer and relative path, contains no timestamp or absolute machine paths, and hashes the original bytes. `catalog --check` compares the regenerated inventory against the committed version without writing it.

## Provenance still to document

The maintainer should add the original transcript URLs and versions, acquisition dates, extraction scripts and settings, profile creation method, word-count rules, and selection/scoring definitions. No train/validation/test split is supplied; any downstream split needs its own leakage assessment.
