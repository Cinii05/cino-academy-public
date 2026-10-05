# Orchestration contract

Stage order: Assignment -> Rubric -> Research/Evidence -> Argument -> Draft -> Voice -> MarkerReview -> Revision -> First+.

Blocking gates: NOT_VERIFIED, STOP, FAIL. PASS_WITH_NOTES is non-blocking but notes remain attached downstream. A stage may only consume accepted upstream artifacts. Provider failures are bounded and must not be rewritten as model certainty.
