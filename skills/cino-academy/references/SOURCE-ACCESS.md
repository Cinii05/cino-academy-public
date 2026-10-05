# Source access and independence

A source record must describe what was actually inspected. Identity, prestige, a DOI, a citation, or a URL does not prove access to the supporting text.

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
