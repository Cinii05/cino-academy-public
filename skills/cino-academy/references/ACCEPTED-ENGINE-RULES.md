# Assignment Engine

# Assignment Engine acceptance rules

- Every authoritative execution requirement must exist both as a Core constraint and as an AssignmentSpec requirement bound to that constraint.
- Every AssignmentSpec source must resolve to an inspected Core SourceRecord.
- Material unresolved ambiguity must exist as a blocking Core uncertainty and be referenced by AssignmentSpec.
- A missing protected dependency must be represented as uncertainty rather than guessed content.
- Equal-current conflicting instructions with no precedence rule must not become active constraints.
- Explicit supersession may select the newer instruction without false uncertainty.
- Context-only or informal notes cannot override official assessment authority.
- The engine gate is PASS only when no blocking uncertainty remains; otherwise NOT_VERIFIED. Contract or semantic failures are STOP in the acceptance runner.

---

# Rubric Engine

# Rubric Engine v0.1 acceptance rules

- Consume the exact Assignment Engine envelope named by the scenario.
- Stop immediately when the upstream Assignment Engine gate is not PASS.
- The model emits only rubric interpretation, never a rewritten CinoTask or AssignmentSpec.
- Inspect every supplied rubric source when upstream is PASS, including table notes, footer criteria and appendices.
- Respect CURRENT, SUPERSEDED and CONTEXT_ONLY authority status.
- Superseded material cannot control the RubricMap.
- Preserve weights exactly. Never normalize an invalid percentage total.
- Conflicting current descriptors, weights or grade-band thresholds remain unresolved unless supplied authority resolves them.
- Missing current rubric material or a required descriptor appendix returns NOT_VERIFIED.
- A PASS interpretation creates one Core acceptance criterion per rubric criterion.
- NOT_VERIFIED creates no RubricMap and no rubric-backed Core acceptance criteria.
- Do not infer a target band merely because the rubric contains a First or top band.
- Stable Academy criterion IDs are assigned by the adapter through the v0.1 canonical-ID map.

---

# Research/Evidence Engine

# Research/Evidence Engine v0.1 rules

1. Correct negative conclusions are valid outputs. `UNSUPPORTED`, `CONTRADICTED` and `UNVERIFIED` are not engine failures.
2. SOURCE_FACT requires an inspected source.
3. Source quality does not by itself establish a claim.
4. Promotional/unverified material may be retained as background but cannot be the sole load-bearing basis of a central academic claim.
5. Known contradictory evidence must remain visible in Claim counterevidence or in a status that reflects the conflict.
6. Copy-derived sources and analyses of one underlying dataset share one independence chain.
7. Citation relevance is not claim support; a source about satisfaction does not prove productivity.
8. Missing primary evidence remains missing. Secondary reporting cannot be silently promoted to primary verification.
9. Narrow evidence must not be generalised beyond its stated population/outcome without qualification.
10. EvidencePack is dependency-closed across claims, evidence derivations and source support.

---

# Argument Architect

# Normative v0.1 rules

1. Final graph nodes may reference only Core Claims present in accepted EvidencePack inputs.
2. The thesis statement must exactly match the selected Core Claim statement.
3. UNSUPPORTED, CONTRADICTED and UNVERIFIED claims cannot be thesis.
4. PARTIALLY_SUPPORTED thesis requires PASS_WITH_NOTES and explicit material challenge/limitation.
5. Material counterarguments cannot be replaced by easy strawmen.
6. Material claims may not be omitted merely because they weaken the preferred thesis.
7. Support/dependency/synthesis/lead-to cycles are invalid.
8. All argument-required rubric criteria must be covered.
9. Every graph node must be placed in at least one section.

---

# Academic Drafter

# Academic Drafter v0.1 rules

