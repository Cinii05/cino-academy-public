# Source access and independence

A source record must describe what was actually inspected. Identity, prestige, a DOI, a citation, or a URL does not prove access to the supporting text.

## Evidence record schema

Record **four separate dimensions** for every study claim: `access_level` (what text was actually inspected), `provenance` (independently retrieved vs USER_SUPPLIED_UNCONFIRMED), `attribution_verification` (VERIFIED or NOT_VERIFIED against the identified publication), and `support_state` (exactly one of SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED or UNVERIFIED). Notes about matching or contradicting a user-provided excerpt are `comparison_note` free text, **not** additional support states. Keep a user-supplied passage's claimed publication/page unverified until a genuine source is checked. Every helper must carry these fields into synthesis and citation audits; a source access level alone never proves authenticity.

## Access modes
- `FULL_TEXT_INSPECTED`: the relevant full source was inspectable and the supporting section was checked.
- `PARTIAL_TEXT_INSPECTED`: only identified pages/sections were inspected. Support cannot exceed those inspected portions.
- `ABSTRACT_ONLY`: only an abstract/summary supplied by the publisher or index was inspected. It may support claims explicitly stated at abstract level, with that limitation preserved, but must never be described as full-text inspection.
- `METADATA_ONLY`: bibliographic metadata only. It may establish metadata facts, not substantive academic claims.
- `USER_SUMMARY_ONLY`: the user's description of a source without inspectable source text. Treat as context pending verification.
- `UNAVAILABLE`: the source could not be inspected. It cannot support a substantive claim.

## Claim-strength rule
A Claim may never be stronger than the combination of its inspected evidence, access mode, population, outcome, timeframe and methodology supports. Missing access is an epistemic gap, not permission to infer.

`UNVERIFIED` is a legitimate state when evidence or access is missing. Do not convert it into a fabricated fact or automatically treat honest uncertainty as misconduct.

## Independence
Every EvidenceItem should retain an independence-chain identifier where sources derive from the same underlying study, dataset, press release, report, repository copy, or analysis. Multiple URLs or secondary reports from one origin do not become independent corroboration.

A systematic review or genuinely independent analysis may add value, but independence must be based on underlying evidence provenance, not domain count.

## Contradiction
Known credible contradictory evidence remains visible. Do not resolve a conflict by silently dropping the weaker-looking side. If the current evidence cannot responsibly settle a load-bearing conflict, preserve the uncertainty and route it back to Research/Evidence.

## Citations
Citation presence proves neither access nor support. Every load-bearing citation must resolve to an accepted source/evidence record whose inspected content actually supports the bound claim at the asserted strength.

A user-provided paraphrase said to derive from an abstract is still `USER_SUMMARY_ONLY` until the original abstract wording is inspected. Citation-to-claim support remains `UNVERIFIED` on a paraphrase alone; tag apparent agreements/mismatches as hypotheses rather than inspected source support.

## Supplied verbatim publisher snippets versus user paraphrases

If the user pastes actual quoted text *claimed* to be from a publisher abstract or identified Results passage (rather than their paraphrase), record `ABSTRACT_ONLY` or `PARTIAL_TEXT_INSPECTED` for only that inspected passage, with `provenance=USER_SUPPLIED_UNCONFIRMED` and `attribution_verification=NOT_VERIFIED`. This records what words were read, **not** that those words genuinely occur in the named publication or on the claimed page. A paraphrase remains `USER_SUMMARY_ONLY`. A numeric contradiction against the pasted excerpt can be described in a `comparison_note`, but independent publication attribution and full-source claim support remain `UNVERIFIED` until the original source is verified. Do not use a new composite status token for excerpt-scoped comparisons.
