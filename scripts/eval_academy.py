"""Score genuinely executed, independently labelled Cino Academy comparisons.

This script NEVER invokes a model or judges essays; it only aggregates verified
human ratings on identical, frozen tasks across the required three arms.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ARMS = ("no_plugin", "academy_v1_3", "academy_candidate")
DIMENSIONS = ("factual_accuracy", "citation_fidelity", "reasoning",
              "rubric_coverage", "permission_safety", "useful_feedback")

class BenchmarkError(ValueError):
    pass

def score_suite(suite: dict) -> dict:
    cases = suite.get("cases")
    if not isinstance(cases, list) or not cases:
        raise BenchmarkError("At least one test case is required")
    ids = [c.get("case_id") if isinstance(c, dict) else None for c in cases]
    if None in ids or len(ids) != len(set(ids)):
        raise BenchmarkError("Case IDs must be unique and non-empty")
    by_arm = {a: {k: 0 for k in DIMENSIONS} for a in ARMS}
    counted = {a: 0 for a in ARMS}
    raw = {}
    for case in cases:
        if not case.get("frozen_input_sha256") or len(case["frozen_input_sha256"]) != 64:
            raise BenchmarkError("Each case requires a fixed input SHA-256")
        outcomes = case.get("outcomes", {})
        if set(outcomes) != set(ARMS):
            raise BenchmarkError(f"{case['case_id']}: all three comparison arms required")
        for arm in ARMS:
            row = outcomes[arm]
            if row.get("human_verified") is not True or not row.get("reviewer_id"):
                raise BenchmarkError(f"{case['case_id']}:{arm}: independently verified label missing")
            if not row.get("response_sha256") or len(row["response_sha256"]) != 64:
                raise BenchmarkError("Actual model response SHA-256 required")
            marks = row.get("ratings")
            if not isinstance(marks, dict) or set(marks) != set(DIMENSIONS):
                raise BenchmarkError("All six fixed rating dimensions required")
            if any(type(v) is not bool for v in marks.values()):
                raise BenchmarkError("Ratings must be adjudicated booleans, not AI-generated confidence")
            counted[arm] += 1
            for k in DIMENSIONS:
                by_arm[arm][k] += int(marks[k])
        raw[case["case_id"]] = "independently_adjudicated"
    return {"case_count": len(cases), "arms": {
        a: {"n": counted[a], "pass_rates": {k: by_arm[a][k]/counted[a] for k in DIMENSIONS}}
        for a in ARMS
    }, "disclaimer": "Human-labelled task accuracy only, not university grades or author voice proof"}

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    a=ap.parse_args()
    try:
        score=score_suite(json.loads(a.results.read_text(encoding="utf-8")))
        output=json.dumps(score,indent=2,ensure_ascii=False)+"\n"
        if a.output:a.output.write_text(output,encoding="utf-8")
        else:print(output)
        return 0
    except (BenchmarkError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"NOT_BLIND_BENCHMARKED: {exc}",file=__import__("sys").stderr)
        return 2
if __name__=="__main__":
    raise SystemExit(main())
