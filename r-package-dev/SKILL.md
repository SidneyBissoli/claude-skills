---
name: r-package-dev
description: Modern R package development (r-lib/tidyverse practice as of 2026) for creating, extending, testing, documenting, checking and releasing R packages on this Windows machine (R 4.6 + Rtools45, packages under C:\dev\r-packages, hosted on GitHub as SidneyBissoli or the DataSenado org). Use it whenever the user wants to create an R package, add a function, test, vignette, dataset or dependency to one, fix R CMD check / testthat / lintr / roxygen problems, set up pkgdown or CI for a package, prepare a CRAN release, or mentions usethis, devtools, testthat, roxygen2, DESCRIPTION, NAMESPACE, rcmdcheck, pkgdown, "pacote R", "criar pacote", "R CMD check". Also use it when editing any file inside a directory that contains a DESCRIPTION file, even if the user never says "package".
---

# R package development

This skill encodes how the R community builds packages today, so that the
package you produce looks like one written by the r-lib team in 2026 rather
than one from the "R packages" first edition. Read the whole file once; open
the references only when the task touches them.

Talk to the user in Portuguese. Write code, roxygen, messages, NEWS and commit
messages in English.

## 0. Existing package? Its own rules win

Before touching a package, look for `CLAUDE.md`, `CONTRIBUTING.md`,
`status/*decisions*.md` or a roadmap at its root and read them. Where they
disagree with this skill, **the package wins**. The table lists only where
each package's rules live and the defaults of section 2 it contradicts; the
rest is in those files (checked 2026-10-16).

| Package | Rules | Contradicts section 2 |
|---|---|---|
| cvmdata | `CLAUDE.md`, `CONTRIBUTING.md` | Portuguese column names and values |
| educabR | `CLAUDE.md` | `README.pt-br.md` (lower-case) |
| healthbR | `CLAUDE.md`, `CONTRIBUTING.md` | vendored C in `src/`, not cpp11; non-ASCII as `\u` escapes |
| senado | `status/05-architecture-decisions.md` | at most 7 Imports (ADR-007) |
| datasenado | `package-roadmap-pt.md` | BSD-3, © Instituto de Pesquisa DataSenado; org DataSenado; Portuguese README; no local `.git` |
| welfarebR | none | nothing |

Do not retrofit an existing package with the new-package defaults (Air,
`.lintr`, README.pt-BR, `Language:` field, S7) as a side effect of another
task. Each of those is a separate, user-approved change, in its own commit.

## 1. This environment (facts, not preferences)

- **Windows 11, R 4.6.1** at `C:\Program Files\R\R-4.6.1`, **Rtools45**
  (`pkgbuild::has_build_tools()` is TRUE). Personal library
  `~/AppData/Local/R/win-library/4.6`. R's `~` depends on the launcher:
  RStudio (no `HOME` set) uses `%USERPROFILE%\OneDrive\Documentos`, where
  `.Rprofile` and one `.Renviron` live; `Rscript` from Git Bash inherits
  `HOME=%USERPROFILE%` and reads the other `.Renviron` there. Check which
  one applies before blaming a missing variable.
- **Dev packages installed:** devtools, usethis, testthat, roxygen2, pkgdown,
  rcmdcheck, pak, lintr, covr, spelling, vdiffr, urlchecker, httptest2, vcr,
  cli, rlang, withr, lifecycle, renv, rhub, languageserver, cpp11, Rcpp, S7,
  quarto, ellmer, mcptools, btw. Check before assuming anything else:
  `Rscript -e 'requireNamespace("x")'`; install with `pak::pak("x")`.
- **CLIs:** `Rscript`, `air` (0.12, in `~/.local/bin`), `git`, `gh` (logged in
  as SidneyBissoli), `quarto`, `pandoc`. All visible from both PowerShell and
  Git Bash. `jq` is **not** installed.
- **Hosting is GitHub**: `SidneyBissoli/<pkg>`, except datasenado
  (`DataSenado/datasenado`). GitHub Actions run for real. Any `gh` command you
  hand the user to run carries `-R owner/repo` (the session cwd is `C:\dev`,
  not the package).
