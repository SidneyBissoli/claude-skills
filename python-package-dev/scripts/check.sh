#!/usr/bin/env bash
# Full quality gate for a Python package: lock, lint, format, types, tests with
# coverage, docs and build. Run inside the package root (where pyproject.toml is).
# Usage: bash check.sh [--quick] [--fix]
#   --quick  skip the docs site and the build
#   --fix    let ruff rewrite files instead of only checking them
# Steps whose tool the package does not declare are skipped, so the gate also
# works on projects that predate the template (no pyright, no mkdocs, ...).
set -u
quick=0; fix=0
for a in "$@"; do case "$a" in --quick) quick=1;; --fix) fix=1;; esac; done
[ -f pyproject.toml ] || { echo "check.sh: no pyproject.toml in $(pwd)" >&2; exit 2; }
grep -q '^\[project\]' pyproject.toml || { echo "check.sh: pyproject.toml has no [project] table" >&2; exit 2; }
status=0
step() { printf '\n==> %s\n' "$1"; }
skip() { printf '\n==> %s: skipped (%s)\n' "$1" "$2"; }
declares() { grep -Eq "\"$1([<>=~!\[ ;\"]|$)" pyproject.toml; }

step "uv.lock up to date and environment in sync"
uv lock --check || { echo "   -> run: uv lock"; status=1; }
uv sync --locked --quiet || status=1

if declares ruff; then
  if [ $fix = 1 ]; then
    step "ruff (rewriting)"
    uv run --no-sync ruff check --fix || status=1
    uv run --no-sync ruff format || status=1
  else
    step "ruff check + format --check"
    uv run --no-sync ruff check || { echo "   -> run with --fix or: uv run ruff check --fix"; status=1; }
    uv run --no-sync ruff format --check || { echo "   -> run with --fix or: uv run ruff format"; status=1; }
  fi
else
  skip "ruff" "ruff not in pyproject.toml"
fi

if declares pyright; then
  step "pyright"
  uv run --no-sync pyright || status=1
else
  skip "pyright" "pyright not in pyproject.toml"
fi

if declares pytest; then
  if declares pytest-cov; then
    step "pytest with coverage (threshold from [tool.coverage.report])"
    uv run --no-sync pytest --cov || status=1
  else
    step "pytest"
    uv run --no-sync pytest || status=1
  fi
else
  skip "pytest" "pytest not in pyproject.toml"
fi

if [ $quick = 0 ]; then
  # Zensical when declared (the template default), MkDocs for older projects.
  # --strict always: Zensical exits 0 on broken links without it.
  if [ -f mkdocs.yml ] || [ -f zensical.toml ]; then
    if declares zensical; then
      step "zensical build --strict"
      uv run --no-sync zensical build --strict || status=1
    elif declares mkdocs-material || declares mkdocs; then
      step "mkdocs build --strict"
      NO_MKDOCS_2_WARNING=1 uv run --no-sync mkdocs build --strict --quiet || status=1
    else
      skip "docs" "neither zensical nor mkdocs in pyproject.toml"
    fi
  else
    skip "docs" "no mkdocs.yml or zensical.toml"
  fi

  if grep -q '^\[build-system\]' pyproject.toml; then
    step "uv build (sdist + wheel into dist/)"
    uv build --quiet || status=1
    ls dist/ 2>/dev/null | sed 's/^/   /'
  else
    skip "uv build" "no [build-system]: an application, not a package"
  fi
fi

printf '\n==> check.sh finished with status %d\n' "$status"
exit $status
