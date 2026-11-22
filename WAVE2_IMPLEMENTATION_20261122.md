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
- Wave2 functional tests: 29/29 PASS including the 12-case frozen benchmark inventory; integrated full suite: 86/86 PASS on MSI.
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

## Post-CI code review improvements
- Corrected source_audit output to use the formal FULL/PARTIAL/UNAVAILABLE access vocabulary, never an invented access status. PDF page extraction now rejects overlong text instead of silently truncating it.
- Searching an absent research database now fails visibly without silently creating an empty, misleading SQLite file.
- Marker calibration requires an auditable source locator for claimed verified human feedback. The comparator now requires distinct generator and reviewer identities on each model arm.
- Added negative tests for each issue: final local suite 86/86 PASS; CI must be rerun on the updated exact commit.

## Independent Codex findings and verified repairs — 22 November 2026

Independent Codex review against PR #2 initially identified three P2 correctness defects. The following scoped fixes are committed on the existing v1.4 feature branch, not merged into main or deployed:

1. `scripts/research_memory.py`: a SUPPORTED card with omitted `access_level` is now rejected, matching the stored default UNAVAILABLE. The new regression test covers the omitted and explicit UNAVAILABLE cases plus a valid PARTIAL_TEXT_INSPECTED record.
2. `scripts/research_memory.py`: a source_path is resolved to the existing file's absolute canonical path before hashing and persistence. The new regression test switches between two directories containing identically named, different source files, and checks that staleness is determined against the original one.
3. `scripts/marker_calibration.py`: independently verified human marker feedback must have the literal JSON boolean `true`; strings such as "false"/"UNVERIFIED", integers and null can no longer enter calibration as verified. The new test checks these invalid cases.
4. A second read-only Codex review of the updated PR identified a further P2 numeric-sign error in `scripts/source_audit.py`: negative percentages or correlations matched positive numbers. The expression and text normaliser now preserve ASCII/Unicode minus signs, with tests for +/−20% and +/−0.6 source/claim reversals and equivalent negative glyphs.

**Evidence:**
- Fix commits `1e183f31dc87064b3207b98f6fb03d5dfc6dc450` and `fe3cf082d1279a0647ef85cc624591f24d3b98cd`.
- The new tests failed before the corresponding code fixes, then passed after the repairs.
- MSI full test suite: **90/90 PASS**, including the optional two-page PDF integration test.
- GitHub Actions for `fe3cf08`: **SUCCESS**, **90 tests**, one optional Linux PDF test skipped; the same test passed on MSI.
- Exact skills-only ZIP hash remains `0656c9d88c25d2113d56f1499981b3cb7b0df8e482d62b20a179ec33b3460840` because executable Python tools and their tests are intentionally outside the portable six-skill archive.
- No real student data was used in regression tests, no new dependency was installed, and the private v1.3 release is unchanged.

A third, narrow, read-only Codex review was requested on commit `fe3cf08` to validate the final sign-handling fix. This review is independent of the MSI and CI test results and is not a merge or publication approval.

### Third Codex review and runtime adjudication

Codex completed a read-only review of sign-fix commit `fe3cf08` and raised a P2 concern that a range such as `10-20%` would be parsed as `-20%`. Codex's restricted read-only shell could not run Python. We checked the exact claim on the real MSI host: `test_numeric_range_hyphen_is_not_a_negative_sign` verifies that ASCII `10-20%` and mathematical-minus `10−20%` both parse as positive endpoints `10` and `20%`, accept a `20%` reference and warn against a `-20%` interpretation. The regression test **passed**, so this exact reported case is a false positive and no additional source-auditor code change is needed.

This check tests parsing only, not the truth of the whole interval or any scientific inference. More ambiguous spaced ranges and unusual PDF extraction remain reasons for human/source review, not automatic claim support. The new test and source-linked review receipt are retained in PR #2.