- **Line endings:** git stores LF; most working copies are CRLF
  (`core.autocrlf=input` normalises on `git add`; no `.gitattributes`), so
  `git status` stays clean either way. Keep `air.toml` `line-ending = "auto"`.
  Measure CR by bytes (`tr -cd '\r' < f | wc -c`); `grep` with a CR pattern
  returns 0 in this Git Bash even when CRs are there.
- **R tools via MCP (`r-btw`):** `btw_tool_pkg_load_all`, `_document`,
  `_test`, `_check`, `_coverage`; docs tools `btw_tool_docs_help_page`,
  `_package_help_topics`, `_vignette`, `_package_news`; and four read-only
  groups: `env` (objects and data frames in the selected session),
  `sessioninfo` (platform, installed packages), `cran` (`cran_versions` gives
  release dates: use it before proposing a CRAN submission) and `ide`
  (`read_current_editor`, only when the user asks about what is open).
  `btw_tool_run_r` runs R code in the selected session (enabled 2026-10-16
  with the user's consent). In the user's RStudio session it evaluates in
  their global environment with no undo, so: wrap work in `local({ ... })`;
  never assign over, `rm()`, `setwd()`, `options()` or `library()` there
  without saying so first; no long-running or network-heavy code without
  warning. Without a selected session it runs in the server's own process.
  Prefer them over
  guessing: read the actual help page of a function before using it, run the
  test tool instead of re-deriving output mentally. `list_r_sessions` /
  `select_r_session` reach the user's open RStudio/Positron session (the
  `.Rprofile` calls `btw::btw_mcp_session()`). If the tools are absent, fall
  back to `Rscript -e`.
- **Up-to-date docs:** Context7 (`mcp__claude_ai_Context7__*`) has current
  docs for usethis, testthat, roxygen2, pkgdown, cli, rlang, S7, cpp11.
- **Posit's `r-lib` plugin stays disabled** (evaluated 2026-10-16). Its generic
  `r-package-development` skill would compete with this one, and it conflicts
  with this skill: no roxygen on internal functions, no `expect_error()`,
  `air format .` everywhere, and `%>%` in examples. Its CRAN DESCRIPTION rules
  were copied into `references/ci-release.md`. For deep cli, lifecycle or
  snapshot questions, read its files directly under
  `~/.claude/plugins/marketplaces/posit-dev-skills/r-lib/` (`cli`,
  `lifecycle`, `testing-r-packages`), and keep this skill's decisions where
  they differ.
- **Formatting:** a PostToolUse hook (`scripts/air-hook.mjs`, in the user
  settings.json) runs `air format` on every `.R` file you Edit or Write, but
  only under an `air.toml`/`.air.toml` (all six packages since 2026-10-17).
  It does not see shell edits: after `sed`, heredocs or
  scripts that touch `.R` files, run `air format .` yourself. After an Edit on
  a formatted package, Read before the next Edit of the same region — the
  hook may have reflowed it. Adopting Air in a package = three
  commits (config, `style:` formatting only, `.git-blame-ignore-revs`),
  merged with a merge commit so the formatting SHA survives. Air is not
  whitespace-only: it adds braces around one-line `if`/`for` bodies, so prove
  "formatting only" by comparing `getParseData()` terminal tokens (only `{`/`}`
  pairs may differ), not by reading the diff. `.R` files that ship with data
  (reading examples under `data/`) are not package code: list them in the
  `air.toml` `exclude`.

## 2. Defaults for NEW packages (do not re-ask)

