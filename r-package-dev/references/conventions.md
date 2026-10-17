# Code conventions for modern R packages

Read the section you need. Each pattern says why it is preferred, so you can
adapt it rather than copy it blindly.

## Contents

1. Errors, warnings, messages (cli + rlang)
2. Input validation
3. Function design
4. roxygen2
5. testthat edition 3
6. S7 classes
7. cpp11
8. Tidy evaluation inside packages
9. Things that date a package (avoid)

## 1. Errors, warnings, messages

Why cli: messages get consistent formatting, semantic markup (`{.arg}`,
`{.fn}`, `{.cls}`, `{.path}`, `{.val}`), pluralisation, bullets, and the error
carries a class and the user-facing call.

```r
check_positive_int <- function(x, arg = rlang::caller_arg(x), call = rlang::caller_env()) {
  if (!rlang::is_integerish(x, n = 1) || x <= 0) {
    cli::cli_abort(
      "{.arg {arg}} must be a single positive integer, not {.obj_type_friendly {x}}.",
      call = call
    )
  }
  invisible(x)
}

fetch_rows <- function(n) {
  check_positive_int(n)          # error will say "Error in fetch_rows()"
  ...
}
```

- Bullets: `cli::cli_abort(c("Main message.", "i" = "Info line.", "x" = "What was wrong.", ">" = "What to do."))`.
- Classed errors so callers can `tryCatch(..., pkgname_error_x = ...)`:
  `cli::cli_abort("...", class = "pkgname_error_notfound")`.
- Chain errors: `tryCatch(expr, error = function(e) cli::cli_abort("Failed to read {.path {path}}.", parent = e))`.
- Messages that the user can silence: give the function a `quiet = FALSE`
  argument, or honour `getOption("pkgname.quiet")`, and route through
  `cli::cli_inform()`. Never `message()` with `paste0`, never `cat()`.
- Warnings are rare; prefer an error with a clear fix or a silent, documented
  fallback. If you warn, `cli::cli_warn()` with the same markup.

## 2. Input validation

Import the standalone checkers once:

```r
usethis::use_standalone("r-lib/rlang", "types-check")
```

This drops `R/import-standalone-types-check.R` (and `obj-type.R`) with
`check_string()`, `check_bool()`, `check_number_whole()`,
`check_number_decimal()`, `check_character()`, `check_data_frame()`,
`check_function()`, `check_logical()`, all accepting `allow_null`, `arg`,
`call`. They produce the same error style as cli and cost nothing at runtime.

```r
summarise_votes <- function(data, by, min_n = 1, na_rm = TRUE) {
  check_data_frame(data)
  check_string(by)
  check_number_whole(min_n, min = 0)
  check_bool(na_rm)
  ...
}
```

- Enumerated arguments: `type <- rlang::arg_match(type)` with the choices in
  the default `type = c("mean", "median")`.
- Reserved dots: `rlang::check_dots_empty()`; dots forwarded to another
  function: document with `@inheritDotParams other_fun`.
- Required arguments without defaults: `rlang::check_required(x)` gives a
  better error than "argument x is missing".

## 3. Function design

- Verbs for functions, nouns for objects; snake_case everywhere; a common
  prefix for the public API of a small package (`sen_votes()`, `sen_members()`)
  helps autocomplete.
- Data first, then required arguments, then optional arguments with defaults,
  `...` before optional arguments only when they are forwarded.
- Return the same type regardless of input size (a tibble with zero rows, not
  `NULL`); return invisibly when called for side effects.
- Pure functions where possible; side effects (files, options, env vars) are
  wrapped in `withr::local_*()` or `withr::with_*()`.
- `%||%` from rlang (or base in R >= 4.4) for defaults; `rlang::is_installed()`
  / `check_installed()` for optional dependencies.
- Internal helpers are not exported, carry `@noRd`, and live below the
  exported functions in the same file.
- Keep each file under ~300 lines; split by topic, not by function count.

## 4. roxygen2

```r
#' Summarise roll-call votes
#'
#' Collapses one row per vote into one row per `by` group, counting yes, no
#' and abstention. Groups with fewer than `min_n` votes are dropped.
#'
#' @param data A data frame with at least the columns `vote` and the column
#'   named in `by`.
#' @param by A single string: the column to group by.
#' @param min_n Minimum number of votes a group needs to be kept. Default `1`.
#' @param na_rm Should missing votes be dropped before counting? Default `TRUE`.
#'
#' @returns A tibble with columns `by`, `yes`, `no`, `abstain`, `n`, one row
#'   per group, ordered by `n` descending.
#'
#' @family vote summaries
#' @seealso [count_votes()] for the ungrouped version.
#' @export
#' @examples
#' summarise_votes(votes_2025, by = "party")
#' summarise_votes(votes_2025, by = "state", min_n = 10)
#'
#' @examplesIf rlang::is_installed("ggplot2")
#' library(ggplot2)
#' ggplot(summarise_votes(votes_2025, "party"), aes(party, yes)) + geom_col()
```

- First line: title in sentence case, no period. Second paragraph: description.
  Further paragraphs go to `@details` implicitly.
- `@returns` (plural) on every exported function, including "Called for its
  side effect; returns `x` invisibly".
- `@inheritParams other_fun` to avoid repeating param docs; `@rdname` to group
  variants in one page.
