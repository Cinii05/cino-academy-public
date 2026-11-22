"""Compare an Academy review with independently observed marker findings.

No grade prediction, no personal-data export and no invented ground truth.
The assessor's verified comments must be independently labelled before review.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

CATEGORIES = {"brief_compliance", "evidence", "case_application", "critical_evaluation",
              "reflection", "method", "structure", "referencing"}
SEVERITIES = {"material", "minor"}

def _labels(findings: list[dict], name: str) -> dict[str, str]:
    if not isinstance(findings, list):
        raise ValueError(f"{name} must be a list")
    out = {}
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError(f"{name} finding must be an object")
        label, severity = finding.get("criterion"), finding.get("severity")
        if label not in CATEGORIES or severity not in SEVERITIES:
            raise ValueError(f"Invalid {name} criterion or severity")
        if label in out:
            raise ValueError(f"Duplicate {name} finding for criterion {label}; consolidate evidence first")
        out[label] = severity
    return out

def compare_sample(sample: dict) -> dict:
    if not sample.get("sample_id") or sample.get("human_feedback_verified") is not True:
        raise ValueError("A sample ID and independently VERIFIED marker feedback are required")
    if not isinstance(sample.get("human_feedback_locator"), str) or not sample["human_feedback_locator"].strip():
        raise ValueError("Verified marker feedback needs an auditable local/document locator")
    truth = _labels(sample.get("human_findings"), "human")
    candidate = _labels(sample.get("academy_findings"), "academy")
    correct = sorted(set(truth) & set(candidate))
    missed = sorted(set(truth) - set(candidate))
    invented = sorted(set(candidate) - set(truth))
    severity_mismatch = [c for c in correct if truth[c] != candidate[c]]
    return {
        "sample_id": sample["sample_id"], "true_positives": len(correct),
        "false_positives": len(invented), "false_negatives": len(missed),
        "missed_criteria": missed, "unmatched_academy_flags": invented,
        "severity_mismatches": severity_mismatch,
        "material_misses": [x for x in missed if truth[x] == "material"],
        "note": "Category agreement only; cannot establish grade validity or correctness of all prose",
    }

def calibrate(data: dict) -> dict:
    cases = data.get("samples")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Require at least one independently labelled test sample")
    ids = [c.get("sample_id") if isinstance(c,dict) else None for c in cases]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate sample IDs")
    individual = [compare_sample(c) for c in cases]
    tp = sum(x["true_positives"] for x in individual)
    fp = sum(x["false_positives"] for x in individual)
    fn = sum(x["false_negatives"] for x in individual)
    precision = tp/(tp+fp) if (tp+fp) else None
    recall = tp/(tp+fn) if (tp+fn) else None
    return {
        "sample_count": len(cases), "true_positives": tp, "false_positives": fp,
        "false_negatives": fn, "precision": precision, "recall": recall,
        "material_misses": [f"{x['sample_id']}:{y}" for x in individual for y in x["material_misses"]],
        "per_sample": individual,
        "interpretation": "Diagnostic agreement with labelled reviewer feedback; not predicted marks",
    }

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()
    try:
        res=calibrate(json.loads(a.input.read_text("utf-8")))
        content=json.dumps(res,indent=2,ensure_ascii=False)+"\n"
        if a.output:a.output.write_text(content,encoding="utf-8")
        else:print(content)
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"MARKER_CALIBRATION_NOT_VERIFIED: {exc}", file=__import__("sys").stderr)
        return 2
if __name__ == "__main__":
    raise SystemExit(main())
