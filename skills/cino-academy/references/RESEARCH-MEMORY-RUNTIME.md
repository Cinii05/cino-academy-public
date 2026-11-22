# Private, searchable research memory (v1.4 candidate)

The Academy repository contains `scripts/research_memory.py`, a **local SQLite reference-card notebook**. It does not create a cloud database, connect Zotero automatically, sync to Drive, embed coursework in the plugin, or scan folders by default.

## Using the tool with consent
Run `py -3 scripts/research_memory.py --db C:\path\private-academy.sqlite3 --add approved-card.json` or `--search "sustainability" --module-id MODULE123`. The database parent folder must exist. **Never store the SQLite file in GitHub, a plugin ZIP or a shared folder.** Only excerpts and notes deliberately supplied for one source card are stored; no full PDF or personal essay is copied.

A card has a stable `card_id`, `module_id`, `source_id`, `title`, `locator` (page/section), short `excerpt`, student's distinct `note`, `origin_chain`, access/provenance/support states and optional real `source_path`. If a source file exists, record its actual SHA-256. A changed/missing file flags all matching cards as stale using `--check-stale --module-id MODULE123` and re-verification is necessary before using them.

Default `support_state=UNVERIFIED`; a user-provided excerpt is not an authenticated publication. Never let search results upgrade evidence automatically. Search is restricted to a specified module by default, preventing cross-assignment facts or permission leakage. Duplicated IDs require explicit `--replace`, preventing silent accidental note loss.

## Literature workflow
1. Scout finds real source candidates and checks metadata/versions.
2. Auditor verifies actual passages and source identity with available tools.
3. Student chooses bounded excerpts and writes own notes in local cards.
4. Synthesiser retrieves by `module_id`, compares source methods and origin chains, and preserves conflicting evidence.
5. If an original PDF changes, stale cards must be rechecked, not silently trusted.

Optional **read-only** Zotero connection is future integration, not installed or required for this release. Do not install new dependencies or share a university library without explicit permission.
