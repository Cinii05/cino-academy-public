"""Cino Academy local source-to-passage audit.

Offline and read-only. Uses optional, already-installed pypdf for PDF text.
Quote/number presence is NOT semantic support or publisher authentication.
No OCR, web requests, model API, third-party uploads or automatic installation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

MAX_BYTES = 32 * 1024 * 1024
MAX_PAGES = 300
MAX_CLAIMS = 100
NUMBERS = re.compile(r"(?<!\w)(?:[£$])?\d[\d,]*(?:\.\d+)?\s*%?(?!\w)")

class SourceAuditError(ValueError):
    pass

def _norm(value: str) -> str:
    s = unicodedata.normalize("NFKC", value or "").replace("\u00ad", "")
    s = s.replace("\u2010", "-").replace("\u2011", "-").replace("\u2013", "-")
    return " ".join(s.split()).casefold()

def numbers(value: str) -> set[str]:
    return {re.sub(r"\s+", "", x).replace(",", "") for x in NUMBERS.findall(value)}

def read_pdf(path: Path) -> tuple[list[str], str]:
    path = Path(path)
    if not path.is_file() or path.suffix.lower() != ".pdf":
        raise SourceAuditError("Source must be an existing local PDF")
    if not (0 < path.stat().st_size <= MAX_BYTES):
        raise SourceAuditError("PDF empty or exceeds 32 MiB local safety limit")
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SourceAuditError("pypdf is not installed; no automatic installation performed") from exc
    data = path.read_bytes()
    try:
        reader = PdfReader(path, strict=False)
        if reader.is_encrypted or len(reader.pages) > MAX_PAGES:
            raise SourceAuditError("Encrypted or over 300 PDF pages")
        pages = [(p.extract_text() or "")[:500000] for p in reader.pages]
    except SourceAuditError:
        raise
    except Exception as exc:
        raise SourceAuditError(f"PDF could not be extracted: {type(exc).__name__}") from exc
    return pages, hashlib.sha256(data).hexdigest()

def audit_claim(claim: dict, pages: list[str]) -> dict:
    if not isinstance(claim, dict) or not isinstance(claim.get("claim_id"), str) or not claim["claim_id"].strip():
        raise SourceAuditError("Each claim requires a nonempty claim_id")
    if not isinstance(claim.get("claim_text"), str) or not claim["claim_text"].strip():
        raise SourceAuditError("Each claim requires claim_text")
    quote = claim.get("quoted_passage") or ""
    if not isinstance(quote, str) or len(quote) > 2000:
        raise SourceAuditError("quoted_passage must be text under 2,000 characters")
    expected = claim.get("pdf_page")
    if expected is not None and (not isinstance(expected, int) or isinstance(expected, bool)
                                 or not (1 <= expected <= len(pages))):
        raise SourceAuditError("pdf_page must be a real 1-based PDF page, not printed pagination")
    matched = [i + 1 for i, p in enumerate(pages) if quote.strip() and _norm(quote) in _norm(p)]
    if not quote.strip():
        status = "NO_QUOTE_TO_CHECK"
    elif not any(p.strip() for p in pages):
        status = "NO_EXTRACTABLE_TEXT"
    elif not matched:
        status = "QUOTE_NOT_LOCATED"
    elif expected is not None and expected not in matched:
        status = "QUOTE_ON_OTHER_PDF_PAGE"
    else:
        status = "EXACT_QUOTE_LOCATED"
    in_claim = numbers(claim["claim_text"])
    in_quote = numbers(quote)
    missing = sorted(in_claim - in_quote) if quote.strip() else []
    return {
        "claim_id": claim["claim_id"], "quote_check": status,
        "actual_pdf_pages": matched, "claimed_pdf_page": expected,
        "numbers_in_claim_not_in_supplied_quote": missing,
        "numeric_check": "REVIEW_REQUIRED" if missing else "NO_MISSING_TOKENS_FOUND",
        "claim_support_state": "UNVERIFIED", # semantic interpretation never automatic
        "source_access": "PARTIAL_TEXT_INSPECTED" if matched else "UNVERIFIED",
        "publication_attribution": "NOT_VERIFIED", # a user-provided local PDF is not authenticated
        "notes": [
            "PDF page index is not necessarily the printed page number.",
            "Text or number presence does not establish causation or support the claim.",
        ],
    }

def audit_document(manifest: dict) -> dict:
    if not isinstance(manifest, dict) or not isinstance(manifest.get("pdf"), str):
        raise SourceAuditError("Manifest needs a local pdf path")
    claims = manifest.get("claims")
    if not isinstance(claims, list) or not (1 <= len(claims) <= MAX_CLAIMS):
        raise SourceAuditError("Manifest needs 1–100 claims")
    ids = [c.get("claim_id") if isinstance(c, dict) else None for c in claims]
    if any(not isinstance(i, str) or not i.strip() for i in ids):
        raise SourceAuditError("Each claim requires a nonempty text claim_id")
    if len(ids) != len(set(ids)):
        raise SourceAuditError("Duplicate claim IDs")
    pages, digest = read_pdf(Path(manifest["pdf"]))
    return {
        "pdf_name": Path(manifest["pdf"]).name,
        "pdf_sha256": digest,
        "pdf_page_count": len(pages),
        "publisher_identity": "NOT_VERIFIED",
        "automation_limits": "Text/quote checks only; no OCR or semantic support inference",
        "results": [audit_claim(c, pages) for c in claims],
    }

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, required=True, help="JSON with local PDF and claims")
    ap.add_argument("--output", type=Path, help="Optional JSON report path")
    args = ap.parse_args()
    try:
        result = audit_document(json.loads(args.manifest.read_text("utf-8")))
        output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output)
        return 0
    except (SourceAuditError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"SOURCE_AUDIT_NOT_VERIFIED: {exc}", file=__import__("sys").stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
