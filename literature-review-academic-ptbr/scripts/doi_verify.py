"""DOI verification — hard gate of the literature-review-academic-ptbr skill.

Usage
-----
Verify a fixture of cases (recommended for batteries):

    python doi_verify.py --cases tests/teste03_doi_verify_cases.json --output report.md
    python doi_verify.py --cases tests/teste03_doi_verify_cases.json --output report.json

Verify all entries from a BibTeX file (no expected metadata; only
checks DOI resolution and retraction):

    python doi_verify.py --bib references.bib --output report.md

Verify a single DOI ad hoc:

    python doi_verify.py --doi 10.1016/S0140-6736(97)11096-0

Report formats
--------------
The output suffix selects the renderer: ``.md`` (default) for a
human-readable Markdown table, ``.json`` for a structured payload
suitable for downstream pipelines. When ``--output`` is omitted, the
Markdown report is written to stdout.

Exit code
---------
Non-zero if any case carries an ``expected`` field and the observed
state diverges from it. This makes the script suitable as a CI hard
gate against the regression battery.

Six return states
-----------------
``OK``        DOI resolves AND the composite metadata fuzzy score is
              at or above ``COMPOSITE_OK_THRESHOLD``.
``MISMATCH``  DOI resolves but composite score below threshold.
              Catches Sub-30.2 of references/_changelog.md
              (fabrication with collided identifier).
``NOT_FOUND`` DOI does not resolve in CrossRef nor in OpenAlex.
``NO_DOI``    Reference provided without a DOI. Treated as a
              declared limitation in the output, per decision 4 of
              references/_changelog.md (carimbo de confiança).
``RETRACTED`` DOI resolves but the publication is marked retracted
              in CrossRef ``relation``/``update-nature`` or in
              OpenAlex ``is_retracted``.
``ERROR``     Network failure, timeout, or API error. Distinct from
              NOT_FOUND so transient failures do not silently
              promote to "fabricated".

Threshold justification
-----------------------
``COMPOSITE_OK_THRESHOLD = 75`` (out of 100) is calibrated against
the strong test case **Silva & Lopes (2020)** of the Teste 03 battery
— exemplar of Sub-30.2 (fabrication with collided identifier). The
provided DOI ``10.1590/s0102-6992-202035020008`` resolves in CrossRef
to a *real, distinct* article (SILVA, R. A. da. "Para além do Estado:
Marx, Lenin e a crítica da estatalidade", *Sociedade e Estado* v.35
n.2 p.553-579, 2020). A threshold blind to any single field would
produce a false OK, because:

* author overlap: token "Silva" matches → ~50% on token_set_ratio,
  even though the actual authors and ORCID are different;
* journal: identical → 100%;
* year: identical → 100%;
* title: completely divergent → ~10%;
* first page: 521 vs 553 → ~0%.

Composite score under the weights below evaluates to roughly 44/100,
well under 75 → ``MISMATCH``. Genuine cases (Machado 2021, Escudero
2022, Campos et al. 2021) with all fields aligned land at 95–100 →
``OK``. The threshold is therefore the lowest defensible value that
catches Silva & Lopes 2020 without producing false positives on
genuine matches; it is not tuned to bound MISMATCH from below
(every below-threshold resolved DOI is MISMATCH, regardless of how
low). Revisit if a future test produces a genuine match that scores
under 75 or a fabrication that scores over 75; record the change in
references/_changelog.md.

Field weights (sum = 1.0):

* authors  0.30 — most discriminative single signal in academic refs.
* title    0.40 — least likely to coincide between distinct works.
* journal  0.15 — frequent collision (same journal, distinct article).
* year     0.10 — categorical match/mismatch.
* pages    0.05 — auxiliary signal; absent or noisy in many records.

When ``pages`` are missing in expected metadata, its weight is
redistributed proportionally over the remaining fields.

Fallback OpenAlex
-----------------
CrossRef is queried first. On 404, the script falls back to
OpenAlex via the canonical DOI URL form
``https://api.openalex.org/works/https://doi.org/<DOI>``. The
fallback contributes (i) NOT_FOUND vs ERROR distinction when
CrossRef is silent and (ii) ``is_retracted`` cross-fence on
retraction detection — even when CrossRef has no retraction signal,
OpenAlex may still flag the work, in which case the result is
RETRACTED. Both APIs are public and require no API key; the
CrossRef ``mailto`` User-Agent is set per CrossRef etiquette.

Parallelism
-----------
HTTP I/O is parallelised via ``concurrent.futures.ThreadPoolExecutor``
with ``max_workers = 16``, mirroring the ``--transfers 16`` profile
of rclone for similar-magnitude REST batches. Network timeout is 30
seconds per request. Inside each worker, CrossRef and OpenAlex are
queried sequentially (CrossRef first, OpenAlex on demand). This is
adequate for the typical battery size (≤100 cases) of the skill;
larger batteries should consider a session with retry/backoff,
which is not needed at this scope.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import sys
import time
import urllib.parse
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import requests
from rapidfuzz import fuzz

# --- Constants -------------------------------------------------------

CROSSREF_API = "https://api.crossref.org/works"
OPENALEX_API = "https://api.openalex.org/works"

# Per CrossRef etiquette, a polite User-Agent with mailto enables
# the higher rate-limit pool. Defaults to the author's e-mail; set
# CROSSREF_MAILTO to use your own.
_MAILTO = os.environ.get("CROSSREF_MAILTO", "").strip() or "sbissoli76@gmail.com"
USER_AGENT = (
    "literature-review-academic-ptbr/1.0 "
    "(https://github.com/SidneyBissoli/literature-review-academic-ptbr"
    + (f"; mailto:{_MAILTO}" if _MAILTO else "")
    + ")"
)

REQUEST_TIMEOUT = 30  # seconds
MAX_WORKERS = 16      # mirrors rclone --transfers 16

# OK / MISMATCH boundary on the composite 0-100 score. See the
# "Threshold justification" section of the module docstring.
COMPOSITE_OK_THRESHOLD = 75

# Field weights for the composite metadata score. Sum to 1.0.
WEIGHTS: dict[str, float] = {
    "authors": 0.30,
    "title": 0.40,
    "journal": 0.15,
    "year": 0.10,
    "pages": 0.05,
}


# --- Result type -----------------------------------------------------


@dataclass
class VerificationResult:
    case_id: Any
    label: str
    doi: str | None
    state: str
    expected_state: str | None = None
    score: float | None = None
    notes: str = ""
    field_scores: dict[str, float] = field(default_factory=dict)
    crossref_metadata: dict | None = None
    openalex_metadata: dict | None = None
    elapsed_seconds: float = 0.0


# --- HTTP helpers ----------------------------------------------------


def _crossref_get(doi: str) -> dict | None:
    """Return the ``message`` body from CrossRef, or ``None`` on 404."""
    encoded = urllib.parse.quote(doi, safe="/()")
    url = f"{CROSSREF_API}/{encoded}"
    resp = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json().get("message")


def _openalex_get(doi: str) -> dict | None:
    """Return the OpenAlex work payload, or ``None`` on 404."""
    encoded = urllib.parse.quote(doi, safe="/()")
    url = f"{OPENALEX_API}/https://doi.org/{encoded}"
    resp = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


# --- Retraction detection -------------------------------------------


def _is_retracted_crossref(message: dict | None) -> tuple[bool, str]:
    """Inspect CrossRef message for retraction signals.

    Returns (flag, reason). Multiple signals are checked because
    CrossRef exposes retraction information across several fields
    depending on whether the queried DOI is the original work or
    the retraction notice itself.
    """
    if not message:
        return False, ""

    # Direction A: this DOI is itself a retraction notice updating
    # another DOI.
    for upd in message.get("update-to") or []:
        nature = (upd.get("update-nature") or upd.get("type") or "").lower()
        if "retract" in nature:
            return True, f"crossref.update-to: {nature}"

    # Direction B: relation field on the original DOI points to a
    # retraction-by record.
    relations = message.get("relation") or {}
    for rel_key in ("is-retracted-by", "has-retraction"):
        rels = relations.get(rel_key)
        if rels:
            return True, f"crossref.relation.{rel_key}"

    # Direction C: subtype/type carries a retraction marker.
    subtype = (message.get("subtype") or "").lower()
    if "retract" in subtype:
        return True, f"crossref.subtype: {subtype}"

    # Direction D: CrossMark "update-policy" with retraction tag.
    crossmark = message.get("crossmark-restriction")
    if crossmark and "retract" in str(crossmark).lower():
        return True, "crossref.crossmark-restriction"

    return False, ""


def _is_retracted_openalex(work: dict | None) -> tuple[bool, str]:
    if not work:
        return False, ""
    if bool(work.get("is_retracted")):
        return True, "openalex.is_retracted"
    return False, ""


# --- Fuzzy comparison -----------------------------------------------


def _normalise(s: str | None) -> str:
    return " ".join((s or "").split()).lower()


def _author_similarity(expected: list[str], cr_authors: list[dict]) -> float:
    if not expected or not cr_authors:
        return 0.0
    cr_str = " ".join(
        f"{a.get('family', '')} {a.get('given', '')}".strip()
        for a in cr_authors
    )
    exp_str = " ".join(expected)
    return float(fuzz.token_set_ratio(_normalise(exp_str), _normalise(cr_str)))


def _title_similarity(expected: str, cr_titles: list[str] | None) -> float:
    if not expected or not cr_titles:
        return 0.0
    cr_title = cr_titles[0] if cr_titles else ""
    return float(fuzz.token_set_ratio(_normalise(expected), _normalise(cr_title)))


def _journal_similarity(expected: str, cr_container: list[str] | None) -> float:
    if not expected or not cr_container:
        return 0.0
    cr_journal = cr_container[0] if cr_container else ""
    return float(fuzz.token_set_ratio(_normalise(expected), _normalise(cr_journal)))


def _extract_cr_year(cr_message: dict) -> int | None:
    for key in ("issued", "published-print", "published-online", "created"):
        parts = (cr_message.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return int(parts[0][0])
    return None


def _year_match(expected_year: Any, cr_message: dict) -> float:
    cr_year = _extract_cr_year(cr_message)
    if cr_year is None or expected_year is None:
        return 0.0
    try:
        return 100.0 if int(cr_year) == int(expected_year) else 0.0
    except (TypeError, ValueError):
        return 0.0


def _pages_similarity(expected: str, cr_pages: str | None) -> float:
    if not expected or not cr_pages:
        return 0.0
    return float(fuzz.token_set_ratio(_normalise(str(expected)), _normalise(str(cr_pages))))


def _composite_score(expected: dict, cr_message: dict) -> tuple[float, dict[str, float]]:
    """Return (composite, per-field) scores."""
    a = _author_similarity(expected.get("authors") or [], cr_message.get("author") or [])
    t = _title_similarity(expected.get("title") or "", cr_message.get("title"))
    j = _journal_similarity(expected.get("journal") or "", cr_message.get("container-title"))
    y = _year_match(expected.get("year"), cr_message)
    pages_field = expected.get("first_page") or expected.get("pages") or ""
    p = _pages_similarity(str(pages_field), cr_message.get("page"))

    # Drop pages weight if expected has no pages information.
    weights = dict(WEIGHTS)
    if not pages_field:
        weights["pages"] = 0.0
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}

    composite = (
        weights["authors"] * a
        + weights["title"] * t
        + weights["journal"] * j
        + weights["year"] * y
        + weights["pages"] * p
    )
    return composite, {
        "authors": a, "title": t, "journal": j, "year": y, "pages": p,
    }


# --- Summaries -------------------------------------------------------


def _crossref_summary(m: dict | None) -> dict:
    if not m:
        return {}
    return {
        "title": (m.get("title") or [None])[0],
        "authors": [
            f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
            for a in m.get("author") or []
        ],
        "journal": (m.get("container-title") or [None])[0],
        "year": _extract_cr_year(m),
        "volume": m.get("volume"),
        "issue": m.get("issue"),
        "page": m.get("page"),
    }


def _openalex_summary(w: dict | None) -> dict:
    if not w:
        return {}
    return {
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "is_retracted": w.get("is_retracted"),
    }


# --- Verification core ----------------------------------------------


def verify_one(case: dict) -> VerificationResult:
    case_id = case.get("id")
    label = case.get("label", "")
    doi = case.get("doi")
    expected = case.get("expected_metadata") or {}
    expected_state = case.get("expected")

    started = time.monotonic()

    if not doi:
        return VerificationResult(
            case_id=case_id, label=label, doi=None, state="NO_DOI",
            expected_state=expected_state,
            notes="Reference has no DOI; declared limitation per decision 4.",
            elapsed_seconds=time.monotonic() - started,
        )

    cr_message: dict | None = None
    oa_work: dict | None = None
    notes_parts: list[str] = []
    crossref_failed = False

    # Try CrossRef.
    try:
        cr_message = _crossref_get(doi)
    except requests.RequestException as exc:
        crossref_failed = True
        notes_parts.append(f"CrossRef error: {exc}")

    # If CrossRef returned 404 or failed, try OpenAlex as primary fallback.
    if cr_message is None:
        try:
            oa_work = _openalex_get(doi)
        except requests.RequestException as exc:
            notes_parts.append(f"OpenAlex error: {exc}")

        if oa_work is None:
            state = "ERROR" if (crossref_failed and "OpenAlex error" in "; ".join(notes_parts)) else "NOT_FOUND"
            if state == "NOT_FOUND" and not notes_parts:
                notes_parts.append("DOI not found in CrossRef nor OpenAlex.")
            return VerificationResult(
                case_id=case_id, label=label, doi=doi, state=state,
                expected_state=expected_state,
                notes="; ".join(notes_parts),
                elapsed_seconds=time.monotonic() - started,
            )

    # Cross-source retraction fence: even if CrossRef resolved, ask
    # OpenAlex about retraction status. is_retracted is OpenAlex's
    # most reliable signal and is independent of CrossRef field
    # population.
    cr_retracted, cr_reason = _is_retracted_crossref(cr_message)
    if oa_work is None and cr_message is not None:
        try:
            oa_work = _openalex_get(doi)
        except requests.RequestException:
            oa_work = None  # secondary fence is best-effort
    oa_retracted, oa_reason = _is_retracted_openalex(oa_work)

    if cr_retracted or oa_retracted:
        reason = "; ".join(filter(None, [cr_reason, oa_reason]))
        notes_parts.append(f"retraction signal: {reason}")
        return VerificationResult(
            case_id=case_id, label=label, doi=doi, state="RETRACTED",
            expected_state=expected_state,
            notes="; ".join(notes_parts),
            crossref_metadata=_crossref_summary(cr_message),
            openalex_metadata=_openalex_summary(oa_work),
            elapsed_seconds=time.monotonic() - started,
        )

    # Score against expected metadata when both are available.
    score: float | None = None
    field_scores: dict[str, float] = {}
    if cr_message and expected:
        score, field_scores = _composite_score(expected, cr_message)
        state = "OK" if score >= COMPOSITE_OK_THRESHOLD else "MISMATCH"
    elif cr_message:
        state = "OK"
        notes_parts.append("DOI resolved in CrossRef; no expected metadata to score.")
    else:
        # CrossRef silent, OpenAlex resolved.
        state = "OK"
        notes_parts.append("DOI resolved via OpenAlex fallback only.")

    return VerificationResult(
        case_id=case_id, label=label, doi=doi, state=state,
        score=score, expected_state=expected_state,
        notes="; ".join(notes_parts),
        field_scores=field_scores,
        crossref_metadata=_crossref_summary(cr_message),
        openalex_metadata=_openalex_summary(oa_work),
        elapsed_seconds=time.monotonic() - started,
    )


# --- BibTeX adapter -------------------------------------------------


def _read_bib(path: Path) -> list[dict]:
    import bibtexparser

    with path.open("r", encoding="utf-8") as fp:
        bib = bibtexparser.load(fp)

    cases: list[dict] = []
    for entry in bib.entries:
        year_raw = entry.get("year", "").strip()
        year = int(year_raw) if year_raw.isdigit() else None
        cases.append({
            "id": entry.get("ID"),
            "label": entry.get("ID"),
            "doi": entry.get("doi") or entry.get("DOI"),
            "expected": None,
            "expected_metadata": {
                "authors": [entry["author"]] if entry.get("author") else [],
                "title": entry.get("title", "").strip("{}"),
                "journal": entry.get("journal") or entry.get("booktitle") or "",
                "year": year,
                "pages": entry.get("pages", ""),
            },
        })
    return cases


# --- Reporting ------------------------------------------------------


def _render_md(results: list[VerificationResult]) -> str:
    lines = [
        "# DOI verification report",
        "",
        f"Total cases: {len(results)}",
        "",
        "| # | Label | DOI | State | Expected | Pass | Score | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        score_str = f"{r.score:.1f}" if r.score is not None else "—"
        expected_str = r.expected_state or "—"
        if r.expected_state:
            pass_mark = "✓" if r.state == r.expected_state else "✗"
        else:
            pass_mark = "—"
        notes_escaped = (r.notes or "").replace("|", "\\|")
        lines.append(
            f"| {r.case_id} | {r.label} | `{r.doi or ''}` | "
            f"`{r.state}` | `{expected_str}` | {pass_mark} | {score_str} | "
            f"{notes_escaped} |"
        )
    lines.append("")
    return "\n".join(lines)


def _render_json(results: list[VerificationResult]) -> str:
    return json.dumps(
        [asdict(r) for r in results],
        indent=2,
        ensure_ascii=False,
    )


# --- CLI ------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Hard gate: verify DOIs against CrossRef + OpenAlex.",
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--cases", type=Path,
                     help="JSON fixture with 'cases' array (regression battery).")
    src.add_argument("--bib", type=Path,
                     help="BibTeX file; each entry becomes a case (no expected).")
    src.add_argument("--doi", type=str,
                     help="Single DOI (no expected metadata).")
    parser.add_argument("--output", type=Path,
                        help="Write report to file (.md or .json). Default: stdout (md).")

    args = parser.parse_args(argv)

    if args.cases:
        with args.cases.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        cases = data.get("cases") if isinstance(data, dict) else data
    elif args.bib:
        cases = _read_bib(args.bib)
    else:
        cases = [{"id": "single", "label": args.doi, "doi": args.doi}]

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(verify_one, cases))

    fmt = "md"
    if args.output and args.output.suffix.lower() == ".json":
        fmt = "json"
    rendered = _render_md(results) if fmt == "md" else _render_json(results)

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
        if not rendered.endswith("\n"):
            sys.stdout.write("\n")

    failures = [r for r in results if r.expected_state and r.state != r.expected_state]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
