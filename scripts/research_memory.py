"""Private local Cino Academy source-card database.

Python stdlib SQLite only. Explicit database path; no cloud sync, OCR, network,
embedding API, background indexing or auto import of assignments.
Only short user-approved excerpts/notes, never full PDFs or essays.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

ALLOWED_ACCESS = {"FULL_TEXT_INSPECTED", "PARTIAL_TEXT_INSPECTED", "ABSTRACT_ONLY",
                  "METADATA_ONLY", "USER_SUMMARY_ONLY", "UNAVAILABLE"}
ALLOWED_SUPPORT = {"SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED",
                   "CONTRADICTED", "UNVERIFIED"}

def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    if not path.parent.is_dir():
        raise ValueError("Database parent folder must exist; no implicit data directories")
    con = sqlite3.connect(str(path))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript("""
    CREATE TABLE IF NOT EXISTS cards (
      card_id TEXT PRIMARY KEY,
      module_id TEXT NOT NULL,
      source_id TEXT NOT NULL,
      title TEXT NOT NULL,
      locator TEXT NOT NULL,
      excerpt TEXT NOT NULL,
      note TEXT NOT NULL,
      source_path TEXT NOT NULL DEFAULT '',
      source_sha256 TEXT NOT NULL DEFAULT '',
      origin_chain TEXT NOT NULL DEFAULT 'ORIGIN_UNKNOWN',
      access_level TEXT NOT NULL DEFAULT 'UNAVAILABLE',
      provenance TEXT NOT NULL DEFAULT 'USER_SUPPLIED_UNCONFIRMED',
      attribution_verification TEXT NOT NULL DEFAULT 'NOT_VERIFIED',
      support_state TEXT NOT NULL DEFAULT 'UNVERIFIED',
      stale INTEGER NOT NULL DEFAULT 0 CHECK (stale IN (0,1))
    );
    CREATE INDEX IF NOT EXISTS idx_cards_module ON cards(module_id,source_id);
    CREATE INDEX IF NOT EXISTS idx_cards_chain ON cards(origin_chain);
    """)
    return con

def _validate(card: dict) -> dict:
    if not isinstance(card, dict):
        raise ValueError("Expected one JSON card")
    keys = ("card_id", "module_id", "source_id", "title", "locator", "excerpt", "note")
    for name in keys:
        if not isinstance(card.get(name), str) or not card[name].strip():
            raise ValueError(f"Missing required field: {name}")
    for name, n in (("excerpt", 1200), ("note", 2000), ("title", 300), ("locator", 300)):
        if len(card[name]) > n:
            raise ValueError(f"{name} exceeds local privacy/size limit")
    if card.get("support_state", "UNVERIFIED") not in ALLOWED_SUPPORT:
        raise ValueError("Invalid support status")
    if card.get("access_level", "UNAVAILABLE") not in ALLOWED_ACCESS:
        raise ValueError("Invalid access level")
    if card.get("support_state", "UNVERIFIED") != "UNVERIFIED":
        if card.get("attribution_verification") != "VERIFIED":
            raise ValueError("Claim support cannot be accepted without verified source attribution")
        if card.get("provenance") != "INDEPENDENTLY_RETRIEVED":
            raise ValueError("Unverified user passages cannot establish publication claim support")
        if card.get("access_level") in {"UNAVAILABLE", "METADATA_ONLY", "USER_SUMMARY_ONLY"}:
            raise ValueError("Claim support needs inspected real source text")
    path = card.get("source_path", "")
    digest = card.get("source_sha256", "")
    if path and not Path(path).is_file():
        raise ValueError("Local source file not found")
    if digest and (len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest)):
        raise ValueError("Invalid SHA-256")
    if path:
        if Path(path).stat().st_size > 32 * 1024 * 1024:
            raise ValueError("Local source file exceeds 32 MiB safe hashing limit")
        true_digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        if digest and digest != true_digest:
            raise ValueError("Provided source hash does not match local file")
        digest = true_digest
    return {
        "card_id": card["card_id"], "module_id": card["module_id"],
        "source_id": card["source_id"], "title": card["title"],
        "locator": card["locator"], "excerpt": card["excerpt"], "note": card["note"],
        "source_path": path, "source_sha256": digest,
        "origin_chain": card.get("origin_chain", "ORIGIN_UNKNOWN"),
        "access_level": card.get("access_level", "UNAVAILABLE"),
        "provenance": card.get("provenance", "USER_SUPPLIED_UNCONFIRMED"),
        "attribution_verification": card.get("attribution_verification", "NOT_VERIFIED"),
        "support_state": card.get("support_state", "UNVERIFIED"),
        "stale": 0,
    }

def add_card(con: sqlite3.Connection, card: dict, *, replace: bool = False) -> dict:
    c = _validate(card)
    old = con.execute("SELECT card_id FROM cards WHERE card_id=?", (c["card_id"],)).fetchone()
    if old and not replace:
        raise ValueError("Card already exists; use explicit replace flag")
    if old:
        con.execute("DELETE FROM cards WHERE card_id=?", (c["card_id"],))
    names = tuple(c)
    con.execute(f"INSERT INTO cards ({','.join(names)}) VALUES ({','.join('?' for _ in names)})",
                tuple(c.values()))
    con.commit()
    return {"card_id": c["card_id"], "stored": True, "source_sha256": c["source_sha256"]}

def search_cards(con: sqlite3.Connection, query: str, module_id: str, limit: int = 20) -> list[dict]:
    if not isinstance(module_id, str) or not module_id.strip():
        raise ValueError("Search requires explicit module_id to prevent accidental cross-module leaks")
    if not query.strip() or not 1 <= limit <= 100:
        raise ValueError("A nonempty query and limit of 1–100 are required")
    rows = con.execute("""SELECT card_id,module_id,source_id,title,locator,excerpt,note,
                                 origin_chain,source_sha256,access_level,provenance,
                                 attribution_verification,support_state,stale
                          FROM cards WHERE module_id=? AND
                          (instr(lower(title),lower(?))>0 OR
                           instr(lower(note),lower(?))>0 OR
                           instr(lower(excerpt),lower(?))>0 OR
                           instr(lower(source_id),lower(?))>0)
                          ORDER BY card_id LIMIT ?""",
                       (module_id, query, query, query, query, limit)).fetchall()
    return [dict(r) for r in rows]

def refresh_stale(con: sqlite3.Connection, *, module_id: str) -> list[str]:
    if not module_id:
        raise ValueError("module_id required")
    rows = con.execute("SELECT card_id,source_path,source_sha256 FROM cards WHERE module_id=?",
                       (module_id,)).fetchall()
    changed = []
    for row in rows:
        if not row["source_path"]:
            continue
        path = Path(row["source_path"])
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
        if digest != row["source_sha256"]:
            con.execute("UPDATE cards SET stale=1 WHERE card_id=?", (row["card_id"],))
            changed.append(row["card_id"])
    con.commit()
    return changed

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", type=Path, required=True)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", type=Path, help="JSON card from a specifically approved excerpt")
    group.add_argument("--search", type=str)
    group.add_argument("--check-stale", action="store_true")
    ap.add_argument("--module-id", help="Required for searching/checking file staleness")
    ap.add_argument("--replace", action="store_true")
    args = ap.parse_args()
    try:
        with connect(args.db) as con:
            if args.add:
                answer = add_card(con, json.loads(args.add.read_text("utf-8")), replace=args.replace)
            elif args.search is not None:
                answer = search_cards(con, args.search, args.module_id or "")
            else:
                answer = {"stale_card_ids": refresh_stale(con, module_id=args.module_id or "")}
        print(json.dumps(answer, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, sqlite3.Error, json.JSONDecodeError) as exc:
        print(f"RESEARCH_MEMORY_ERROR: {exc}", file=__import__("sys").stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
