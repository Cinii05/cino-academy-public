# Cino Academy v1.4.0 second-wave implementation — 22 November 2026

## Selected and implemented
Only the four owner-selected improvements have been added: (1) real source-to-passage checking, (3) marker-feedback calibration including reflective writing logic, (4) private research memory, and (6) controlled performance tests. The v1.3 six-skill structure, nine accepted engine contracts, GenAI policy gates, research provenance, module separation and private data boundaries remain unchanged.

### 1. Source-to-passage auditing
- scripts/source_audit.py: offline audit of a local PDF using the already-installed optional pypdf dependency; checks exact quote location, 1-based PDF page, PDF SHA-256 and numeric tokens that need review.
- Cannot authenticate a publisher, infer meaning or prove a research claim from string matches; the substantive claim remains UNVERIFIED by the tool.
- Rejects non-PDF/missing source, malformed manifests and duplicate IDs, empty/oversized/encrypted PDF, invalid PDF pages; flags no extractable text rather than inventing OCR.
- Local integration test generates and reads a two-page synthetic PDF; test has run successfully on the MSI.

### 3. Marker calibration and critical reflection
- scripts/marker_calibration.py: compares exact criterion categories and severity against independently labelled marker feedback; reports true and false positives, material misses, severity disagreement and aggregate precision/recall.
- Never predicts university marks or treats self-generated rubric scores as a verified human grade.
- skills/cino-academy/references/MARKER-CALIBRATION.md: reflection checklist for authentic event, initial assumption, evidence-based challenge, changed judgement, named compulsory case, qualified action and evidence; applied only to reflective assignments permitted by current module rules.
- Generalised from an existing bounded, private historical feedback audit; no original coursework, student identifiers, grades, unique case details or marker comments copied into the public source or package.

### 4. Research memory
- scripts/research_memory.py: local-only Python standard-library SQLite source-card storage; explicit database path, short student-approved excerpts, locator, module ID, provenance, origin chain and source SHA-256.
- Scoped searches prevent accidental retrieval of other modules' notes; duplicate IDs require explicit replacement, changed source files mark cards stale.
- No automatic Zotero import, online sync, embeddings, account credentials, private essay uploads or new subscriptions.

### 6. Controlled benchmark
- scripts/eval_academy.py: requires the same frozen prompts across no-plugin, v1.3 and candidate, independently labelled actual response hashes and six dimensions. Reports pass rates without claiming grade accuracy.
- tests/fixtures/wave2_blind_tasks.json: 12 synthetic frozen cases for quote/source integrity, causal overstatement, reflections, rubric coverage and marker misses. The model runs are NOT_RUN.
- tests/test_wave2.py: real executable negative/positive tests of all four upgrades, plus the optional actual PDF round trip on MSI.

## Release architecture and limitations
- The ChatGPT private plugin remains **six skills**, with four new detailed reference guides under skills/cino-academy/references and targeted routes in existing skills.
- scripts/*.py are **local companion tools in the source repository, not bundled into the skills-only plugin ZIP**. Loading a skill alone cannot run them; an authorised local host (MSI with Desktop Commander, for example) must execute them.
- The scripts perform no network calls and require no new dependency installation. pypdf and reportlab were already present on the MSI; reportlab is used only in an optional integration test.
- A real PDF/string match is not a genuine semantic claim verdict. Historical marker patterns are not an independent assessor or proof of future marks.
- The existing privately released v1.3 plugin is untouched. This is a separately reviewed v1.4 candidate, not a public or private release.

## Verification and test boundaries
- Baseline v1.3: 57 local tests green.
- Wave2 functional tests: 26/26 PASS including the 12-case frozen benchmark inventory; integrated full suite: 83/83 PASS on MSI.
- Integrated local tests and ZIP integrity passed for the current worktree; GitHub CI must be rerun against the final commit before accepting the release.
- Archive privacy, schema, deterministic ZIP, file integrity and existing academic policy tests remain mandatory.
- Independent model A/B/C comparison with real anonymised prompts and verified human judgements is NOT_RUN; no paid model was invoked.
- No actual student paper was uploaded to any model service or source-control repository.
- Full quality assessment on real past essays remains permission-sensitive and should be performed locally/within private approved sources.

## How to use on the MSI
- Source checker: py -3 scripts/source_audit.py --manifest <local-safe-claims.json> --output <local-result.json>
- Library: py -3 scripts/research_memory.py --db <private-local.sqlite3> --add <approved-card.json>
- Search: py -3 scripts/research_memory.py --db <private-local.sqlite3> --search <term> --module-id <module>
- Invalidate changed sources: py -3 scripts/research_memory.py --db <private-local.sqlite3> --check-stale --module-id <module>
- Reviewer comparison: py -3 scripts/marker_calibration.py --input <private-verified-feedback.json>
- Model comparator: py -3 scripts/eval_academy.py --results <real-human-adjudicated-three-arm-runs.json>

All input paths must refer to specifically approved files; never process unrelated client/private files or silently copy the output into Drive. Never install unreviewed dependencies.
