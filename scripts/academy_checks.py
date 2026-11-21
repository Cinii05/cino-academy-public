"""Offline, deterministic Academy QA checks; no network calls or personal data.

These are pre-release fixtures and optional local QA helpers, NOT a semantic
fact-checker, a citation database, a mark predictor, or a ChatGPT-hosted service.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

SUPPORT = frozenset({"SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED",
                     "CONTRADICTED", "UNVERIFIED"})
ACCESS = frozenset({"FULL_TEXT_INSPECTED", "PARTIAL_TEXT_INSPECTED", "ABSTRACT_ONLY",
                    "METADATA_ONLY", "USER_SUMMARY_ONLY", "UNAVAILABLE"})
ALLOWED_SCOPE = frozenset({"UNKNOWN", "ALL_GENAI_PROHIBITED",
                          "LIMITED_VERIFIED", "OTHER_VERIFIED"})
ROUTES = frozenset({"QUICK", "RESEARCH", "ARGUMENT", "REVIEW", "FULL"})
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assess_policy(card: dict[str, Any], *, action: str) -> tuple[bool, list[str]]:
    """Conservative policy gate for a *single* assignment; cannot certify source auth."""
    problems: list[str] = []
    if not card.get("assignment_id") or not card.get("task"):
        problems.append("missing assignment identity or task")
    if card.get("request_mode") not in ROUTES:
        problems.append("invalid request mode")
    policy = card.get("genai_policy") or {}
    scope = policy.get("scope", "UNKNOWN")
    if scope not in ALLOWED_SCOPE:
        problems.append("invalid policy scope")
    source = policy.get("source", "UNVERIFIED")
    if action == "GENERIC_STUDY_GUIDANCE":
        return not problems, problems
    if source != "INSTITUTIONAL_VERIFIED":
        problems.append("policy not institutionally verified")
    if scope in {"UNKNOWN", "ALL_GENAI_PROHIBITED"}:
        problems.append("assessed GenAI assistance not authorised")
    if action not in policy.get("permitted_actions", []):
        problems.append("requested assessed action not explicitly permitted")
    if action in policy.get("prohibited_actions", []):
        problems.append("action expressly prohibited")
    return not problems, problems


def check_assignment_separation(first: dict[str, Any], second: dict[str, Any]) -> bool:
    """Must carry independently identified policy records per assignment."""
    a, b = first.get("assignment_id"), second.get("assignment_id")
    return bool(a and b and a != b and first.get("genai_policy") is not second.get("genai_policy"))


def normalise_doi(value: str) -> str:
    s = (value or "").strip().lower()
    s = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", s)
    return s


def _normalise_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).casefold()).strip()


def metadata_comparison(candidate: dict[str, Any], registry_record: dict[str, Any]) -> dict[str, Any]:
    """Check already supplied records; does not query any registry itself."""
    mismatches = []
    for key in ("title", "year"):
        if not candidate.get(key) or not registry_record.get(key):
            mismatches.append(f"{key}:missing")
        elif _normalise_text(candidate[key]) != _normalise_text(registry_record[key]):
            mismatches.append(f"{key}:mismatch")
    a, b = candidate.get("first_author"), registry_record.get("first_author")
    if not a or not b:
        mismatches.append("first_author:missing")
    elif _normalise_text(a).split(" ")[-1] != _normalise_text(b).split(" ")[-1]:
        mismatches.append("first_author:mismatch")
    if normalise_doi(candidate.get("doi", "")) != normalise_doi(registry_record.get("doi", "")):
        mismatches.append("doi:mismatch")
    return {"metadata_match": not mismatches, "mismatches": mismatches,
            "claim_support": "NOT_CHECKED", "mode": "OFFLINE_SUPPLIED_RECORD_COMPARISON"}


def evidence_record_errors(record: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if record.get("support_state") not in SUPPORT:
        errs.append("illegal support_state")
    if record.get("access_level") not in ACCESS:
        errs.append("illegal access_level")
    for k in ("claim_id", "claim_text", "source_id", "independence_chain"):
        if not record.get(k):
            errs.append(f"missing {k}")
    supported = record.get("support_state") != "UNVERIFIED"
    if supported:
        if record.get("access_level") in {"METADATA_ONLY", "USER_SUMMARY_ONLY", "UNAVAILABLE"}:
            errs.append("metadata or summary cannot prove content")
        if record.get("attribution_verification") != "VERIFIED":
            errs.append("unverified attribution cannot prove content")
        if record.get("provenance") != "INDEPENDENTLY_RETRIEVED":
            errs.append("unverified user source cannot prove publication claim")
        if not record.get("passage_locator"):
            errs.append("missing inspected passage locator")
    if record.get("access_level") == "FULL_TEXT_INSPECTED" and record.get("provenance") == "USER_SUPPLIED_UNCONFIRMED":
        errs.append("unconfirmed extract is not independently inspected full text")
    return errs


def count_independent_origins(records: list[dict[str, Any]]) -> int:
    ids = [r.get("independence_chain") for r in records if r.get("independence_chain")]
    return len({x for x in ids if x != "ORIGIN_UNKNOWN"})


_NUMBER = re.compile(r"(?<!\w)\d[\d,]*(?:\.\d+)?\s*%?(?!\w)")
_CITATION = re.compile(r"\([A-Z][A-Za-z '-]+,\s*\d{4}[a-z]?(?:,\s*p{1,2}\.\s*\d+)?\)")
_QUOTE = re.compile(r"(?<!\w)[“\"][^”\"]+[”\"]")
_QUALIFIER = re.compile(r"\b(?:may|might|could|suggests?|appears?|possibly|likely|associated with|not|never|no evidence)\b", re.I)
_CAUSAL = re.compile(r"\b(?:causes?|caused|proves?|proven|always|never|guarantee[sd]?)\b", re.I)


def style_lock_differences(before: str, after: str) -> list[str]:
    """Conservative textual lock: catches common meaning drift, NOT deep semantics."""
    difference = []
    for label, pat in (("number", _NUMBER), ("citation", _CITATION),
                       ("quotation", _QUOTE), ("qualifier", _QUALIFIER),
                       ("causal_strength", _CAUSAL)):
        x = [v.casefold() for v in pat.findall(before)]
        y = [v.casefold() for v in pat.findall(after)]
        if x != y:
            difference.append(label)
    return difference


def can_learn_voice(sample: dict[str, Any]) -> tuple[bool, str]:
    if not sample.get("consented"):
        return False, "no affirmative consent"
    if sample.get("authorship") != "SELF_AUTHORED_VERIFIED":
        return False, "unverified self-authorship"
    if not sample.get("genre"):
        return False, "unknown genre"
    if not sample.get("locator"):
        return False, "no provenance"
    return True, "eligible for a proposed trait (not automatic approval)"


def approve_human_edit(candidate: dict[str, Any]) -> tuple[bool, str]:
    if not candidate.get("author_accepted"):
        return False, "not accepted"
    if not candidate.get("user_edit") or not candidate.get("genre") or not candidate.get("source_locator"):
        return False, "missing actual user edit or provenance"
    if candidate.get("train_from_ai_draft"):
        return False, "AI text cannot be a self-authored sample"
    return True, "allowed only as a proposed genre-specific preference"


def check_revision_receipt(receipt: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if receipt.get("finding_status") not in {"OPEN", "RESOLVED"}:
        errs.append("invalid finding state")
    if not receipt.get("finding_id") or not receipt.get("location") or not receipt.get("observed_problem"):
        errs.append("missing actionable finding")
    for label in ("draft_sha256",):
        if not SHA256_RE.fullmatch(receipt.get(label) or ""):
            errs.append(f"invalid {label}")
    if receipt.get("finding_status") == "RESOLVED":
        revision = receipt.get("revision_sha256") or ""
        if not SHA256_RE.fullmatch(revision) or revision == receipt.get("draft_sha256"):
            errs.append("resolved without a different verified revision")
        if receipt.get("independent_reviewer_result") != "ACCEPTED":
            errs.append("no independent acceptance")
        if not receipt.get("reviewer_role") or receipt.get("reviewer_role") == receipt.get("writer_role"):
            errs.append("self-reviewed closure")
    return errs


def check_word_allocation(total: int | None, allocations: dict[str, int],
                          *, exact: bool) -> list[str]:
    if total is None:
        return ["word limit unverified"]
    if total < 0 or any(not isinstance(v, int) or v < 0 for v in allocations.values()):
        return ["invalid word allocation"]
    used = sum(allocations.values())
    if used > total:
        return ["allocations exceed the verified word limit"]
    if exact and used != total:
        return ["exact allocations do not sum to the verified total"]
    return []


def check_package_privacy(path_names: list[str], raw_content: list[bytes]) -> list[str]:
    errors = []
    forbidden_name_parts = ("voiceprofile.json", "personal-coursework", ".env",
                            "student-record", "private-marking", "client-data")
    for name in path_names:
        if any(x in name.lower() for x in forbidden_name_parts):
            errors.append(f"private file name: {name}")
    for raw in raw_content:
        content = raw.decode("utf-8", errors="replace")
        # This is a limited static guard; not a DLP or antivirus product.
        if re.search(r"(?i)\b(sk-[a-z0-9]{20,}|ghp_[a-z0-9]{30,})\b", content):
            errors.append("probable credential")
    return errors