| Topic | Decision |
|---|---|
| Language | Code, roxygen, error messages, NEWS, commit messages (Conventional Commits) in **English**. README.Rmd in English; Portuguese page in **README.pt-BR.md** linked from the top of README ("Leia em português"). |
| Target | GitHub with **CRAN-ready discipline**: `R CMD check --as-cran` clean (0 errors, 0 warnings, ideally 0 notes), valid URLs, runnable examples, data under 5 MB, `Language: en-US`. Submitting to CRAN is the user's call, never yours. |
| Style | Native pipe `|>` only; `stringr::str_c()` over `paste0()` when stringr is already a dependency; `pkg::fun()` fully qualified; 80 columns; **Air** (`air.toml`) + **lintr** (`.lintr`) + spelling (`inst/WORDLIST`). |
| Errors | `cli::cli_abort()` / `cli_warn()` / `cli_inform()` with `{.arg}`, `{.cls}`, `{.fn}` markup, `call = caller_env()` propagation and a `class = "<pkg>_error_*"`. Never `stop(paste(...))`. |
| HTTP | httr2; tests offline with httptest2 (or `local_mocked_bindings()`); never hit the network in examples. |
| Tests | **testthat edition 3**, snapshot tests for errors and printed output, `withr::local_*` for state. |
| Docs | roxygen2 Markdown, `@returns`, `@family`, `@inheritParams`, `@examplesIf`; pkgdown on GitHub Pages. |
| Compiled code | **cpp11** for new code. |
| OOP | **S7** for new classes; S3 for simple dispatch; never S4 or R5. |
| License | MIT, copyright "Sidney da Silva Pereira Bissoli" (as in the CRAN packages), author email sbissoli76@gmail.com. |

## 3. Workflow A: create a new package

```bash
Rscript ~/.claude/skills/r-package-dev/scripts/new-package.R \
  --path C:/dev/r-packages/pkgname \
  --title "What The Package Does" \
  --description "One paragraph, full sentence, ending with a period." \
  [--cpp11] [--no-git]
```

Author defaults to "Sidney da Silva Pereira Bissoli" <sbissoli76@gmail.com>.
It creates: DESCRIPTION (`Language: en-US`, Markdown roxygen, testthat 3e),
MIT license, `R/pkgname-package.R`, NEWS.md, README.Rmd + README.pt-BR.md,
`air.toml`, `.lintr`, WORDLIST, `.github/workflows/R-CMD-check.yaml`
(r-lib `check-standard`), `.Rbuildignore` entries, git init on `main` with
an initial commit. It does **not** create the GitHub repo: ask, then
`gh repo create SidneyBissoli/pkgname --public --source . --push`. Run
`scripts/check.sh` once to prove the skeleton passes before adding code.

Package name rules: letters, digits, dots; starts with a letter; no dot at the
end; not already on CRAN (`pak::pkg_name_check("name")`).

## 4. Workflow B: the development loop

Every change goes through this loop, in this order.

1. **Load, don't install:** `devtools::load_all()` (MCP: `btw_tool_pkg_load_all`).
2. **Write the function** in `R/<topic>.R`, one file per topic, exported
   functions first, internal helpers below. Full roxygen block on every
   exported function (`@param`, `@returns`, `@examples`, `@export`), a short
   `@noRd` block on internal ones.
3. **Write the test first or alongside** in `tests/testthat/test-<topic>.R`.
   One `test_that()` per behaviour; test the error path with
   `expect_snapshot(error = TRUE)` or `expect_error(class =)`.
4. **Document:** `devtools::document()`. Never edit NAMESPACE or `man/*.Rd`
   by hand.
5. **Test:** `devtools::test()`; one file: `testthat::test_file()`.
6. **Format and lint:** `air format .` (only if `air.toml` exists), then
   `lintr::lint_package()` (only if `.lintr` exists).
7. **Check** before every commit that touches R code or DESCRIPTION, run
   from the package root:
   `bash ~/.claude/skills/r-package-dev/scripts/check.sh` (document, format
   check, lint, spelling, tests, `rcmdcheck --as-cran`). Steps whose tool
   config is absent (no `air.toml`, no `.lintr`, no WORDLIST) are skipped, so
   it works on the existing packages too. A NOTE is a bug unless you can
   explain it.
8. **NEWS.md** bullet under `# pkgname (development version)` for every
   user-visible change. Version bump only at release.

Shell equivalents when the MCP server is not connected:

