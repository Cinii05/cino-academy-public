# Cino Academy 1.3.0 - verified upgrade evidence

## Baseline and scope
- Isolated worktree `max/academy-evidence-voice-20261121` from existing [PR #1](https://github.com/Cinii05/cino-academy-public/pull/1) at `a0ef5dc8f0c919d47c8af10652a3d211f59a6876`; no modifications to TMC or Motion.
- The old six-skill release candidate passed 18 existing local tests before any edits.
- Copied the two newer locally installed Academy references into the isolated worktree and added five small references with targeted routing rather than replacing the nine-stage Academy.
- All actual student essays and genuine writing profiles remain local/connected; this source and distributable package contain only generic instructions and synthetic QA cases.

## Release QA
- Source package v1.3.0 ZIP SHA-256: `99dbf807c1f2fc76bb934c51f784b9e7a6d8eaaf091b53d3c54fcdbfd7818f7c`; 27 allowlisted files, six SKILL.md entry points.
- Static suite after upgrades: 57/57 PASS (18 original + 28 new offline functional + 11 private-package security). Commands: `py -3 scripts/build_package.py`, `py -3 -m unittest discover -s tests -v`; `git diff --check`.
- Independent cross-package tests involve no private coursework or third-party model charges. They verify contract behaviour and intentional failure cases, **not** empirical writing quality or factual relevance of arbitrary source passages.
- Existing installed Kalaris citation-verification script, inspected before execution, resolved public example DOI `10.1038/nature14539`: 1/1 verified. This confirms an online metadata lookup in the MSI, not source-to-claim verification or automatic availability inside ChatGPT.
- Five model-comparison prompts are frozen in `tests/fixtures/academy_compare_cases.json`, explicitly marked `NOT_YET_BLIND_SCORED`. No blind model comparison, real assessment mark uplift or author-voice preference evaluation is claimed.
- No DOCX/PDF deliverable was requested in this upgrade; rendering is part of Academy's future preflight, not a claim that a specimen report was visually reviewed.

## Sources and intellectual property
- [WenyuChiou academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills): evidence binding, rhetorical functions and final-candidate review as *ideas*, not copied prose.
- [SNL-UCSB paper-writing-skill](https://github.com/snl-ucsb/paper-writing-skill): empirical editing workflow and independent criticism as *ideas*; research manuscript rules do not automatically govern undergraduate Business/Management writing.
- [Kalaris Labs research-agent-skills](https://github.com/KalarisLabs/research-agent-skills): MIT-licensed reference verifier already installed separately on the MSI; no third-party executable bundled into the plugin.
- [forjd/better-writing](https://github.com/forjd/better-writing), [andyuninvited/write-like-a-human](https://github.com/andyuninvited/write-like-a-human), [Hiro-Inagawa/write-like-me](https://github.com/Hiro-Inagawa/write-like-me): authentic voice and user-approved editing *ideas*, not copied private corpora or code.
- No external skill repository was automatically installed or vendored. The plugin has no services, MCP server, additional dependencies or copied Academic Phrasebank passages.

## Known limits and follow-ups
- The old platform Academy plugin ID recorded on MSI was inaccessible in this signed-in Plugin Creator account. This is an identity/history discrepancy, not an assertion that the old plugin never existed.
- The v1.3.0 skill is a workflow guide plus portable references; it does not automatically run the local Python QA or live Crossref checks in ChatGPT. Relevant connected tools must be used separately and source results verified.
- Private-plugin creation/availability and platform-native six-route behaviour require a separate actual release receipt. Do not infer them from the local ZIP or tests.
- Authored voice calibration requires genuinely student-authored, consenting samples, ideally including held-out samples, and module-specific verified AI permissions; the synthetic QA suite cannot substitute for that evidence.
