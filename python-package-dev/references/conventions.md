# Code conventions for modern Python packages

Read the section you need. Each pattern says why it is preferred, so you can
adapt it rather than copy it blindly.

## Contents

1. Errors, warnings, logging
2. Input validation
3. Function and API design
4. Type hints under pyright strict
5. Docstrings (Google style) and doctests
6. pytest
7. HTTP and data access
8. Packaging details (`pyproject.toml`)
9. Things that date a package (avoid)

## 1. Errors, warnings, logging

Why: callers catch by type, so the type carries the meaning; the message tells
the user which argument was wrong, what was expected and what came in.

```python
class BrDataError(Exception):
    """Base class for every error raised by this package."""


class UnknownCodeError(BrDataError, LookupError):
    """A code is not in the reference table."""


def municipality(code: int) -> str:
    if code not in _NAMES:
        msg = f"`code` must be a 7-digit IBGE municipality code, not {code!r}."
        raise UnknownCodeError(msg)
    return _NAMES[code]
```

- Assign the message to `msg` first (ruff `EM`/`TRY` style; keeps tracebacks
  readable).
- Chain: `raise DownloadError(msg) from exc` when translating a lower-level
  error; `from None` when the original adds nothing (a `KeyError` from a dict
  lookup).
- Warnings are rare; prefer an error with a clear fix. If you warn:
  `warnings.warn(msg, UserWarning, stacklevel=2)` so the warning points at
  the caller.
- Progress and diagnostics: `logger = logging.getLogger(__name__)` at module
  level, `logger.info(...)`; never configure handlers in the library and never
  `print()`. A `quiet`/`verbose` argument is fine for long downloads.

## 2. Input validation

Validate at the public boundary, once, then trust the types inside.

```python
from collections.abc import Iterable
from typing import Literal

Source = Literal["sim", "sinasc", "sih"]


def read(source: Source, years: Iterable[int], *, uf: str | None = None) -> pl.DataFrame:
    if source not in ("sim", "sinasc", "sih"):  # runtime check for untyped callers
        msg = f"`source` must be 'sim', 'sinasc' or 'sih', not {source!r}."
        raise ValueError(msg)
    years = sorted(set(years))
    if not years:
        msg = "`years` must contain at least one year."
        raise ValueError(msg)
    ...
```

- Enumerations: `Literal[...]` in the signature (pyright checks callers) plus
  a runtime check (users in notebooks are untyped), or `enum.StrEnum`.
- `isinstance` checks of annotated arguments make pyright report
  `reportUnnecessaryIsInstance`; keep them only at the public boundary and
  silence that one line.
- Normalise early (`strip().upper()`, `sorted(set(...))`), validate, then
  compute.

## 3. Function and API design

- Verbs for functions, nouns for data; snake_case; a common prefix for a
  family (`sim_read()`, `sim_years()`) helps discovery, as in the R packages.
- Required arguments positional, options keyword-only after `*`; defaults
  immutable (`None`, then `x = x or []` inside).
- Return the same type regardless of input size (a frame with zero rows and
  the right schema, not `None`).
- Public API = what `__init__.py` re-exports and lists in `__all__`; every
  other module-level name starts with `_` or lives in a `_private.py` module.
- Pure functions where possible; side effects (cache files, environment)
  isolated in small functions that tests can redirect with `tmp_path` and
  `monkeypatch`.
- Keep each module under ~400 lines; split by topic.

## 4. Type hints under pyright strict

- Built-in generics and unions (`list[int]`, `str | None`) — no `typing.List`,
  `Optional`, `Union` (ruff `UP` rewrites them).
- Parameters accept the most general protocol (`Iterable`, `Mapping`,
  `Sequence` from `collections.abc`); return the concrete type.
