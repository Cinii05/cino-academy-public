# Source-to-passage verification (v1.4 candidate)

**Authority:** Existing `SOURCE-ACCESS.md` and `EVIDENCE-LEDGER.md` remain controlling.

## Actual executable on an authorised local machine
The source repo contains `scripts/source_audit.py`, an offline PDF text/quotation inspector that can run on the MSI where `pypdf` is already installed. The plugin ZIP is skills-only: **loading this skill does not run the script, access local PDFs, or guarantee PDF text extraction**. Use an authorised local tool to execute it, or use actual connected file/PDF tools where permitted. No paid API, network, OCR or model judgement occurs in the script.

Input is a JSON manifest with a real local PDF path and 1–100 claims. Each claim has `claim_id`, `claim_text`, optionally `quoted_passage` and `pdf_page` (1-based **PDF** page, not printed page). Run `py -3 scripts/source_audit.py --manifest local-manifest.json --output local-report.json`. Never commit the manifest, report or PDF if it contains personal or copyrighted coursework.

A quote located on a PDF page means the text occurs in **that file**, not that it was said by a particular author, that the publication is authenticated, or that its methods support a student's interpretation. PDF extraction can miss tables, columns, scanned pages, ligatures and printed page numbers. Missing passage = **NOT VERIFIED**, not a categorical claim that the publication never contains it. Numbers missing from the quoted passage create a review warning, not a proof of contradiction.

## Review procedure
1. Confirm the source's identity separately from title/author/year/DOI; label a user-supplied PDF `USER_SUPPLIED_UNCONFIRMED` until independently matched to the publisher or identified public original.
2. Record actual PDF SHA, accessed section/page and quote-check status; report page-index ambiguity.
3. Compare the **precise claim** against the inspected passage, population, method, outcome and timeframe with a human or explicitly labelled model-assisted critical judgement.
4. Only the authorised Research/Evidence engine can set `SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED` or `CONTRADICTED` after sufficient authenticated evidence. The local script always returns substantive claim support as `UNVERIFIED`.
5. Stop at suspicious citation swaps, invented page numbers, numerical mismatches and inaccessible source text; never let fluency override the evidence gate.

## Acceptance and limits
Required examples: correct quotation, correct quotation on a different PDF page, absent text, source with no machine-readable text, exact numeric mismatch, repeated PDF, altered PDF SHA and misleading causal statement despite a genuine quotation. Confirm no network or model call. Redo audits if the actual source bytes change.
