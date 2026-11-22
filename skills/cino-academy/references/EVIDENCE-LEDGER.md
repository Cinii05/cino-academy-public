# Claim–source evidence ledger — exact provenance

The ledger is a **handoff format** for the existing Research/Evidence, Literature Scout, Reference Auditor and Synthesiser. It does not supersede the accepted `SOURCE-ACCESS.md` four-dimensional schema or make a claim true.

For each load-bearing claim, maintain one record with:

```json
{
  "claim_id": "C1",
  "claim_text": "Exact statement being considered",
  "source_id": "S1",
  "bibliographic_identity": {"identifier":"DOI or other real ID","title":"verified or supplied title","authors":[],"year":null,"metadata_checked":false,"metadata_check_source":null},
  "access_level": "UNAVAILABLE",
  "provenance": "USER_SUPPLIED_UNCONFIRMED",
  "attribution_verification": "NOT_VERIFIED",
  "support_state": "UNVERIFIED",
  "passage_locator": null,
  "passage_quote": null,
  "inference_scope": {"population":null,"method":null,"measure":null,"setting":null,"period":null},
  "method_limits": [],
  "counterevidence_ids": [],
  "independence_chain": "ORIGIN_UNKNOWN",
  "comparison_note": "No claim-level source content inspected",
  "checked_at": null
}
```

## Separate five checks

1. **Identity:** title, author, year and actual identifier agree with a publisher, index or original source; *matching DOI alone is insufficient*.
2. **Access:** state whether metadata, authentic abstract, identified partial pages or full source was inspected, or whether the text came from an unauthenticated user excerpt.
3. **Claim support:** compare the actual asserted outcome and level of certainty to an inspected passage, not just topic overlap. A real DOI never makes this automatically SUPPORTED.
4. **Inference scope:** sample, method, timescale, transferability, limitations and conflicting results can only support a commensurate conclusion.
5. **Citation correctness:** in-text key, full bibliography, quoted wording and page location follow the exact required style. A style-correct entry is not proof of research support.

Do not conflate `access_level`, `provenance`, `attribution_verification` and `support_state`. Only `SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONTRADICTED`, `UNVERIFIED` are permitted support states; commentary about an unverified pasted excerpt belongs exclusively in `comparison_note`.

## Discovery vs accepted support

- Search terms, database, date, records actually found, screening/exclusion reasons, DOI and preprint/publication versions are logged by the Scout. Never fabricate counts or claim an API was consulted if it was not.
- A source record tagged METADATA_ONLY can establish metadata identity but **cannot** substantiate a study's results. A paywall or unavailable article stays UNVERIFIED for source-level findings.
- When a student supplies a supposed verbatim passage, preserve `USER_SUPPLIED_UNCONFIRMED` and `NOT_VERIFIED` attribution until the named publisher/source is checked. An actual pasted passage may have `ABSTRACT_ONLY` or `PARTIAL_TEXT_INSPECTED` access without giving verified publication attribution.
- A limited excerpt may fail to mention an outcome, but that does not prove the entire paper contains none; report the inspection limit.
- A fabricated quotation, page number or retraction claim must never be supplied from model memory. A DOI-title mismatch is a metadata identity failure even when the DOI resolves.
- Mirrors, preprints, popular reporting and the same dataset keep **one origin chain** unless genuine independent evidence is established. Do not manufacture independent corroboration from domain count.
- A PRISMA/systematic review designation requires an actual protocol and reproducible documented search/screening stages; otherwise label a narrative or scoped review accurately.

## Tools and executable verification

On an authorised MSI with the *already installed* `citation-verification/scripts/verify_citations.py` and its network prerequisites, a trusted tool runner may execute that script on an approved, non-sensitive reference fixture. Check its source and output; identity checking is **not** claim verification. For a standalone private ChatGPT plugin, first see which genuine tools/connectors exist; this Markdown reference by itself cannot execute Python or query Crossref/OpenAlex. If no source-reading tool succeeds, return a bounded search/check plan with `NOT_VERIFIED` fields, not fabricated papers.

## Handoff and acceptance

A Synthesiser receives source IDs, passage locators, method, contradictions, origin chains and all four provenance dimensions. The Writer inherits accepted Claim IDs, never fills missing support by making citations sound plausible. The reviewer asks: *Could the cited source actually prove this precise sentence?* If not, route back to Research/Evidence before rewriting.
