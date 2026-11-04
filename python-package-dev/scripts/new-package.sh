#!/usr/bin/env bash
# Scaffold a new Python package from the copier template and leave it ready:
# git repository on main, .venv + uv.lock, pre-commit hooks installed, one
# initial commit (copier update needs a git-tracked, committed project).
#
# Usage:
#   bash new-package.sh --path DIR --description "One sentence." [--python 3.11]
#                       [--template C:/dev/claude] [--no-git]
# The package name is the last component of DIR (lowercase, digits, hyphens).
set -euo pipefail

path=""; description=""; python_min="3.11"; template="C:/dev/claude"; do_git=1
while [ $# -gt 0 ]; do
  case "$1" in
    --path) path="$2"; shift 2;;
    --description) description="$2"; shift 2;;
    --python) python_min="$2"; shift 2;;
    --template) template="$2"; shift 2;;
    --no-git) do_git=0; shift;;
    *) echo "new-package.sh: unknown argument $1" >&2; exit 2;;
  esac
done
[ -n "$path" ] && [ -n "$description" ] || {
  echo "Required: --path DIR --description \"One sentence.\"" >&2; exit 2; }
name="$(basename "$path")"
[[ "$name" =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]] || {
  echo "Invalid package name '$name': lowercase letters, digits, single hyphens." >&2; exit 2; }
[ ! -e "$path" ] || { echo "$path already exists; refusing to overwrite." >&2; exit 2; }
command -v copier >/dev/null || { echo "copier missing: uv tool install copier" >&2; exit 2; }

# The template must be committed: copier renders a dirty template from a
# synthetic commit that `copier update` can never find again.
if [ -n "$(git -C "$template" status --porcelain -- copier.yml templates/)" ]; then
  echo "Template has uncommitted changes in $template; commit them first." >&2; exit 2
fi

# PyPI name check (informative). The JSON API normalises names, so a 200 also
# catches variants PyPI would refuse (zope-interface -> zope.interface).
# Anything other than 200/404 means "could not check", never "free".
code="$(curl -s -m 15 -o /dev/null -w '%{http_code}' "https://pypi.org/pypi/$name/json" || true)"
case "$code" in
  200) echo "WARNING: '$name' already exists on PyPI; pick another name before publishing.";;
  404) ;;
  *) echo "WARNING: could not check '$name' on PyPI (HTTP ${code:-none}); check it before publishing.";;
esac

copier copy --vcs-ref HEAD --defaults \
  --data "project_name=$name" \
  --data "description=$description" \
  --data "python_min=$python_min" \
  "$template" "$path"

cd "$path"
uv sync
if [ "$do_git" = 1 ]; then
  git init -q -b main
  git add -A
  uv run pre-commit install
  # Hooks may fix files on the first pass (end of file, ruff); the second
  # pass must be clean. The commit then runs them once more through git.
  if ! uv run pre-commit run --all-files; then
    git add -A
    uv run pre-commit run --all-files
  fi
  git add -A
  git commit -q -m "chore: initial package skeleton from the python-package template"
fi

echo
echo "Package '$name' ready at $path."
echo "Next: bash ~/.claude/skills/python-package-dev/scripts/check.sh (inside the package)."
echo "GitHub (ask the user first): gh repo create SidneyBissoli/$name --public --source . --push"
