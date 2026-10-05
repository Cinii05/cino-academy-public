# Submission-readiness preflight

Run this preflight before calling any artifact submission-ready. It does not override assessment-specific requirements.

## Required checks
1. Current assessment brief, rubric/marking criteria and material module guidance are identified and conflicts are resolved or explicitly blocking.
2. The assessment's current GenAI policy is known for the requested use. Unknown or prohibitive policy blocks generative submission prose.
3. Required primary evidence exists where the assessment or argument depends on it.
4. Load-bearing claims have accepted evidence whose access mode and scope support the asserted strength.
5. Known material contradictions and limitations are represented rather than hidden.
6. Rubric criteria have explicit coverage states; no required criterion is silently omitted.
7. In-text citations resolve to inspected accepted sources, and the reference list has no material orphan or missing entries.
8. Structure, word-count rules, required sections, appendices, tables and figures satisfy the current authority.
9. Academic Twin, if used, changed style only and preserved meaning, citations, numbers and claim strength.
10. MarkerReview inspected the current rendered draft; Revision did not self-close findings.
11. Required DOCX/PDF output was structurally checked and visually inspected when a rendered artifact is part of the deliverable.
12. Remaining notes, uncertainties and limitations are visible to the user.

## Gate
- `PASS`: mandatory preflight checks are satisfied for the requested deliverable.
- `PASS_WITH_NOTES`: the deliverable may proceed, but non-blocking limitations remain attached.
- `NOT_VERIFIED`: a required authority, evidence, policy, source-access or output check is missing or materially unresolved.
- `STOP`: proceeding would require fabrication, misrepresentation, prohibited conduct or another hard safety/integrity violation.
- `FAIL`: the preflight itself or a required deterministic validation failed.

Do not replace `NOT_VERIFIED` with polished prose. Route the unresolved dependency to the relevant upstream stage.
