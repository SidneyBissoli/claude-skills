# CI, documentation site and release

## GitHub Actions (from the template)

| Workflow | Trigger | What it does |
|---|---|---|
| `ci.yaml` | push to `main`, PRs, manual | matrix ubuntu/windows × Python (minimum → 3.13): `uv sync --locked`, ruff check + format check, pyright, pytest with coverage (fails under 75 %) |
| `docs.yaml` | push to `main`, PRs (build only), manual | `mkdocs build --strict`; on `main`, deploys `site/` to GitHub Pages |
| `release.yaml` | tag `v*` | checks tag = `pyproject.toml` version, `uv build`, smoke-tests the wheel in a clean env, publishes to PyPI by trusted publishing |

Conventions kept in all three (copy them into any workflow you add):

- `permissions: contents: read` at the top; extra permissions only on the job
  that needs them (`id-token: write` for PyPI and Pages, `pages: write`).
- `concurrency:` on every workflow (CI cancels superseded runs; Pages queues
  instead of racing — an unguarded deploy is a race).
- Every job has `timeout-minutes` (the default is 360) and every setup step a
  deadline (`setup-uv` 5 min, `uv sync` 10 min), so a stalled mirror fails
  fast and is re-run instead of holding the PR.
- `actions/checkout` with `persist-credentials: false`.
- Action majors pinned (`@v7`, `@v10`); PyPA's publisher on `@release/v1`, as
  its README asks.

Validate any workflow edit with actionlint, not with a YAML parser:

```bash
uvx --from actionlint-py actionlint .github/workflows/*.yaml
```

(No shellcheck on this machine, so `run:` scripts are not linted; read them.)

After a push, look at the run, not at the push:
`gh run list -R SidneyBissoli/<pkg> -L 3`; `gh run view <id> --log-failed`.

## GitHub Pages (once per repository)

The docs workflow deploys through Actions, so Pages must use the "GitHub
Actions" source. Hand the user (or run on their go-ahead):

```bash
gh api -X POST repos/SidneyBissoli/<pkg>/pages -f build_type=workflow
```

The site URL is `https://sidneybissoli.github.io/<pkg>/` (already in
`mkdocs.yml`, `pyproject.toml` and `CITATION.cff`). Never commit `site/`.

Material for MkDocs reaches end of life on 2027-05-05 (banner printed by
9.8.0). Its successor, Zensical, reads the same `mkdocs.yml`; plan the switch
in the template, not package by package.

## PyPI trusted publishing (once per package)

1. On <https://pypi.org/manage/account/publishing/> (user logged in), add a
   **pending publisher**: PyPI project name `<pkg>`, owner `SidneyBissoli`,
   repository `<pkg>`, workflow `release.yaml`, environment `pypi`.
2. In the GitHub repository, create the environment `pypi` (Settings →
   Environments); optionally require the user's approval for deployments.
3. Optional dry run: TestPyPI with a second publisher and
   `repository-url: https://test.pypi.org/legacy/` in a copy of the publish
   job.

The first successful run turns the pending publisher into the project. No
token is ever stored. Both steps are the user's: they touch their PyPI account.

## CHANGELOG entries

Keep a Changelog sections under `## [Unreleased]`: Added, Changed, Deprecated,
Removed, Fixed, Security. One bullet per user-visible change, written for the
user, function name first, issue/PR at the end: `` - `read_sim()` accepts
`uf` (#12). ``. Internal refactors and doc tweaks get no entry.

## Release checklist

1. `git pull --ff-only`; clean tree; on `main`; CI green on the last commit.
2. Decide the bump from the CHANGELOG: a change in the type or shape of an
   existing output, or a removed argument, is **major** (minor while < 1.0).
   `uv version --bump minor` (or `patch`/`major`; `--bump stable` turns
   `0.1.0.dev0` into `0.1.0`). It updates `pyproject.toml` and `uv.lock`.
3. CHANGELOG: rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, add an
   empty `## [Unreleased]` above it, update the compare links at the bottom if
   the file has them.
4. `bash ~/.claude/skills/python-package-dev/scripts/check.sh` clean, plus
   the integration tests: `<PKG>_INTEGRATION=true uv run pytest -m integration`.
5. Commit `chore: release vX.Y.Z` through a PR; merge first.
6. **On the user's go-ahead**, tag the merged commit and push the tag:
   `git tag vX.Y.Z && git push origin vX.Y.Z` — `release.yaml` publishes.
   Then the GitHub release:
   `gh release create vX.Y.Z -R SidneyBissoli/<pkg> --title "<pkg> X.Y.Z" --notes-file <notes>`
   with the CHANGELOG section as notes.
7. Watch the run (`gh run list -R SidneyBissoli/<pkg> -L 3`) and check
   `https://pypi.org/project/<pkg>/`.
8. Back to development when the next change lands:
   `uv version --bump minor --bump dev` (`0.2.0` → `0.3.0.dev1`; measured: the
   dev counter starts at 1); commit `pyproject.toml` and `uv.lock`.

A PyPI version can never be re-uploaded, even after deletion: a broken release
is fixed by a new patch version.

## Installing

Released: `uv add <pkg>` / `pip install <pkg>`. Development version:
`uv add "<pkg> @ git+https://github.com/SidneyBissoli/<pkg>"`. Put both in the
README once the package is on PyPI (released first).
