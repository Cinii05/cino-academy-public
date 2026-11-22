# Cino Academy 1.4.0 - Wave 2 private release candidate (not published)

Six independent skills built on the original nine-stage Academy contract:
- Cino Academy: assessment permissions, rubric/brief and source-controlled full workflow.
- Cino Essay Planner: argument outline and bounded Socratic challenge.
- Cino Literature Scout: genuine source discovery and access reporting.
- Cino Literature Synthesiser: contrasts, method limits and independent evidence.
- Cino Reference Auditor: metadata checks distinct from claim/passage support.
- Cino Writing Master: genre-sensitive author voice, editing and document review.

New source and author-voice methods are reference guidance. The standard
portable ChatGPT ZIP does not execute the local test scripts or consult a
research index automatically. A source or browser check is verified only
when an actual tool successfully performed it. Individual user writing
profiles, university work and credentials are excluded from this archive.

The Academy operates within the current verified module-specific GenAI
policy and does not guarantee a grade or an AI-detector outcome.

This is a separate Academy project; no TMC or Motion source is changed.
Source: https://github.com/Cinii05/cino-academy-public

## Wave 2: selected improvements (22 November 2026)

1. Source-to-passage audit: scripts/source_audit.py locates user-supplied text and numeric tokens on actual PDF page indices; it never proves the factual claim or authenticates the publisher. pypdf is optional and already on the MSI.
2. Marker calibration and reflection: scripts/marker_calibration.py compares verified marker finding categories to Academy findings without predicting grades. Only generic lessons from past private feedback are in the bundled skill reference; historical essays are not committed.
3. Private research memory: scripts/research_memory.py uses an explicit local SQLite file, module scoping, excerpt size limits, source hashes and stale warnings.
4. Controlled benchmark: scripts/eval_academy.py requires human-labelled real output from three comparison arms. Real model-level improvement has not been proven by deterministic checks.

Scripts live outside the skills-only plugin archive; ChatGPT skill references alone cannot execute programs. An authorised host with Remote Desktop Commander can invoke them. The existing private v1.3 release is untouched and remains available for rollback pending approved v1.4 release.
