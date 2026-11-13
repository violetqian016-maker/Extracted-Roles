# Known data issues

1. **Wrong identity in `profiles/Bones_Jack.json`.** Its content describes a Canadian novelist named Jack Hodgins rather than the television character. `profiles/Bones_Hodgins.json` also exists. The original files are retained pending a sourced correction or an explicit deduplication decision. Exclude `Bones_Jack.json` from character analysis until resolved.
2. **Layer counts differ.** Dialogue, pair, and vocabulary layers each have 96 files; profiles have 97. The original GitHub description says 95 characters. File counts alone do not prove unique identity counts.
3. **Names are not normalized across layers.** Examples include `HIMYM` / `How I Met Your Mother`, `GoT` / `Game of Thrones`, and abbreviated versus full character names. A verified cross-layer mapping is not supplied.
4. **Upstream sources and pipeline are absent.** Pair metadata points to unbundled transcript files. The original extraction, scoring, and cleaning procedures cannot be reproduced from this repository alone.
5. **Quality flags can remain on kept records.** Short utterances and recovered/context-derived pairs are present. Review flags and source metadata for downstream filtering; structural validation cannot establish valid conversational adjacency.
6. **Profile assertions are unverified.** Backgrounds and style guides should not be treated as authoritative biographies or exact quotations without supporting sources.

The inventory and validation tools make these files inspectable; they do not resolve the semantic issues above.