1. Accepted ArgumentGraph Claims are the maximum substantive claim set.
2. Every non-transition sentence must bind to accepted Claim/Evidence state.
3. `primary_claim_ref` identifies the Claim whose meaning and strength the sentence is asserting.
4. Auxiliary Claim refs may provide synthesis context but cannot silently widen the primary assertion.
5. Citation keys must resolve to the accepted EvidencePack; no invented author/date/DOI data.
6. Lexical causal or universal wording is independently checked; model strength labels are not trusted blindly.
7. Counterclaims and limitations required by the ArgumentGraph must appear materially in prose.
8. Each non-conclusion section must contain analysis or synthesis, not only description.
9. Three or more paragraphs sharing the same four-word opening is a v0.1 formulaic-pattern failure.
10. Thesis conclusions cannot exceed the accepted thesis strength.
11. Section word targets are enforced with a 20% tolerance in v0.1 acceptance.
12. Production defaults to ArgumentGraph word targets; the acceptance suite uses compressed execution targets to keep adversarial fixtures tractable.
13. Academic Voice is out of scope. The Drafter proves reasoning fidelity first.
14. Accepted rendered drafts become Core GENERATED_OUTPUT SourceRecords with UNINSPECTED status for downstream independent review.

---

# Academic Voice

# Academic Voice v0.1 rules

1. Text only: structure, Claim/Evidence/citation/strength bindings are copied deterministically.
2. Every applied personal trait must exist in VoiceProfile and trace to inspected SELF_AUTHORED evidence.
3. Citation markers and numerical facts are immutable in v0.1.
4. Negated or bounded meaning cannot become positive/unbounded meaning.
5. Voice transformation cannot increase the Drafter sentence strength ceiling.
6. No deliberate errors, slang, filler, fake quirks or detector-evasion behaviour.
7. Document word count must stay within +/-15% in acceptance.
8. The transformed draft is GENERATED_OUTPUT and remains UNINSPECTED for downstream MarkerReview.

---

# MarkerReview

# MarkerReview v0.1 rules

- Inspect the actual post-voice submission.
- Submission hash must match the accepted Voice artifact.
- Reviewer must be independent of Academic Drafter and Academic Voice.
- Review every RubricMap criterion exactly once.
- Every review observation must quote the actual submission.
- Formal review EvidenceItems must be supported by the inspected submission SourceRecord.
- Literature can inform judgement but is not evidence that the submission itself demonstrates a rubric criterion.
- Material weaknesses cannot be omitted.
- Coverage cannot exceed the controlled evidence available in the submission.
- Overall gate is derived from criterion gates and findings.
- A rubric band may only be selected when the submission is complete enough and all material review evidence supports that decision.
- Otherwise create an UNRESOLVED Core DecisionRecord.

---

# Revision Engine

# Revision Engine rules

- Every edit targets one OPEN Core CinoFinding.
- The smallest effective edit wins.
- Accepted Claim/Evidence/citation/strength/role bindings are copied mechanically.
- No new empirical fact or source may enter through Revision Engine. Research changes must return to Research/Evidence Engine.
- Counterarguments and limitations are protected from deletion unless the finding specifically targets them.
- The engine may request re-review but cannot mark a finding resolved.
- Closure requires independent inspection of the revised GENERATED_OUTPUT.
- Repeating the same edit or reaching attempt 3 without closure stops as a revision-loop risk.

---

# First+

# First+ v0.1 rules

1. Activate only after independent closure of prior material/blocking findings and with no open P0/P1 finding.
2. First+ proposes intellectual opportunities. It does not rewrite the submission.
3. Existing accepted Claim wording is immutable at this layer.
4. New substantive claims require Research/Evidence rather than First+ invention.
5. Genuine originality is a defensible new connection, comparison or tension among accepted evidence chains. Naming a framework is not originality.
6. Sophisticated vocabulary or imported theory without evidence is not an improvement.
7. Grade, band and percentage chasing is forbidden.
8. `NO_CHANGE` is a successful outcome when the remaining opportunity is stylistic, unsupported, redundant or immaterial.
9. Independently closed findings remain protected.
10. Every accepted escalation returns through the relevant governed capability and then through Drafter, Voice and MarkerReview before adoption.
11. First+ may route a genuine research gap to Research/Evidence only with an explicit research question.
12. First+ uses PLAN authority only and never receives a mutation grant.
