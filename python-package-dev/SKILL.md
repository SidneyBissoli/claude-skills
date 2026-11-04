---
name: python-package-dev
description: Modern Python package development (2026 practice) for creating, extending, testing, type-checking, documenting and releasing Python packages on this Windows machine (uv, uv_build, src layout, ruff, pyright strict, pytest, Zensical docs, GitHub Actions, PyPI trusted publishing; packages under C:\dev\python-packages, hosted as SidneyBissoli on GitHub, published on PyPI). Use it whenever the user wants to create a Python package, add a function, module, test, dependency, docs page or CLI to one, fix ruff / pyright / pytest / coverage / Zensical or mkdocs / uv build errors, set up CI or a PyPI release, update a package from its copier template, or mentions "pacote Python", "criar pacote Python", pyproject.toml, pytest, pyright, PyPI, uv build, copier. Also use it when editing any file inside a directory whose pyproject.toml has a [project] table, even if the user never says "package".
---

# Python package development

This skill encodes how Python packages are built in 2026, so that the package
you produce looks like one started this year (uv, `src/` layout, typed, strict
type checking, trusted publishing) rather than a `setup.py` relic. It is the
counterpart of the `r-package-dev` skill. Read the whole file once; open the
references only when the task touches them.

Talk to the user in Portuguese. Write code, docstrings, error messages,
CHANGELOG and commit messages in English.

## 0. Existing project? Its own rules win

Before touching a project, look for `CLAUDE.md`, `CONTRIBUTING.md`, `ROADMAP.md`
or `status/*decisions*.md` at its root and read them. Where they disagree with
this skill, **the project wins**. Not every `pyproject.toml` is a package: an
application (no `[build-system]`) is never built nor published, so sections 2, 3
and 8 do not apply to it; the conventions (section 6) and the loop (section 4)
still do. Checked 2026-11-03:

| Project | Kind | Rules | Differs from section 2 |
|---|---|---|---|
| `mcp\geosgb-br-mcp` (`geosgb-mcp`) | package, MCP server | `ROADMAP.md` | hatchling; no pyright, no docs site |
| `pipelines` | application | `~\.claude\CLAUDE.md` § pipelines, `claude_auth.py` | pinned `anthropic`/`claude-agent-sdk`; keep `uv.lock` |
| `utils\pdf2md` | application | `~\.claude\CLAUDE.md` § pdf2md | `marker-pdf<2` pinned; do not swap libs |
| `tools\jlab` | application | `~\.claude\CLAUDE.md` § notebooks | not a git repository |
| `web\wimoveis-df` | application | none | setuptools backend |
| `python\fable-foundation-backend`, `sandbox-python` | applications | none | nothing |

Do not retrofit an existing project with the new-package defaults (uv_build,
pyright strict, the pre-commit config, the docs site, README.pt-BR.md) as a side
effect of another task. Each is a separate, user-approved change in its own
commit.

## 1. This environment (facts, not preferences)

- **Windows 11.** The global Python (3.14, `py`) is **frozen**: never
  `pip install`, never the bare `python`. Everything goes through **uv** 0.11
  (`~\.local\bin\uv.exe`), which manages Pythons 3.11, 3.12 and 3.13.
  `PYTHONUTF8=1` is set; still pass `encoding="utf-8"` to every `open()`.
