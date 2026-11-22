# Orchestration contract

Stage order: Assignment -> Rubric -> Research/Evidence -> Argument -> Draft -> Voice -> MarkerReview -> Revision -> First+.

Blocking gates: NOT_VERIFIED, STOP, FAIL. PASS_WITH_NOTES is non-blocking but notes remain attached downstream. A stage may only consume accepted upstream artifacts. Provider failures are bounded and must not be rewritten as model certainty.

## Five routes, one authority

See `ASSIGNMENT-CARD.md`. QUICK invokes the smallest permitted writing helper. RESEARCH invokes appropriate Scout/Auditor/Synthesiser helpers. ARGUMENT invokes Essay Planner/Argument Workshop. REVIEW inspects the exact current draft and creates a revision receipt. FULL retains the nine accepted gates in order. Helper findings are **inputs**, not new PASS gates.

Persist the current assignment's identity, authoritative policy and source provenance. Different module policies never carry across a new assignment. Not checked must remain NOT_VERIFIED. A model proposal must never be reported as a script, search, renderer, reviewer or rubric gate actually executed.