```bash
Rscript -e 'devtools::document(); devtools::test()'
Rscript -e 'rcmdcheck::rcmdcheck(args = c("--as-cran", "--no-manual"), error_on = "never")'
```

Two Windows traps with `Rscript -e`: keep the code on **one line** (embedded
newlines segfault, exit 139), and keep `>`, `|`, `&` and `<` **out of R string
literals** (`cat("a -> b")` fails with a cmd.exe path error: the R quotes
close the quoting Rscript adds for cmd.exe). Operators outside strings
(`x > 0`) are fine. For anything longer, write a `.R` file with the Write tool
and run `Rscript file.R`.

## 5. Adding specific things

- **Dependency:** `usethis::use_package("pkg")` (Imports) or
  `use_package("pkg", "Suggests")`. Call it as `pkg::fun()`; `@importFrom`
  only for operators (`%||%`, `:=`) or hot loops. Suggested packages are
  guarded with `rlang::check_installed("pkg")`. Keep Imports minimal.
- **Data:** raw data and its build script in `data-raw/`
  (`usethis::use_data_raw("name")`); export with
  `usethis::use_data(name, overwrite = TRUE)`; document in `R/data.R` with
  `@format` for every column and `@source`. Internal tables:
  `use_data(..., internal = TRUE)`.
- **Vignette:** `usethis::use_vignette("name", "Title")`. Keep vignettes fast
  and offline; heavy computation is pre-computed.
- **Compiled code:** `usethis::use_cpp11()`, then `src/*.cpp` with
  `[[cpp11::register]]`. See `references/conventions.md` "cpp11".
- **S7 class:** `usethis::use_package("S7")`, `S7::new_class()` in
  `R/<class>.R`, `.onLoad <- function(...) S7::methods_register()`.
- **Deprecating:** `usethis::use_lifecycle()`, then
  `lifecycle::deprecate_warn("1.1.0", "old()", "new()")`; keep it for at
  least one release.
- **Options:** `options(pkgname.setting = ...)`, read with `getOption()`,
  document in `?pkgname-package`.
- **HTTP APIs:** httr2, httptest2 or vcr for recorded tests,
  `testthat::skip_if_offline()`, never the network in examples.

## 6. Conventions that make code look current

Full detail in `references/conventions.md`. The short list:

- Errors via cli with the argument named and a class; `call = call` when the
  check lives in a helper.
- Input checks with the rlang standalone checkers
  (`usethis::use_standalone("r-lib/rlang", "types-check")`).
- `rlang::arg_match()` for enumerated arguments; `rlang::check_dots_empty()`.
- `vapply()`/`purrr`, never `sapply()`; `seq_along()`, never `1:length()`;
  `inherits()`, never `class(x) ==`; `%||%` for defaults.
- No `library()`/`require()`/`setwd()` in package code; no `print()`/`cat()`
  for messages.
- Every exported function has `@returns` and a runnable example.
- Tests independent of each other, working directory, locale, time and
  network.

## 7. Reading check output

- ERROR or WARNING: must fix.
- NOTE "no visible binding for global variable": `.data$col` or
  `utils::globalVariables()` in `R/globals.R`.
- NOTE "Undefined global functions or variables" for `.data`:
  `@importFrom rlang .data`.
- NOTE about non-standard top-level files: `usethis::use_build_ignore()`.
- NOTE "installed package size": move big files out or
  `use_data(..., compress = "xz")`.
- NOTE "No news entries found" under `(development version)`: expected
  before the first release.
- NOTE about `\dontrun`: replace with `@examplesIf` or make it run.
- Windows-only: object files (`src/*.o`, `*.dll`) left in the tree by a local
  build are not a check problem but must stay out of git.

## 8. CI, pkgdown and release

See `references/ci-release.md`: r-lib workflows on GitHub Actions, pkgdown on
GitHub Pages, and the release checklist. CRAN submission and any GitHub
release are the user's decision; prepare everything, hand over the commands.

## 9. Reporting back

When you finish, tell the user in Portuguese: what was added or changed
(files), the result of the last `check.sh` run (errors / warnings / notes),
and what is still open. Paste only the relevant lines of check output.
