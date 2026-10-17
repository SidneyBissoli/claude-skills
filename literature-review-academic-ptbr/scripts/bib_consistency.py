"""Bibliographic consistency — hard gate of the literature-review-academic-ptbr skill.

Verifies bidirectional correspondence between in-text citations
(ABNT autor-data style) and entries in a BibTeX reference list.
Designed for the A3 vector of the Teste 03 ground truth: detect
references that are cited but never registered in the reference
list (orphan citations — including the canonical Sub-30.1
"cadeia probatória interna contaminada" subtype) as well as
entries that sit in the .bib without any in-text citation.

Usage
-----
Run the regression battery (Suite B) against fixtures derived from
Teste 03::

    python bib_consistency.py --cases tests/teste03_bib_consistency_cases.json --output report.md
    python bib_consistency.py --cases tests/teste03_bib_consistency_cases.json --output report.json

Verify a specific text/bib pair::

    python bib_consistency.py --text capitulo.md --bib referencias.bib --output report.md
    python bib_consistency.py --text capitulo.docx --bib referencias.bib

Report formats
--------------
The output suffix selects the renderer (``.md`` default, ``.json``
optional). When ``--output`` is omitted, Markdown is written to stdout.

Exit code
---------
Non-zero if any element diverges from its expected state when an
``expected_states`` map is supplied (regression battery mode).

Four return states (per element)
--------------------------------
``OK``                  Citation in the text has a matching entry in
                        the .bib AND vice versa.
``ORPHAN_CITATION``     Citation appears in the text but no entry in
                        the .bib carries a matching surname+year. This
                        is the canonical Sub-30.1 signature when the
                        orphan citation appears inside a paraphrase
                        attributed to a real review (cadeia probatória
                        interna contaminada).
``UNCITED_REFERENCE``   Entry in the .bib is not referenced by any
                        in-text citation.
``APUD_ONLY``           Citation appears exclusively via apud (e.g.
                        ``(VELHO apud TAVARES; CAMURÇA, 2004)``) with
                        no primary entry in the .bib. ABNT NBR 10520
                        requires both primary and secondary works in
                        the reference list when an apud expression is
                        used; ``APUD_ONLY`` flags the violation.

Granularity decision (APUD_ONLY vs ORPHAN_CITATION)
---------------------------------------------------
Plan canônico §4.2.2 case 4 leaves the granularity open: APUD_ONLY
may either be a category distinct from ORPHAN_CITATION or be
subsumed in ORPHAN_CITATION. This script keeps APUD_ONLY as a
**distinct state**. Reasons:

* the corrective action is different — orphans require active
  existence verification (potential fabrication signal); apud
  orphans require reincorporation of the primary work to the list
  (structural Regra 2 violation, not necessarily a fabrication);
* §(xii) of references/_phase2-handoff.md addresses the apud vector
  specifically; Sub-30.4 of the changelog canonised the rule of
  active verification of canonical anchor concepts mobilised via
  apud — distinct in name from ORPHAN_CITATION;
* downstream consumers (matrices, manual ABNT auditing) benefit
  from the three-way distinction without paying a complexity cost.

bibtexparser version pinning
----------------------------
``bibtexparser >= 1.4, < 2`` (currently 1.4.4). The 2.x line was
still in alpha/beta at 2026-04 with breaking API changes between
point releases (notable rewrite around the writer module and the
Library/Block/Failed-Block model). The 1.4 series is stable and
battle-tested for the surface area used here (entry parsing, basic
field access). If 2.x stabilises in the future, revisit by editing
``scripts/requirements.in`` and recompiling the lockfile.

Citation parsing
----------------
Two regex patterns cover the ABNT autor-data forms encountered in
practice:

* ``RE_PAREN_CITATION`` matches ``(SURNAMES, YYYY)`` with optional
  letter suffix and detects ``apud`` inside the parens;
* ``RE_AUTHOR_YEAR`` matches ``Surname[s] (YYYY)`` immediately
  preceding a four-digit parenthesised year.

The parser is deliberately conservative on Brazilian conventions
(``e``, ``&``, ``et al.``, ``apud``). It does not attempt to handle
multi-reference parentheticals like ``(SOUSA, 2010; LIMA, 2015)``
correctly — at most one citation is captured per parenthesis. This
is a known limit; expand if the regression battery ever requires it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import bibtexparser

# --- States ----------------------------------------------------------

STATE_OK = "OK"
STATE_ORPHAN = "ORPHAN_CITATION"
STATE_UNCITED = "UNCITED_REFERENCE"
STATE_APUD_ONLY = "APUD_ONLY"

# --- Regex -----------------------------------------------------------

# Parenthesised citation: (SURNAMES[; SURNAMES][ apud SURNAMES; SURNAMES], YYYY[a])
RE_PAREN_CITATION = re.compile(
    r"\(([^()]+?),\s*(\d{4})[a-z]?\)",
    re.UNICODE,
)

# Author-year form: Surname[s] (YYYY)
# Allows up to ~50 chars of name expression (multiple surnames + connectors)
# preceding the parenthesised year, anchored on a leading capitalised letter.
# Connectors (e, &, et al., de, da, do, dos, das) are matched without
# a trailing \b because "et al." ends in a period — a non-word
# character — and \b would silently fail there.
RE_AUTHOR_YEAR = re.compile(
    r"((?:[A-ZÁÉÍÓÚÀÂÊÔÃÕÇÑ][\wÀ-ɏ.\-']+(?:\s+(?:et\s+al\.?|&|e|de|da|do|dos|das))*\s*){1,4})"
    r"\((\d{4})[a-z]?\)",
    re.UNICODE,
)

# Detector for apud inside a parenthesised citation content.
RE_APUD = re.compile(r"\bapud\b", re.IGNORECASE)


# --- Data classes ----------------------------------------------------


@dataclass
class Citation:
    raw: str
    surnames: list[str]
    year: int
    is_apud: bool
    primary_surname: str | None
    secondary_surnames: list[str]
    citation_key: str
    char_offset: int
    keys_for_match: set[str] = field(default_factory=set)


@dataclass
class BibEntry:
    entry_id: str
    authors: list[str]
    surnames: list[str]
    year: str
    fields: dict[str, str]
    keys_for_match: set[str] = field(default_factory=set)


@dataclass
class ElementResult:
    key: str
    state: str
    direction: str
    expected_state: str | None = None
    pass_: bool | None = None
    notes: str = ""


# --- Helpers ---------------------------------------------------------


def _normalise(text: str | None) -> str:
    """Lowercase ASCII fold; collapse whitespace."""
    if not text:
        return ""
    folded = unicodedata.normalize("NFKD", text)
    folded = folded.encode("ascii", "ignore").decode()
    return " ".join(folded.split()).lower().strip()


def _surname_from_bib_author(author_field: str) -> str:
    """Return surname token from a BibTeX-formatted author string.

    Handles "Surname, Given Names" and "Given Names Surname" forms.
    """
    s = author_field.strip().strip("{}")
    if not s:
        return ""
    if "," in s:
        return s.split(",", 1)[0].strip()
    parts = s.split()
    return parts[-1] if parts else ""


def _split_bib_authors(author_field: str) -> list[str]:
    if not author_field:
        return []
    return [a.strip() for a in re.split(r"\s+and\s+", author_field) if a.strip()]


def _bib_entry_keys(entry: BibEntry) -> set[str]:
    """Compute every plausible canonical key for a bib entry.

    For 1 author: {surname_year}.
    For 2 authors: {first_year, first_second_year, second_year}.
    For 3+ authors: {first_year} only — et al. style.
    """
    keys: set[str] = set()
    surnames = [_normalise(s) for s in entry.surnames if s]
    year = entry.year.strip()
    if not year or not surnames:
        return keys
    keys.add(f"{surnames[0]}_{year}")
    if len(surnames) == 2:
        keys.add(f"{surnames[0]}_{surnames[1]}_{year}")
        keys.add(f"{surnames[1]}_{year}")
    return keys


def _citation_keys(citation: Citation) -> set[str]:
    """Compute every plausible canonical key for a parsed citation."""
    if citation.is_apud:
        return set()
    surnames = [_normalise(s) for s in citation.surnames if s]
    year = str(citation.year)
    keys: set[str] = set()
    if not surnames:
        return keys
    keys.add(f"{surnames[0]}_{year}")
    if len(surnames) == 2:
        keys.add(f"{surnames[0]}_{surnames[1]}_{year}")
    return keys


def _canonical_key(citation: Citation) -> str:
    """Pick a single canonical key per citation for reporting."""
    if citation.is_apud:
        primary = _normalise(citation.primary_surname or "")
        return f"{primary}:apud:{citation.year}"
    surnames = [_normalise(s) for s in citation.surnames if s]
    year = str(citation.year)
    if len(surnames) >= 2:
        return f"{surnames[0]}_{surnames[1]}_{year}"
    if surnames:
        return f"{surnames[0]}_{year}"
    return f"unknown_{year}"


def _bib_entry_canonical_key(entry: BibEntry) -> str:
    surnames = [_normalise(s) for s in entry.surnames if s]
    year = entry.year.strip()
    if len(surnames) == 2:
        return f"{surnames[0]}_{surnames[1]}_{year}"
    if surnames:
        return f"{surnames[0]}_{year}"
    return f"{entry.entry_id}_{year}"


# --- Parsing ---------------------------------------------------------


def _split_surnames_chunk(chunk: str) -> list[str]:
    """Split a citation chunk into surname tokens.

    Handles separators: ``;``, `` e ``, ``&``, `` and ``. Strips
    trailing ``et al.`` (period optional; no trailing ``\b`` because
    the period is a non-word character and a word boundary after it
    silently fails).
    """
    chunk = chunk.strip()
    chunk = re.sub(r"\bet\s+al\.?", "", chunk, flags=re.IGNORECASE).strip()
    parts = re.split(r"\s*;\s*|\s+e\s+|\s*&\s*|\s+and\s+", chunk)
    cleaned: list[str] = []
    for p in parts:
        token = p.strip(" .,;")
        # Drop bare punctuation residues left by "et al." stripping.
        if token and any(ch.isalpha() for ch in token):
            cleaned.append(token)
    return cleaned


def parse_citations(text: str) -> list[Citation]:
    citations: list[Citation] = []

    # Pass 1: parenthesised "(... , YYYY)" — including apud forms.
    for m in RE_PAREN_CITATION.finditer(text):
        content = m.group(1).strip()
        year = int(m.group(2))
        if RE_APUD.search(content):
            split = re.split(r"\s+apud\s+", content, maxsplit=1, flags=re.IGNORECASE)
            primary_chunk = split[0]
            secondary_chunk = split[1] if len(split) > 1 else ""
            primary_surnames = _split_surnames_chunk(primary_chunk)
            secondary_surnames = _split_surnames_chunk(secondary_chunk)
            citation = Citation(
                raw=m.group(0),
                surnames=primary_surnames,
                year=year,
                is_apud=True,
                primary_surname=primary_surnames[0] if primary_surnames else None,
                secondary_surnames=secondary_surnames,
                citation_key="",
                char_offset=m.start(),
            )
        else:
            surnames = _split_surnames_chunk(content)
            citation = Citation(
                raw=m.group(0),
                surnames=surnames,
                year=year,
                is_apud=False,
                primary_surname=None,
                secondary_surnames=[],
                citation_key="",
                char_offset=m.start(),
            )
        citation.citation_key = _canonical_key(citation)
        citation.keys_for_match = _citation_keys(citation)
        citations.append(citation)

    # Pass 2: "Surname[s] (YYYY)" form.
    for m in RE_AUTHOR_YEAR.finditer(text):
        chunk = m.group(1).strip()
        year = int(m.group(2))
        # Skip if the same (or overlapping) match was already captured
        # by the parenthesised pass.
        if any(
            c.char_offset <= m.start() <= c.char_offset + len(c.raw)
            for c in citations
        ):
            continue
        surnames = _split_surnames_chunk(chunk)
        # Defensive: the regex can occasionally start at a stop-word
        # within a longer phrase. Drop empty / lowercase-only.
        surnames = [s for s in surnames if s and s[0].isupper()]
        if not surnames:
            continue
        citation = Citation(
            raw=m.group(0),
            surnames=surnames,
            year=year,
            is_apud=False,
            primary_surname=None,
            secondary_surnames=[],
            citation_key="",
            char_offset=m.start(),
        )
        citation.citation_key = _canonical_key(citation)
        citation.keys_for_match = _citation_keys(citation)
        citations.append(citation)

    return citations


def parse_bib(path: Path) -> list[BibEntry]:
    with path.open("r", encoding="utf-8") as fp:
        bib_db = bibtexparser.load(fp)
    entries: list[BibEntry] = []
    for raw in bib_db.entries:
        author_field = raw.get("author", "")
        authors = _split_bib_authors(author_field)
        surnames = [_surname_from_bib_author(a) for a in authors]
        be = BibEntry(
            entry_id=raw.get("ID", ""),
            authors=authors,
            surnames=surnames,
            year=raw.get("year", "").strip(),
            fields=dict(raw),
        )
        be.keys_for_match = _bib_entry_keys(be)
        entries.append(be)
    return entries


# --- Text reading ----------------------------------------------------


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".docx":
        from docx import Document
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"Unsupported text format: {suffix}")


# --- Verification core ----------------------------------------------


def verify_pair(
    text: str,
    bib_entries: list[BibEntry],
    expected_states: dict[str, str] | None = None,
) -> list[ElementResult]:
    citations = parse_citations(text)
    expected_states = expected_states or {}

    # Fold citations by canonical key (multiple text occurrences
    # collapse into one element).
    citations_by_key: dict[str, Citation] = {}
    for cit in citations:
        if cit.citation_key not in citations_by_key:
            citations_by_key[cit.citation_key] = cit

    # Match bib entries against citations.
    matched_bib_keys: set[str] = set()
    matched_citation_keys: set[str] = set()
    for entry in bib_entries:
        for cit_key, cit in citations_by_key.items():
            if cit.is_apud:
                continue
            if entry.keys_for_match & cit.keys_for_match:
                matched_bib_keys.add(_bib_entry_canonical_key(entry))
                matched_citation_keys.add(cit_key)
                break

    # Apud handling: APUD_ONLY when primary surname has no bib entry.
    bib_surnames = {
        _normalise(s)
        for entry in bib_entries
        for s in entry.surnames
        if s
    }
    apud_results: list[tuple[str, str]] = []
    for cit_key, cit in citations_by_key.items():
        if not cit.is_apud:
            continue
        primary = _normalise(cit.primary_surname or "")
        if primary and primary in bib_surnames:
            apud_results.append((cit_key, STATE_OK))
        else:
            apud_results.append((cit_key, STATE_APUD_ONLY))

    results: list[ElementResult] = []

    # Bib entries: OK if matched, UNCITED otherwise.
    for entry in bib_entries:
        canon = _bib_entry_canonical_key(entry)
        state = STATE_OK if canon in matched_bib_keys else STATE_UNCITED
        notes = ""
        if state == STATE_OK:
            notes = f"matched citation in text (entry id: {entry.entry_id})"
        else:
            notes = f"bib entry id={entry.entry_id} not referenced by any in-text citation"
        results.append(_finalise(canon, state, "bib", expected_states, notes))

    # Citations: ORPHAN if not matched; OK otherwise (already counted).
    for cit_key, cit in citations_by_key.items():
        if cit.is_apud:
            continue
        canon = cit_key
        # Avoid duplicating bib entries already reported.
        if any(r.key == canon for r in results):
            continue
        state = STATE_OK if canon in matched_citation_keys else STATE_ORPHAN
        notes = (
            f"citation `{cit.raw}` at offset {cit.char_offset}"
            if state == STATE_ORPHAN
            else f"citation matched bib entry"
        )
        results.append(_finalise(canon, state, "text", expected_states, notes))

    # Apud results.
    for cit_key, state in apud_results:
        cit = citations_by_key[cit_key]
        notes = (
            f"apud citation `{cit.raw}`; primary surname `{cit.primary_surname}` "
            f"{'present' if state == STATE_OK else 'absent'} in bib"
        )
        results.append(_finalise(cit_key, state, "apud", expected_states, notes))

    # Sort results: bib-OK first, then orphans, apud, uncited.
    order = {STATE_OK: 0, STATE_ORPHAN: 1, STATE_APUD_ONLY: 2, STATE_UNCITED: 3}
    results.sort(key=lambda r: (order.get(r.state, 9), r.key))
    return results


def _finalise(
    key: str,
    state: str,
    direction: str,
    expected: dict[str, str],
    notes: str,
) -> ElementResult:
    expected_state = expected.get(key)
    pass_ = (state == expected_state) if expected_state else None
    return ElementResult(
        key=key, state=state, direction=direction,
        expected_state=expected_state, pass_=pass_, notes=notes,
    )


# --- Reporting ------------------------------------------------------


def render_md(
    cases: list[tuple[dict, list[ElementResult]]],
) -> str:
    lines = ["# Bib consistency report", ""]
    for case_meta, results in cases:
        label = case_meta.get("label", case_meta.get("id", "case"))
        lines.append(f"## Case {case_meta.get('id', '?')} — {label}")
        lines.append("")
        lines.append(f"- Text: `{case_meta.get('text_file', '')}`")
        lines.append(f"- Bib: `{case_meta.get('bib_file', '')}`")
        lines.append(f"- Total elements: {len(results)}")
        lines.append("")
        lines.append("| Key | Direction | State | Expected | Pass | Notes |")
        lines.append("|---|---|---|---|---|---|")
        for r in results:
            expected_str = r.expected_state or "—"
            if r.pass_ is None:
                pass_mark = "—"
            else:
                pass_mark = "✓" if r.pass_ else "✗"
            notes_escaped = r.notes.replace("|", "\\|")
            lines.append(
                f"| `{r.key}` | {r.direction} | `{r.state}` | "
                f"`{expected_str}` | {pass_mark} | {notes_escaped} |"
            )
        lines.append("")
    return "\n".join(lines)


def render_json(
    cases: list[tuple[dict, list[ElementResult]]],
) -> str:
    payload = []
    for case_meta, results in cases:
        payload.append({
            "case": case_meta,
            "results": [asdict(r) for r in results],
        })
    return json.dumps(payload, indent=2, ensure_ascii=False)


# --- CLI ------------------------------------------------------------


def _run_suite(suite_path: Path) -> tuple[int, list[tuple[dict, list[ElementResult]]]]:
    with suite_path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    fixtures_root = data.get("fixtures_root", ".")
    base_dir = suite_path.parent / fixtures_root

    cases_data = data.get("cases") or []
    out: list[tuple[dict, list[ElementResult]]] = []
    failures = 0
    for case in cases_data:
        text_path = base_dir / case["text_file"]
        bib_path = base_dir / case["bib_file"]
        text = read_text(text_path)
        bib_entries = parse_bib(bib_path)
        results = verify_pair(
            text=text,
            bib_entries=bib_entries,
            expected_states=case.get("expected_states") or {},
        )
        failures += sum(1 for r in results if r.pass_ is False)
        # Report unexpected elements (in observed but not in expected) as failures.
        if case.get("expected_states"):
            observed_keys = {r.key for r in results}
            for k in observed_keys - set(case["expected_states"].keys()):
                # Flag as ✗ via a synthetic note — but we already added them
                # to results; mark them.
                for r in results:
                    if r.key == k and r.expected_state is None:
                        r.notes = f"{r.notes}; UNEXPECTED in expected_states"
                        r.pass_ = False
                        failures += 1
        out.append((case, results))
    return failures, out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Hard gate: bidirectional citation/bib consistency.",
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--cases", type=Path,
                     help="JSON fixture with cases (regression battery).")
    src.add_argument("--text", type=Path,
                     help="Text source file (.md, .txt, or .docx).")
    parser.add_argument("--bib", type=Path,
                        help="BibTeX file. Required when --text is used.")
    parser.add_argument("--output", type=Path,
                        help="Write report to file (.md or .json). Default: stdout (md).")

    args = parser.parse_args(argv)

    if args.cases:
        failures, cases = _run_suite(args.cases)
    else:
        if not args.bib:
            parser.error("--bib is required when --text is used")
        text = read_text(args.text)
        bib_entries = parse_bib(args.bib)
        results = verify_pair(text=text, bib_entries=bib_entries)
        failures = 0
        cases = [(
            {
                "id": "ad-hoc",
                "label": f"{args.text.name} vs {args.bib.name}",
                "text_file": str(args.text),
                "bib_file": str(args.bib),
            },
            results,
        )]

    fmt = "md"
    if args.output and args.output.suffix.lower() == ".json":
        fmt = "json"
    rendered = render_md(cases) if fmt == "md" else render_json(cases)

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
        if not rendered.endswith("\n"):
            sys.stdout.write("\n")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
