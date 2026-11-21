# Revision receipt — evidence-based closure

A fluent second draft is not proof that the identified problem was fixed. MarkerReview is independent and read-only; Revision edits only a finding the user authorises. First+ proposes opportunities after material closure, not an arbitrary grade chase.

## Required fields

```json
{
  "draft_id": "synthetic-draft-01",
  "draft_sha256": "64 lowercase hexadecimal characters for the actual reviewed bytes",
  "finding_id": "F1",
  "finding_status": "OPEN",
  "location": "Section and exact quoted excerpt",
  "rubric_criterion": "Verbatim criterion if verified",
  "severity": "P0|P1|P2",
  "observed_problem": "Specific issue in this draft",
  "evidence_refs": [],
  "smallest_proposed_fix": "The affected claim or paragraph, not a full rewrite",
  "student_decision": "PENDING|ACCEPTED|REJECTED",
  "revision_sha256": null,
  "reviewer_role": null,
  "independent_reviewer_result": "NOT_REVIEWED",
  "checked_claims": [],
  "checked_citations": [],
  "outstanding": []
}
```

- Hash the actual draft when source bytes are available; otherwise use an honest stable version identifier and say hash NOT_VERIFIED. A model must not invent hashes.
- The reviewer quotes and inspects the exact current draft; a prior version's feedback cannot close a different draft.
- A finding cannot be marked RESOLVED by the same Writer/Revision worker who applied it. The independent reviewer must inspect the exact **new** draft and record an acceptance or an open finding.
- Any changed numbers, citations, quotations, causal terms, scope qualifications or first-person experience requires new fidelity/evidence checks. The stylistic editor does not invent facts or silently modify a supported claim.
- Reject repeated cosmetic changes when the same issue persists; stop after the accepted three-attempt cap rather than declaring success.
- A material new source or empirical claim is a Research/Evidence change, not a permissible style pass.
- Report **fixed / independently rechecked / still open / learner decision**. Do not issue a fabricated mark, PASS or "submission-ready" label.

## Synthetic no-self-closure test

Writer changes "caused a 20% increase" to "was associated with a 20% increase" in revision R1. This is potentially a genuine evidential repair, but the reviewer must inspect the source and exact R1 text before marking F1 resolved. If the reviewer only inspected the old draft, status stays OPEN.

## Real marker feedback

Use only feedback actually supplied and distinguish course-specific criticism from portable writing principles. Record each issue with its rubric location and the author's accepted correction; never train on invented reviewer comments.