- `@examples` must run on CRAN in a few seconds, offline. Use `@examplesIf`
  for optional packages or interactive-only code; `\dontrun{}` only for things
  that genuinely cannot run (writing to the user's home, calling a paid API)
  and say why in a comment.
- Package doc: `R/pkgname-package.R` with `"_PACKAGE"` and `@keywords
  internal`; put `@importFrom rlang .data :=` and `@useDynLib` lines there.
- Markdown is on (`Roxygen: list(markdown = TRUE)`): use backticks, `[fun()]`
  links, bullet lists; no `\code{}`.

## 5. testthat edition 3

```r
test_that("summarise_votes() drops small groups", {
  out <- summarise_votes(votes_fixture(), by = "party", min_n = 3)
  expect_s3_class(out, "tbl_df")
  expect_named(out, c("party", "yes", "no", "abstain", "n"))
  expect_true(all(out$n >= 3))
})

test_that("summarise_votes() validates its inputs", {
  expect_snapshot(error = TRUE, {
    summarise_votes(1, by = "party")
    summarise_votes(votes_fixture(), by = c("a", "b"))
  })
})

test_that("print method is stable", {
  withr::local_options(width = 80, cli.num_colors = 1)
  expect_snapshot(print(summarise_votes(votes_fixture(), "party")))
})
```

- Fixtures: small, built by a helper in `tests/testthat/helper-*.R` or stored
  under `tests/testthat/fixtures/`; use `testthat::test_path()` for paths.
- `expect_snapshot()` for error messages and printed output; review snapshots
  with `testthat::snapshot_review()`; commit the `_snaps/` directory.
- `expect_equal()` (tolerance) over `expect_identical()` for doubles;
  `expect_identical()` for everything else.
- `skip_on_cran()`, `skip_if_offline()`, `skip_if_not_installed()` only
  for tests that truly need it; local runs must execute everything.
- `local_mocked_bindings()` to mock internal functions; never redefine
  functions in the global environment.
- Parallel tests (`Config/testthat/parallel: true`) only when the suite is
  slow and has no shared state.
- Coverage: `covr::package_coverage()`; aim at the public API and error
  branches, not at a number.

## 6. S7 classes

```r
#' @export
Vote <- S7::new_class(
  "Vote",
  package = "pkgname",
  properties = list(
    id = S7::class_character,
    date = S7::class_Date,
    result = S7::new_property(S7::class_character, default = "pending")
  ),
  validator = function(self) {
    if (length(self@id) != 1) "@id must be a single string"
  }
)

#' @export
print.pkgname::Vote <- function(x, ...) {   # S3 fallback for base generics
  cat("<Vote> ", x@id, " (", format(x@date), ")\n", sep = "")
  invisible(x)
}

summary_method <- S7::new_generic("summary_method", "x")
S7::method(summary_method, Vote) <- function(x) { ... }

.onLoad <- function(libname, pkgname) {
  S7::methods_register()
}
```

Use S7 when you need properties with validation or multiple dispatch; use a
plain S3 class (`structure(list(...), class = "pkgname_thing")` with a
`new_thing()` constructor and a `validate_thing()`) when you only need
`print`/`format` methods. DESCRIPTION needs `Imports: S7` and, for base
generics, `@rawNamespace if (getRversion() < "4.3.0") S3method(...)` is not
needed any more on R 4.5; S7 handles it with `methods_register()`.

## 7. cpp11

```r
usethis::use_cpp11()       # DESCRIPTION LinkingTo, src/, @useDynLib
```

```cpp
// src/count.cpp
#include <cpp11.hpp>
using namespace cpp11;

[[cpp11::register]]
int count_positive(doubles x) {
  int n = 0;
  for (double v : x) if (v > 0) ++n;
  return n;
}
```

`devtools::document()` (or `cpp11::cpp_register()`) regenerates
`R/cpp11.R` and `src/cpp11.cpp`; never edit those. Prefer cpp11 types
(`doubles`, `integers`, `strings`, `writable::doubles`) over raw SEXP;
throw `cpp11::stop()` for errors, which becomes an R error. Keep the R wrapper
responsible for argument checking so error messages stay in cli style.

## 8. Tidy evaluation inside packages

- Columns named by the user as strings: `.data[[by]]`; as bare names:
  `{{ by }}` (embrace) and document `@param by <[`data-masked`][dplyr::dplyr_data_masking]>`.
- Import `.data` (and `:=` when creating columns) from rlang in the package
  doc: `@importFrom rlang .data :=`.
- Never `eval(parse(text = ...))`; never `get()` on user strings.

## 9. Things that date a package (avoid)

| Dated | Current |
|---|---|
| `stop(paste0("x must be ", ...))` | `cli::cli_abort("{.arg x} must be ...")` |
| `stopifnot(is.character(x))` | `check_string(x)` / `check_character(x)` |
| `match.arg(type)` | `rlang::arg_match(type)` |
| `styler::style_pkg()` | `air format .` |
| testthat 2 `context()`, `expect_error(..., "regex")` | edition 3, `expect_snapshot(error = TRUE)` or `expect_error(class =)` |
| `setClass()` / R5 | S7 (or S3) |
| Rcpp for new packages | cpp11 |
| `\dontrun{}` everywhere | `@examplesIf`, runnable examples |
| `sapply()`, `1:length(x)` | `vapply()`/`purrr::map_*()`, `seq_along(x)` |
| `library(dplyr)` in R/ | `dplyr::fun()` + `use_package("dplyr")` |
| README.md edited by hand | README.Rmd rendered with `devtools::build_readme()` |
| `@return` | `@returns` |
| Travis / AppVeyor | GitHub Actions with `r-lib/actions` |
| `%>%` | native `|>` |
