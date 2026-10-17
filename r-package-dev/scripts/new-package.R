#!/usr/bin/env Rscript
# Scaffold a modern R package non-interactively.
# Usage:
#   Rscript new-package.R --path DIR --title "Title" --description "Sentence." \
#     [--author "Name"] [--email x@y] [--license mit|gpl3|cc0] [--cpp11] [--no-git]
# Everything is idempotent enough to re-run on a partially created package.

args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(flag, default = NULL) {
  i <- match(flag, args)
  if (is.na(i)) return(default)
  if (i == length(args) || startsWith(args[i + 1], "--")) return(TRUE)
  args[i + 1]
}
has_flag <- function(flag) flag %in% args

path <- get_arg("--path")
title <- get_arg("--title")
description <- get_arg("--description")
if (is.null(path) || is.null(title) || is.null(description)) {
  stop("Required: --path, --title, --description", call. = FALSE)
}
git_cfg <- function(key) {
  v <- tryCatch(system2("git", c("config", key), stdout = TRUE, stderr = FALSE), error = function(e) character())
  if (length(v) && nzchar(v[1])) v[1] else NULL
}
author <- get_arg("--author", "Sidney da Silva Pereira Bissoli")
email <- get_arg("--email", "sbissoli76@gmail.com")
if (is.null(author) || is.null(email)) {
  stop("Could not determine author: pass --author and --email (git config user.name/user.email are unset)", call. = FALSE)
}
license <- tolower(get_arg("--license", "mit"))
use_cpp11 <- has_flag("--cpp11")
do_git <- !has_flag("--no-git")

skill_dir <- normalizePath(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)[1])), ".."))
assets <- file.path(skill_dir, "assets")
stopifnot(dir.exists(assets))

path <- normalizePath(path, mustWork = FALSE)
pkg <- basename(path)
if (!grepl("^[A-Za-z][A-Za-z0-9.]*[A-Za-z0-9]$", pkg)) {
  stop("Invalid package name: ", pkg, call. = FALSE)
}

parts <- strsplit(trimws(author), "\\s+")[[1]]
given <- paste(utils::head(parts, -1), collapse = " ")
family <- utils::tail(parts, 1)
if (!nzchar(given)) { given <- family; family <- "" }
person_r <- sprintf('person(given = "%s", family = "%s", email = "%s", role = c("aut", "cre", "cph"))', given, family, email)
options(usethis.quiet = FALSE, usethis.description = list(`Authors@R` = person_r, Language = "en-US"))

cli::cli_h1("Creating package {.pkg {pkg}} at {.path {path}}")
if (!file.exists(file.path(path, "DESCRIPTION"))) {
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE) # create_package() needs the parent
  usethis::create_package(
    path,
    fields = list(Title = title, Description = description),
    rstudio = FALSE, roxygen = TRUE, open = FALSE
  )
}
usethis::proj_set(path, force = TRUE)
setwd(path)

# Parse Authors@R: usethis writes it as a string field; make sure it is R code.
desc <- desc::desc(file = "DESCRIPTION")
desc$set("Authors@R", person_r)
desc$set("Language", "en-US")
desc$del("Author"); desc$del("Maintainer")
desc$write()

switch(license,
  mit = usethis::use_mit_license(author),
  gpl3 = usethis::use_gpl3_license(),
  cc0 = usethis::use_cc0_license(),
  stop("Unknown --license: ", license)
)
usethis::use_package_doc(open = FALSE)
usethis::use_testthat(edition = 3)
usethis::use_news_md(open = FALSE)
usethis::use_air(vscode = FALSE)
file.copy(file.path(assets, "air.toml"), "air.toml", overwrite = TRUE)
file.copy(file.path(assets, ".lintr"), ".lintr", overwrite = TRUE)
usethis::use_build_ignore(c("air.toml", ".lintr", "README.Rmd", "README.pt-BR.md"))
usethis::use_spell_check(lang = "en-US", error = FALSE)
usethis::use_test(pkg, open = FALSE)       # placeholder so R CMD check finds a test file
writeLines(c(paste0("# ", pkg, " (development version)"), "", "* Package skeleton created."), "NEWS.md")
wl <- "inst/WORDLIST"
words <- unique(c(if (file.exists(wl)) readLines(wl), parts, "Leia", "em", "português"))
writeLines(sort(words[nzchar(words)]), wl)

# Bilingual README from template
readme <- readLines(file.path(assets, "README.Rmd"))
readme <- gsub("{{PKGNAME}}", pkg, readme, fixed = TRUE)
readme <- gsub("{{DESCRIPTION}}", description, readme, fixed = TRUE)
readme <- gsub("{{DESCRICAO_PT}}", "(Descreva aqui, em uma frase, o que o pacote faz.)", readme, fixed = TRUE)
writeLines(readme, "README.Rmd")
readme_pt <- readLines(file.path(assets, "README.pt-BR.md"))
readme_pt <- gsub("{{PKGNAME}}", pkg, readme_pt, fixed = TRUE)
readme_pt <- gsub("{{DESCRICAO_PT}}", "(Descreva aqui, em uma frase, o que o pacote faz.)", readme_pt, fixed = TRUE)
writeLines(readme_pt, "README.pt-BR.md")

# CI on GitHub Actions: the current r-lib workflow, or the bundled copy when offline
tryCatch(
  # no badge here: it needs the GitHub remote, which does not exist yet
  usethis::use_github_action("check-standard", badge = FALSE),
  error = function(e) {
    cli::cli_warn("use_github_action() failed ({conditionMessage(e)}); using the bundled workflow.")
    dir.create(".github/workflows", recursive = TRUE, showWarnings = FALSE)
    file.copy(file.path(assets, "R-CMD-check.yaml"), ".github/workflows/R-CMD-check.yaml", overwrite = TRUE)
    usethis::use_build_ignore("^\\.github$", escape = FALSE)
  }
)

if (use_cpp11) usethis::use_cpp11()

usethis::use_tidy_description()

# Render README.md once so the repo has one from the start
tryCatch(devtools::build_readme(quiet = TRUE), error = function(e) {
  cli::cli_warn("README.md not rendered: {conditionMessage(e)}")
})

if (nzchar(Sys.which("air"))) system2("air", c("format", "."))

if (do_git && !dir.exists(".git")) {
  system2("git", c("init", "-q", "-b", "main"))
  usethis::use_git_ignore(c(".Rhistory", ".RData", ".Rproj.user", "docs/"))
  system2("git", c("add", "-A"))
  system2("git", c("-c", shQuote(paste0("user.name=", author)), "-c", shQuote(paste0("user.email=", email)),
                   "commit", "-q", "-m", shQuote("Initial package skeleton")))
}

cli::cli_alert_success("Package {.pkg {pkg}} ready. Next: bash {.path {file.path(skill_dir, 'scripts/check.sh')}} inside {.path {path}}")
