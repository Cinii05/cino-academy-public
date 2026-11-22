# Lecturer-feedback calibration and reliable reflective critique

Academy MarkerReview is **not a real university marker**. It must quote the exact inspected draft, apply the verified current rubric, report actionable issues and preserve uncertainty. Never promise a numerical grade or a First.

## Actual calibration tool
The repository contains `scripts/marker_calibration.py`. Give it an approved, local JSON file containing independently verified `human_findings` and proposed `academy_findings`, both labelled by criterion and severity. It calculates true positives, false positives, missed criteria, material misses, severity disagreements, precision and recall. It **does not** generate findings or use an LLM; unverified or invented marker labels are rejected. On a machine run `py -3 scripts/marker_calibration.py --input private-comparison.json --output private-calibration.json`.

Permitted criterion categories: `brief_compliance`, `evidence`, `case_application`, `critical_evaluation`, `reflection`, `method`, `structure`, `referencing`. A human-verified comment can establish that *a marker raised this issue*; it does not independently prove that a model is a reliable marker across modules. Calibration is only category agreement; report sample size, missing categories, and data provenance.

## Private historical feedback: only generalisable findings

An existing **private** University evidence audit reviewed a bounded set of past marked assignments and quotations from marker notes, not every past paper. It records useful contrasting examples: a successful reflection made the change from an earlier assumption to a challenged understanding and a future decision explicit; another evaluation successfully challenged a management method but omitted the required specific earlier practical example. Recurring weaker marks arose from missed brief requirements, superficial discussion, stale/weak evidence, unsubstantiated business claims and missing case details. This review's underlying submissions and exact feedback stay **outside public GitHub and the plugin archive**. Its module-specific conclusions and marks are not universal training targets.

### Reflection diagnostic (only when the current assignment actually asks for reflection)
- **Actual event and specific role:** Is the claimed experience genuine and from the student? Do not invent participation or emotions.
- **Initial assumption:** What did the student believe or do before, and why?
- **Evidence-based challenge:** What actual event, result, feedback or theory challenged that view? A generic "I learnt" is insufficient.
- **Changed judgement:** What exactly changed in their reasoning, and what alternative interpretation remains possible?
- **Own-case application:** Is a compulsory product, meeting, decision or task **named and explained**, rather than "the project"?
- **Action with consequence:** What would be done differently, under which condition, and how would improvement be known?
- **Rubric fidelity:** Reflective first-person voice is used only if the current task calls for it; do not transfer previous module's third-person/report rule or specific case facts.

This is a **review prompt and evidence checklist**, not a fake automated reflective-grade algorithm. For a generic critical essay, do not demand a personal anecdote or first-person text.

## Limits
Only draw on private marked examples with genuine provenance and author permission. No automatic learn-and-rewrite from university submissions. A marker's comment may be wrong or incomplete; record scope and evidence. Benchmarks must use anonymised/synthetic public fixtures; human real-work calibration remains local/private.
