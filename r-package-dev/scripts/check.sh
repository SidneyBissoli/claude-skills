#!/usr/bin/env bash
# Full quality gate for an R package: document, format, lint, spelling, tests, R CMD check.
# Usage: bash check.sh [--quick] [--fix]   (run inside the package directory)
#   --quick  skip R CMD check (document + format + lint + tests only)
#   --fix    let Air rewrite files instead of only checking them
# Format, lint and spelling run only when the package opted in (air.toml,
# .lintr, `spelling` in DESCRIPTION), so the gate also works on packages that
# predate them.
set -u
quick=0; fix=0
for a in "$@"; do case "$a" in --quick) quick=1;; --fix) fix=1;; esac; done
[ -f DESCRIPTION ] || { echo "check.sh: no DESCRIPTION in $(pwd)" >&2; exit 2; }
status=0
step() { printf '\n==> %s\n' "$1"; }
skip() { printf '\n==> %s: skipped (%s)\n' "$1" "$2"; }

# A missing Suggests package makes tests skip silently and R CMD check fail
# minutes later; name it up front instead. No `>`, `|` or `&` inside R string
# literals in `Rscript -e` here: Windows hands the code to cmd.exe, which
# reads them as redirection once the R quotes close its own.
step "dependencies installed"
Rscript -e 'd <- desc::desc_get_deps(); m <- setdiff(d$package[d$package != "R"], rownames(utils::installed.packages())); if (length(m) > 0) { cat("   missing:", m, "\n   install them with pak::pak() first; tests that need them skip silently\n"); quit(status = 1) } else cat("   all", nrow(d), "declared dependencies present\n")' || status=1

step "roxygen (devtools::document)"
Rscript -e 'devtools::document(quiet = TRUE)' || status=1

if [ -f air.toml ] || [ -f .air.toml ]; then
  step "air format $( [ $fix = 1 ] && echo '(rewriting)' || echo '--check' )"
  if [ $fix = 1 ]; then air format . || status=1; else air format --check . || { echo "   -> run with --fix or: air format ."; status=1; }; fi
else
  skip "air format" "no air.toml"
fi

if [ -f .lintr ]; then
  step "lintr"
  Rscript -e 'l <- lintr::lint_package(); print(l); if (length(l) > 0) quit(status = 1)' || status=1
else
  skip "lintr" "no .lintr"
fi

# Opt-in signal is `spelling` declared in DESCRIPTION (use_spell_check() does
# that), not inst/WORDLIST alone: healthbR keeps a WORDLIST only for CRAN's
# DESCRIPTION check and never adopted full-docs spelling.
if grep -qw spelling DESCRIPTION; then
  step "spelling"
  Rscript -e 'w <- spelling::spell_check_package(); print(w); if (nrow(w) > 0) quit(status = 1)' || status=1
else
  skip "spelling" "spelling not in DESCRIPTION"
fi

step "testthat"
Rscript -e 'res <- as.data.frame(devtools::test(stop_on_failure = FALSE, reporter = "summary")); if (sum(res$failed) + sum(res$error) > 0) quit(status = 1)' || status=1

if [ $quick = 0 ]; then
  step "R CMD check --as-cran (CRAN incoming checks off; release checklist turns them on)"
  # One line on purpose: a multi-line `Rscript -e` segfaults on Windows (exit 139).
  _R_CHECK_CRAN_INCOMING_=false Rscript -e 'chk <- rcmdcheck::rcmdcheck(args = c("--no-manual", "--as-cran"), error_on = "never", quiet = TRUE); print(chk); cat(sprintf("\nCHECK SUMMARY: %d error(s), %d warning(s), %d note(s)\n", length(chk$errors), length(chk$warnings), length(chk$notes))); if (length(chk$errors) + length(chk$warnings) > 0) quit(status = 1)' || status=1
fi

printf '\n==> check.sh finished with status %d\n' "$status"
exit $status
