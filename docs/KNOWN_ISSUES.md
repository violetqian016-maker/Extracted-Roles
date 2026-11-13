# Known data issues

1. **Wrong identity in `profiles/Bones_Jack.json`.** Its content describes a Canadian novelist named Jack Hodgins rather than the television character. `profiles/Bones_Hodgins.json` also exists. The original files are retained pending a sourced correction or an explicit deduplication decision. Exclude `Bones_Jack.json` from character analysis until resolved.
2. **Layer counts differ.** Dialogue, pair, and vocabulary layers each have 96 files; profiles have 97. The original GitHub description says 95 characters. File counts alone do not prove unique identity counts.
3. **Names are not normalized across layers.** Examples include `HIMYM` / `How I Met Your Mother`, `GoT` / `Game of Thrones`, and abbreviated versus full character names. A verified cross-layer mapping is not supplied.
4. **Upstream sources and pipeline are absent.** Pair metadata points to unbundled transcript files. The thesis methodology and Appendix A source links are summarized in [RESEARCH.md](RESEARCH.md) and [SOURCES.md](SOURCES.md), but the original executable extraction, scoring, and cleaning pipeline is not bundled.
5. **Quality flags can remain on kept records.** Short utterances and recovered/context-derived pairs are present. Review flags and source metadata for downstream filtering; structural validation cannot establish valid conversational adjacency.
6. **Profile assertions are unverified.** Backgrounds and style guides should not be treated as authoritative biographies or exact quotations without supporting sources.

7. **Thesis and release utterance counts differ.** Thesis Table 4 reports 550,601 cleaned utterances; the catalog counts 550,628 nonempty text lines, a difference of 27. The underlying cause is unresolved; neither source has been silently adjusted.
8. **Minimum seed count differs.** Thesis Table 5 reports a minimum of 1,025 seeds per role; current JSON arrays have a minimum of 1,083. Both have 174,000 total pairs, a maximum of 2,000, and a median of 1,900. The cause is unresolved.

9. **Text duplicates remain despite unique IDs.** The read-only [quality review](PIPELINE_REVIEW.md) identifies 139 within-role normalized-text duplicate groups. These require contextual review, not automatic removal.
10. **Length statistics differ from the thesis.** Stored word counts yield 49 responses under 3 words and 4,075 over 50, versus 14 and 4,460 in thesis Table 8. Version and token-count rules need reconciliation.

The inventory and validation tools make these files inspectable; they do not resolve the semantic issues above. See [PIPELINE_REVIEW.md](PIPELINE_REVIEW.md) for measured findings and proposed improvements.
