# CI, pkgdown and release

## GitHub Actions

All packages live on GitHub and their workflows run for real. Use r-lib's
maintained workflows instead of hand-written ones:

```r
usethis::use_github_action("check-standard")   # R-CMD-check on Linux, macOS, Windows
usethis::use_github_action("test-coverage")    # covr -> Codecov (optional)
usethis::use_github_action("pkgdown")          # site to the gh-pages branch
```

They go to `.github/workflows/` (already in `.Rbuildignore` via usethis).
`assets/R-CMD-check.yaml` and `assets/test-coverage.yaml` are offline
fallbacks only. Existing packages already carry their own workflows
(including extras such as `rhub.yaml`, `check-endpoints.yaml`,
`etl-mirror.yaml`); edit them in place, do not replace them with the
standard ones.

**Every R setup step carries a deadline** (`timeout-minutes: 10` on
`r-lib/actions/setup-r@v2`; `15` on `setup-r-dependencies@v2` where the
job installs binaries only — ubuntu + current release with
`use-public-rspm` — and `45` in the check matrix, because on R devel, or
for a package whose binary P3M has not built yet, pak compiles from source:
duckdb alone took 13 min on 2026-10-24, and that is work, not a stall) and
every CI job a ceiling (`timeout-minutes: 60`; the default is 360). Measured
2026-10-23: the steps take 20-80 s when the Ubuntu apt mirror of the
runners answers, and hung for two hours when `azure.archive.ubuntu.com`
crawled, holding the PRs; past the deadline the job fails fast and is
re-run. The assets carry it; add it when touching an older workflow.

Validate any workflow edit with `actionlint`, not with a YAML parser: a
parseable file can still be a broken workflow. If the runner lacks a system
library (e.g. GDAL), add `extra-packages: any::pkgname` or an `apt-get` step.

After a push, look at the run, not at the push:
`gh run list -R SidneyBissoli/<pkg> -L 3`. A merge push that does not trigger
a workflow is possible; `gh workflow run` re-triggers it.

## pkgdown

```r
usethis::use_pkgdown_github_pages()   # _pkgdown.yml, workflow, gh-pages, URL in DESCRIPTION
pkgdown::build_site()                 # local preview into docs/ (git-ignored)
```

One `- title:` block per `@family` in `_pkgdown.yml`; articles are the
vignettes. Never commit `docs/`. After adding an exported topic, run
`pkgdown::check_pkgdown()`: it fails if the topic is missing from the
reference index.

## NEWS bullets

One bullet per user-visible change (none for doc tweaks or internal
refactors), written for the user. Put the function name early, and the issue
or PR before the final period: `` * `get_x()` now accepts `year` (#12). ``.
Within a section, bullets without a function name come first, then the rest
in alphabetical order of function name.

## CRAN rules for DESCRIPTION (not caught by `R CMD check`)

Borrowed from Posit's `cran-extrachecks` skill (posit-dev/skills, 2026-09).

- **Title:** Title Case (`tools::toTitleCase()`), under 65 characters, no
  "Tools for", "A Toolkit for" or "for R".
- **Description:** 3–4 sentences (what it does, why it is useful). It must not
  start with "This package", the package name or "Functions for".
- **Quoting:** software, package, API and data-source names in single quotes,
  'R' included (`'DATASUS'`, `'httr2'`); function names unquoted with `()`.
  Double quotes only for publication titles.
- **Acronyms** expanded on first use: "Brazilian Securities and Exchange
  Commission ('CVM')".
- **Authors@R:** `"cph"` always, even for a sole author:
  `role = c("aut", "cre", "cph")`.
- **LICENSE year** = the year of this submission (2024 → 2026 when submitting
  in 2026).

## Release checklist (adapted from usethis::use_release_issue())

1. `git pull --ff-only`; working tree clean; default branch.
2. `usethis::use_version("minor")` (or "patch"/"major") bumps DESCRIPTION and
   turns the NEWS heading into `# pkgname X.Y.Z`. A change that alters the
   type or shape of an existing output (e.g. a column that can now be `NA`
   where it never was) is a **major** bump; decide it explicitly.
3. Review NEWS.md: every user-visible change, grouped by "Breaking changes",
   "New features", "Bug fixes", in the bullet format above. For a first CRAN
   submission, re-read DESCRIPTION against the CRAN rules above.
4. `devtools::build_readme()` if README.Rmd changed.
5. `urlchecker::url_check()`; `spelling::spell_check_package()`.
6. `bash ~/.claude/skills/r-package-dev/scripts/check.sh` clean, with
   `_R_CHECK_CRAN_INCOMING_=true` for CRAN-bound releases.
7. CRAN-bound only, **on the user's go-ahead**: `rhub::rhub_check()`,
   `devtools::check_win_devel()`, `cran-comments.md`
   (`usethis::use_cran_comments()`), then the user runs
   `devtools::submit_cran()` and confirms the e-mail. CRAN asks for releases
   no more often than every one to two months; check the date of the last
   one before proposing a submission.
8. Commit "chore: release vX.Y.Z" through a PR; merge first.
9. Only after the merge: tag and GitHub release, handed to the user as
   `gh release create vX.Y.Z -R SidneyBissoli/<pkg> --title "<pkg> X.Y.Z" --notes-file <notes>`
   with the NEWS section as notes.
10. `usethis::use_dev_version()` to start `X.Y.Z.9000`.

## Installing from GitHub

`pak::pak("SidneyBissoli/pkgname")`. Put that line in the README install
section; once on CRAN, `install.packages("pkgname")` comes first.