- Constants: `Final`; read-only tables: `types.MappingProxyType` (as the
  template's `UF_CODES`).
- Untyped boundaries (JSON, CSV rows, untyped libraries): annotate the
  receiving variable or `typing.cast` once; explicit `Any` is accepted by
  strict mode, inferred *Unknown* is not.
- `TYPE_CHECKING` imports for annotation-only dependencies (coverage excludes
  the block).
- Ignore by rule: `# pyright: ignore[reportPrivateUsage]`; never a bare
  `# type: ignore`.

## 5. Docstrings (Google style) and doctests

```python
def uf_code(uf: str) -> int:
    """Return the IBGE code of a Brazilian federative unit.

    Args:
        uf: Two-letter abbreviation (e.g. ``"SP"``); case and surrounding
            whitespace are ignored.

    Returns:
        The two-digit IBGE code.

    Raises:
        ValueError: If ``uf`` is not one of the 27 federative units.

    Examples:
        >>> uf_code("SP")
        35
    """
```

- First line: imperative summary ending with a period; blank line; details.
- `Examples` run as doctests (`--doctest-modules`): deterministic, offline,
  fast. Long outputs: show a slice (`df.shape`, `df.columns[:3]`) or use
  `# doctest: +ELLIPSIS`.
- Module docstring on every module (ruff `D100`), one sentence is enough.
- Document attributes of constants with a string literal right below them
  (mkdocstrings picks it up).

## 6. pytest

```python
@pytest.mark.parametrize(("uf", "expected"), [("SP", 35), (" df ", 53)])
def test_uf_code_normalises_input(uf: str, expected: int) -> None:
    assert uf_code(uf) == expected


def test_cache_is_written(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BRDATA_CACHE", str(tmp_path))
    download("sim", 2023)
    assert (tmp_path / "sim" / "2023.parquet").exists()
```

- One behaviour per test; names say the behaviour (`test_x_rejects_empty_years`).
- Fixtures in `conftest.py`; small static fixtures under `tests/data/`, found
  with `Path(__file__).parent / "data"`.
- `pytest.raises(ErrorType, match=...)` for every documented error.
- Network: mock in unit tests; the real thing only in `integration` tests.
- Snapshot-style checks of printed/serialised output: compare against a file
  in `tests/data/` (or `syrupy` if the suite grows).
- Coverage is a floor (75 %), not a goal: test the public API and the error
  branches.

## 7. HTTP and data access

- `httpx.Client` with explicit `timeout`, a `User-Agent` naming the package
  and version, `raise_for_status()`, retries with backoff only for idempotent
  GETs (`httpx.HTTPTransport(retries=3)` covers connection errors).
- Decode text by the declared charset; Brazilian sources often send
  `latin-1`/`cp1252` without saying so: detect once, document it, test with a
  fixture containing accents.
- Cache downloads under `platformdirs.user_cache_dir("<pkg>")`; expose
  `cache_dir()` and `clear_cache()`.
- Frames: polars, with an explicit schema when reading CSV (codes as strings:
  IBGE codes, CNPJ, CEP keep leading zeros).

## 8. Packaging details (`pyproject.toml`)

- Metadata is PEP 621 only (`[project]`); license as an SPDX expression
  (`license = "MIT"`, `license-files = ["LICENSE"]`) — no license classifier.
- Dependency groups (PEP 735, `[dependency-groups]`) for dev tools, extras
  (`[project.optional-dependencies]`) only for user-facing optional features.
- `requires-python` lower bound only.
- `uv.lock` is committed (reproducible dev and CI); it does not constrain
  users of the published package.
- `[tool.uv.build-backend] source-include` adds files to the sdist (the
  template ships `tests/` and `CHANGELOG.md`).

## 9. Things that date a package (avoid)

| Dated | Current |
|---|---|
| `setup.py`, `setup.cfg`, `requirements*.txt` | `pyproject.toml` (PEP 621) + `uv.lock` + dependency groups |
| flat layout (`pkg/` at the root) | `src/pkg/` |
| `pip install -e .`, activated venvs, tox | `uv sync`, `uv run`, the CI matrix |
| black + isort + flake8 | ruff (lint + format) |
| mypy defaults | pyright strict |
| `typing.List`, `Optional[X]` | `list`, `X \| None` |
| `os.path`, `%`/`.format()` | `pathlib`, f-strings |
| `__version__ = "1.2.3"` maintained by hand next to setup.py | static `version` in `pyproject.toml`, read with `importlib.metadata` |
| API token secret for PyPI | trusted publishing (OIDC) |
| `requests` | `httpx` |
| pandas by default | polars |
| `print()` for progress | `logging` / opt-in progress |
| Sphinx + reST docstrings | mkdocs + mkdocstrings, Google docstrings |