- **CLI tools** (`uv tool install`, in `~\.local\bin`): `copier` 9.19, `ruff`,
  `pre-commit`. pytest, pyright, zensical and ruff for a package come from the
  package's own dev groups (`uv run <tool>`), so their versions are the ones in
  its `uv.lock`. `actionlint`: `uvx --from actionlint-py actionlint`.
  Node 24 is on PATH (pyright's PyPI wrapper uses it). `jq` is **not**
  installed.
- **Template:** `C:\dev\claude\templates\python-package\` (repository
  `claude-config`), served from the repository root `C:\dev\claude` so that
  `copier update` works. Its README holds the decisions behind every default.
- **Hosting:** GitHub `SidneyBissoli/<pkg>`; Actions run for real; PyPI via
  trusted publishing. Any `gh` command you hand the user carries
  `-R SidneyBissoli/<pkg>` (the session cwd is usually `C:\dev`).
- **Hooks in Claude Code:** a PostToolUse hook runs `ruff check --fix` and
  `ruff format` on every `.py` you Edit or Write, with the project's ruff
  config; fix whatever it reports back. It does not see shell edits: after
  `sed`, heredocs or scripts, run `uv run ruff check --fix; uv run ruff format`
  yourself. After an Edit, Read before editing the same region again (the hook
  may have reflowed it). A PreToolUse hook blocks any path under a folder with a
  `.no-mcp` file: do not work around it.
- **Line endings:** `core.autocrlf=input`; the template ships
  `.gitattributes` `* text=auto eol=lf`. Measure CR by bytes
  (`tr -cd '\r' < f | wc -c`), not with grep.
- **Up-to-date docs:** Context7 (`mcp__claude_ai_Context7__*`) for uv, ruff,
  pytest, pyright, polars, httpx, mkdocstrings, zensical. Check versions on PyPI
  (`https://pypi.org/pypi/<pkg>/json`) before pinning anything.

## 2. Defaults for NEW packages (do not re-ask)

| Topic | Decision |
|---|---|
| Language | Code, docstrings, errors, CHANGELOG, commits (Conventional Commits) in **English**. `README.md` in English with "Leia em português" linking **README.pt-BR.md**. |
| Layout | `src/<import_name>/`, `py.typed`, tests in `tests/`, docs in `docs/`. Distribution name lowercase with hyphens; import name with underscores. |
| Build | `uv_build`; static `version` in `pyproject.toml`; `__version__` from `importlib.metadata`. Dev versions end in `.dev0`. |
| Python | Minimum 3.11 unless a dependency forces more; CI from the minimum to 3.13 on Ubuntu and Windows. |
| Style | ruff (`E W F I UP B D`, Google docstrings, line length 88); pre-commit with ruff and pyright through `uv run`. |
| Types | Full annotations on every public function; pyright **strict** on `src/` and `tests/`. |
| Errors | Built-in exceptions (`ValueError`, `TypeError`, `LookupError`) or subclasses of a package base error; the message names the argument, what was expected and what was received. Never `print()` for messages; `warnings.warn(..., stacklevel=2)` or `logging` (library logger, no handlers). |
| HTTP | `httpx` (sync client, explicit timeout, `User-Agent` naming the package); tests offline with `respx` or `pytest-httpx`; never the network in docstring examples. |
| Data | polars for new code (pandas only when a consumer requires it); heavy optional dependencies in `[project.optional-dependencies]`, imported lazily. |
| Tests | pytest 9, doctests on, coverage ≥ 75 % (branch); integration tests marked `integration`, run only with `<PKG>_INTEGRATION=true`. |
| Docs | Google-style docstrings rendered by mkdocstrings; Zensical site (reading `mkdocs.yml`) on GitHub Pages. |
| License | MIT, copyright "Sidney da Silva Pereira Bissoli", email sbissoli76@gmail.com; `CITATION.cff`. |

## 3. Workflow A: create a new package

```bash
bash ~/.claude/skills/python-package-dev/scripts/new-package.sh \
  --path C:/dev/python-packages/pkgname \
  --description "One English sentence ending with a period." \
  [--python 3.11] [--no-git]
```

It refuses an invalid or existing path and a dirty template, warns when the
name is taken on PyPI, runs `copier copy --vcs-ref HEAD C:/dev/claude <path>`,
`uv sync` (creates `.venv` and `uv.lock`), `git init -b main`,
`pre-commit install`, runs every hook and makes the initial commit. It does
**not** create the GitHub repository: ask, then
`gh repo create SidneyBissoli/pkgname --public --source . --push`. Then run
`scripts/check.sh` once to prove the skeleton passes, and replace the example
module (`uf.py`, its tests and the README examples) with the real code.

The generated package has: `pyproject.toml`, `src/<pkg>/` (`__init__.py`,
`py.typed`, example module), `tests/` (`conftest.py` with the integration
switch, unit tests, one integration test), `docs/` + `mkdocs.yml`,
`.github/workflows/{ci,docs,release}.yaml`, `.pre-commit-config.yaml`,
`.gitignore`, `.gitattributes`, `LICENSE`, `README.md`, `README.pt-BR.md`,
`CHANGELOG.md`, `CITATION.cff`, `CLAUDE.md` and `.copier-answers.yml`.

Name rules: lowercase letters, digits, single hyphens, starting with a letter;
free on PyPI (PyPI also refuses names that normalise to an existing one:
`my_pkg`, `my.pkg` and `My-Pkg` are all `my-pkg`).

## 4. Workflow B: the development loop

Every change goes through this loop, in this order.

1. **Sync, don't install:** `uv sync` after pulling or after editing
   dependencies. Run everything as `uv run <tool>`; never activate `.venv`.
2. **Write the code** in `src/<pkg>/<topic>.py`, one module per topic,
   public functions first, private helpers (`_name`) below. Re-export the
   public API in `__init__.py` and list it in `__all__`.
3. **Write the test first or alongside** in `tests/test_<topic>.py`. One test
   per behaviour; `pytest.mark.parametrize` for input tables; the error path
   with `pytest.raises(ErrorType, match="...")`.
4. **Document:** Google-style docstring on every public object with `Args`,
   `Returns`, `Raises` and an `Examples` section of doctests (they run in
   `pytest`). New public module → add it to `docs/reference.md` if it is not
   re-exported from the package root.
5. **Test:** `uv run pytest`; one file: `uv run pytest tests/test_x.py`;
   one test: `-k name`; stop at first failure: `-x`.
6. **Format, lint, type-check:** `uv run ruff check --fix`,
   `uv run ruff format`, `uv run pyright`.
7. **Gate** before every commit that touches code or `pyproject.toml`, from
   the package root: `bash ~/.claude/skills/python-package-dev/scripts/check.sh`
   (lock, ruff, pyright, pytest with coverage, `zensical build --strict`, `uv build`;
   `--quick` skips the last two, `--fix` lets ruff rewrite). Steps whose tool
   the project does not declare are skipped, so it works on older projects.
   A failing step is a bug unless you can explain it.
8. **CHANGELOG.md** entry under `## [Unreleased]` (Added / Changed /
   Deprecated / Removed / Fixed / Security) for every user-visible change.
   Version bump only at release.

## 5. Adding specific things

- **Runtime dependency:** `uv add "pkg>=X.Y"` (lower bound = the version you
  tested; no upper bound unless a release is known to break). Dev tool:
  `uv add --group test pkg` (or `lint`, `docs`). Optional extra:
  `uv add --optional parquet pyarrow`, then import it inside the function and
  raise an `ImportError` naming the extra (`pip install pkgname[parquet]`).
  Commit `pyproject.toml` and `uv.lock` together. `uv add` asks for approval
  on this machine.
- **Bundled data:** small files under `src/<pkg>/data/`, read with
  `importlib.resources.files(__package__) / "data" / "x.csv"`; the build
  script that produced them in `data-raw/` (outside `src/`, so it is not
  shipped). Keep the wheel small (< 5 MB); large data is downloaded and cached
  with `platformdirs.user_cache_dir("<pkg>")`.
- **HTTP client:** `httpx.Client(timeout=..., headers={"User-Agent": f"{pkg}/{__version__}"})`,
  `response.raise_for_status()`; decode by the declared charset; tests mock
  the transport (`httpx.MockTransport`, `respx` or `pytest-httpx`). Measured
  2026-11-03: the IBGE API answers gzip even to `Accept-Encoding: identity`
  (urllib's default) and `urllib` hands back the compressed bytes; httpx
  decodes by `Content-Encoding`. Never assume the body is what you asked for.
- **Integration test:** `@pytest.mark.integration`; `conftest.py` skips it
  unless `<PKG>_INTEGRATION=true` (`$env:<PKG>_INTEGRATION = "true"` in
  PowerShell). Run them before a release.
- **CLI:** `[project.scripts] pkgname = "pkgname.cli:main"`; `argparse` for
  small CLIs; test `main([...])` directly.
- **Exceptions:** `src/<pkg>/errors.py` with `class PkgError(Exception)` and
  specific subclasses that also inherit the matching built-in
  (`class UnknownCodeError(PkgError, LookupError)`), exported from the root.
- **Deprecating:** `warnings.warn("old() is deprecated; use new()",
  DeprecationWarning, stacklevel=2)` (or `typing_extensions.deprecated` /
  `warnings.deprecated` on 3.13+); keep it for at least one minor release;
  CHANGELOG "Deprecated".
- **Template update:** with a clean, committed tree,
  `copier update --vcs-ref HEAD --skip-answered`; review the diff and any
  `.rej`/conflict markers; if `pyproject.toml` changed, run `uv lock` and
  `uv sync` (measured: the update leaves `uv.lock` stale, and CI's
  `uv sync --locked` would fail); run `check.sh`; commit `uv.lock` with it as
  `chore: update from the python-package template`.

## 6. Conventions that make code look current

Full detail in `references/conventions.md`. The short list:

- Types everywhere: built-in generics (`list[str]`, `dict[str, int]`),
  `X | None`, `collections.abc` for parameters (`Iterable`, `Mapping`,
  `Sequence`), `Final` for constants, `Literal` for enumerated arguments.
- `pathlib.Path` over `os.path`; f-strings; `dataclass(frozen=True, slots=True)`
  for records; `enum.StrEnum` for string choices.
- Keyword-only optional arguments (`def f(x, *, year=None)`); no mutable
  defaults; return the same type regardless of input size (empty frame, not
  `None`).
- No `print()` in library code; no module-level side effects (network, file
  writes, logging configuration) at import time.
- Every public function has a docstring with a runnable example.
- Tests independent of each other, of the working directory, of locale, time
  and network (`tmp_path`, `monkeypatch`, fixed dates).

## 7. Reading tool output

- **pyright strict**, the frequent ones:
  `reportUnknownMemberType` / `reportUnknownVariableType` /
  `reportUnknownArgumentType`: an untyped library or `json` data; annotate the
  variable (`rows: list[dict[str, Any]] = ...`) or `cast()` at the boundary;
  explicit `Any` is accepted, *Unknown* is not. `reportMissingTypeStubs`: add
  the stubs package (`uv add --group lint pandas-stubs`) or a narrow
  `# pyright: ignore[reportMissingTypeStubs]` on the import.
  `reportPrivateUsage`: tests touching `_helpers`; test through the public API
  or ignore per line. `reportUnnecessaryIsInstance`: a runtime check of an
  annotated argument; keep it only for public input validation and silence it
  on that line. Always ignore by rule name (`# pyright: ignore[rule]`), never a
  bare `# type: ignore`.
- **pytest:** `PytestUnknownMarkWarning` is an error here (`strict = true`):
  register the marker in `[tool.pytest] markers`. Doctest failures print
  "Expected / Got": fix the example or the code, never `# doctest: +SKIP`
  without a reason. `Required test coverage of 75% not reached`: the report
  lists missing lines per file; test the public behaviour and error branches.
- **ruff:** `D1xx` missing docstring (public object), `D41x` Google sections,
  `B008` call in a default argument, `UP` modernisations (accept them),
  `E501` only for strings and comments the formatter cannot wrap.
- **uv:** `uv sync --locked` failing in CI means `uv.lock` is stale: run
  `uv lock` and commit it. `uv build` puts `pyproject.toml.orig` in the sdist
  (uv_build 0.13 normalises the manifest): expected, not a bug.
- **zensical build --strict:** a broken link, an unresolved cross-reference or
  a docstring parsing warning fails the build; the message names the page or
  object. Always pass `--strict`: without it Zensical prints the issue and
  still exits 0 (measured with 0.0.74). Zensical silently ignores MkDocs
  plugins outside its supported list, so a plugin that "does nothing" is
  probably unsupported (list:
  https://zensical.org/docs/compatibility/mkdocs/plugins/). Older projects on
  mkdocs-material: same `--strict` rule; the end-of-life banner (2027-05-05)
  is informational.

## 8. CI, docs and release

See `references/ci-release.md`: the three workflows, enabling GitHub Pages,
registering the PyPI trusted publisher, and the release checklist. Publishing to
PyPI, creating tags and GitHub releases are the user's decision; prepare
everything, hand over the commands.

## 9. Reporting back

When you finish, tell the user in Portuguese: what was added or changed
(files), the result of the last `check.sh` run (which steps passed, coverage
percentage), and what is still open. Paste only the relevant lines of tool
output.
