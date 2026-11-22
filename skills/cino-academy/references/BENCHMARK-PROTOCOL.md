# Cino Academy controlled performance benchmark

The 57 passed v1.3 tests proved static source rules and archive integrity; they **did not** demonstrate source auditing accuracy across real PDFs, lecturer agreement or genuine learning improvement. The v1.4 candidate adds executable offline unit and integration tests, and a comparator of genuinely run model responses.

## Fair comparison

Use frozen task inputs and one known tool set for **A = no plugin**, **B = v1.3**, **C = candidate**. Give identical papers and policies, capture model/version, actual tool and skill invocations, prompt/response hashes, runtime and any external costs. Do not run paid models without permission. Independently inspect examples; do not let the generating agent mark its own output without disclosure.

After genuine model output is collected, label each case against a frozen rubric covering: citation identity, exact quotation correctness, numerical fidelity, absence of hallucinations, specific counterarguments, rubric coverage, permission safety, reflection depth, and useful next actions. An expert human or independent adjudicator signs the label. The comparison tool is `scripts/eval_academy.py`; it **never calls a model** and refuses unverified labels. Actual model-quality benchmarking is NOT_RUN until all three arms and qualified assessor labels exist.

## Minimum cases
- Real DOI, mismatched title and wrong claim
- Genuine PDF passage and invented quotation
- Correct quote on wrong PDF page
- Metadata-only source presented as empirical support
- Quote correctly located but causal interpretation unsupported
- Numeric percentage/denominator mismatch
- Two URLs to one origin study
- Missing institutional AI-use permission
- Weak reflection with no challenged assumption or specified consequence
- Strong reflection that omits required case detail
- Feedback misses material rubric requirement
- Reviewer self-closes a finding or assigns an unsupported mark

**Release gate:** runnable checks and negative paths pass; exact ZIP file inventory and privacy scan pass; no unsupported "improvement" claims; evaluation summary explicitly distinguishes simulated examples, real PDF checks, live model comparisons and genuine lecturer outcomes. Do not upload/private-publish the candidate automatically based on an offline test score.
